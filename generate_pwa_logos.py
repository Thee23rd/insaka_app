#!/usr/bin/env python3
"""
PWA Logo Generator for Insaka Conference App
This script helps generate different logo sizes for PWA icons
"""

import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def create_pwa_icons():
    """Generate PWA icons from the main logo"""
    
    # Create assets/pwa directory if it doesn't exist
    os.makedirs("assets/pwa", exist_ok=True)
    
    # Define required PWA icon sizes
    sizes = [
        (48, 48),
        (72, 72),
        (96, 96),
        (144, 144),
        (152, 152),
        (167, 167),
        (180, 180),
        (192, 192),
        (512, 512)
    ]
    
    # Try to load the existing logo
    logo_paths = [
        "assets/logos/insaka.jpg",
        "assets/insaka.jpg",
        "assets/logos/Zamii Logo.jpeg"
    ]
    
    logo_image = None
    for path in logo_paths:
        if os.path.exists(path):
            try:
                logo_image = Image.open(path)
                print(f"✅ Loaded logo from: {path}")
                break
            except Exception as e:
                print(f"❌ Failed to load {path}: {e}")
                continue
    
    if logo_image is None:
        print("❌ No logo found. Creating a simple text-based logo...")
        # Create a simple logo with text
        logo_image = create_text_logo()
    
    # Generate icons for each size
    for size in sizes:
        try:
            # Resize the logo
            resized_logo = logo_image.resize(size, Image.Resampling.LANCZOS)
            
            # Create a square canvas with background
            canvas = Image.new('RGB', size, '#198A00')  # Zambian green background
            canvas.paste(resized_logo, (0, 0))
            
            # Save the icon
            icon_path = f"assets/pwa/icon-{size[0]}x{size[1]}.png"
            canvas.save(icon_path, 'PNG', optimize=True)
            print(f"✅ Generated: {icon_path}")
            
        except Exception as e:
            print(f"❌ Failed to generate {size[0]}x{size[1]} icon: {e}")
    
    print("\n🎉 PWA icons generated successfully!")
    print("📁 Icons saved in: assets/pwa/")
    print("\n📋 Next steps:")
    print("1. Update manifest.json to use the new icon paths")
    print("2. Test the PWA installation on mobile devices")
    print("3. Customize the logo if needed")

def create_text_logo():
    """Create a simple text-based logo"""
    # Create a 512x512 image with Zambian colors
    img = Image.new('RGB', (512, 512), '#198A00')
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a system font
        font_large = ImageFont.truetype("arial.ttf", 80)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Add text
    text1 = "INSAKA"
    text2 = "CONFERENCE"
    text3 = "2025"
    
    # Calculate text positions
    bbox1 = draw.textbbox((0, 0), text1, font=font_large)
    bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    bbox3 = draw.textbbox((0, 0), text3, font=font_small)
    
    text1_width = bbox1[2] - bbox1[0]
    text2_width = bbox2[2] - bbox2[0]
    text3_width = bbox3[2] - bbox3[0]
    
    # Center the text
    x1 = (512 - text1_width) // 2
    x2 = (512 - text2_width) // 2
    x3 = (512 - text3_width) // 2
    
    y1 = 150
    y2 = 250
    y3 = 300
    
    # Draw text with white color
    draw.text((x1, y1), text1, fill='white', font=font_large)
    draw.text((x2, y2), text2, fill='white', font=font_small)
    draw.text((x3, y3), text3, fill='white', font=font_small)
    
    # Add a border
    draw.rectangle([10, 10, 502, 502], outline='#2BA300', width=4)
    
    return img

def update_manifest_with_new_icons():
    """Update manifest.json to use the new PWA icons"""
    
    manifest_content = {
        "name": "Insaka Conference 2025",
        "short_name": "Insaka",
        "description": "Zambian Mining and Investment Conference - Delegate Portal",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#198A00",
        "theme_color": "#198A00",
        "orientation": "portrait-primary",
        "scope": "/",
        "lang": "en",
        "categories": ["business", "productivity", "education"],
        "icons": [
            {
                "src": "assets/pwa/icon-48x48.png",
                "sizes": "48x48",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "assets/pwa/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "assets/pwa/icon-96x96.png",
                "sizes": "96x96",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "assets/pwa/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "assets/pwa/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "assets/pwa/icon-167x167.png",
                "sizes": "167x167",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "assets/pwa/icon-180x180.png",
                "sizes": "180x180",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "assets/pwa/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "assets/pwa/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "screenshots": [
            {
                "src": "assets/pwa/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "form_factor": "narrow",
                "label": "Insaka Conference Dashboard"
            }
        ],
        "shortcuts": [
            {
                "name": "Delegate Dashboard",
                "short_name": "Dashboard",
                "description": "Access your conference dashboard",
                "url": "/pages/1_Delegate_Dashboard.py",
                "icons": [
                    {
                        "src": "assets/pwa/icon-96x96.png",
                        "sizes": "96x96"
                    }
                ]
            },
            {
                "name": "Agenda",
                "short_name": "Schedule",
                "description": "View conference schedule",
                "url": "/pages/1_Agenda.py",
                "icons": [
                    {
                        "src": "assets/pwa/icon-96x96.png",
                        "sizes": "96x96"
                    }
                ]
            },
            {
                "name": "Matchmaking",
                "short_name": "Network",
                "description": "Connect with other delegates",
                "url": "/pages/11_Matchmaking.py",
                "icons": [
                    {
                        "src": "assets/pwa/icon-96x96.png",
                        "sizes": "96x96"
                    }
                ]
            }
        ]
    }
    
    # Write the updated manifest
    import json
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest_content, f, indent=2, ensure_ascii=False)
    
    print("✅ Updated manifest.json with new PWA icons")

if __name__ == "__main__":
    print("🚀 Insaka PWA Logo Generator")
    print("=" * 40)
    
    try:
        # Generate PWA icons
        create_pwa_icons()
        
        # Update manifest
        update_manifest_with_new_icons()
        
        print("\n🎉 PWA setup complete!")
        print("\n📱 To test your PWA:")
        print("1. Deploy to Streamlit Cloud or your server")
        print("2. Open in Chrome/Edge on mobile")
        print("3. Look for 'Add to Home Screen' option")
        print("4. Install and test the app")
        
    except ImportError:
        print("❌ PIL (Pillow) is required. Install it with:")
        print("pip install Pillow")
    except Exception as e:
        print(f"❌ Error: {e}")
