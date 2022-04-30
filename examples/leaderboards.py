def main(client, _testing=False):
    hof = client.get_hof()
    print(hof[0])
    for i in hof:
        print(i)


if __name__ == "__main__":
    from base import client as example_client

    main(example_client)
