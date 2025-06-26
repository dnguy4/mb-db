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
}

PATH = "content"
PAGE_PATHS = ["pages"]
STATIC_PATHS = ["cards", "images"]

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
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (("Github", "https://www.github.com/dnguy4"),)

DEFAULT_PAGINATION = False
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True

# RELATIVE_URLS = True
THEME = "./pelican-fh5co-marble"

# https://github.com/getpelican/pelican/issues/686#issuecomment-48603981
PATH_METADATA = "(?P<path_no_ext>.*)\..*"
PAGE_SAVE_AS = "{path_no_ext}.html"
PAGE_URL = "{path_no_ext}.html"

STATIC_SAVE_AS = "{path}"
