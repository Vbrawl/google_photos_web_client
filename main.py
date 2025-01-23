import re
import http.cookiejar
import requests


def load_cookies_from_file(filename):
    cookie_jar = http.cookiejar.MozillaCookieJar(filename)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    return cookie_jar


def save_cookies_to_file(session, filename):
    cookie_jar = http.cookiejar.MozillaCookieJar(filename)
    requests.utils.cookiejar_from_dict({c.name: c.value for c in session.cookies}, cookie_jar)
    cookie_jar.save(ignore_discard=True, ignore_expires=True)


def main():
    # Load Netscape format cookies from file
    cookie_file_path = "cookie.txt"
    cookies = load_cookies_from_file(cookie_file_path)

    headers = {
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    }

    # Create a session and set the cookies
    session = requests.Session()
    session.cookies.update(cookies)

    # Send a request
    response = session.get(
        "https://photos.google.com/",
        cookies=cookies,
        headers=headers,
    )

    doc = response.text

    # with open("response.html", "w", encoding="UTF-8") as f:
    #     f.write(doc)

    match = re.search(r"\"SNlM0e\"\:\"(.*?)\"", doc)

    SNlM0e = match.group(1)

    SNlM0e = SNlM0e.replace(":", "%3A")

    data = f"f.req=%5B%5B%5B%22lcxiM%22%2C%22%5Bnull%2Cnull%2C500%2Cnull%2C1%2C3%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={SNlM0e}"

    params = {
        "rpcids": "lcxiM",
        "source-path": "/photo/",
        "pageId": "none",
        "rt": "c",
    }

    response = session.post(
        "https://photos.google.com/_/PhotosUi/data/batchexecute",
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )

    print(response.text)

    # Save updated cookies back to file
    save_cookies_to_file(session, cookie_file_path)


if __name__ == "__main__":
    main()
