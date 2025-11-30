#!/usr/bin/env python3
"""
Quick logo updater for extension
Usage: python update_logo.py <your_logo_image.png>
"""

from PIL import Image
import sys
import os

def update_logo(image_path):
    """Process logo and create extension icons"""
    try:
        print(f"🖼️  Processing: {image_path}")
        
        # Open and convert to RGB
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Crop to square (center crop)
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        cropped = img.crop((left, top, left + size, top + size))
        
        # Create icons directory
        os.makedirs('icons', exist_ok=True)
        
        # Generate icons
        sizes = [16, 48, 128]
        for size in sizes:
            resized = cropped.resize((size, size), Image.Resampling.LANCZOS)
            output = f'icons/icon{size}.png'
            resized.save(output, 'PNG', optimize=True)
            print(f"✅ Created: {output}")
        
        print("\n🎉 Logo updated successfully!")
        print("📌 Next steps:")
        print("   1. Reload your extension in Chrome (chrome://extensions/)")
        print("   2. The new logo should appear!")
        
    except FileNotFoundError:
        print(f"❌ Error: File not found: {image_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python update_logo.py <image_file>")
        print("\nExample:")
        print("  python update_logo.py my_logo.png")
        sys.exit(1)
    
    try:
        update_logo(sys.argv[1])
    except ImportError:
        print("❌ Error: Pillow not installed")
        print("   Install with: pip install Pillow")

