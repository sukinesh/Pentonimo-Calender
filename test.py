from PIL import Image, ImageDraw

# Create a blank image with a white background
image = Image.new("RGB", (700, 700), "#8d4331")

# Create a draw object
draw = ImageDraw.Draw(image)

# Define the coordinates of the square
x0, y0 = 0, 0
x1, y1 = 100, 100

# Draw the square
draw.rectangle([x0, y0, x1, y1], fill="black")

# Save the image
image.save("pic/square.png")