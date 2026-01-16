
import requests
import os

images = {
    "boulevard.jpg": "https://upload.wikimedia.org/wikipedia/commons/e/ec/Boulevard_Vlissingen.jpg",
    "badstrand.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Vlissingen_Badstrand.jpg/1200px-Vlissingen_Badstrand.jpg",
    "bellamypark.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Bellamypark_Vlissingen.jpg/1200px-Bellamypark_Vlissingen.jpg"
}

output_dir = "public/images"
os.makedirs(output_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for filename, url in images.items():
    try:
        print(f"Downloading {filename}...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Saved to {filepath}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
