from ytmusicapi import YTMusic
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from pathlib import Path
from datetime import datetime
import json
import uuid
import os

# ========= PARAMETRES A ADAPTER =========
GCP_PROJECT_ID = "ytmusic-analytics-478417"          # ex: "ytmusic-project"
BQ_DATASET_ID = "ytmusic_analytics"           # le dataset créé dans BigQuery
BQ_TABLE_ID = "raw_history"                   # nom de la table
GCP_CREDENTIALS_PATH = "secrets/ytmusic-analytics-478417-692a6c5d2282.json"

# ========================================

# 0) Authent BigQuery via service account
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCP_CREDENTIALS_PATH

# 1) Client YT Music
yt = YTMusic("browser.json")

# 2) Récupérer l'historique
history = yt.get_history()
print(f"Fetched {len(history)} history items from YouTube Music")

rows = []
ingestion_ts = datetime.utcnow().isoformat()

for item in history:
    video_id = item.get("videoId")
    title = item.get("title")

    artists = item.get("artists") or []
    artist_names = ", ".join(
        a.get("name") for a in artists if a.get("name")
    )

    album_obj = item.get("album") or {}
    album_name = album_obj.get("name")

    played_at_raw = item.get("played")
    duration_raw = item.get("duration")
    like_status = item.get("likeStatus")

    raw_json = json.dumps(item, ensure_ascii=False)

    rows.append({
        "raw_history_id": str(uuid.uuid4()),
        "video_id": video_id,
        "title": title,
        "artist_names": artist_names,
        "album_name": album_name,
        "played_at_raw": played_at_raw,
        "duration_raw": duration_raw,
        "like_status": like_status,
        "source_raw": "history_api",
        "raw_json": raw_json,
        "ingestion_ts": ingestion_ts,
    })

print(f"Prepared {len(rows)} rows for raw_history")

# 3) Client BigQuery
client = bigquery.Client(project=GCP_PROJECT_ID)

dataset_ref = client.dataset(BQ_DATASET_ID)
table_ref = dataset_ref.table(BQ_TABLE_ID)

# 4) Définir le schéma (doit matcher ton data model)
schema = [
    bigquery.SchemaField("raw_history_id", "STRING"),
    bigquery.SchemaField("video_id", "STRING"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("artist_names", "STRING"),
    bigquery.SchemaField("album_name", "STRING"),
    bigquery.SchemaField("played_at_raw", "STRING"),
    bigquery.SchemaField("duration_raw", "STRING"),
    bigquery.SchemaField("like_status", "STRING"),
    bigquery.SchemaField("source_raw", "STRING"),
    bigquery.SchemaField("raw_json", "STRING"),
    bigquery.SchemaField("ingestion_ts", "TIMESTAMP"),
]

# 5) Créer la table si elle n'existe pas
try:
    table = client.get_table(table_ref)
    print(f"Table {table.full_table_id} already exists.")
except NotFound:
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)
    print(f"Created table {table.full_table_id}")

# 6) Charger les données (WRITE_TRUNCATE = on remplace tout à chaque run, WRITE_APPEND pour append)
job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

load_job = client.load_table_from_json(
    rows,
    table_ref,
    job_config=job_config,
)

print("Starting BigQuery load job...")
load_job.result()  # attendre la fin du job

print(f"Loaded {len(rows)} rows into {BQ_DATASET_ID}.{BQ_TABLE_ID}")
