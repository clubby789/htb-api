from pytest import raises
from hackthebox import HTBClient


def test_get_machine(htb_client: HTBClient):
    """Tests the ability to retrieve a specific machine"""
    machine = htb_client.get_machine(1)
    assert machine.id == 1
    assert machine.name == "Lame"


def test_get_non_existent_machine(htb_client: HTBClient):
    """Tests for a failure upon a non existent challenge"""
    with raises(Exception):
        htb_client.get_machine(10000000)


def test_list_machines(htb_client: HTBClient):
    """Tests that the challenges can be listed"""
    machines = htb_client.get_machines()
    assert len(machines) >= 20
    retired = htb_client.get_machines(retired=True)
    assert len(retired) >= 150


def test_machine_author(htb_client: HTBClient):
    """Tests retrieving the author of a machine"""
    machine = htb_client.get_machine(1)
    author = machine.authors[0]
    assert author.name == "ch4p"
