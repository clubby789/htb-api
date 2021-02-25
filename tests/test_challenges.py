import pytest
from pytest import raises
from hackthebox import HTBClient


@pytest.mark.asyncio
async def test_get_challenge(htb_client: HTBClient):
    """Tests the ability to retrieve a specific challenge"""
    challenge = await htb_client.get_challenge(69)
    assert challenge.id == 69
    assert challenge.name == "TheFutureBender"
    assert challenge.retired


@pytest.mark.asyncio
async def test_get_non_existent_challenge(htb_client: HTBClient):
    """Tests for a failure upon a non existent challenge"""
    with raises(Exception):
        await htb_client.get_challenge(10000000)


@pytest.mark.asyncio
async def test_get_challenges(htb_client: HTBClient):
    """Tests that the challenges can be listed"""
    challenges = await htb_client.get_challenges(limit=30)
    assert len(challenges) == 30
    challenges = await htb_client.get_challenges(limit=30, retired=True)
    assert len(challenges) == 30


@pytest.mark.asyncio
async def test_fill_in_summary(htb_client: HTBClient):
    """Test that partial `Challenges` can be 'filled in'"""
    challenge = (await htb_client.get_challenges(limit=1))[0]
    assert challenge.description is not None
