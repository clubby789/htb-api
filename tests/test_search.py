from hackthebox import HTBClient


def test_search(mock_htb_client: HTBClient):
    search = mock_htb_client.search("lame")
    print(search)
    # Resolve the results of the search
    print(search.items)
    assert len(search) > 0
    print(search)
