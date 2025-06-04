from itertools import product
import os
from PIL import Image
from pathlib import Path


# todo: clean up ~/.keras_ocr folder
def copy_images_by_size(source_dir, target_dir, dims):
    """
    Copies images with exact resolution from source_dir to target_dir

    Args:
        source_dir (str): Path to the source directory containing images
        target_dir (str): Path where matching images will be copied

    Returns:
        int: Number of images copied
    """
    # Create target directory if it doesn't exist
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    # Initialize counter for copied images
    copied_count = 0

    # Iterate through all files in the source directory
    for file_path in Path(source_dir).iterdir():
        if file_path.is_file() and file_path.suffix.lower() in {
            ".jpg",
            ".jpeg",
            ".png",
        }:
            try:
                # Open the image
                with Image.open(file_path) as img:
                    # Get dimensions
                    width, height = img.size

                    # Check if dimensions match exactly
                    if width == dims[0] and height == dims[1]:
                        # Copy the file to target directory
                        target_path = Path(target_dir) / file_path.name
                        file_path.rename(target_path)
                        # print(f"Copied {file_path.name}")
                        copied_count += 1

            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

    return copied_count


def split_images(source_dir, dest_dir, dim):
    # Iterate through all files in the source directory
    img_exts = {".jpg", ".jpeg", ".png"}
    count = 0
    os.makedirs(dest_dir, exist_ok=True)
    for file_path in Path(source_dir).iterdir():
        ext = file_path.suffix.lower()
        if not file_path.is_file() or ext not in img_exts:
            continue

        with Image.open(file_path) as img:
            w, h = img.size
            num_rows, num_cols = dim
            tile_w = w // num_cols
            tile_h = h // num_rows
            grid = product(
                range(0, h - h % tile_h, tile_h),
                range(0, w - w % tile_w, tile_w),
            )
            for i, j in grid:
                box = (j, i, j + tile_w, i + tile_h)
                out = os.path.join(dest_dir, f"{count}.webp")
                tile = img.crop(box)
                extrema = tile.convert("L").getextrema()
                # if abs(extrema[0] - extrema[1]) < 20:
                if abs(extrema[0] - extrema[1]) < 40:
                    continue
                tile.save(out, "WEBP")
                count += 1
        # return
    print(count)


if __name__ == "__main__":
    source_folder = "~/.local/share/Tabletop Simulator/Mods/Images_mb"

    dims = [
        ((750, 1050), (1, 1)),
        ((3000, 2100), (2, 4)),
        ((2250, 3150), (3, 3)),
        ((3000, 3150), (3, 4)),
        ((3658, 4096), (4, 5)),
        ((3750, 3150), (3, 5)),
        ((4096, 3986), (7, 10)),
        ((4096, 3990), (7, 10)),
    ]
    for img_dim, card_dim in dims:
        target_folder = f"./images/{card_dim[0]}_{card_dim[1]}"
        num_copied = copy_images_by_size(source_folder, target_folder, img_dim)
        print(f"Total images copied for dim {img_dim}: {num_copied}")

    for _, (x, y) in dims:
        split_images(f"./images/{x}_{y}", f"./master_imgs/{x}_{y}", (x, y))
