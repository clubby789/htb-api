from hackthebox import HTBClient


def test_get_fortress(htb_client: HTBClient):
    """Tests the ability to retrieve a specific fortress"""
    fortress = htb_client.get_fortress(1)
    assert fortress.id == 1
    assert fortress.name == "Jet"
    print(fortress)


def test_get_fortresses(htb_client: HTBClient):
    """Tests the ability to retrieve the list of Fortresses"""
    fortresses = htb_client.get_fortresses()
    assert len(fortresses) >= 3
    assert fortresses[0].num_flags == 11
