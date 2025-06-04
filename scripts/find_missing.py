import json
import glob
from pathlib import Path

with open("card_list.json") as f:
    card_dict = json.load(f)
    card_names = {}
    for c in card_dict:
        n = c["card_name"].lower().replace(" ", "_")
        card_names[n] = {
            "source": c["source"],
            "set": c["set"],
            "card_type": c["card_type"],
        }

fs = glob.glob("./master_imgs/**/*.webp", recursive=True)
for fn in fs:
    card_name = Path(fn).stem
    if card_name in card_names:
        del card_names[card_name]

print(len(card_names))

with open("missing_cards.json", "w") as fp:
    json.dump(card_names, fp, indent=2)
