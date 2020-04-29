import json
import os
import unittest

from app import factory
from app.env import SERVER_CONFIG, parse_env_variables
from app.tests.globals import HTTP_REQUIRED_HEADERS, TEST_INPUT, ROUTEST, build_basic_auth_header


class ContactTestCase(unittest.TestCase):
    """Implementation of all tests for Contact"""

    def setUp(self):
        self.app = factory.create_app()
        self.client = self.app.test_client()
        parse_env_variables()
        self.env_confg = SERVER_CONFIG
        self.token = self._get_valid_login_token()
        self.required_valid_headers = {
            "x-auth-token": self.token
        }

    # TODO(David): Move this in the global file when move then one package requires it's usage.
    def _get_valid_login_token(self):
        """Returns valid JWT token that can be used in all further requests"""
        resp = self.client.post(
            ROUTEST["login"],
            headers=build_basic_auth_header(
                username=self.env_confg["API_AUTH_USERNAME"],
                password=self.env_confg["API_AUTH_PASSWORD"]
            )
        )
        json_data = json.loads(resp.data)

        return json_data["token"]

    # Contact GET tests
    def test_get_contact_without_token(self):
        resp = self.client.get(
            ROUTEST["contact"]
        )

        self.assertEqual(resp.status_code, 403)

    def test_get_contacts_with_valid_token(self):
        resp = self.client.get(
            ROUTEST["contact"],
            headers=self.required_valid_headers
        )
        self.assertEqual(resp.status_code, 200)

    def test_get_contact_non_existing(self):
        resp = self.client.get(
            "{}?username={}".format(
                ROUTEST["contact"],
                "nonExistingUsername"
            ),
            headers=self.required_valid_headers
        )
        self.assertEqual(resp.status_code, 404)

    # Contact POST tests
    def test_post_contact_without_token(self):
        resp = self.client.post(
            ROUTEST["contact"]
        )
        self.assertEqual(resp.status_code, 403)

    def test_post_contact_missing_http_body(self):
        resp = self.client.post(
            ROUTEST["contact"],
            headers=self.required_valid_headers
        )
        self.assertEqual(resp.status_code, 400)

    # Contact PUT tests
    def test_put_contact_without_token(self):
        resp = self.client.put(
            ROUTEST["contact"]
        )
        self.assertEqual(resp.status_code, 403)

    def test_put_contact_missing_http_body(self):
        resp = self.client.put(
            ROUTEST["contact"],
            headers=self.required_valid_headers
        )
        self.assertEqual(resp.status_code, 400)

    # Contact DELETE tests
    def test_delete_contact_without_token(self):
        resp = self.client.delete(
            ROUTEST["contact"]
        )
        self.assertEqual(resp.status_code, 403)

    def test_delete_contact_invalid_request(self):
        resp = self.client.delete(
            ROUTEST["contact"],
            headers=self.required_valid_headers
        )
        self.assertEqual(resp.status_code, 400)


if __name__ == "__main__":
    unittest.main()
