import requests


class LabelStudioAPI:
    def __init__(self, url: str) -> None:
        self.url = url
        self.token = None

    def set_token(self, token: str):
        self.token = token

    def auth(self):
        endpoint = self.url + "/api/projects"
        headers = {
            'Authorization': f'Token {self.token}'
        }

        response = requests.get(endpoint, headers=headers)

        # Check the response
        if response.status_code == 200:
            return True
        else:
            return False

    def get_user(self):
        endpoint = self. url + "/api/current-user/whoami"
        headers = {
            'Authorization': f'Token {self.token}'
        }

        response = requests.get(endpoint, headers=headers)

        # Check the response
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code

    def list_project(self):
        endpoint = self.url + "/api/projects"
        headers = {
            'Authorization': f'Token {self.token}'
        }

        response = requests.get(endpoint, headers=headers)

        # Check the response
        if response.status_code == 200:
            return response.json()
        else:
            return False


if __name__ == "__main__":
    api = LabelStudioAPI(
        "https://labelstudio-labelstudio.hf.space"
    )

    api.set_token("6150e0602992c2276c335914ba92684fdcb4e486")

    result = api.auth()
    user = api.list_project()

    print(user['results'][0])