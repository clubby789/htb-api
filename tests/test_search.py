from hackthebox import HTBClient


def test_search(htb_client: HTBClient):
    search = htb_client.search("blue")
    print(search)
    # Resolve the results of the search
    print(search.items)
    assert len(search) > 0
    print(search)
