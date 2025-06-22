from collections import defaultdict
import sqlite3 as sq
from jinja2 import Environment, FileSystemLoader

from contextlib import closing


environment = Environment(loader=FileSystemLoader("page_templates/"))
set_template = environment.get_template("sets.html")
set_index_template = environment.get_template("sets_index.html")


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
            set_normalized = set_name.lower().replace(" ", "_")
            set_dict[source].append((set_name, set_normalized))

        if card_type == "Core":
            set_dict = {"Core Sets:": set_dict["Base"]}
        sets = list(set_dict.items())
        content = set_template.render(set_dict=sets, card_type=card_type)
        with open(f"content/sets/{card_type}.html", "w") as fp:
            fp.write(content)

    with open("content/pages/sets.html", "w") as fp:
        content = set_index_template.render(card_types=card_types)
        fp.write(content)


if __name__ == "__main__":
    with closing(sq.connect("card_list.sqlite")) as conn:
        card_types = get_card_types(conn)

        # param_lst = ", ".join("?" for _ in card_types)
        # rows = conn.execute(
        #     f"""
        #     SELECT DISTINCT card_type, source, divider
        #     FROM card_list
        #     WHERE card_type IN ({param_lst})
        #     ORDER BY card_type, source, divider
        #     """,
        #     card_types,
        # ).fetchall()
        make_set_pages(conn, card_types)
