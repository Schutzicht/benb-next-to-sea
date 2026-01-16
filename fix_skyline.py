from PIL import Image, ImageOps
import numpy as np
import os

# Source path
src_path = "/Users/jorikschut/.gemini/antigravity/brain/edce318d-ef0c-4e17-90b4-6466e53cb62d/uploaded_image_1768581458143.png"
out_path = "/Users/jorikschut/Documents/Projecten-sites/benb-next-to-sea/public/images/vlissingen-skyline-panorama.png"

try:
    img = Image.open(src_path).convert("RGBA")
    print(f"Original Dimensions: {img.size}")

    # 1. CLEAN & COLORIZE
    # Instead of luma-to-alpha, we trust the alpha of the uploaded PNG (if it's a cutout)
    # OR we treat all non-white/non-transparent pixels as the "shape".
    
    # Create valid mask:
    # If existing alpha is 0, it's transparent.
    # If pixel is white/light, it should be transparent (in case it's not a clear cutout)
    
    data = np.array(img)
    r, g, b, a = data.T
    
    # Define "Content" as pixels that are NOT transparent AND NOT white
    # (assuming the user might have uploaded a blue-on-white or blue-on-transparent)
    # We want to force the content to be EXACTLY the footer blue: #0e4c92
    
    # Target color
    target_blue = [14, 76, 146] # matches bg-sea-blue
    
    # Create new RGBA array
    new_data = np.zeros_like(data)
    
    # Identify content pixels: 
    # Alpha > 20 AND it's not pure white (allow some anti-aliased edges by keeping alpha?)
    # PREVIOUS ISSUE: "Color doesn't match" -> likely because semi-transparent pixels were blending with white background.
    # FIX: Force high opacity for the main body, but keep edges soft? 
    # OR better: The user wants it "strak" (tight/clean). 
    
    # Let's take the Alpha channel directly.
    # And make the RGB channels consistent sea-blue.
    
    # If the image comes with its own colors, ignore them. overwrite with sea-blue.
    new_data[..., 0] = target_blue[0]
    new_data[..., 1] = target_blue[1]
    new_data[..., 2] = target_blue[2]
    new_data[..., 3] = data[..., 3] # Keep original alpha structure from the cutout
    
    img = Image.fromarray(new_data)

    # 2. Trim whitespace
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        print(f"Cropped to content: {bbox} -> {img.size}")
    
    # 3. Upscale (High Quality)
    w, h = img.size
    target_scale = 3.0 # Good balance
    new_w = int(w * target_scale)
    new_h = int(h * target_scale)
    
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    print(f"Upscaled tile size: {img.size}")

    # 4. Create Panorama (Simple Repetition)
    # Mirroring caused "things falling behind each other". 
    # Users image is likely not perfectly seamless, but simple repetition is often cleaner than mirroring for skylines.
    # Let's try simple A-A-A repetition.
    
    img_arr = np.array(img)
    combined_arr = np.hstack([img_arr, img_arr, img_arr])
    
    # 5. Save
    final_img = Image.fromarray(combined_arr)
    final_img.save(out_path)
    print(f"Saved solid-color panoramic skyline to {out_path}")

except Exception as e:
    print(f"Error: {e}")
