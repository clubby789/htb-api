import random


def main(client, _testing=False):
    machines = client.get_machines()
    print(f"Chosen Machine: {random.choice(machines)}")


if __name__ == "__main__":
    from base import client as example_client

    main(example_client)
