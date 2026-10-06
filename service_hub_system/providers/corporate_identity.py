"""Fail-closed corporate identity contract for the M01 boundary.

The Service Hub domain depends only on the types in this module. A corporate
app owns any adapter that reads its own DocTypes and registers its factory via
the documented Frappe hook.
"""

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

import frappe

CONTRACT_ID = "corporate-identity/v1"
PROVIDER_HOOK = "service_hub_corporate_identity_provider"
_CORPORATE_REF_PATTERN = re.compile(r"^corpref:v1:employee:[A-Za-z0-9_-]+$")


class IdentityDenialReason(StrEnum):
	ANONYMOUS = "anonymous"
	NOT_FOUND = "not_found"
	AMBIGUOUS = "ambiguous"
	INACTIVE = "inactive"
	INVALID = "invalid"
	NOT_AUTHORIZED = "not_authorized"
	PROVIDER_UNAVAILABLE = "provider_unavailable"


@dataclass(frozen=True)
class CorporateRef:
	"""Opaque, versioned identity reference that Service Hub only compares."""

	value: str

	def __post_init__(self) -> None:
		if not _CORPORATE_REF_PATTERN.fullmatch(self.value):
			raise ValueError("CorporateRef must use the corporate-identity/v1 employee format")


@dataclass(frozen=True)
class RequesterIdentityProjection:
	"""The complete M01 projection permitted across the provider boundary."""

	corporate_ref: CorporateRef
	display_name: str


@dataclass(frozen=True)
class IdentityResolutionDenied:
	"""A safe identity-resolution failure with no corporate value."""

	reason: IdentityDenialReason


@dataclass(frozen=True)
class CorporateAccessGranted:
	"""Successful corporate identity access check; intentionally carries no data."""


@dataclass(frozen=True)
class CorporateAccessDenied:
	"""A safe corporate-access failure with no corporate value."""

	reason: IdentityDenialReason


class CorporateIdentityProvider(Protocol):
	"""The M01 provider interface implemented by the corporate-data owner."""

	contract_id: str

	def resolve_requester(
		self, actor_user: str, purpose: str
	) -> RequesterIdentityProjection | IdentityResolutionDenied: ...

	def check_identity_access(
		self, actor_user: str, corporate_ref: CorporateRef, purpose: str
	) -> CorporateAccessGranted | CorporateAccessDenied: ...


class CorporateIdentityProviderConfigurationError(RuntimeError):
	"""Raised when the mandatory provider registration is absent or invalid."""


def get_registered_provider() -> CorporateIdentityProvider:
	"""Resolve exactly one compatible provider factory from the Frappe hook."""

	factories = frappe.get_hooks(PROVIDER_HOOK) or []
	if not isinstance(factories, (list, tuple)) or len(factories) != 1:
		raise CorporateIdentityProviderConfigurationError("exactly one provider factory is required")

	factory_path = factories[0]
	if not isinstance(factory_path, str) or not factory_path:
		raise CorporateIdentityProviderConfigurationError("provider factory registration is invalid")

	factory = frappe.get_attr(factory_path)
	provider = factory()
	if getattr(provider, "contract_id", None) != CONTRACT_ID:
		raise CorporateIdentityProviderConfigurationError("provider contract is incompatible")
	return provider


def resolve_requester(
	actor_user: str | None, purpose: str = "request.submit"
) -> RequesterIdentityProjection | IdentityResolutionDenied:
	"""Resolve the current requester without exposing provider implementation data."""

	if not actor_user or actor_user == "Guest":
		return IdentityResolutionDenied(IdentityDenialReason.ANONYMOUS)

	try:
		result = get_registered_provider().resolve_requester(actor_user, purpose)
	except Exception:
		return IdentityResolutionDenied(IdentityDenialReason.PROVIDER_UNAVAILABLE)

	if isinstance(result, IdentityResolutionDenied):
		return result
	if _is_valid_projection(result):
		return result
	return IdentityResolutionDenied(IdentityDenialReason.INVALID)


def check_identity_access(
	actor_user: str | None, corporate_ref: CorporateRef, purpose: str
) -> CorporateAccessGranted | CorporateAccessDenied:
	"""Check corporate eligibility and convert provider errors to a safe denial."""

	if not actor_user or actor_user == "Guest":
		return CorporateAccessDenied(IdentityDenialReason.ANONYMOUS)

	try:
		result = get_registered_provider().check_identity_access(actor_user, corporate_ref, purpose)
	except Exception:
		return CorporateAccessDenied(IdentityDenialReason.PROVIDER_UNAVAILABLE)

	if isinstance(result, (CorporateAccessGranted, CorporateAccessDenied)):
		return result
	return CorporateAccessDenied(IdentityDenialReason.INVALID)


def has_effective_team_task_access(
	actor_user: str | None,
	corporate_ref: CorporateRef,
	purpose: str,
	*,
	has_active_team_membership: bool,
	has_contextual_task_permission: bool,
) -> bool:
	"""Evaluate the approved M01 conjunction without owning Task persistence.

	M01 will supply the membership, contextual policy, and atomic Task-state
	checks. This boundary helper only proves that corporate grant is necessary,
	and re-resolves the actor before allowing the remaining checks to decide.
	"""

	identity = resolve_requester(actor_user, purpose=purpose)
	if not isinstance(identity, RequesterIdentityProjection) or identity.corporate_ref != corporate_ref:
		return False

	access = check_identity_access(actor_user, corporate_ref, purpose)
	return (
		isinstance(access, CorporateAccessGranted)
		and has_active_team_membership
		and has_contextual_task_permission
	)


def _is_valid_projection(value: object) -> bool:
	return (
		isinstance(value, RequesterIdentityProjection)
		and isinstance(value.corporate_ref, CorporateRef)
		and isinstance(value.display_name, str)
		and bool(value.display_name.strip())
	)
