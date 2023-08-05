import errno
import os
import platform
import requests

from requests.exceptions import Timeout
from uuid import uuid4


class Scout:

    def __init__(self, app, version, **kwargs):
        self.app = Scout.__not_blank("app", app)
        self.version = Scout.__not_blank("version", version)
        self.metadata = kwargs if kwargs is not None else {}
        self.user_agent = self.create_user_agent()

        self.__init_install_id(app)

        # scout options; controlled via env vars
        self.scout_host = os.getenv("SCOUT_HOST", "kubernaut.io")
        self.use_https = os.getenv("SCOUT_HTTPS", "1").lower() in {"1", "true", "yes"}
        self.disabled = Scout.__is_disabled()

    def report(self, **kwargs):
        result = {'latest_version': self.version}

        if self.disabled:
            return result

        merged_metadata = Scout.__merge_dicts(self.metadata, kwargs)

        headers = {
            'User-Agent': self.user_agent
        }

        payload = {
            'application': self.app,
            'version': self.version,
            'install_id': self.install_id,
            'user_agent': self.create_user_agent(),
            'metadata': merged_metadata
        }

        url = ("https://" if self.use_https else "http://") + "{}/scout".format(self.scout_host).lower()
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=1)
            if resp.status_code / 100 == 2:
                result = Scout.__merge_dicts(result, resp.json())
        except:
            # If scout is down or we are getting errors just proceed as if nothing happened. It should not impact the
            # user at all.
            pass

        if "new_install" in self.metadata:
            del self.metadata["new_install"]

        return result

    def create_user_agent(self):
        result = "{0}/{1} ({2}; {3}; python {4})".format(
            self.app,
            self.version,
            platform.system(),
            platform.release(),
            platform.python_version()).lower()

        return result

    def __init_install_id(self, app):
        config_root = os.path.join(os.path.expanduser("~"), ".config", app)
        try:
            os.makedirs(config_root)
        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(config_root):
                pass
            else:
                raise

        id_file = os.path.join(config_root, "id")
        if not os.path.isfile(id_file):
            with open(id_file, 'w') as f:
                self.install_id = str(uuid4())
                self.metadata["new_install"] = True
                f.write(self.install_id)
        else:
            with open(id_file, 'r') as f:
                self.install_id = f.read()

    @staticmethod
    def __not_blank(name, value):
        if value is None or str(value).strip() == "":
            raise ValueError("Value for '{}' is blank, empty or None".format(name))

        return value

    @staticmethod
    def __merge_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z

    @staticmethod
    def __is_disabled():
        if str(os.getenv("TRAVIS_REPO_SLUG")).startswith("datawire/"):
            return True

        return os.getenv("SCOUT_DISABLE", "0").lower() in {"1", "true", "yes"}
