# -*- coding: utf-8 -*-
#
# Copyright 2017 Joseph Weston
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Interface to the NordVPN web API.

This module contains a single class, `Client`, which encapsulates
all the methods provided by NordVPN.
"""
from hashlib import sha512

import aiohttp

from ._version import get_versions
from ._utils import async_lru_cache


PORTS = dict(tcp=443, udp=1194)


# Low-level utilities

def normalized_hostname(hostname):
    """Return the fully qualified domain name of a NordVPN host."""
    host, *domain = hostname.split('.')
    if not domain:
        return f'{host}.nordvpn.com'
    elif tuple(domain) != ('nordvpn', 'com'):
        raise ValueError(f'invalid NordVPN host {hostname}')
    return hostname


def _config_filename(vpn_host, protocol='tcp'):
    return f'{vpn_host}.{protocol}{PORTS[protocol]}'


def _openvpn_compatible(host):
    features = host['features']
    return features['openvpn_udp'] and features['openvpn_tcp']


class Client:
    """Interface to the NordVPN web API.

    Instances of this class can be used as async context managers
    to auto-close the session with the Nord API on exit.

    Parameters
    ----------
    api_url : str, default: 'https://api.nordvpn.com'
    """
    def __init__(self, api_url='http://api.nordvpn.com/'):
        self.api_url = api_url
        client_version = get_versions()['version'].split('+')[0]
        self.headers = {
            'User-Agent': f"nord/{client_version}"
        }
        self._session = aiohttp.ClientSession(raise_for_status=True)

    def close(self):
        """Close the underlying aiohttp.ClientSession."""
        self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_typ, exc, traceback):
        self.close()

    async def _get_json(self, endpoint):
        url = ''.join((self.api_url, endpoint))
        async with self._session.get(url, headers=self.headers) as resp:
            return await resp.json()

    async def _get_text(self, endpoint):
        url = ''.join((self.api_url, endpoint))
        async with self._session.get(url, headers=self.headers) as resp:
            return await resp.text()

    # API methods

    @async_lru_cache()
    async def host_config(self, host, protocol='tcp'):
        """Return the OpenVPN config file contents for a NordVPN host.

        Parameters
        ----------
        host : str
            This hostname may be provided either with or without
            the trailing '.nordvpn.com'.
        protocol: str, 'tcp' or 'udp'
        """
        host = normalized_hostname(host)
        endpoint = f'files/download/{_config_filename(host, protocol)}'
        return await self._get_text(endpoint)


    async def host_load(self, host=None):
        """Return the load on a NordVPN host.

        Parameters
        ----------
        host : str, optional
            This hostname may be provided either with or without the trailing
            '.nordvpn.com'. If not provided, get the load on all NordVPN hosts.

        Returns
        -------
        load : int or (dict: str → int)
            If 'host' was provided, returns the load on the host as
            a percentage, otherwise returns a map from hostname
            to percentage load.
        """
        if host:
            host = normalized_hostname(host)
        endpoint = f'server/stats/{host}' if host else 'server/stats'
        resp = await self._get_json(endpoint)
        if host:
            if len(resp) != 1:
                # Nord API returns load on all hosts if 'host' does not exist.
                raise KeyError(f'{host} does not exist')
            return resp['percent']
        else:
            return {host: load['percent'] for host, load in resp.items()}


    async def current_ip(self):
        """Return our current public IP address, as detected by NordVPN."""
        return await self._get_text('user/address')


    @async_lru_cache()
    async def host_info(self):
        """Return detailed information about all hosts.

        Returns
        -------
        host_info : (dict: str → dict)
            A map from hostnames to host info dictionaries.
        """
        info = await self._get_json('server')
        return {h['domain']: h for h in info}


    @async_lru_cache()
    async def dns_servers(self):
        """Return a list of ip addresses of NordVPN DNS servers."""
        return await self._get_json('dns/smart')


    async def valid_credentials(self, username, password):
        """Return True if NordVPN accepts the username and password.

        Sometimes connecting to the VPN server gives an authentication
        error even if the correct credentials are given. This function
        is useful to first verify credentials so as to avoid unecessary
        reconnection attempts.

        Parameters
        ----------
        username, password : str
        """
        try:
            resp = await self._get_json(f'token/token/{username}')
        except aiohttp.ClientResponseError as error:
            # If the username is incorrect the Nord API returns at 200
            # response, but the mimetype is set to HTML. lol.
            if error.code == 0 and 'unexpected mimetype' in error.message:
                return False
            else:
                raise

        token, salt, key = (resp[k] for k in ['token', 'salt', 'key'])

        round1 = sha512(salt.encode() + password.encode())
        round2 = sha512(round1.hexdigest().encode() + key.encode())
        response = round2.hexdigest()

        try:
            return await self._get_json(f'token/verify/{token}/{response}')
        except aiohttp.ClientResponseError as error:
            if error.code == 401:
                return False
            else:
                raise
