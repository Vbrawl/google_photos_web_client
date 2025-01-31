import unittest

from gpwc import Client


class TestClient(unittest.TestCase):
    def setUp(self):
        self.cookies_txt = "cookies.txt"
        self.client = Client(self.cookies_txt)

    def test_client(self):
        """Client test."""
        payload = self.client.get_items_by_taken_date()
        response = self.client.send_api_request([payload])[0]
        print(response)
        self.client.save_cookies_to_file()


if __name__ == "__main__":
    unittest.main()
