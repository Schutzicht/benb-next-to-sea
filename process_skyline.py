from PIL import Image
import numpy as np

# Load the image
img_path = "/Users/jorikschut/.gemini/antigravity/brain/edce318d-ef0c-4e17-90b4-6466e53cb62d/vlissingen_skyline_vector_check_1768512068772.png"
img = Image.open(img_path).convert("RGBA")

# Check orientation and rotate if vertical
if img.height > img.width:
    print("Image is vertical, rotating -90 degrees...")
    img = img.rotate(-90, expand=True)

# Resize to a reasonable height to make processing faster and consistent
target_h = 500
aspect = img.width / img.height
target_w_img = int(target_h * aspect)
img = img.resize((target_w_img, target_h))

data = np.array(img)


# Define the target color: Sea Blue #0e4c92 (R=14, G=76, B=146)
target_color = [14, 76, 146, 255]

# Identify white pixels (background) vs black pixels (skyline)
# Assuming image is grayscale/bw. White is high values, Black is low.
# We want: White -> Transparent
# Black -> Target Color

r, g, b, a = data.T

# Create a mask for "not white" (i.e., the skyline)
# We can use brightness. Darker pixels should be opaque blue. Lighter pixels transparent.
# Let's calculate brightness
brightness = (r.astype(int) + g.astype(int) + b.astype(int)) / 3

# Threshold for background (white)
threshold = 200

# Create new image array
new_data = np.zeros_like(data)

# Set Color to Sea Blue everywhere
new_data[:, :, 0] = target_color[0]
new_data[:, :, 1] = target_color[1]
new_data[:, :, 2] = target_color[2]

# Set Alpha based on darkness (inverted brightness)
# Pure black (0) -> Alpha 255
# Pure white (255) -> Alpha 0
new_alpha = 255 - brightness
# Clip alpha: make near-whites fully transparent to clean up artifacts
new_alpha[brightness > 240] = 0
new_data[:, :, 3] = new_alpha

# Create a wide canvas to prevent vertical scaling issues
# Target ratio 3:1
h, w, c = new_data.shape
target_w = int(h * 4) # Make it very wide
canvas = np.zeros((h, target_w, 4), dtype=np.uint8)

# Calculate x offset to center the skyline
x_offset = (target_w - w) // 2

# Place image in center of canvas
canvas[:, x_offset:x_offset+w, :] = new_data

# Save
new_img = Image.fromarray(canvas)
new_img.save("/Users/jorikschut/Documents/Projecten-sites/benb-next-to-sea/public/images/vlissingen-skyline-blue-wide.png")
print("Successfully created vlissingen-skyline-blue-wide.png")
