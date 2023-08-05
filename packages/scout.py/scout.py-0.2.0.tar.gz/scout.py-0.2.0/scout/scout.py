import sys

import errno
import json
import logging
import os
import platform
import requests
import traceback

from requests.exceptions import Timeout
from uuid import uuid4


class Scout:

    def __init__(self, app, version, install_id=None, id_plugin=None, **kwargs): 
        """
        Create a new Scout instance for later reports.

        :param app: The application name. Required.
        :param version: The application version. Required.
        :param install_id: Optional install_id. If set, Scout will believe it.
        :param id_plugin: Optional plugin function for obtaining an install_id. See below.
        :param kwargs: Any other keyword arguments will be merged into Scout's metadata.

        If an id_plugin is present, it is called with the Scout instance as its first
        parameter and the app name as its second parameter. It must return

        - None to fall back to the default filesystem ID, or
        - a dict containing the ID and optional metadata:
           - The dict **must** have an `install_id` key with a non-empty value.
           - The dict **may** have other keys present, which will all be merged into
             Scout's `metadata`.

        If the plugin returns something invalid, Scout falls back to the default filesystem
        ID.

        Scout logs to the datawire.scout logger. It assumes that the logging system is
        configured to a sane default level, but you can change Scout's debug level with e.g.

        logging.getLogger("datawire.scout").setLevel(logging.DEBUG)

        """

        self.app = Scout.__not_blank("app", app)
        self.version = Scout.__not_blank("version", version)
        self.metadata = kwargs if kwargs is not None else {}
        self.user_agent = self.create_user_agent()

        self.logger = logging.getLogger("datawire.scout")

        self.install_id = install_id

        if not self.install_id and id_plugin:
            plugin_response = id_plugin(self, app)

            self.logger.debug("Scout: id_plugin returns {0}".format(json.dumps(plugin_response)))

            if plugin_response:
                if "install_id" in plugin_response:
                    self.install_id = plugin_response["install_id"]
                    del(plugin_response["install_id"])

                if plugin_response:
                    self.metadata = Scout.__merge_dicts(self.metadata, plugin_response)

        if not self.install_id:
            self.install_id = self.__filesystem_install_id(app)

        self.logger.debug("Scout using install_id {0}".format(self.install_id))

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
        except Exception as e:
            # If scout is down or we are getting errors just proceed as if nothing happened. It should not impact the
            # user at all.
            tb = "\n".join(traceback.format_exception(*sys.exc_info()))

            result['exception'] = e
            result['traceback'] = tb

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

    def __filesystem_install_id(self, app):
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
                install_id = str(uuid4())
                self.metadata["new_install"] = True
                f.write(install_id)
        else:
            with open(id_file, 'r') as f:
                install_id = f.read()

        return install_id

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

    @staticmethod
    def configmap_install_id_plugin(scout, app):
        plugin_response = None
        map_name = "scout.config.{0}".format(app)
        base_url = "https://kubernetes/api/v1/namespaces/default/configmaps"

        kube_token = None

        try:
            kube_token = open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r").read()
        except OSError:
            pass

        if not kube_token:
            # We're not running in Kubernetes. Fall back to the usual filesystem stuff.
            scout.logger.debug("Scout: not running in Kubernetes")
            return None

        # OK, we're in a cluster. Load our map.
        auth_headers = { "Authorization": "Bearer " + kube_token }
        install_id = None

        r = requests.get("{0}/{1}".format(base_url, map_name),
                         headers=auth_headers, verify=False)

        if r.status_code == 200:
            # OK, the map is present. What do we see?
            map_data = r.json()

            if "data" not in map_data:
                # This is "impossible".
                scout.logger.error("Scout: no map data in returned map???")
            else:
                map_data = map_data.get("data", {})
                scout.logger.debug("Scout: configmap has map data %s" % json.dumps(map_data))

                install_id = map_data.get("install_id", None)

                if install_id:
                    scout.logger.debug("Scout: got install_id %s from map" % install_id)
                    plugin_response = { "install_id": install_id }

        if not install_id:
            # No extant install_id. Try to create a new one.
            install_id = str(uuid4())

            cm = {
                "apiVersion":"v1",
                "kind":"ConfigMap",
                "metadata":{
                    "name": map_name,
                    "namespace":"default"
                },
                "data": {
                    "install_id": install_id
                }
            }

            scout.logger.debug("Scout: saving new install_id %s" % install_id)

            r = requests.post(base_url, headers=auth_headers, verify=False, json=cm)

            if r.status_code == 201:
                scout.logger.debug("Scout: saved install_id %s" % install_id)

                plugin_response = {
                    "install_id": install_id,
                    "new_install": True
                }
            else:
                scout.logger.error("Scout: could not save install_id: {0}, {1}".format(r.status_code, r.text))

        scout.logger.debug("Scout: plugin_response %s" % json.dumps(plugin_response))
        return plugin_response
