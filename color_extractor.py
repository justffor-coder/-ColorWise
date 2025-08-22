# color_extractor.py
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import os


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def extract_colors(image_path, n_colors=5):
    # Open image
    image = Image.open(image_path)
    image = image.resize((150, 150))  # Reduce size for speed
    # Convert to RGB (in case of RGBA/PNG)
    image = image.convert('RGB')
    # Reshape to list of pixels
    pixels = np.array(image).reshape(-1, 3)

    # Use KMeans to find dominant colors
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)

    # Count how often each color appears
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    sorted_colors = [colors[i]
                     for i in counts.argsort()[::-1]]  # Sort by frequency

    # Convert to HEX
    hex_colors = [rgb_to_hex(c) for c in sorted_colors]
    rgb_colors = [tuple(c) for c in sorted_colors]

    return hex_colors, rgb_colors
