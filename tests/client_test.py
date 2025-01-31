import unittest

from gpwc import Client, payloads


class TestClient(unittest.TestCase):
    def setUp(self):
        self.cookies_txt = "cookies.txt"

    def test_client(self):
        """Client test."""
        payload = payloads.get_items_by_taken_date()
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

    def test_client_context(self):
        """Client context test."""
        payload = payloads.get_items_by_taken_date()
        with Client(self.cookies_txt) as client:
            response = client.send_api_request([payload])[0]
        print(response)


if __name__ == "__main__":
    unittest.main()
