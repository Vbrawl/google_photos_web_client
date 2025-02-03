import unittest

from gpwc import Client, payloads


class TestClient(unittest.TestCase):
    def setUp(self):
        self.cookies_txt = "cookies.txt"


    def test_SetFavorite(self):
        """Client test."""
        payload = payloads.SetFavorite(["0J7Wh1iXHA4BalGgYaK9sDyxkW4"])
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

    def test_CreateAlbum(self):
        """Client test."""
        payload = payloads.CreateAlbum("__TEST__")
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

    def test_RestoreFromTrash(self):
        """Client test."""
        payload = payloads.RestoreFromTrash(["0J7Wh1iXHA4BalGgYaK9sDyxkW4"])
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

    def test_MoveToTrash(self):
        """Client test."""
        payload = payloads.MoveToTrash(["0J7Wh1iXHA4BalGgYaK9sDyxkW4"])
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

    def test_GetBatchMediaInfo(self):
        """Client test."""
        payload = payloads.GetBatchMediaInfo(["AF1QipN-pG0lbvzcuWrM2V4cMgorke21AVWIL-KPSj4P", "AF1QipMohHAqtyGq4IQsgYrnGvnaQG8e5E4Hzu3YBG6x"])
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

    def test_GetRemoteMatchesByHash(self):
        """Client test."""
        payload = payloads.GetRemoteMatchesByHash(["0J7Wh1iXHA4BalGgYaK9sDyxkW4"])
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

    def test_GetItemInfoExt(self):
        """Client test."""
        payload = payloads.GetItemInfoExt("AF1QipN-pG0lbvzcuWrM2V4cMgorke21AVWIL-KPSj4P")
        client = Client(self.cookies_txt)
        response = client.send_api_request([payload])[0]
        client.save_cookies_to_file()
        print(response)

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
