import unittest

from gpwc import Client, payloads


class TestClient(unittest.TestCase):
    def setUp(self):
        self.cookies_txt = "cookies.txt"

    def test_GetItemInfo(self):
        """Client test."""
        payload = payloads.GetItemInfo("AF1QipN-pG0lbvzcuWrM2V4cMgorke21AVWIL-KPSj4P")
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

    def test_client(self):
        """Client test."""
        payload = payloads.GetItemsByTakenDate()
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

    def test_client_context(self):
        """Client context test."""
        taken = payloads.GetItemsByTakenDate()
        uploaded = payloads.GetItemsByUploadedDate()
        with Client(self.cookies_txt) as client:
            response = client.send_api_request([taken, uploaded])
        for r in response:
            print(r.data)
        print(response)


if __name__ == "__main__":
    unittest.main()
