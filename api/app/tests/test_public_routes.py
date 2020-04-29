import json
import os
import unittest

from app import factory
from app.env import SERVER_CONFIG, parse_env_variables
from app.tests.globals import build_basic_auth_header, ROUTEST


class PublicRoutesTestCase(unittest.TestCase):
    """Tests for all public routes"""

    def setUp(self):
        self.app = factory.create_app()
        self.client = self.app.test_client()
        parse_env_variables()
        self.env_config = SERVER_CONFIG

    # Test route /api/status
    def test_status_route_with_valid_http_method(self):
        """Test the public route used for service status validation"""
        resp = self.client.get("/api/status")
        self.assertEqual(resp.status_code, 200)

    def test_status_route_with_invalid_http_method(self):
        """Test the public route but with wrong HTTP method"""
        resp = self.client.put("/api/status")
        self.assertEqual(resp.status_code, 405)

    # Test route /api/login
    def test_login_without_basic_auth(self):
        """The login route requires Basic Authentication with username and password to generate and return valid token."""
        resp = self.client.post("/api/login")
        self.assertEqual(resp.status_code, 400)

    def test_login_with_unsuported_method(self):
        """The login route works only with HTTP POST"""
        resp = self.client.get(ROUTEST["login"])
        self.assertEqual(resp.status_code, 405)

    def test_login_with_wrong_username_and_password(self):
        """Login route works only with the predefined values in global ENV: API_AUTH_USERNAME, API_AUTH_PASSWORD"""
        resp = self.client.post(
            ROUTEST["login"],
            headers=build_basic_auth_header(
                username="nonExistingUsername123!123.asd",
                password="nonExistingUsername123!123.asd"
            )
        )
        self.assertEqual(resp.status_code, 403)

    def test_login_get_token_success(self):
        """Use correct Basic Auth for login and get token"""
        resp = self.client.post(
            ROUTEST["login"],
            headers=build_basic_auth_header(
                username=self.env_config["API_AUTH_USERNAME"],
                password=self.env_config["API_AUTH_PASSWORD"]
            )
        )

        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
