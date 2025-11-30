#!/usr/bin/env python3
"""
Process and crop logo image for extension icons
Requires: pip install Pillow
Usage: python process_logo.py <image_path>
"""

from PIL import Image
import sys
import os

def process_logo(image_path, crop_percent=100, x_offset=0, y_offset=0):
    """
    Process logo image and create extension icons
    
    Args:
        image_path: Path to source image
        crop_percent: Crop size percentage (50-150)
        x_offset: X offset percentage (-50 to 50)
        y_offset: Y offset percentage (-50 to 50)
    """
    try:
        # Open source image
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate crop dimensions
        width, height = img.size
        crop_size = min(width, height) * (crop_percent / 100)
        
        # Calculate crop box (centered with offsets)
        left = (width - crop_size) / 2 + (x_offset * width / 100)
        top = (height - crop_size) / 2 + (y_offset * height / 100)
        right = left + crop_size
        bottom = top + crop_size
        
        # Ensure crop box is within image bounds
        left = max(0, min(left, width))
        top = max(0, min(top, height))
        right = max(crop_size, min(right, width))
        bottom = max(crop_size, min(bottom, height))
        
        # Crop to square
        cropped = img.crop((int(left), int(top), int(right), int(bottom)))
        
        # Create icons directory if it doesn't exist
        icons_dir = 'icons'
        if not os.path.exists(icons_dir):
            os.makedirs(icons_dir)
        
        # Generate all sizes
        sizes = [16, 48, 128]
        print(f"🎨 Processing logo: {image_path}")
        print(f"   Original size: {width}x{height}")
        print(f"   Crop size: {crop_percent}%")
        
        for size in sizes:
            # Resize with high-quality resampling
            resized = cropped.resize((size, size), Image.Resampling.LANCZOS)
            
            # Save
            output_path = f'{icons_dir}/icon{size}.png'
            resized.save(output_path, 'PNG', optimize=True)
            print(f"   ✅ Generated {output_path} ({size}x{size})")
        
        print(f"\n✅ All logos generated successfully in {icons_dir}/ directory!")
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: Image file not found: {image_path}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_logo.py <image_path> [crop_percent] [x_offset] [y_offset]")
        print("\nExample:")
        print("  python process_logo.py logo.png")
        print("  python process_logo.py logo.png 90 0 0  # Crop to 90%, no offset")
        print("  python process_logo.py logo.png 100 -10 5  # Full size, shift left 10%, down 5%")
        sys.exit(1)
    
    image_path = sys.argv[1]
    crop_percent = float(sys.argv[2]) if len(sys.argv) > 2 else 100
    x_offset = float(sys.argv[3]) if len(sys.argv) > 3 else 0
    y_offset = float(sys.argv[4]) if len(sys.argv) > 4 else 0
    
    process_logo(image_path, crop_percent, x_offset, y_offset)

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("❌ Error: Pillow library not found.")
        print("   Please install it with: pip install Pillow")
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")

