import unittest
from unittest.mock import MagicMock, patch
from unittest import mock
import typer
import yaml
from requests import HTTPError
from yaml.parser import ParserError
from munch import Munch
from typer.testing import CliRunner

from openstack_flavor_manager.main import (
    run,
    get_flavor_definitions,
    FlavorManager,
    Cloud,
    get_spec_or_default,
)

app = typer.Typer()
app.command()(run)

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
mandatory:
- name: SCS-1V-4
  cpus: 1
  ram: 4096
  disk: 0
- name: SCS-2V-8
  cpus: 2
  ram: 8192
  disk: 0
- name: SCS-4V-16
  cpus: 4
  ram: 16384
  disk: 0
recommended:
- name: SCS-8V-32
  cpus: 8
  ram: 32768
  disk: 0
"""


class TestCLIArguments(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("openstack_flavor_manager.main.get_flavor_definitions")
    @patch("openstack_flavor_manager.main.Cloud.__init__")
    @patch("openstack_flavor_manager.main.FlavorManager.run")
    @patch("openstack_flavor_manager.main.FlavorManager.__init__")
    def test_ensure_command_0(
        self,
        mock_flavor_manager_init,
        mock_run,
        mock_cloud_init,
        mock_get_flavor_definitions,
    ):
        mock_cloud_init.return_value = None
        mock_flavor_manager_init.return_value = None
        mock_get_flavor_definitions.return_value = {}
        result = self.runner.invoke(app, ["--name=scs"])

        # Check that '--name scs' is a valid CLI call
        self.assertEqual(result.exit_code, 0)

    @patch("openstack_flavor_manager.main.get_flavor_definitions")
    @patch("openstack_flavor_manager.main.Cloud.__init__")
    @patch("openstack_flavor_manager.main.FlavorManager.run")
    @patch("openstack_flavor_manager.main.FlavorManager.__init__")
    def test_ensure_command_1(
        self,
        mock_flavor_manager_init,
        mock_run,
        mock_cloud_init,
        mock_get_flavor_definitions,
    ):
        mock_cloud_init.return_value = None
        mock_flavor_manager_init.return_value = None
        mock_get_flavor_definitions.return_value = {}
        result = self.runner.invoke(app, ["--name=scs", "--recommended"])

        # Check that '--name scs --recommended' is a valid CLI call
        self.assertEqual(result.exit_code, 0)

    @patch("openstack_flavor_manager.main.Cloud.__init__")
    @patch("openstack_flavor_manager.main.FlavorManager.__init__")
    def test_ensure_command_2(self, mock_flavor_manager_init, mock_cloud_init):
        mock_cloud_init.return_value = None
        mock_flavor_manager_init.return_value = None
        result = self.runner.invoke(app, ["--name=invalid_name"])

        # Check that '--name invalid_name' is NOT a valid CLI call
        self.assertNotEqual(result.exit_code, 0)

    @patch("openstack_flavor_manager.main.get_flavor_definitions")
    @patch("openstack_flavor_manager.main.Cloud.__init__")
    @patch("openstack_flavor_manager.main.FlavorManager.run")
    @patch("openstack_flavor_manager.main.FlavorManager.__init__")
    def test_callback(
        self,
        mock_flavor_manager_init,
        mock_run,
        mock_cloud_init,
        mock_get_flavor_definitions,
    ):
        mock_cloud_init.return_value = None
        mock_flavor_manager_init.return_value = None
        mock_get_flavor_definitions.return_value = {}
        result = self.runner.invoke(app, ["--debug", "--name=scs"])

        # Check that '--debug' is a valid global CLI option
        self.assertEqual(result.exit_code, 0)


class TestGetFlavorDefinitions(unittest.TestCase):
    @patch("requests.get")
    def test_get_flavor_definitions_0(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = MOCK_YML
        result = get_flavor_definitions("scs")

        expected_result = yaml.safe_load(MOCK_YML)

        # Check if get_flavor_definitions returns the expected dict
        self.assertEqual(result, expected_result)

    @patch("requests.get")
    def test_get_flavor_definitions_1(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.content = "Test 123"
        mock_get.return_value.raise_for_status = mock.Mock(side_effect=HTTPError())

        # Check if the function raises an exception
        self.assertRaises(HTTPError, get_flavor_definitions, "scs")

    @patch("requests.get")
    def test_get_flavor_definitions_2(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = "-" + MOCK_YML

        # Check if the function raises an invalid yaml exception
        self.assertRaises(ParserError, get_flavor_definitions, "scs")

    def test_get_flavor_definitions_3(self):
        # Here we _actually_ download the YML files uploaded to GitHub
        # Therefore, this test requires an active internet connection

        # Resolve 'scs' to correct url
        result = get_flavor_definitions("scs")
        self.assertIs(type(result), dict)

        # Resolve 'osism' to correct url
        result = get_flavor_definitions("osism")
        self.assertIs(type(result), dict)


class TestFlavorManager(unittest.TestCase):
    @patch("openstack_flavor_manager.main.Cloud.__init__")
    def test_init_0(self, mock_init):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = Cloud(cloud="testcloud")

        manager = FlavorManager(c, definitions)

        expected_result = {item["name"]: item for item in definitions["mandatory"]}
        actual_result = {item["name"]: item for item in manager.required_flavors}

        # Check if mandatory items are added to the FlavorManager object
        self.assertEqual(manager.cloud, c)
        self.assertEqual(expected_result, actual_result)

    @patch("openstack_flavor_manager.main.Cloud.__init__")
    def test_init_1(self, mock_init):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = Cloud(cloud="testcloud")

        manager = FlavorManager(c, definitions, True)

        expected_result = {item["name"]: item for item in definitions["mandatory"]}
        for item in definitions["recommended"]:
            expected_result[item["name"]] = item

        actual_result = {item["name"]: item for item in manager.required_flavors}

        # Check if mandatory + recommended items are added to the FlavorManager object
        self.assertEqual(manager.cloud, c)
        self.assertEqual(expected_result, actual_result)

    @patch("openstack_flavor_manager.main.Cloud.__init__")
    def test_init_2(self, mock_init):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = Cloud(cloud="testcloud")

        test = FlavorManager(c, definitions)
        test2 = FlavorManager(c, definitions, True)
        manager = FlavorManager(c, definitions)

        expected_result = {}
        for item in definitions["reference"]:
            if "default" in item:
                expected_result[item["field"]] = item["default"]

        # Check if default fields are correctly parsed
        self.assertEqual(expected_result, manager.defaults_dict)
        self.assertEqual(expected_result, test.defaults_dict)
        self.assertEqual(expected_result, test2.defaults_dict)

    @patch("openstack_flavor_manager.main.Cloud.set_flavor")
    @patch("openstack_flavor_manager.main.Cloud.__init__")
    def test_run_0(self, mock_init, mock_setflavor):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = Cloud(cloud="testcloud")

        manager = FlavorManager(c, definitions)
        manager.run()

        # Check if set_flavor was called once for all mandatory entries
        self.assertEqual(mock_setflavor.call_count, len(definitions["mandatory"]))

    @patch("openstack_flavor_manager.main.Cloud.set_flavor")
    @patch("openstack_flavor_manager.main.Cloud.__init__")
    def test_run_1(self, mock_init, mock_setflavor):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = Cloud(cloud="testcloud")

        manager = FlavorManager(c, definitions, True)
        manager.run()

        # Check if set_flavor was called once for all mandatory + recommended entries
        expected_result = len(definitions["mandatory"]) + len(
            definitions["recommended"]
        )
        self.assertEqual(mock_setflavor.call_count, expected_result)

    @patch("openstack_flavor_manager.main.Cloud.set_flavor")
    @patch("openstack_flavor_manager.main.Cloud.__init__")
    def test_run_2(self, mock_init, mock_setflavor):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = Cloud(cloud="testcloud")

        manager = FlavorManager(c, definitions)
        manager.run()

        # Check if set_flavor was called with the correct arguments
        for i in range(len(definitions["mandatory"])):
            mock_setflavor.assert_any_call(
                flavor_spec=definitions["mandatory"][i], defaults=manager.defaults_dict
            )

    @patch("openstack_flavor_manager.main.Cloud.set_flavor")
    @patch("openstack_flavor_manager.main.Cloud.__init__")
    def test_run_3(self, mock_init, mock_setflavor):
        definitions = yaml.safe_load(MOCK_YML)

        mock_init.return_value = None
        c = Cloud(cloud="testcloud")

        manager = FlavorManager(c, definitions, True)
        manager.run()

        # Check if set_flavor was called with the correct arguments for recommended flavors
        for i in range(len(definitions["recommended"])):
            mock_setflavor.assert_any_call(
                flavor_spec=definitions["recommended"][i],
                defaults=manager.defaults_dict,
            )


class TestCloud(unittest.TestCase):
    def test_spec_or_default_0(self):
        test_spec = {"existing_key": "value1", "existing_key_2": "value2"}

        # Check if existing key is returned
        self.assertEqual(get_spec_or_default("existing_key", test_spec, {}), "value1")
        self.assertEqual(get_spec_or_default("existing_key_2", test_spec, {}), "value2")

    def test_spec_or_default_1(self):
        test_spec = {"existing_key": "value1", "existing_key_2": "value2"}
        default_spec = {"default_key": "value3", "default_key_2": "value4"}

        # Check if default key is returned
        self.assertEqual(
            get_spec_or_default("default_key", test_spec, default_spec), "value3"
        )
        self.assertEqual(
            get_spec_or_default("default_key_2", test_spec, default_spec), "value4"
        )

    def test_spec_or_default_2(self):
        test_spec = {
            "existing_key": True,
            "existing_key_2": False,
        }
        default_spec = {"default_key": True, "default_key_2": False}

        self.assertEqual(
            get_spec_or_default("existing_key", test_spec, default_spec), True
        )
        self.assertEqual(
            get_spec_or_default("existing_key_2", test_spec, default_spec), False
        )

        self.assertEqual(
            get_spec_or_default("default_key", test_spec, default_spec), True
        )
        self.assertEqual(
            get_spec_or_default("default_key_2", test_spec, default_spec), False
        )

    def test_spec_or_default_3(self):
        test_spec = {"existing_key": "value1", "existing_key_2": "value2"}
        default_spec = {"default_key": "value3", "default_key_2": "value4"}

        # Check if Exception is raised
        self.assertRaises(
            ValueError, get_spec_or_default, "unknown_key", test_spec, default_spec
        )

    @patch("openstack.connect")
    def test_init_0(self, mock_connect):
        mock_flavors = MagicMock()
        mock_connect.return_value.list_flavors = mock_flavors

        mock_flavors.return_value = [
            Munch({"name": "SCS-4V-16"}),
            Munch({"name": "SCS-2V-16"}),
            Munch({"name": "SCS-8V-32"}),
        ]

        c = Cloud(cloud="testcloud")

        # Check if connect and list_flavor command against fake openstack data was successful
        self.assertEqual(mock_connect.call_count, 1)
        mock_connect.assert_called_with(cloud="testcloud")
        self.assertEqual(mock_flavors.call_count, 1)
        self.assertEqual(
            c.existing_flavor_names, {"SCS-8V-32", "SCS-2V-16", "SCS-4V-16"}
        )

    @patch("openstack_flavor_manager.main.Cloud.__init__")
    def test_set_flavor_0(self, mock_init):
        mock_init.return_value = None
        c = Cloud(cloud="testcloud")
        c.conn = MagicMock()
        c.conn.create_flavor = MagicMock()
        c.conn.create_flavor.return_value = Munch(
            {"id": "49186969-54a4-470e-ad14-315081685a3d"}
        )
        c.existing_flavor_names = set()
        flavor = c.set_flavor(
            {"name": "SCS-1V-4", "cpus": 1, "ram": 4096, "disk": 0, "t:foo": "bar"},
            {"public": True},
        )
        c.conn.create_flavor.assert_called_with(
            name="SCS-1V-4",
            ram=4096,
            vcpus=1,
            disk=0,
            ephemeral=0,
            swap=0,
            rxtx_factor=1.0,
            is_public=True,
            flavorid="auto",
        )
        c.conn.set_flavor_specs.assert_called_with(
            flavor_id="49186969-54a4-470e-ad14-315081685a3d",
            extra_specs={"t:foo": "bar"},
        )

        # Check that the flavor was created successfully
        self.assertNotEqual(flavor, None)

    @patch("openstack_flavor_manager.main.Cloud.__init__")
    def test_set_flavor_1(self, mock_init):
        mock_init.return_value = None
        c = Cloud(cloud="testcloud")
        c.conn = MagicMock()
        c.conn.create_flavor = MagicMock()
        c.conn.create_flavor.return_value = Munch(
            {"id": "49186969-54a4-470e-ad14-315081685a3d"}
        )
        c.existing_flavor_names = {"SCS-1V-4"}
        flavor = c.set_flavor(
            {"name": "SCS-1V-4", "cpus": 1, "ram": 4096, "disk": 0}, {"public": True}
        )
        c.conn.create_flavor.assert_not_called()
        c.conn.set_flavor_specs.assert_not_called()

        # Check that no flavor has been returned, because it already exists
        self.assertEqual(flavor, None)


if __name__ == "__main__":
    unittest.main()
