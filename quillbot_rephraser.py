#!/usr/bin/env python3

import requests

from json import loads
from urllib.parse import quote

API_URL = "https://quillbot.com/api/singleParaphrase"
PARAMS = "?userID=N/A&text={}&strength={}&autoflip={}&wikify={}&fthresh={}"


def setup_session():
    """Update headers for the session.

    Returns
    -------
    obj
        Requests Session
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
            "content-type": "application/text",
        }
    )
    return session


def get_parameterized_url(text):
    """Gets parametrized url

    Parameters
    ----------
    text : str

    Returns
    -------
    url: str
        string containing url and quoted text
    """
    url_encoded_text = quote(text)
    autoflip = "true"
    fthresh = "true"
    strength = "2"
    wikify = "9"
    url = API_URL + PARAMS.format(url_encoded_text, strength, autoflip, wikify, fthresh)
    return url


def paraphrasor(url, session):
    """Gets paraphrased text

    Parameters
    ----------
    url : str
        Complete url containing text
    session : class `requests.sessions.Session`
            Requests session.
            Provides cookie persistence, connection-pooling, and configuration.

    Raises
    ------
    RuntimeError
        If return status-code is not successful
    """
    # Cookies are configurable
    cookies = {
        "__cfduid": "d15a685b3f1c19949ad29b09ead2590fa1566130401",
        "__stripe_mid": "547b38b0-4c5c-4d94-89aa-928ad35b93d8",
        "__stripe_sid": "82964a7c-d775-468a-99be-5f097c1570c8",
        "_pk_id.2.48cd": "da4e8c5c080bfe6b.1566130403.1.1566130403.1566130403.",
        "_pk_ses.2.48cd": "*",
        "sessID": "fec1e0c7b541d98d",
        "connect.sid": "s%3AoJCREvXNaX3V1EgJREtU9UbHSlxdBtQB.Zrj0yid9sCeGWgKuO1hjdQraPlZlpkKyNvcj4DIcc9o",
        "userIDToken": "N/A",
        "prioritize": "2",
    }
    req = session.get(url, cookies=cookies)
    if req.status_code == 200:
        json_text = loads(req.text)
        end = "\n\n"
        try:
            json_text = json_text[0] if len(json_text) == 1 else json_text
            print(f"\nData Sent: {json_text['sent']}", end)
            paras = [key for key in json_text if key.startswith("paras")]
            texts = list(
                set([text.get("alt") for para in paras for text in json_text[para]])
            )
            print("Alternative Texts:")
            print("-" * 80)
            for text in texts:
                print(text, end)
        except Exception:
            raise
    else:
        raise RuntimeError("Failed to get paraphrase...")


def main():
    """Main

    Raises
    ------
    RuntimeError
        If received texts if more than 700 characters
    """
    session = setup_session()
    print("Quillbot Paraphrasing tool.")
    while True:
        try:
            text = input("Enter text: ")
            if not (700 >= len(text) > 1):
                raise RuntimeError("Text should be less than 700 characters")
            url = get_parameterized_url(text)
            paraphrasor(url, session)
            print("#" * 80)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
