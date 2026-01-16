from PIL import Image, ImageOps
import numpy as np
import os

# Source path
src_path = "/Users/jorikschut/.gemini/antigravity/brain/edce318d-ef0c-4e17-90b4-6466e53cb62d/vlissingen_skyline_vector_check_1768512068772.png"
out_path = "/Users/jorikschut/Documents/Projecten-sites/benb-next-to-sea/public/images/vlissingen-skyline-final.png"

try:
    img = Image.open(src_path).convert("RGBA")
    print(f"Original Dimensions: {img.size} (Width x Height)")

    # 0. Make White Transparent (Crucial for proper cropping)
    # Get alpha (or create it)
    datas = img.getdata()
    newData = []
    for item in datas:
        # If pixels are white (R>240, G>240, B>240), make transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    
    # 1. Force Rotation if Vertical (unlikely if square, but keep check)
    if img.height > img.width:
        print("Image is taller than wide. Rotating -90 degrees...")
        img = img.rotate(-90, expand=True)
    
    # 2. Trim whitespace (Crop to content)
    # Now that white is transparent, getbbox works on alpha
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        print(f"Cropped to content: {bbox} -> {img.size}")
    else:
        print("Warning: Image seems empty after removing white.")

    # 3. Create Panoramic Canvas (5x Width for 4K Coverage)
    # Pattern: [Mirrored] [Original] [Mirrored] [Original] [Mirrored]
    
    w, h = img.size
    TARGET_HEIGHT = h 
    TARGET_WIDTH = w * 5
    
    # UPSCALING (1.8x) to ensure 3 tiles cover 4k width
    new_w = int(w * 1.8)
    new_h = int(h * 1.8)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    w, h = img.size # Update w, h

    print(f"Upscaled tile size: {w}x{h}")

    # 4. Create Panorama (Symmetric: Flip - Original - Flip)
    # This creates a 3-tile wide panorama (~5000px) which is much less repetitive than 5x
    img_flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Convert to numpy for easy concatenation
    img_arr = np.array(img)
    img_flipped_arr = np.array(img_flipped)
    
    # Pattern: Mirror | Original | Mirror
    combined_arr = np.hstack([img_flipped_arr, img_arr, img_flipped_arr])
    
    combined_skyline = Image.fromarray(combined_arr)

    # 5. Colorize to Sea Blue #0e4c92
    data = np.array(combined_skyline)
    
    # Vectorized mask operation
    alpha_channel = data[:, :, 3]
    mask = alpha_channel > 10
    
    target_color = [14, 76, 146]
    
    # Assign RGB colors where mask is True
    data[mask, 0] = target_color[0]
    data[mask, 1] = target_color[1]
    data[mask, 2] = target_color[2]
    
    # 6. Save as PNG
    out_path = "/Users/jorikschut/Documents/Projecten-sites/benb-next-to-sea/public/images/vlissingen-skyline-panorama.png"
    final_img = Image.fromarray(data)
    final_img.save(out_path)
    print(f"Saved panoramic skyline to {out_path}")

except Exception as e:
    print(f"Error: {e}")
