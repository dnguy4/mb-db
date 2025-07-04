import glob
import os
import sqlite3 as sq
from collections import defaultdict
from contextlib import closing

from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("page_templates/"))
set_template = environment.get_template("sets.html")
card_template = environment.get_template("card_template.html")

SITEURL = "https://dnguy4.github.io/mb-db"


ALL_SETS_SOURCES = [
    "Base",
    "Set Rotation",
    "Collusion",
    "Mini Expansion #1 (Crossover)",
    "Mini Expansion #2 (Sponsors)",
    "Mini Expansion #3 (Fusion Chaos)",
    "Mini Expansion #4 (Final Bosses)",
    "Mini Expansion #5 (Futures)",
    "Mini Expansion #6 (Professionals)",
    "Mini Expansion #7 (Crossovers 2)",
    "Mini Expansion #8 (Crossovers 3)",
    "Mini Expansion #9 (Co-Op Bosses)",
    "Mini Expansion #10 (Extra Characters)",
    "Mini Expansion #11 (Extra Sets)",
    "Mini Expansion #12 (Finaler Bosses)",
    "Mini Expansion BGG (BoardGameGeek)",
    "The Dice Tower Promo",
]


def get_card_types(conn) -> list[str]:
    # rows = conn.execute(
    #     """
    #     SELECT DISTINCT card_type FROM card_list ORDER BY card_type
    #     """
    # ).fetchall()
    # card_types = set(r[0] for r in rows)

    # DONT_INCLUDE = ["Friendship", "Keyword", "Team", "Trigger", "Blank Custom"]
    # for type in DONT_INCLUDE:
    #     card_types.remove(type)

    # return list(card_types)

    return [
        "Core",
        "Starter",
        "Expansion",
        "Premium",
        "Master",
        "Bronze Promo",
        "Silver Promo",
        "Gold Promo",
        "Meta",
        "NPC",
        "Pro Player",
        "Character",
        "Character (Co-Op)",
        "Character Expansion",
        "Co-Op Boss",
        "Event",
    ]


def normalize_str(s: str) -> str:
    """Make lowercase, replace whitespace with underscores, and remove hashtags."""
    return s.lower().replace(" ", "_").replace("#", "")



def pelican_transform_str(s: str) -> str:
    """Transform url strings the same way Pelican does."""
    return s.lower().replace(" ", "-").replace("#","").replace("(", "").replace(")", "").rstrip(".")



def make_set_pages(conn, card_types):
    for card_type in card_types:
        rows = conn.execute(
            """
            SELECT DISTINCT source, divider 
            FROM card_list
            WHERE card_type = ?
            ORDER BY source, divider
            """,
            [card_type],
        ).fetchall()

        set_dict = defaultdict(list)
        for source, set_name in rows:
            set_normalized = pelican_transform_str(set_name)
            set_dict[source].append((set_name, set_normalized))

        if card_type == "Core":
            set_dict = {"Core Sets:": set_dict["Base"]}
        sets = list(set_dict.items())
        content = set_template.render(set_dict=sets, card_type=card_type, SITEURL=SITEURL)
        with open(f"content/sets/{normalize_str(card_type)}.html", "w") as fp:
            fp.write(content)


def make_card_pages(conn):
    conn.row_factory = sq.Row
    rows = conn.execute(
        """
        SELECT *
        FROM card_list
        """
    ).fetchall()
    for row in rows:
        card_dict = dict(row)
        src, card_type = (
            normalize_str(card_dict["source"]),
            normalize_str(card_dict["card_type"]),
        )
        card_name = normalize_str(card_dict["card_name"])
        image_path = f"/images/{src}/{card_type}/{card_name}.webp"
        if not os.path.exists(f"content{image_path}"):
            paths = glob.glob(f"content/images/**/{card_type}/{card_name}.webp")
            if paths == []:
                paths = glob.glob(f"content/images/**/**/{card_name}.webp")
            if paths:
                image_path = paths[0][7:] # Trim to the /images part
        if SITEURL:
            image_path = f"{SITEURL}{image_path}"
        
        image_path = image_path.replace("\"", "&quot;")
        card_name = card_name.replace("\"", "")
        file_path = f"content/cards/{card_type}/"
        os.makedirs(file_path, exist_ok=True)
        with open(f"{file_path}/{card_name}.html", "w") as fp:
            fp.write(card_template.render(**card_dict, image_path=image_path))

if __name__ == "__main__":
    with closing(sq.connect("card_list.sqlite")) as conn:
        card_types = get_card_types(conn)
        make_set_pages(conn, card_types)
        make_card_pages(conn)

        # card_cats = [(
        #     src, f"category/{pelican_transform_str(src)}.html"
        # ) for src in ALL_SETS_SOURCES]
        # print(card_cats)
