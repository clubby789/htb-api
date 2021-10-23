from __future__ import annotations

import os

from . import htb


class VPNServer(htb.HTBObject):
    """Class representing individual VPN servers provided by Hack The Box

    Attributes:
        friendly_name: Friendly name of the server
        current_clients: The number of currently connected clients
        location: The physical location of the server

    """

    friendly_name: str = None
    current_clients: int = None
    location: str = None

    # noinspection PyUnresolvedReferences
    def __init__(self, data: dict, client: "HTBClient", summary=False):
        """Initialise a `VPNServer` using API data"""
        self._client = client
        self._detailed_func = lambda x: None
        self.id = data["id"]
        self.friendly_name = data["friendly_name"]
        self.current_clients = data["current_clients"]
        self.location = data["location"]
        self.summary = summary

    def __repr__(self):
        return f"<VPN Server '{self.friendly_name}'>"

    def switch(self) -> bool:
        # TODO: Throw exception on failure
        return self._client.do_request(f"connections/servers/switch/{self.id}", post=True)["status"] is True

    def download(self, path=None, tcp=False) -> str:
        """

        Args:
            path: The name of the OVPN file to download to. If none is provided, it is saved to the current directory.
            tcp: Download TCP instead of UDP

        Returns: The path of the file

        """
        if path is None:
            path = os.path.join(os.getcwd(), f"{self.friendly_name}.ovpn")
        url = f"access/ovpnfile/{self.id}/0"
        if tcp:
            # Funky URL
            url += "/1"
        data = self._client.do_request(url, download=True)
        # We can't download VPN packs for servers we're not assigned to
        if b'You are not assigned' in data:
            self.switch()
        data = self._client.do_request(url, download=True)
        with open(path, 'wb') as f:
            f.write(data)
        return path
