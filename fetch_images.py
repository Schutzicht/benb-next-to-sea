import urllib.request
import urllib.error
import re
import os
import ssl
import time

# Bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Updated list with better URLs and fallbacks
sites = [
    # Culinary
    ("gevangentoren", "https://restaurantdegevangentoren.nl/"),
    ("brasserie_blvd", "https://www.brasserieblvd.nl/"), 
    ("gecroonde_liefde", "https://www.degecroondeliefde.nl/"),
    ("timmerfabriek", "https://gastrobardetimmerfabriek.nl/"),
    # La Bella Cucina - ALREADY HAVE
    
    # Culture
    ("muzeeum", "https://www.muzeeum.nl/"),
    ("iguana", "https://www.iguana.nl/"),
    ("michiel_de_ruyter", "https://nl.wikipedia.org/wiki/Standbeeld_van_Michiel_de_Ruyter_(Vlissingen)"),
    ("oranjemolen", "https://nl.wikipedia.org/wiki/Oranjemolen_(Vlissingen)"), # Wikipedia is more reliable for scraping
    # Sint Jacobskerk - ALREADY HAVE
    
    # Active
    # Windorgel - ALREADY HAVE
    # Zonnetrein - ALREADY HAVE
    ("nollestrand", "https://vlissingen.com/nl/strand/nollestrand.php"), # New source
    ("cinecity", "https://www.biosagenda.nl/bioscoop/pathe-vlissingen_36.html"), # Pathé often blocks, biosagenda is easier
    ("duinen", "https://nl.wikipedia.org/wiki/Duinen"), # Generic dunes if specific fail
]

output_dir = "public/images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def get_og_image(url):
    print(f"  Fetching metadata from {url}...")
    try:
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # 1. Try og:image
            match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
            if match: return match.group(1)
            
            # 2. Try twitter:image
            match = re.search(r'<meta\s+name=["\']twitter:image["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
            if match: return match.group(1)
            
            # 3. specific fallback for common site structures or just find the first decent jpg/png
            # This is a bit risky but better than nothing for a demo
            # Look for large images
            images = re.findall(r'<img\s+[^>]*src=["\'](.*?)["\']', html, re.IGNORECASE)
            for img in images:
                if 'logo' not in img.lower() and 'icon' not in img.lower() and (img.endswith('.jpg') or img.endswith('.png')):
                    if img.startswith('http'):
                        return img
                    elif img.startswith('/'):
                        # rudimentary relative path handling
                        base_url_match = re.search(r'(https?://[^/]+)', url)
                        if base_url_match:
                            return base_url_match.group(1) + img
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
    return None

def download_image(img_url, filename_base):
    if not img_url: return None
    
    try:
        # Fix protocol relative URLs
        if img_url.startswith("//"):
            img_url = "https:" + img_url
            
        ext = "jpg"
        if ".png" in img_url.lower(): ext = "png"
        elif ".webp" in img_url.lower(): ext = "webp"
        
        filename = f"{filename_base}.{ext}"
        filepath = os.path.join(output_dir, filename)
        
        # Don't re-download if exists and > 0 bytes
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print(f"  File {filename} already exists. Skipping.")
            return filename
            
        print(f"  Downloading {img_url} to {filename}...")
        
        req = urllib.request.Request(
            img_url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return filename
    except Exception as e:
        print(f"  Failed download {img_url}: {e}")
        return None

results = {}

for name, url in sites:
    print(f"Processing {name}...")
    img_url = get_og_image(url)
    if img_url:
        print(f"  Found image: {img_url}")
        saved = download_image(img_url, name)
        if saved:
            results[name] = f"/images/{saved}"
    else:
        print(f"  No image found for {name}")
    time.sleep(1) # Be nice

print("\n--- RESULTS ---")
for k, v in results.items():
    print(f"{k}: {v}")
