import os
import urllib.request
import ssl

# Create unverified context to avoid SSL errors on some systems
ssl_context = ssl._create_unverified_context()

fonts = {
    "Roboto.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf",
    "GreatVibes.ttf": "https://github.com/google/fonts/raw/main/ofl/greatvibes/GreatVibes-Regular.ttf",
    "PlayfairDisplay.ttf": "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Regular.ttf",
    "Inter.ttf": "https://github.com/google/fonts/raw/main/ofl/inter/Inter-Regular.ttf"
}

target_dir = r"v:\Inventobots\backend\certifications\fonts"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

for name, url in fonts.items():
    print(f"Downloading {name}...")
    try:
        with urllib.request.urlopen(url, context=ssl_context) as response, open(os.path.join(target_dir, name), 'wb') as out_file:
            out_file.write(response.read())
        print(f"✅ {name} saved.")
    except Exception as e:
        print(f"❌ Failed to download {name}: {e}")
