import os
import cv2

import sqlite3 as sq
from contextlib import closing
from rapidfuzz import process, fuzz

def normalize_str(s: str) -> str:
    """Normalize descriptor strings."""
    return s.strip().lower().replace(" ", "_")


def valid_sets() -> set[str]:
    """Return all valid card sets."""
    with closing(sq.connect("card_list.sqlite")) as conn:
        rows = conn.execute(
            """
            SELECT DISTINCT "set" 
            FROM card_list

            """,
        ).fetchall()
        names = set([normalize_str(r[0]) for r in rows])
        return names



def label_images(image_dir: str, output_dir: str) -> None:
    """
    Prompt user to rename webp files in the image directory.

    Args:
        image_dir (str): dir containing the unlabelled images.
        output_dir (str): dir where labelled images are saved.
    """
    src_dir = os.fsencode(image_dir)
    cv2.namedWindow("Image Viewer", cv2.WINDOW_AUTOSIZE)
    set_names = valid_sets()

    for file in os.listdir(src_dir):
        filename = os.fsdecode(file)
        if not filename.endswith(".webp"):
            continue

        path = os.path.join(image_dir, filename)
        img = cv2.imread(path)
        if img is None:
            print(f"Failed to load {filename}")
            continue

        cv2.imshow("Image Viewer", img)
        # Important: allow OpenCV to actually draw the window
        cv2.waitKey(1)

        valid_input = False
        while not valid_input:
            user_input = input("Press Enter for next image, or type 'e' then Enter to exit: ")
            label = normalize_str(user_input)

            if label == "e":
                print("Exiting.")
                cv2.destroyAllWindows()
                return
            elif label == "d":
                os.remove(path)
                valid_input = True

            elif len(user_input) > 1:
                label = normalize_str(user_input)
                if label not in set_names:
                    print(f"{label} not found")
                    matches = process.extract(
                        label,
                        set_names,
                        scorer=fuzz.ratio,
                        limit=3
                    )
                    print("Close matches are", matches)
                    choice = input("Use 1, 2, 3, or none: ")
                    if not choice.strip():
                        continue
                    else:
                        label = matches[int(choice.strip())][0]

                new_path = os.path.join(output_dir, label + ".webp")
                os.rename(path, new_path)
                valid_input = True
    
            else:
                valid_input = True

    cv2.destroyAllWindows()
        

def find_missing_backs(output_dir: str) -> None:
    """Determine what sets are missing card back images."""
    src_dir = os.fsencode(output_dir)
    set_names = valid_sets()
    for file in os.listdir(src_dir):
        filename = os.fsdecode(file)[:-5]
        if filename in set_names:
            set_names.remove(filename)
    
    with open("missing_card_backs.txt", "w") as f:
        alpha = sorted(list(set_names))
        f.writelines([s + "\n" for s in alpha])


if __name__ == "__main__":
    label_images("./unsorted/2_4", "./master_imgs/backs")
    # find_missing_backs("./master_imgs/backs")
