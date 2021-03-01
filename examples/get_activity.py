def main(client, _testing=False):
    print(client.user.activity)


if __name__ == "__main__":
    from base import client as example_client
    main(example_client)
