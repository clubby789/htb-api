import pytest
from pytest import raises
from hackthebox import HTBClient


@pytest.mark.asyncio
async def test_get_machine(htb_client: HTBClient):
    """Tests the ability to retrieve a specific machine"""
    machine = await htb_client.get_machine(1)
    assert machine.id == 1
    assert machine.name == "Lame"


@pytest.mark.asyncio
async def test_get_non_existent_machine(htb_client: HTBClient):
    """Tests for a failure upon a non existent challenge"""
    with raises(Exception):
        await htb_client.get_machine(10000000)


@pytest.mark.asyncio
async def test_list_machines(htb_client: HTBClient):
    """Tests that the challenges can be listed"""
    machines = await htb_client.get_machines()
    assert len(machines) >= 20
    retired = await htb_client.get_machines(retired=True)
    assert len(retired) >= 150


@pytest.mark.asyncio
async def test_machine_author(htb_client: HTBClient):
    """Tests retrieving the author of a machine"""
    machine = await htb_client.get_machine(1)
    author = (await machine.authors)[0]
    assert author.name == "ch4p"
