AUTHOR = "soup"
SITENAME = "Millenium Blades Wiki"
SITEURL = ""

PLUGIN_PATHS = [
    "../pelican-plugins",
]
PLUGINS = ["i18n_subsites", "search"]
JINJA_ENVIRONMENT = {
    "extensions": ["jinja2.ext.i18n"],
}
JINJA_GLOBALS = {
    "card_types": [
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
    ],
    "card_categories": [
        ("Base", "category/base.html"),
        ("Set Rotation", "category/set-rotation.html"),
        ("Collusion", "category/collusion.html"),
        ("Mini Expansion #1 (Crossover)", "category/mini-expansion-1-crossover.html"),
        ("Mini Expansion #2 (Sponsors)", "category/mini-expansion-2-sponsors.html"),
        (
            "Mini Epxpansion #3 (Fusion Chaos)",
            "category/mini-expansion-3-fusion-chaos.html",
        ),
        (
            "Mini Expansion #4 (Final Bosses)",
            "category/mini-expansion-4-final-bosses.html",
        ),
        ("Mini Expansion #5 (Futures)", "category/mini-expansion-5-futures.html"),
        (
            "Mini Expansion #6 (Professionals)",
            "category/mini-expansion-6-professionals.html",
        ),
        (
            "Mini Expansion #7 (Crossovers 2)",
            "category/mini-expansion-7-crossovers-2.html",
        ),
        (
            "Mini Expansion #8 (Crossovers 3)",
            "category/mini-expansion-8-crossovers-3.html",
        ),
        (
            "Mini Expansion #9 (Co-Op Bosses)",
            "category/mini-expansion-9-co-op-bosses.html",
        ),
        (
            "Mini Expansion #10 (Extra Characters)",
            "category/mini-expansion-10-extra-characters.html",
        ),
        (
            "Mini Expansion #11 (Extra Sets)",
            "category/mini-expansion-11-extra-sets.html",
        ),
        (
            "Mini Expansion #12 (Finaler Bosses)",
            "category/mini-expansion-12-finaler-bosses.html",
        ),
        (
            "Mini Expansion BGG (BoardGameGeek)",
            "category/mini-expansion-bgg-boardgamegeek.html",
        ),
        ("The Dice Tower Promo", "category/the-dice-tower-promo.html"),
    ],
}

PATH = "content"
PAGE_PATHS = ["pages"]
STATIC_PATHS = ["cards", "images", "sets"]

TIMEZONE = "America/Belize"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    # ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (("Github", "https://www.github.com/dnguy4/mb-db"),)

DEFAULT_PAGINATION = False
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True

# RELATIVE_URLS = True
THEME = "./pelican-fh5co-marble"

# https://github.com/getpelican/pelican/issues/686#issuecomment-48603981
# Mirror content hierarchy to output hierarchy. When this is on, Stork doesn't work
# and the set pages need to be changed a little so their links work
PATH_METADATA = "(?P<path_no_ext>.*)\..*"
PAGE_SAVE_AS = "{path_no_ext}.html"
PAGE_URL = "{path_no_ext}.html"
ARTICLE_SAVE_AS = "{path_no_ext}.html"
ARTICLE_URL = "{path_no_ext}.html"

STATIC_SAVE_AS = "{path}"
STATIC_URL = "{path_no_ext}.html"

# Modify stork search? Slow when things are in separate folders
STORK_INPUT_OPTIONS = {"title_boost": "Large"}
