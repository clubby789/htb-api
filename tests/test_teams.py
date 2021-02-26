import pytest
from pytest import raises
from hackthebox import HTBClient


@pytest.mark.asyncio
async def test_get_team(htb_client: HTBClient):
    """Tests the ability to retrieve a specific team"""
    team = await htb_client.get_team(2710)
    assert team.id == 2710
    assert team.name == "TheWINRaRs"
    print(team)


@pytest.mark.asyncio
async def test_get_non_existent_team(htb_client: HTBClient):
    """Tests for a failure upon a non existent team"""
    with raises(Exception):
        await htb_client.get_team(10000000)


@pytest.mark.asyncio
async def test_get_ranking(htb_client: HTBClient):
    team = await htb_client.get_team(2710)
    assert (await team.ranking) is not None


@pytest.mark.asyncio
async def test_get_captain(htb_client: HTBClient):
    admins = await htb_client.get_team(21)
    assert (await admins.captain).name == "ch4p"
