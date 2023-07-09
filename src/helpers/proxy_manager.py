import requests

from src.helpers.template.proxy import template as proxy_template


class NginxProxyManagerAPI():
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def auth_token(self) -> str:
        endpoints = f"{self.host}:{self.port}/api/tokens"
        payload = {
            "identity": self.user,
            "secret": self.password
        }

        response = requests.post(
            url=endpoints,
            json=payload
        )

        if response.status_code == 200:
            return response.json()['token']
        else:
            return response.status_code

    def list_proxy_host(self):
        # session = requests.session()
        token = self.auth_token()
        endpoint = f"{self.host}:{self.port}/api/nginx/proxy-hosts?expand=owner"

        headers = {
            'Accept': 'application/json',
            "Authorization": f"Bearer {token}"
        }

        response = requests.request("GET", endpoint, headers=headers, data={})

        if response.status_code == 200:
            return response.text
        else:
            return response.status_code
        
    def create_proxy_host(self, domain_name, forward_host, forward_port):
        endpoint = f"{self.host}:{self.port}/api/nginx/proxy-hosts"
        token = self.auth_token()

        headers = {
            'Accept': 'application/json',
            "Authorization": f"Bearer {token}"
        }

        payload = proxy_template

        hostname = self.host.split("//")[1]
        domain_name = f"{domain_name}.{hostname}"

        payload['domain_names'] = [
            domain_name
        ]
        payload['forward_host'] = forward_host
        payload['forward_port'] = forward_port

        proxy_response = requests.request("POST", endpoint, headers=headers, json=payload)

        if proxy_response.status_code == 201:
            return domain_name
        else:
            _ = requests.request("POST", endpoint, headers=headers, json=payload)
            return domain_name

    def remove_proxy_host(self, id: int):
        endpoint = f"{self.host}:{self.port}/api/nginx/proxy-hosts/{id}"
        token = self.auth_token()

        headers = {
            'Accept': 'application/json',
            "Authorization": f"Bearer {token}"
        }
        response = requests.request("DELETE", endpoint, headers=headers)

        return response.text


if __name__ == "__main__":
    api = NginxProxyManagerAPI(
        host="http://127.0.0.1",
        port=81,
        user="tsdocode@gmail.com",
        password="2112001a"
    )

    response = api.create_proxy_host(
        "app.127.0.0.1.nip.io",
        "budibase",
        80
    )
