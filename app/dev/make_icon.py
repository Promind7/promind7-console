from PIL import Image
import os

source_path = r"C:/Users/zaq/.gemini/antigravity/brain/bcd6cffa-be3d-49b0-b26d-20379a2b131b/uploaded_image_1769368364138.png"
dest_path = r"d:\Promind7\IA\V2\promind7_logo.ico"

try:
    img = Image.open(source_path).convert("RGBA")
    
    # Create white background
    background = Image.new("RGBA", img.size, (255, 255, 255, 255))
    combined = Image.alpha_composite(background, img)
    
    # Convert to RGB and save as ICO
    combined = combined.convert("RGB")
    combined.save(dest_path, format="ICO", sizes=[(256, 256)])
    print("Icon created successfully.")
except Exception as e:
    print(f"Error: {e}")
