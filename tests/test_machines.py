from pytest import raises

from hackthebox import HTBClient


def test_get_machine(mock_htb_client: HTBClient):
    """Tests the ability to retrieve a specific machine"""
    machine = mock_htb_client.get_machine(1)
    assert machine.id == 1
    assert machine.name == "Lame"
    repr(machine)


def test_get_active_machine(mock_htb_client: HTBClient):
    """Tests the ability to retrieve active machine"""
    machine = mock_htb_client.get_active_machine()
    assert machine.id == 387
    assert machine.name == "Driver"
    print(machine)


def test_get_solves(mock_htb_client: HTBClient):
    """Tests the ability to retrieve a specific machine"""
    machine = mock_htb_client.get_machine(1)
    repr(machine.root_blood)
    assert machine.root_blood.machine == machine


def test_get_non_existent_machine(mock_htb_client: HTBClient):
    """Tests for a failure upon a non existent challenge"""
    with raises(Exception):
        mock_htb_client.get_machine(10000000)


def test_list_machines(mock_htb_client: HTBClient):
    """Tests that the challenges can be listed"""
    machines = mock_htb_client.get_machines()
    assert len(machines) >= 20
    retired = mock_htb_client.get_machines(retired=True)
    assert len(retired) >= 150


def test_machine_author(mock_htb_client: HTBClient):
    """Tests retrieving the author of a machine"""
    machine = mock_htb_client.get_machine(1)
    author = machine.authors[0]
    assert author.name == "ch4p"
