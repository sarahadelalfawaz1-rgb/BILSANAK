
locations_by_language = {
    "English": ["Terminal 1", "Terminal 1", "Terminal 2", "Terminal 2", "Terminal 3", "Terminal 3"],
    "French": ["Terminal 1", "Terminal 1", "Terminal 2", "Terminal 3"],
    "Chinese": ["Terminal 1", "Terminal 2", "Terminal 3"],
    "Spanish": ["Terminal 1", "Terminal 2", "Terminal 3"],
    "Urdu": ["Terminal 1", "Terminal 2", "Terminal 3"],
}

TRANSLATORS = []

for language, locations in locations_by_language.items():
    for location in locations:
        TRANSLATORS.append({
            "translator_id": f"T{len(TRANSLATORS) + 1:02d}",
            "language": language,
            "location": location,
            "status": "Available",
        })
