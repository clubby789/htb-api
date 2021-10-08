from hackthebox import HTBClient


def test_get_endgame(mock_htb_client: HTBClient):
    """Tests the ability to retrieve a specific endgame"""
    endgame = mock_htb_client.get_endgame(1)
    assert endgame.id == 1
    assert endgame.name == "P.O.O."
    print(endgame)


def test_get_endgames(mock_htb_client: HTBClient):
    """Tests the ability to retrieve the list of Endgames"""
    endgames = mock_htb_client.get_endgames()
    assert len(endgames) >= 5
    assert endgames[-1].name == "P.O.O."
    # The Endgame has been retired
    assert endgames[-1].points == 0


def test_get_endgame_authors(mock_htb_client: HTBClient):
    """Tests the ability to retrieve the authors of an Endgame"""
    endgame = mock_htb_client.get_endgame(1)
    authors = endgame.authors
    assert authors[0].name == "eks"
