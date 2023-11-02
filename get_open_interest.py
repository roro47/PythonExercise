#!/usr/bin/env python
import re

import requests
from bs4 import BeautifulSoup

contracts_url = "https://www.cftc.gov/dea/futures/deanymesf.htm"


def get_open_interest():
    response = requests.get(contracts_url)
    if not response.ok:
        return

    soup = BeautifulSoup(response.content, "html5lib")
    content = soup.find("pre").text

    names = re.findall(r"(.+) - .*Code-.*?\n", content)
    raw_open_interests = re.findall(r"OPEN INTEREST: +([0-9,]+)\n", content)
    open_interests = map(lambda x: int(x.replace(",", "")), raw_open_interests)

    print("contract,open_interest")
    for name, open_interest in zip(names, open_interests):
        print(f"{name},{open_interest}")


if __name__ == "__main__":
    get_open_interest()
