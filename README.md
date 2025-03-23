# google_photos_web_client

## Example

```python
from gpwc import Client, payloads
cookies_txt = "cookies.txt"
lib_page_taken = payloads.GetLibraryPageByTakenDate()
storage_quota = payloads.GetStorageQuota()

# single payload
client = Client(cookies_txt)
response = lib_page_taken.execute(client)
for item in response.data.items:
    print(item.media_key)

# or multiple payloads at once
with Client(cookies_txt) as client:
    response = client.send_api_request([lib_page_taken, storage_quota])
for item in response:
    print(item)
```

## Proper way to extract the cookies

1. Install [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/Get%20cookies.txt%20LOCALLY/cclelndahbckbenkjhflpdbgdldlbecc)
2. Allow `Get cookies.txt LOCALLY` to run in private/incognito windows
3. Open a new private browsing/incognito window and log into Google
4. Open a new [Google Photos](https://photos.google.com/) tab, navigate to your libray page
5. Open a new empty tab
6. Close the Google Photos tab
7. Export all cookies from the browser with "Export All Cookies" button in `Get cookies.txt LOCALLY`
8. Close the private browsing/incognito window so the session is never opened in the browser again
