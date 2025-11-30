#!/usr/bin/env python3
"""
Generate beautiful QR code extension logos
Requires: pip install Pillow
"""

from PIL import Image, ImageDraw
import os

def generate_logo(size):
    # Create image with gradient background
    img = Image.new('RGB', (size, size), color='#0a58ca')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient effect (simplified)
    for i in range(size):
        ratio = i / size
        r = int(10 + (102 - 10) * (1 - ratio))
        g = int(88 + (16 - 88) * (1 - ratio))
        b = int(202 + (242 - 202) * (1 - ratio))
        draw.rectangle([(0, i), (size, i+1)], fill=(r, g, b))
    
    # Calculate QR code pattern dimensions
    padding = int(size * 0.12)
    qr_size = size - (padding * 2)
    modules = 7
    module_size = qr_size // modules
    
    # Draw position markers (corner squares)
    def draw_position_marker(x, y):
        marker_size = int(module_size * 2.5)
        # Outer white square
        draw.rectangle([x, y, x + marker_size, y + marker_size], fill='white')
        # Inner colored square
        inner_pad = int(module_size * 0.5)
        inner_size = int(module_size * 1.5)
        draw.rectangle([x + inner_pad, y + inner_pad, 
                       x + inner_pad + inner_size, y + inner_pad + inner_size], 
                      fill='#0a58ca')
        # Center white dot
        center_pad = module_size
        center_size = int(module_size * 0.5)
        draw.rectangle([x + center_pad, y + center_pad,
                       x + center_pad + center_size, y + center_pad + center_size],
                      fill='white')
    
    # Draw three position markers
    draw_position_marker(padding, padding)  # Top-left
    draw_position_marker(padding + qr_size - int(module_size * 2.5), padding)  # Top-right
    draw_position_marker(padding, padding + qr_size - int(module_size * 2.5))  # Bottom-left
    
    # Draw data modules
    data_pattern = [
        (3, 0), (4, 0), (5, 0),
        (0, 3), (0, 4), (0, 5),
        (6, 3), (6, 4), (6, 5),
        (3, 6), (4, 6), (5, 6),
        (2, 2), (4, 2), (2, 4), (4, 4)
    ]
    
    for x, y in data_pattern:
        x_pos = padding + x * module_size + int(module_size * 0.1)
        y_pos = padding + y * module_size + int(module_size * 0.1)
        module_draw_size = int(module_size * 0.8)
        draw.rectangle([x_pos, y_pos, x_pos + module_draw_size, y_pos + module_draw_size], 
                      fill='white')
    
    # Add rounded corners mask
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    radius = int(size * 0.2)
    mask_draw.rounded_rectangle([(0, 0), (size, size)], radius=radius, fill=255)
    
    # Apply mask
    output = Image.new('RGB', (size, size), (0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    # Convert back to RGB for PNG
    final_img = Image.new('RGB', (size, size), (255, 255, 255))
    final_img.paste(output, mask=output.split()[3] if output.mode == 'RGBA' else None)
    
    return final_img

def main():
    sizes = [16, 48, 128]
    icons_dir = 'icons'
    
    # Create icons directory if it doesn't exist
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
    
    print("🎨 Generating beautiful QR code extension logos...")
    
    for size in sizes:
        print(f"  Generating icon{size}.png...")
        logo = generate_logo(size)
        logo.save(f'{icons_dir}/icon{size}.png', 'PNG')
    
    print("✅ All logos generated successfully!")
    print(f"📁 Logos saved in {icons_dir}/ directory")

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("❌ Error: Pillow library not found.")
        print("   Please install it with: pip install Pillow")
    except Exception as e:
        print(f"❌ Error: {e}")

