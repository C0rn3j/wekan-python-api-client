import requests
from .models import Board


class WekanApi:
    def api_call(self, url, data=None, authed=True, method='GET'):
        if data is not None and method is 'GET':
            method='POST'
        match method:
            case 'GET':
                api_response = self.session.get(
                    "{}{}".format(self.api_url, url),
                    headers={"Authorization": "Bearer {}".format(self.token)},
                    proxies=self.proxies
                )
            case 'POST':
                api_response = self.session.post(
                    "{}{}".format(self.api_url, url),
                    json=data,
                    headers={"Authorization": "Bearer {}".format(self.token)} if authed else {},
                    proxies=self.proxies
                )
            case 'PUT':
                api_response = self.session.put(
                    "{}{}".format(self.api_url, url),
                    json=data,
                    headers={"Authorization": "Bearer {}".format(self.token)} if authed else {},
                    proxies=self.proxies
                )
            case _:
                print('UNKNOWN METHOD "{}"', format(method))
                exit(1)
        return api_response.json()

    def __init__(self, api_url, credentials, proxies=None):
        if proxies is None:
            proxies = {}
        self.session = requests.Session()
        self.proxies = proxies
        self.api_url = api_url
        api_login = self.api_call("/users/login", data=credentials, authed=False)
        self.token = api_login["token"]
        self.user_id = api_login["id"]

    def get_user_boards(self, filter=''):
        boards_data = self.api_call("/api/users/{}/boards".format(self.user_id))
        return [Board(self, board_data) for board_data in boards_data if filter in board_data["title"]]
