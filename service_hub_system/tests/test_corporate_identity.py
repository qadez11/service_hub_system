from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase

from service_hub_system.providers.corporate_identity import (
	CONTRACT_ID,
	PROVIDER_HOOK,
	CorporateAccessDenied,
	CorporateAccessGranted,
	CorporateRef,
	IdentityDenialReason,
	IdentityResolutionDenied,
	RequesterIdentityProjection,
	has_effective_team_task_access,
	resolve_requester,
)


class FakeCorporateIdentityProvider:
	contract_id = CONTRACT_ID

	def __init__(self):
		self.resolutions = {}
		self.access = {}
		self.raise_on_resolve = False

	def resolve_requester(self, actor_user, purpose):
		if self.raise_on_resolve:
			raise RuntimeError("provider unavailable")
		return self.resolutions.get(actor_user, IdentityResolutionDenied(IdentityDenialReason.NOT_FOUND))

	def check_identity_access(self, actor_user, corporate_ref, purpose):
		return self.access.get(
			(actor_user, corporate_ref, purpose), CorporateAccessDenied(IdentityDenialReason.NOT_AUTHORIZED)
		)


_provider = FakeCorporateIdentityProvider()


def fake_corporate_identity_provider_factory():
	return _provider


class IncompatibleCorporateIdentityProvider:
	contract_id = "corporate-identity/v2"


def incompatible_corporate_identity_provider_factory():
	return IncompatibleCorporateIdentityProvider()


class TestCorporateIdentityContract(FrappeTestCase):
	factory_path = "service_hub_system.tests.test_corporate_identity.fake_corporate_identity_provider_factory"
	incompatible_factory_path = (
		"service_hub_system.tests.test_corporate_identity.incompatible_corporate_identity_provider_factory"
	)

	def setUp(self):
		_provider.resolutions = {}
		_provider.access = {}
		_provider.raise_on_resolve = False
		self.corporate_ref = CorporateRef("corpref:v1:employee:opaque_123")
		self.provider_hook = patch.object(frappe, "get_hooks", return_value=[self.factory_path])
		self.provider_hook.start()
		self.addCleanup(self.provider_hook.stop)

	def test_allowed_read_returns_only_the_identity_projection(self):
		_provider.resolutions["requester@example.test"] = RequesterIdentityProjection(
			corporate_ref=self.corporate_ref,
			display_name="Requester",
		)

		result = resolve_requester("requester@example.test")

		self.assertIsInstance(result, RequesterIdentityProjection)
		self.assertEqual(set(vars(result)), {"corporate_ref", "display_name"})
		self.assertEqual(result.corporate_ref, self.corporate_ref)
		self.assertEqual(result.display_name, "Requester")

	def test_resolution_denies_without_corporate_data(self):
		cases = {
			None: IdentityDenialReason.ANONYMOUS,
			"Guest": IdentityDenialReason.ANONYMOUS,
			"missing@example.test": IdentityDenialReason.NOT_FOUND,
			"ambiguous@example.test": IdentityDenialReason.AMBIGUOUS,
			"inactive@example.test": IdentityDenialReason.INACTIVE,
		}
		_provider.resolutions["ambiguous@example.test"] = IdentityResolutionDenied(
			IdentityDenialReason.AMBIGUOUS
		)
		_provider.resolutions["inactive@example.test"] = IdentityResolutionDenied(
			IdentityDenialReason.INACTIVE
		)

		for actor_user, reason in cases.items():
			with self.subTest(actor_user=actor_user):
				result = resolve_requester(actor_user)
				self.assertEqual(result, IdentityResolutionDenied(reason))
				self.assertEqual(set(vars(result)), {"reason"})

	def test_provider_failure_denies_without_corporate_data(self):
		_provider.raise_on_resolve = True

		result = resolve_requester("requester@example.test")

		self.assertEqual(result, IdentityResolutionDenied(IdentityDenialReason.PROVIDER_UNAVAILABLE))
		self.assertEqual(set(vars(result)), {"reason"})

	def test_missing_multiple_or_incompatible_provider_factory_is_fail_closed(self):
		with patch.object(frappe, "get_hooks", return_value=[]):
			missing = resolve_requester("requester@example.test")
		with patch.object(frappe, "get_hooks", return_value=[self.factory_path, self.factory_path]):
			multiple = resolve_requester("requester@example.test")
		with patch.object(frappe, "get_hooks", return_value=[self.incompatible_factory_path]):
			incompatible = resolve_requester("requester@example.test")

		self.assertEqual(missing, IdentityResolutionDenied(IdentityDenialReason.PROVIDER_UNAVAILABLE))
		self.assertEqual(multiple, IdentityResolutionDenied(IdentityDenialReason.PROVIDER_UNAVAILABLE))
		self.assertEqual(incompatible, IdentityResolutionDenied(IdentityDenialReason.PROVIDER_UNAVAILABLE))

	def test_corporate_grant_without_team_membership_cannot_view_task(self):
		self._grant_active_requester("agent@example.test", "task.view")

		self.assertFalse(
			has_effective_team_task_access(
				"agent@example.test",
				self.corporate_ref,
				"task.view",
				has_active_team_membership=False,
				has_contextual_task_permission=True,
			)
		)

	def test_team_member_with_corporate_deny_cannot_claim_task(self):
		_provider.resolutions["agent@example.test"] = RequesterIdentityProjection(
			corporate_ref=self.corporate_ref,
			display_name="Agent",
		)
		_provider.access[("agent@example.test", self.corporate_ref, "task.claim")] = CorporateAccessDenied(
			IdentityDenialReason.NOT_AUTHORIZED
		)

		self.assertFalse(
			has_effective_team_task_access(
				"agent@example.test",
				self.corporate_ref,
				"task.claim",
				has_active_team_membership=True,
				has_contextual_task_permission=True,
			)
		)

	def _grant_active_requester(self, actor_user, purpose):
		_provider.resolutions[actor_user] = RequesterIdentityProjection(
			corporate_ref=self.corporate_ref,
			display_name="Agent",
		)
		_provider.access[(actor_user, self.corporate_ref, purpose)] = CorporateAccessGranted()
