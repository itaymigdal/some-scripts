import re
import os
import requests
import validators
from sys import argv


def _test_nimbo_new_agent(suspected_nimbo_c2):
    nimbo_headers = {
        'User-Agent': '12345678'
    }
    res = requests.get(suspected_nimbo_c2, headers=nimbo_headers)
    if res.status_code == 200 and len(res.text) == 32:
        return True
    else:
        return False


def _test_nimbo_intruder(suspected_nimbo_c2):
    try:
        requests.get(suspected_nimbo_c2)
    except requests.exceptions.ConnectionError as e:
        if "RemoteDisconnected" in str(e):
            return True
    return False


def test_nimbo_c2(suspected_nimbo_c2):
    try:
        if _test_nimbo_new_agent(suspected_nimbo_c2) and _test_nimbo_intruder(suspected_nimbo_c2):
            return True
        else:
            return False
    except Exception:
        return False


def main():
    if len(argv) != 2 or not validators.url(argv[1]):
        print(f"Usage: {os.path.basename(__file__)} <url>")
        return
    print(test_nimbo_c2(argv[1]))


if __name__ == '__main__':
    main()
