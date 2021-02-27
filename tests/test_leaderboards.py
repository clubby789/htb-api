from hackthebox import HTBClient


def test_get_hofs(htb_client: HTBClient):
    """Tests the ability to retrieve the Halls of Fame"""
    hof = htb_client.get_hof()
    # Shared points = Same rank = More users
    assert len(hof) >= 100

    hof_vip = htb_client.get_hof(vip=True)
    assert len(hof_vip) >= 100

    hof_teams = htb_client.get_hof_teams()
    assert len(hof_teams) >= 100

    hof_countries = htb_client.get_hof_countries()
    assert len(hof_countries) >= 100
