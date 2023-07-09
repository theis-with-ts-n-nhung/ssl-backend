import os
import yaml
from dotenv import load_dotenv

load_dotenv()


class CloudflaredAPI:
    def __init__(self) -> None:
        self.config_file = os.environ["CLOUDFLARED_FILE"]

    def load_config(self):
        with open(self.config_file, "r") as fb:
            try:
                config = yaml.safe_load(fb)
            except yaml.YAMLError as exc:
                print(exc)
                config = {}
        return config

    def write_config(self, config, filepath=None):
        if not filepath:
            filepath = self.config_file
        with open(filepath, 'w') as fp:
            result = yaml.dump(config, fp)

        return result

    def add_host(self, localname="", hostname=""):
        config = self.load_config()
        target = {
            "hostname": hostname,
            "service": localname
        }

        config['ingress'].insert(0, target)

        self.write_config(
            config
        )


if __name__ == "__main__":
    api = CloudflaredAPI()
    api.add_host(
        hostname="pro.tsdocode.online",
        localname="budibase:80"
    )
