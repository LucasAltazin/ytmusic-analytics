import json
import csv
from pathlib import Path
from datetime import datetime, timezone

# CONFIG – adapt paths if needed
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "Takeout"
OUTPUT_CSV = PROJECT_ROOT / "data" / "takeout_history_all.csv"


def parse_time(value: str):
    """
    Parse Takeout 'time' field -> ISO 8601 in UTC
    Example input: '2025-11-18T10:23:45.123Z'
    """
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return None


def extract_title_artist_album(entry: dict):
    """
    Extract track title, artist and album from a Takeout entry.
    (best effort, works for both YouTube & YouTube Music)
    """
    title = entry.get("title") or ""

    subtitles = entry.get("subtitles") or []
    artist = ""
    album = ""

    if subtitles and isinstance(subtitles, list):
        # souvent : index 0 = artiste / chaîne
        artist = subtitles[0].get("name", "") or ""
        # parfois : index 1 = album ou autre info
        if len(subtitles) > 1:
            album = subtitles[1].get("name", "") or ""

    prefix = "Listened to "
    if title.startswith(prefix):
        track_title = title[len(prefix):]
    else:
        track_title = title

    return title.strip(), track_title.strip(), artist.strip(), album.strip()


def iter_history_files():
    """
    Yield all JSON files that look like watch-history from the Takeout folder.
    """
    for path in RAW_DIR.rglob("*.json"):
        if "watch-history" in path.name:
            yield path


def main():
    rows = []

    for json_file in iter_history_files():
        print(f"Parsing {json_file}")
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            continue  # unexpected format

        for entry in data:
            time_raw = entry.get("time")
            played_at = parse_time(time_raw)

            title, track_title, artist, album = extract_title_artist_album(entry)
            header = entry.get("header", "")  # YouTube / YouTube Music / autre
            title_url = entry.get("titleUrl") or ""
            products = entry.get("products") or []

            rows.append({
                "played_at": played_at,
                "title": title,
                "track_title": track_title,
                "artist": artist,
                "album": album,
                "genre": "",
                "play_count": 1,
                "header": header,
                "title_url": title_url,
                "products": ",".join(products) if isinstance(products, list) else str(products),
                "source_file": json_file.name,
            })

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "played_at",
                "title",
                "track_title",
                "artist",
                "album",
                "genre",
                "play_count",
                "header",
                "title_url",
                "products",
                "source_file",
            ],
            delimiter="|",  # pipe separator for BigQuery
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Written {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
