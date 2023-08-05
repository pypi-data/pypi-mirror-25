import logging
import os
import platform 
import requests
import unittest
import uuid

try:
    from unittest import mock
except ImportError:
    # In Python 2, "mock" is an addon
    import mock

from .scout import Scout


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s test_scout %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Uncomment if you're trying to debug the tests.
# logging.getLogger("root").setLevel(logging.DEBUG)
# logging.getLogger("datawire.scout").setLevel(logging.DEBUG)

logging.info("Running under Python %s" % platform.python_version())

install_id = str(uuid.uuid4())

PLUGIN_UUID = str(uuid.uuid4())

def install_id_plugin(scout, app, hello="FAILED"):
    return { "install_id": PLUGIN_UUID,
             "new_install": True,
             "swallow_speed": 42,
             "hello": hello }

# This method will be used by the mock to replace requests.get
def mocked_requests_post(*args, **kwargs):

    apps = {'foshizzolator'}
    latest_version = '0.2.0'

    class MockResponse:
        def __init__(self, json_data, status_code, text=None):
            self.json_data = json_data
            self.status_code = status_code
            self.text = text or "<empty>"

        def json(self):
            return self.json_data

    app = kwargs["json"]["application"]

    mockresp = MockResponse({"latest_version": latest_version}, 200)

    if app not in apps:
        mockresp = MockResponse(None, 404, "Application not found!")

    logging.debug("MR: %d (%s) %s" % 
                  (mockresp.status_code, mockresp.text, mockresp.json_data))

    return mockresp


class ScoutTestCase(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_disable_by_SCOUT_DISABLE_environment_variable(self, mock_post):
        for v in {"1", "true", "yes"}:
            os.environ["SCOUT_DISABLE"] = v

            scout = Scout(app="unknown", version="0.1.0", install_id=install_id)
            scout.report()

            self.assertFalse(mock_post.called)
            del os.environ["SCOUT_DISABLE"]

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_disable_by_TRAVIS_REPO_SLUG_environment_variable(self, mock_post):
        os.environ["TRAVIS_REPO_SLUG"] = "datawire/foobar"

        scout = Scout(app="unknown", version="0.1.0", install_id=install_id)
        scout.report()

        self.assertFalse(mock_post.called)
        del os.environ["TRAVIS_REPO_SLUG"]

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_report_for_unknown_app(self, mock_post):
        
        """When the app is unknown scout will return an HTTP 404 but the report function should just act normally"""
        
        scout = Scout(app="unknown", version="0.1.0", install_id=install_id)
        resp = scout.report()

        logging.debug("SR: %s" % resp)
        self.assertEqual(resp, {"latest_version": "0.1.0"})

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_report(self, mock_post):

        """Scout backend returns the latest version. The scout client returns this to the caller."""

        scout = Scout(app="foshizzolator", version="0.1.0", install_id=install_id)
        resp = scout.report()

        self.assertEqual(resp, {"latest_version": "0.2.0"})

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_plugin(self, mock_post):

        """Scout install-id plugin should set the install_id and requisite metadata."""

        scout = Scout(app="foshizzolator", version="0.1.0", 
                      id_plugin=install_id_plugin, id_plugin_args={ "hello": "world" })

        self.assertEqual(scout.install_id, PLUGIN_UUID)
        self.assertEqual(scout.metadata["new_install"], True)
        self.assertEqual(scout.metadata["swallow_speed"], 42)
        self.assertEqual(scout.metadata["hello"], "world")

if __name__ == '__main__':
    unittest.main()
