import json
import random
import logging
from utils import latin_to_persian_digits


def get_random_poem_message() -> str:
    try:
        with open("hafez_ghazals.json", "r", encoding="utf-8") as f:
            poems = json.load(f)
    except FileNotFoundError:
        logging.error("hafez_ghazals.json file not found.")
        raise SystemExit(1)
    except json.JSONDecodeError:
        logging.error("Failed to parse hafez_ghazals.json file.")
        raise SystemExit(1)

    # randomly select poem with weighted comments
    keys = list(poems.keys())
    weights = [poems[k].get("tedad_comments", 1) for k in keys]
    selected_key = random.choices(keys, weights=weights, k=1)[0]
    selected_poem = poems[selected_key]

    # poem details
    selected_vazn = selected_poem.get("vazn", "—")
    total_baits = int(selected_poem.get("tedad_abiat", 1))
    selected_bait_number = random.randint(1, total_baits)

    selected_bait = selected_poem["baits"].get(str(selected_bait_number), {})
    content = selected_bait.get("content", "—")
    meaning = selected_bait.get("meaning", "")

    # clean meaning
    meaning = meaning.replace(".", "")
    meaning = meaning.split(":", 1)[1] if ":" in meaning else meaning

    # convert digits
    ghazal_num = latin_to_persian_digits(str(selected_key))
    bait_num = latin_to_persian_digits(str(selected_bait_number))

    title = f"غزل شمارهٔ {ghazal_num}   بیت {bait_num}"

    return f"{title}\n{selected_vazn}\n\n\n{content}\n\n\nگنجور:\n{meaning}"
