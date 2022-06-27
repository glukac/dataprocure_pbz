import requests
from datetime import datetime

from domains_config import DOMAINS

proxies = dict(
    http='socks5://localhost:9090',
    https='socks5://localhost:9090')


class RequestMaker:
    def __init__(self, domain, use_proxy=False):
        self.domain_url = DOMAINS[domain].get('url')
        self.token = DOMAINS[domain].get('token')

        self.kwargs = {
        }
        if use_proxy:
            self.kwargs['proxies'] = proxies

    def get_categories(self):
        resp = requests.get('{domain_url}/api/categories?token={token}'.format(
            domain_url=self.domain_url,
            token=self.token), **self.kwargs)

        return resp.json()

    def get_clients(self):
        resp = requests.get('{domain_url}/api/clients?token={token}'.format(
            domain_url=self.domain_url,
            token=self.token), **self.kwargs)

        return resp.json()

    def get_participants(self, client_id, updated_after):
        resp = requests.get('{domain_url}/api/clients/{client_id}/participants?token={token}&updatedAfter={updated_after}'.format(
            domain_url=self.domain_url,
            client_id=client_id,
            token=self.token,
            updated_after=updated_after), **self.kwargs)

        return resp.json()

    def get_participant_detail(self, client_id, participant_id):
        resp = requests.get('{domain_url}/api/clients/{client_id}/participants/{participant_id}?token={token}'.format(
            domain_url=self.domain_url,
            client_id=client_id,
            participant_id=participant_id,
            token=self.token), **self.kwargs)

        return resp.json()

    def get_auctions(self, client_id, updated_after):
        resp = requests.get('{domain_url}/api/clients/{client_id}/auctions?token={token}&updatedAfter={updated_after}'.format(
            domain_url=self.domain_url,
            client_id=client_id,
            token=self.token,
            updated_after=updated_after), **self.kwargs)

        return resp.json()

    def get_auction_detail(self, client_id, auction_id):
        resp = requests.get('{domain_url}/api/clients/{client_id}/auctions/{auction_id}?token={token}'.format(
            domain_url=self.domain_url,
            client_id=client_id,
            auction_id=auction_id,
            token=self.token), **self.kwargs)

        return resp.json()
