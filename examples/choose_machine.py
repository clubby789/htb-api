import random


def main(client):
    machines = client.get_machines()
    print(f"Chosen Machine: {random.choice(machines)}")


if __name__ == "__main__":
    from base import client as example_client
    main(example_client)
