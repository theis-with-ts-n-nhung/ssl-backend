import random
import string
import requests
import time


def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # includes uppercase letters, lowercase letters, and digits
    return ''.join(random.choice(characters) for _ in range(length)).lower()


def health_check(url, health="/health"):
    attemps = 5
    while attemps:
        response = requests.get(url="http://" + url + health)
        print(response.text)
        if response.status_code == 200:
            return True
        attemps -= 1
        time.sleep(15)

    return False
