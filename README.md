# YTMusic Analytics

Project structure aligned with Products & Epics:

- Product A – YT Music Library → `src/library/`
- Product B – Listening History → `src/history/`
- Product C – ETL Automation → `src/automation/`

See Jira epics A/B/C for detailed user stories.


ytmusic-analytics/
├─ dashboards/                        # Looker Studio, captures, doc dashboards
├─ data/
│  ├─ raw/
│  │  ├─ takeout/
│  │  │  ├─ youtube_music/
│  │  │  │  ├─ history/              # search-history.json, watch-history.json (Takeout brut)
│  │  │  │  ├─ music_library/        # music library songs.csv (Takeout brut)
│  │  │  │  └─ playlists/            # tous les *-videos.csv + playlists.csv (Takeout brut)
│  │  │  └─ samples/                 # history_sample.json, library_songs_sample.json
│  │  └─ ytmusic/                    # extractions brutes via ytmusicapi (Product A)
│  ├─ interim/                       # fichiers temporaires (staging local)
│  └─ processed/
│     └─ history/                    # outputs de parsing/agrégation
│        ├─ takeout_history_all.csv
│        └─ takeout_history_mvp.csv
│
├─ dbt/                              # projet dbt (sources, models, tests, docs)
│
├─ orchestration/                    # config n8n, scripts shell, jobs dbt Cloud
│
├─ secrets/                          # identifiants/API keys (gitignored)
│  ├─ browser.json                   # ytmusicapi (cookies)
│  ├─ oauth.json                     # OAuth local
│  ├─ oauth_client.json              # client OAuth GCP
│  └─ ytmusic-analytics-*.json       # service account BigQuery
│
├─ src/
│  ├─ library/                       # Product A – Library
│  │  ├─ a1_extract_load/           # Epic A1 – ytmusicapi → BigQuery
│  │  │  └─ fetch_ytmusic.py
            extract_library.py
│  │  ├─ a2_spotify_enrich/         # Epic A2 – enrichissement Spotify (genres)
│  │  ├─ a3_dbt/                    # Epic A3 – modèles dbt pour la bibliothèque
│  │  └─ a4_dashboard/              # Epic A4 – préparation dashboard Library
│  │
│  ├─ history/                       # Product B – Listening History
│  │  ├─ b1_extract_load/           # Epic B1 – parsing Takeout + load BigQuery
│  │  │  ├─ parse_takeout_history.py
│  │  │  ├─ parse_takeout_history_tt.py
│  │  │  └─ etl_raw_history_bq.py
│  │  ├─ b2_spotify_enrich/         # Epic B2 – enrichissement Spotify pour l’historique
│  │  ├─ b3_dbt/                    # Epic B3 – modèles dbt (stg → int → fact_listening)
│  │  └─ b4_dashboard/              # Epic B4 – dashboard Listening History
│  │
│  └─ automation/                    # Product C – ETL Automation
│     ├─ c1_n8n/                     # Epic C1 – workflows n8n (Library/History)
│     ├─ c2_dbt_automation/          # Epic C2 – jobs dbt, CI, triggers
│     └─ c3_monitoring/              # Epic C3 – logging & monitoring
│
├─ venv/                             # environnement virtuel Python
│
├─ .env.example                      # variables d’environnement d’exemple :contentReference[oaicite:2]{index=2}
├─ .gitignore                        # ignore venv, secrets, data processed/interim, etc. :contentReference[oaicite:3]{index=3}
├─ README.md                         # description projet, mapping produits/épics :contentReference[oaicite:4]{index=4}
└─ setup_structure.py                # script pour créer l’arborescence de base :contentReference[oaicite:5]{index=5