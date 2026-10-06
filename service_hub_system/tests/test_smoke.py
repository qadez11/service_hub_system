from frappe.tests.utils import FrappeTestCase

import service_hub_system


class TestAppSmoke(FrappeTestCase):
	def test_package_is_importable(self):
		self.assertEqual(service_hub_system.__version__, "0.0.1")
