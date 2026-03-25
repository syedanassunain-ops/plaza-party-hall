import urllib.request
import re

urls = [
    "https://maps.app.goo.gl/Gb6Vd1PfoHceBWCA6",
    "https://maps.app.goo.gl/9vaYQLtGdBdCeStw8",
    "https://maps.app.goo.gl/9yK2zktgQpjoA7oW8",
    "https://maps.app.goo.gl/3xSpVmzghYaxFeWU6",
    "https://maps.app.goo.gl/gy6dETssHytWMmKB8",
    "https://maps.app.goo.gl/tGcv3UpD73ddFLuPA",
    "https://maps.app.goo.gl/4EJ6T7ioDTbUjfZLA"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

import sys

for i, url in enumerate(urls, 1):
    req = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(req, context=ctx)
        html = response.read().decode('utf-8', errors='ignore')
        
        # Google Maps links often redirect. The final HTML should have meta tags.
        match = re.search(r'<meta content="([^"]+)" property="og:image"', html)
        if not match:
            match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
            
        if match:
            img_url = match.group(1).replace('&amp;', '&')
            if "googleusercontent.com" in img_url:
                # To get max resolution, replace the sizing params at the end with =s0
                img_url = re.sub(r'=w\d+-h\d+-[a-zA-Z0-9\-]+', '=s0', img_url)
                
            print(f"[{i}] Found image URL: {img_url}")
            
            img_req = urllib.request.Request(img_url, headers=headers)
            with open(f"c:\\Users\\Syed Anas\\OneDrive\\Desktop\\PLAZA PARTY HALL\\images\\img{i}.jpg", 'wb') as f:
                f.write(urllib.request.urlopen(img_req, context=ctx).read())
            print(f"[{i}] Downloaded img{i}.jpg successfully.")
        else:
            print(f"[{i}] No og:image found for {url}")
    except Exception as e:
        print(f"[{i}] Error for {url}: {e}")
