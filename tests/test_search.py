from hackthebox import HTBClient


def test_search(mock_htb_client: HTBClient):
    search = mock_htb_client.search("lame")
    repr(search)
    # Resolve the results of the search
    repr(search.items)
    assert len(search) > 0
    repr(search)
