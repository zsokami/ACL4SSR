import os

import requests

if __name__ == "__main__":
    error = []

    for i, url in enumerate(os.getenv("URLS_UPDATE_SHA").split("|")):
        try:
            requests.get(url, {"value": os.getenv("GITHUB_SHA")}, timeout=5).raise_for_status()
        except Exception:
            error.append(i)

    if error:
        print("error:", error)
