import os
from pathlib import Path

def setup_assets():
    # Create assets directory
    asset_dir = Path("C:/Soft AI Pro/assets")
    asset_dir.mkdir(parents=True, exist_ok=True)
    
    # List required assets
    required_assets = [
        "SoftAI_Logo.png",
        "background.jpg",
        "new_project.png",
        "archive.png",
        "docs.png", 
        "cloud.png",
        "settings.png"
    ]
    
    # Check missing assets
    missing = []
    for asset in required_assets:
        if not (asset_dir / asset).exists():
            missing.append(asset)
    
    if missing:
        print("Missing assets:")
        for asset in missing:
            print(f"- {asset}")
        print(f"\nPlease place these files in: {asset_dir}")
    
    # Setup fonts directory
    fonts_dir = Path("C:/Soft AI Pro/fonts")
    fonts_dir.mkdir(exist_ok=True)
    
    required_fonts = [
        "Montserrat-Bold.ttf",
        "Poppins-Medium.ttf",
        "Quicksand-Bold.ttf",
        "OpenSans-Regular.ttf",
        "Raleway-Light.ttf"
    ]
    
    # Check missing fonts
    missing_fonts = []
    for font in required_fonts:
        if not (fonts_dir / font).exists():
            missing_fonts.append(font)
    
    if missing_fonts:
        print("\nMissing fonts:")
        for font in missing_fonts:
            print(f"- {font}")
        print(f"\nPlease place font files in: {fonts_dir}")

if __name__ == "__main__":
    setup_assets()

# 3. Jalankan aplikasi
python "Soft ΔI Code.py"