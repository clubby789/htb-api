from hackthebox import HTBClient


def test_get_endgame(htb_client: HTBClient):
    """Tests the ability to retrieve a specific endgame"""
    endgame = htb_client.get_endgame(1)
    assert endgame.id == 1
    assert endgame.name == "P.O.O."


def test_get_endgames(htb_client: HTBClient):
    """Tests the ability to retrieve the list of Endgames"""
    endgames = htb_client.get_endgames()
    assert len(endgames) >= 5
    assert endgames[-1].points == 150


def test_get_endgame_authors(htb_client: HTBClient):
    """Tests the ability to retrieve the authors of an Endgame"""
    endgame = htb_client.get_endgame(1)
    authors = endgame.authors
    assert authors[0].name == "eks"
