import copy  # Allows you to create deep copies of composite objects
import sys
from urllib import parse  # URL manipulation
import requests  # For HTTP requests


def request(url):
    headers = {
        "User-Agent": "",
        "Cookie": ""
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def is_vulnerable(html):
    try:
        with open('errors.txt', 'r') as file:
            errors = file.readlines()
    except FileNotFoundError:
        print("Error: 'errors.txt' not found.")
        sys.exit(1)

    for error in errors:
        if error.strip() in html:
            return True
    return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    url_parsed = parse.urlsplit(url)

    # Converts the query parameters (after the ? in the URL) to a dictionary where each key is a parameter name
    params = parse.parse_qs(url_parsed.query)

    for param in params.keys():
        query = copy.deepcopy(params)

        # Try to inject the characters ' and " into each URL parameter to check for vulnerability
        # and rebuild the URL with the modified parameter
        for c in ["'", "\""]:
            query[param] = [c]
            new_params = parse.urlencode(query, doseq=True)
            url_final = url_parsed._replace(query=new_params).geturl()

            html = request(url_final)
            if html and is_vulnerable(html):
                print(f"[ + ] {param} parameter is vulnerable")
                sys.exit(0)

    print("NOT VULNERABLE")
