from oauth2 import Consumer, Token, Client
from typing import Union
from urllib.parse import urlencode, urljoin, parse_qs
from json import loads


class PlurkApi:
    def __init__(self, api_key: str, api_secret: str, token_key: str, token_secret: str,
                 base_url: str = "https://www.plurk.com"):
        consumer = Consumer(api_key, api_secret)  # type:Consumer
        token = Token(token_key, token_secret)  # type:Token
        self.client = Client(consumer, token)  # type:Client
        self.base_url = base_url  # type:str

    def request(self, end_point: str, parameters: Union[dict, str] = None) -> dict:
        if isinstance(parameters, dict):
            parameters = urlencode(parameters)
        if isinstance(parameters, str):
            parameters = parameters.encode()
        else:
            parameters = None
        url = urljoin(self.base_url, end_point)
        header, content = self.client.request(url, "POST", parameters)
        return loads(content.decode())


class PlurkOAuthApi:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://www.plurk.com"):
        self.consumer = Consumer(api_key, api_secret)  # type:Consumer
        self.client = Client(self.consumer)  # type:Client
        self.base_url = base_url  # type:str

    def request_token(self) -> dict:
        url = urljoin(self.base_url, "/OAuth/request_token")
        header, content = self.client.request(url, "POST")
        return parse_qs(content)

    def authorization_url(self, request_token: dict):
        return urljoin(self.base_url, f"/OAuth/authorize?oauth_token={request_token['oauth_token']}")

    def access_token(self, request_token: dict, verifier: str) -> dict:
        url = urljoin(self.base_url, "/OAuth/access_token")
        token = Token(request_token["oauth_token"], request_token["oauth_token_secret"])
        token.set_verifier(verifier)
        self.client.token = token
        header, content = self.client.request(url, "POST")
        return parse_qs(content)
