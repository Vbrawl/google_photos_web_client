# google_photos_web_client

## Example

```python
from gpwc import Client, payloads

cookies_txt = "cookies.txt"
payload = payloads.get_items_by_taken_date()
with Client(cookies_txt) as client:
    response = client.send_api_request([payload])[0]
for item in response.data['items']:
    print(item["thumb"])
```

## Proper way to extract the cookies

1. Install [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/Get%20cookies.txt%20LOCALLY/cclelndahbckbenkjhflpdbgdldlbecc)
2. Allow `Get cookies.txt LOCALLY` to run in private/incognito windows
3. Open a new private browsing/incognito window and log into Google
4. Open a new [Google Photos](https://photos.google.com/) tab, navigate to your libray page
5. Open an new empty tab
6. Close the Google Photos tab
7. Export all cookies from the browser with "Export All Cookies" button in `Get cookies.txt LOCALLY`
8. Close the private browsing/incognito window so the session is never opened in the browser again
