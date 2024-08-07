import unittest
from unittest import mock

import typer
from typer.testing import CliRunner
from unittest.mock import MagicMock
from munch import Munch
import uuid
import yaml

from openstack_flavor_manager.main import run

app = typer.Typer()
app.command()(run)

UUID_LIST = [Munch({"id": str(uuid.uuid4())}) for i in range(40)]

FLAVOR_YML = """
reference:
- field: name
  mandatory_prefix: SCS-
- field: public
  default: True
- field: disabled
  default: False
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
- name: SCS-8V-32
  cpus: 8
  ram: 32768
  disk: 0
- name: SCS-1V-2
  cpus: 1
  ram: 2048
  disk: 0
- name: SCS-2V-4
  cpus: 2
  ram: 4096
  disk: 0
- name: SCS-4V-8
  cpus: 4
  ram: 8192
  disk: 0
- name: SCS-8V-16
  cpus: 8
  ram: 16384
  disk: 0
- name: SCS-16V-32
  cpus: 16
  ram: 32768
  disk: 0
- name: SCS-1V-8
  cpus: 1
  ram: 8192
  disk: 0
- name: SCS-2V-16
  cpus: 2
  ram: 16384
  disk: 0
- name: SCS-4V-32
  cpus: 4
  ram: 32768
  disk: 0
- name: SCS-1L-1
  cpus: 1
  ram: 1024
  disk: 0
- name: SCS-2V-4-20s
  cpus: 2
  ram: 4096
  disk: 20
- name: SCS-4V-16-100s
  cpus: 4
  ram: 16384
  disk: 100
recommended:
- name: SCS-1V-4-10
  cpus: 1
  ram: 4096
  disk: 10
- name: SCS-2V-8-20
  cpus: 2
  ram: 8192
  disk: 20
- name: SCS-4V-16-50
  cpus: 4
  ram: 16384
  disk: 50
- name: SCS-8V-32-100
  cpus: 8
  ram: 32768
  disk: 100
- name: SCS-1V-2-5
  cpus: 1
  ram: 2048
  disk: 5
- name: SCS-2V-4-10
  cpus: 2
  ram: 4096
  disk: 10
- name: SCS-4V-8-20
  cpus: 4
  ram: 8192
  disk: 20
- name: SCS-8V-16-50
  cpus: 8
  ram: 16384
  disk: 50
- name: SCS-16V-32-100
  cpus: 16
  ram: 32768
  disk: 100
- name: SCS-1V-8-20
  cpus: 1
  ram: 8192
  disk: 20
- name: SCS-2V-16-50
  cpus: 2
  ram: 16384
  disk: 50
- name: SCS-4V-32-100
  cpus: 4
  ram: 32768
  disk: 100
- name: SCS-1L-1-5
  cpus: 1
  ram: 1024
  disk: 5
"""


class TestIntegrationEnsure(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @mock.patch("requests.Session.get")
    @mock.patch("openstack_flavor_manager.main.openstack.connect")
    def test_ensure_0(self, mock_conn, mock_request):
        mock_existing_flavors = [
            Munch({"name": "SCS-4V-16"}),
            Munch({"name": "SCS-2V-16"}),
            Munch({"name": "SCS-8V-32"}),
        ]
        mock_conn.return_value.list_flavors.return_value = mock_existing_flavors
        mock_createflavor = MagicMock()
        mock_createflavor.side_effect = UUID_LIST
        mock_conn.return_value.create_flavor = mock_createflavor
        mock_setflavorspecs = MagicMock()
        mock_conn.return_value.set_flavor_specs = mock_setflavorspecs

        mock_request.return_value.status_code = 200
        mock_request.return_value.content = FLAVOR_YML

        self.runner.invoke(app, ["--name=scs"])

        self.assertEqual(mock_request.call_count, 1)

        expected_result = yaml.safe_load(FLAVOR_YML)
        expected_creation_count = len(expected_result["mandatory"]) - len(
            mock_existing_flavors
        )

        self.assertEqual(mock_createflavor.call_count, expected_creation_count)
        self.assertEqual(mock_setflavorspecs.call_count, expected_creation_count)

        for i in range(expected_creation_count):
            mock_setflavorspecs.assert_any_call(
                flavor_id=UUID_LIST[i].id, extra_specs={}
            )

    @mock.patch("requests.Session.get")
    @mock.patch("openstack_flavor_manager.main.openstack.connect")
    def test_ensure_1(self, mock_conn, mock_request):
        mock_existing_flavors = [
            Munch({"name": "SCS-4V-16"}),
            Munch({"name": "SCS-2V-16"}),
            Munch({"name": "SCS-8V-32"}),
        ]
        mock_conn.return_value.list_flavors.return_value = mock_existing_flavors
        mock_createflavor = MagicMock()
        mock_createflavor.side_effect = UUID_LIST
        mock_conn.return_value.create_flavor = mock_createflavor
        mock_setflavorspecs = MagicMock()
        mock_conn.return_value.set_flavor_specs = mock_setflavorspecs

        mock_request.return_value.status_code = 200
        mock_request.return_value.content = FLAVOR_YML

        self.runner.invoke(app, ["--recommended", "--name=scs"])

        self.assertEqual(mock_request.call_count, 1)

        expected_result = yaml.safe_load(FLAVOR_YML)
        expected_creation_count = (
            len(expected_result["mandatory"])
            + len(expected_result["recommended"])
            - len(mock_existing_flavors)
        )

        self.assertEqual(mock_createflavor.call_count, expected_creation_count)
        self.assertEqual(mock_setflavorspecs.call_count, expected_creation_count)

        for i in range(expected_creation_count):
            mock_setflavorspecs.assert_any_call(
                flavor_id=UUID_LIST[i].id, extra_specs={}
            )
