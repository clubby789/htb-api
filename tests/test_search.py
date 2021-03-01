from hackthebox import HTBClient


def test_search(htb_client: HTBClient):
    search = htb_client.do_search("blue")
    print(search)
    # Resolve the results of the search
    items = search.items
    assert len(search) > 0
    print(search)
