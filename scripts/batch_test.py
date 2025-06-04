import argparse
import json
import math
import os
import sqlite3 as sq
from collections import defaultdict
from pathlib import Path

import numpy as np
from fuzzywuzzy import fuzz
from joblib import Parallel, delayed
from keras_ocr import pipeline
from PIL import Image

card_name_img_lookup = defaultdict(list)


def get_distance(predictions):
    """
    Function returns dictionary with (key,value):
        * text : detected text in image
        * center_x : center of bounding box (x)
        * center_y : center of bounding box (y)
        * distance_from_origin : hypotenuse
        * distance_y : distance between y and origin (0,0)
    """

    # Point of origin
    x0, y0 = 0, 0  # Generate dictionary
    detections = []
    for group in predictions:
        # Get center point of bounding box
        top_left_x, top_left_y = group[1][0]
        bottom_right_x, bottom_right_y = group[1][1]
        center_x = (top_left_x + bottom_right_x) / 2
        center_y = (
            top_left_y + bottom_right_y
        ) / 2  # Use the Pythagorean Theorem to solve for distance from origin
        distance_from_origin = math.dist(
            [x0, y0], [center_x, center_y]
        )  # Calculate difference between y and origin to get unique rows
        distance_y = center_y - y0  # Append all results
        detections.append(
            {
                "text": group[0],
                "center_x": center_x,
                "center_y": center_y,
                "distance_from_origin": distance_from_origin,
                "distance_y": distance_y,
            }
        )
    return detections


def resize_image(image, target_size=(128, 96)):
    """
    Resize an image to target size while maintaining aspect ratio.
    """
    # Calculate new dimensions maintaining aspect ratio
    width, height = image.size
    ratio = min(target_size[0] / width, target_size[1] / height)
    new_size = (int(width * ratio), int(height * ratio))

    # Resize image
    resized = image.resize(new_size, Image.BILINEAR)

    # Create padded image with target size
    padded = Image.new("RGB", target_size, color="white")
    offset = ((target_size[0] - new_size[0]) // 2, (target_size[1] - new_size[1]) // 2)
    padded.paste(resized, offset)

    return padded


def calculate_match_score(ocr_title, master_title):
    """
    Calculate match score between two titles.
    This function is cached to avoid recalculating scores.
    """
    return fuzz.ratio(ocr_title.lower(), master_title.lower())


def parallel_find_closest_title(ocr_title, master_titles, threshold=85, n_jobs=-1):
    """
    Find closest matching title using parallel processing.

    Args:
        ocr_title (str): Title recognized by OCR
        master_titles (list): List of known titles
        threshold (int): Minimum match score (0-100)
        n_jobs (int): Number of parallel jobs (-1 for all cores)

    Returns:
        tuple: (best_match, score) or (None, 0) if no match found
    """
    if not master_titles or not ocr_title:
        return None, 0

    # Calculate scores in parallel
    scores = Parallel(n_jobs=n_jobs)(
        delayed(calculate_match_score)(ocr_title, master_title)
        for master_title in master_titles
    )

    # Find best match
    if scores:
        best_index = np.argmax(scores)
        if scores[best_index] >= threshold:
            return master_titles[best_index], scores[best_index]

    return None, 0


def batch_process_images(directory_path, name_list, batch_size=32):
    """
    Batch process all images in a directory using keras_ocr pipeline.

    Args:
        directory_path (str): Path to directory containing images
        batch_size (int): Number of images to process in each batch

    Returns:
        dict: Dictionary mapping image paths to their recognition results
    """
    # Initialize pipeline
    pipeline_instance = pipeline.Pipeline()

    # Get list of all image files
    image_paths = list(Path(directory_path).glob("*"))
    image_paths = [
        p
        for p in image_paths
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        # and "steam" in p.name
    ]

    def dist(x):
        return x["distance_from_origin"]

    # Process in batches
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i : i + batch_size]
        try:
            # Load and prepare batch
            images = []
            for path in batch:
                with Image.open(path) as img:
                    height = int(img.height * 0.125)
                    width = int(img.width * 0.15)

                    # Crop the top portion
                    img = img.crop((width, 0, img.width, height))
                    img = img.convert("L").rotate(4)
                    img = resize_image(img, (640, 130))
                    img = np.array(img)
                    images.append(img)

            # Process batch
            batch_results = pipeline_instance.recognize(images)

            # Store results
            for path, recognition_result in zip(batch, batch_results):
                recognition_result = get_distance(recognition_result)
                row = sorted(recognition_result, key=dist)
                card_name = " ".join([r["text"] for r in row])
                card_name, score = parallel_find_closest_title(
                    card_name, name_list, threshold=75
                )
                if card_name:
                    card_name_img_lookup[card_name].append(str(path))

            print(
                f"Processed batch {i // batch_size + 1} of {len(image_paths) // batch_size + 1}"
            )

        except Exception as e:
            print(f"Error processing batch {i // batch_size + 1}: {str(e)}")
            raise e

    return card_name_img_lookup


def normalize_str(s: str):
    return s.lower().replace(" ", "_")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("rows", type=int, help="Number of rows")
    parser.add_argument("cols", type=int, help="Number of cols")
    args = parser.parse_args()
    directory_path = os.path.join(
        os.getcwd(), "master_imgs", f"{args.rows}_{args.cols}"
    )
    with open("card_list.json") as f:
        card_dict = json.load(f)
        card_names = [c["card_name"] for c in card_dict]

    results = batch_process_images(directory_path, card_names, batch_size=32)
    conn = sq.connect("card_list.sqlite")

    for card_name, paths in results.items():
        card_infos = conn.execute(
            "SELECT source, card_type FROM card_list WHERE card_name = ?",
            [card_name],
        ).fetchall()

        for path, row in zip(paths, card_infos):
            folder_name = os.path.join(
                "./master_imgs", normalize_str(row[0]), normalize_str(row[1])
            )
            os.makedirs(folder_name, exist_ok=True)
            os.rename(
                path, os.path.join(folder_name, normalize_str(card_name) + ".webp")
            )

    # cur = conn.execute(
    #     """SELECT card_name, "set", source FROM card_list WHERE card_name in (
    #         SELECT card_name FROM card_list GROUP BY card_name HAVING COUNT(*) > 1
    #     ) """
    # )
    # rows = cur.fetchall()
    # for card_name, set, source in rows:
    #     print(card_name, source)

    conn.close()
