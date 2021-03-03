def main(client, testing=False):
    if testing:
        return
    search = client.search("Hunting")
    challenge = search.challenges[0]
    challenge.start()
    instance = challenge.instance
    challenge.submit("HTB{fake_flag}", 20)
    print(instance.ip, instance.port)
    instance.stop()


if __name__ == "__main__":
    from base import client as example_client
    main(example_client)
