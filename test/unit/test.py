import unittest
from unittest.mock import MagicMock
from unittest import mock
import yaml
from requests import HTTPError
from yaml.parser import ParserError
from openstack_flavor_manager import reference, cloud, ensure
from munch import Munch
import os
from typer.testing import CliRunner

from openstack_flavor_manager.main import app

MOCK_YML = """
reference:
- field: name
  mandatory_prefix: SCS-
- field: public
  default: 'true'
- field: disabled
  default: 'false'
- field: name
- field: cpus
- field: ram
- field: disk
- field: description
mandatory:
- name: SCS-1V-4
  cpus: 1
  ram: 4096
  disk: 0
  description: alias=SCS-1V:4
- name: SCS-2V-8
  cpus: 2
  ram: 8192
  disk: 0
  description: alias=SCS-2V:8
- name: SCS-4V-16
  cpus: 4
  ram: 16384
  disk: 0
  description: alias=SCS-4V:16
recommended:
- name: SCS-8V-32
  cpus: 8
  ram: 32768
  disk: 0
  description: alias=SCS-8V:32
"""


class TestCLIArguments(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @mock.patch("openstack_flavor_manager.ensure.Ensure.ensure")
    @mock.patch("openstack_flavor_manager.ensure.Ensure.__init__")
    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    @mock.patch("openstack_flavor_manager.reference.get_url")
    def test_ensure_command_0(self, mock_get_url, mock_cloud_init, mock_ensure_init, mock_ensure_ensure):
        mock_cloud_init.return_value = None
        mock_ensure_init.return_value = None
        result = self.runner.invoke(app, ["ensure", "scs"])

        # Check that 'ensure scs' is a valid CLI call
        self.assertEqual(result.exit_code, 0)

    @mock.patch("openstack_flavor_manager.ensure.Ensure.ensure")
    @mock.patch("openstack_flavor_manager.ensure.Ensure.__init__")
    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    @mock.patch("openstack_flavor_manager.reference.get_url")
    def test_ensure_command_1(self, mock_get_url, mock_cloud_init, mock_ensure_init, mock_ensure_ensure):
        mock_cloud_init.return_value = None
        mock_ensure_init.return_value = None
        result = self.runner.invoke(app, ["ensure", "--recommended", "scs"])

        # Check that 'ensure --recommended scs' is a valid CLI call
        self.assertEqual(result.exit_code, 0)

    @mock.patch("openstack_flavor_manager.ensure.Ensure.ensure")
    @mock.patch("openstack_flavor_manager.ensure.Ensure.__init__")
    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    @mock.patch("openstack_flavor_manager.reference.get_url")
    def test_ensure_command_2(self, mock_get_url, mock_cloud_init, mock_ensure_init, mock_ensure_ensure):
        mock_cloud_init.return_value = None
        mock_ensure_init.return_value = None
        result = self.runner.invoke(app, ["ensure"])

        # Check that 'ensure' is NOT a valid CLI call
        self.assertNotEqual(result.exit_code, 0)

    @mock.patch("openstack_flavor_manager.ensure.Ensure.ensure")
    @mock.patch("openstack_flavor_manager.ensure.Ensure.__init__")
    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    @mock.patch("openstack_flavor_manager.reference.get_url")
    def test_callback(self, mock_get_url, mock_cloud_init, mock_ensure_init, mock_ensure_ensure):
        mock_cloud_init.return_value = None
        mock_ensure_init.return_value = None
        result = self.runner.invoke(app, ["--debug", "ensure", "scs"])

        # Check that '--debug' is a valid global CLI option
        self.assertEqual(result.exit_code, 0)


class TestReference(unittest.TestCase):
    @mock.patch("requests.get")
    def test_get_url_0(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = MOCK_YML
        result = reference.get_url("")

        expected_result = yaml.safe_load(MOCK_YML)

        # Check if get_url returns the expected dict
        self.assertEqual(result, expected_result)

    @mock.patch("requests.get")
    def test_get_url_1(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.content = "Test 123"
        mock_get.return_value.raise_for_status = mock.Mock(side_effect=HTTPError())

        # Check if the function raises an exception
        self.assertRaises(HTTPError, reference.get_url, "")

    @mock.patch("requests.get")
    def test_get_url_2(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = "-" + MOCK_YML

        # Check if the function raises an invalid yaml exception
        self.assertRaises(ParserError, reference.get_url, "")

    def test_get_url_3(self):
        # Here we _actually_ download the YML files uploaded to GitHub
        # Therefore, this test requires an active internet connection

        # Resolve 'scs' to correct url
        result = reference.get_url("scs")
        self.assertIs(type(result), dict)

        # Resolve 'osism' to correct url
        result = reference.get_url("osism")
        self.assertIs(type(result), dict)


class TestEnsure(unittest.TestCase):

    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    def test_init_0(self, mock_init):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = cloud.Cloud()

        test = ensure.Ensure(c, definitions)

        expected_result = {item['name']: item for item in definitions["mandatory"]}
        actual_result = {item['name']: item for item in test.required_flavors}

        # Check if mandatory items are added to the ensure object
        self.assertEqual(test.cloud, c)
        self.assertEqual(expected_result, actual_result)

    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    def test_init_1(self, mock_init):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = cloud.Cloud()

        test = ensure.Ensure(c, definitions, True)

        expected_result = {item['name']: item for item in definitions["mandatory"]}
        for item in definitions["recommended"]:
            expected_result[item["name"]] = item

        actual_result = {item['name']: item for item in test.required_flavors}

        # Check if mandatory + recommended items are added to the ensure object
        self.assertEqual(test.cloud, c)
        self.assertEqual(expected_result, actual_result)

    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    def test_init_2(self, mock_init):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = cloud.Cloud()

        test = ensure.Ensure(c, definitions)
        test2 = ensure.Ensure(c, definitions, True)

        expected_result = {}
        for item in definitions["reference"]:
            if "default" in item:
                expected_result[item["field"]] = item["default"]

        # Check if default fields are correctly parsed
        self.assertEqual(expected_result, test.defaults_dict)
        self.assertEqual(expected_result, test2.defaults_dict)

    @mock.patch("openstack_flavor_manager.cloud.Cloud.set_flavor")
    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    def test_ensure_0(self, mock_init, mock_setflavor):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = cloud.Cloud()

        test = ensure.Ensure(c, definitions)
        test.ensure()

        # Check if set_flavor was called once for all mandatory entries
        self.assertEqual(mock_setflavor.call_count, len(definitions["mandatory"]))

    @mock.patch("openstack_flavor_manager.cloud.Cloud.set_flavor")
    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    def test_ensure_1(self, mock_init, mock_setflavor):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = cloud.Cloud()

        test = ensure.Ensure(c, definitions, True)
        test.ensure()

        # Check if set_flavor was called once for all mandatory + recommended entries
        expected_result = len(definitions["mandatory"]) + len(definitions["recommended"])
        self.assertEqual(mock_setflavor.call_count, expected_result)

    @mock.patch("openstack_flavor_manager.cloud.Cloud.set_flavor")
    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    def test_ensure_2(self, mock_init, mock_setflavor):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = cloud.Cloud()

        test = ensure.Ensure(c, definitions)
        test.ensure()

        # Check if set_flavor was called with the correct arguments
        for i in range(len(definitions["mandatory"])):
            mock_setflavor.assert_any_call(flavor_spec=definitions["mandatory"][i], defaults=test.defaults_dict)

    @mock.patch("openstack_flavor_manager.cloud.Cloud.set_flavor")
    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    def test_ensure_3(self, mock_init, mock_setflavor):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = cloud.Cloud()

        test = ensure.Ensure(c, definitions, True)
        test.ensure()

        # Check if set_flavor was called with the correct arguments
        for i in range(len(definitions["recommended"])):
            mock_setflavor.assert_any_call(flavor_spec=definitions["recommended"][i], defaults=test.defaults_dict)


class TestCloud(unittest.TestCase):

    def test_spec_or_default_0(self):
        test_spec = {
            "existing_key": "value1",
            "existing_key_2": "value2"
        }

        # Check if existing key is returned
        self.assertEqual(cloud.get_spec_or_default("existing_key", test_spec, {}), "value1")
        self.assertEqual(cloud.get_spec_or_default("existing_key_2", test_spec, {}), "value2")

    def test_spec_or_default_1(self):
        test_spec = {
            "existing_key": "value1",
            "existing_key_2": "value2"
        }
        default_spec = {
            "default_key": "value3",
            "default_key_2": "value4"
        }

        # Check if default key is returned
        self.assertEqual(cloud.get_spec_or_default("default_key", test_spec, default_spec), "value3")
        self.assertEqual(cloud.get_spec_or_default("default_key_2", test_spec, default_spec), "value4")

    def test_spec_or_default_2(self):
        test_spec = {
            "existing_key": True,
            "existing_key_2": False,
        }
        default_spec = {
            "default_key": True,
            "default_key_2": False
        }

        self.assertEqual(cloud.get_spec_or_default("existing_key", test_spec, default_spec), True)
        self.assertEqual(cloud.get_spec_or_default("existing_key_2", test_spec, default_spec), False)

        self.assertEqual(cloud.get_spec_or_default("default_key", test_spec, default_spec), True)
        self.assertEqual(cloud.get_spec_or_default("default_key_2", test_spec, default_spec), False)

    def test_spec_or_default_3(self):
        test_spec = {
            "existing_key": "value1",
            "existing_key_2": "value2"
        }
        default_spec = {
            "default_key": "value3",
            "default_key_2": "value4"
        }

        # Check if Exception is raised
        self.assertRaises(ValueError, cloud.get_spec_or_default, "unknown_key", test_spec, default_spec)

    @mock.patch("openstack.openstack.connect")
    def test_init_0(self, mock_connect):
        mock_flavors = MagicMock()
        mock_connect.return_value.list_flavors = mock_flavors

        mock_flavors.return_value = [
            Munch({"name": "SCS-4V-16"}),
            Munch({"name": "SCS-2V-16"}),
            Munch({"name": "SCS-8V-32"})
        ]

        oldenv = os.environ.get("OS_CLOUD", "")
        os.environ["OS_CLOUD"] = "testcloud"

        c = cloud.Cloud()

        os.environ["OS_CLOUD"] = oldenv

        # Check if connect and list_flavor command against fake openstack data was successful
        self.assertEqual(mock_connect.call_count, 1)
        mock_connect.assert_called_with(cloud="testcloud")
        self.assertEqual(mock_flavors.call_count, 1)
        self.assertEqual(c.existing_flavor_names, {"SCS-8V-32", "SCS-2V-16", "SCS-4V-16"})

    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    def test_set_flavor_0(self, mock_init):
        mock_init.return_value = None
        c = cloud.Cloud()
        c.conn = MagicMock()
        c.conn.create_flavor = MagicMock()
        c.conn.create_flavor.return_value = Munch({"id": "49186969-54a4-470e-ad14-315081685a3d"})
        c.existing_flavor_names = set()
        flavor = c.set_flavor({'name': 'SCS-1V-4', 'cpus': 1, 'ram': 4096, 'disk': 0, 'description': 'alias=SCS-1V:4'},
                              {'public': True})
        c.conn.create_flavor.assert_called_with(name='SCS-1V-4', ram=4096, vcpus=1, disk=0, ephemeral=0, swap=0,
                                                rxtx_factor=1.0, description='alias=SCS-1V:4', is_public=True)
        c.conn.set_flavor_specs.assert_called_with(flavor_id='49186969-54a4-470e-ad14-315081685a3d', extra_specs={})

        # Check that the flavor was created successfully
        self.assertNotEqual(flavor, None)

    @mock.patch("openstack_flavor_manager.cloud.Cloud.__init__")
    def test_set_flavor_1(self, mock_init):
        mock_init.return_value = None
        c = cloud.Cloud()
        c.conn = MagicMock()
        c.conn.create_flavor = MagicMock()
        c.conn.create_flavor.return_value = Munch({"id": "49186969-54a4-470e-ad14-315081685a3d"})
        c.existing_flavor_names = {'SCS-1V-4'}
        flavor = c.set_flavor({'name': 'SCS-1V-4', 'cpus': 1, 'ram': 4096, 'disk': 0, 'description': 'alias=SCS-1V:4'},
                              {'public': True})
        c.conn.create_flavor.assert_not_called()
        c.conn.set_flavor_specs.assert_not_called()

        # Check that no flavor has been returned, because it already exists
        self.assertEqual(flavor, None)


if __name__ == "__main__":
    unittest.main()
