from pathlib import Path

# Point de départ : dossier où se trouve ce script
ROOT = Path(__file__).resolve().parent

# Dossiers à créer
dirs = [
    "src/library/a1_extract_load",
    "src/library/a2_spotify_enrich",
    "src/library/a3_dbt",
    "src/library/a4_dashboard",
    "src/history/b1_extract_load",
    "src/history/b2_spotify_enrich",
    "src/history/b3_dbt",
    "src/history/b4_dashboard",
    "src/automation/c1_n8n",
    "src/automation/c2_dbt_automation",
    "src/automation/c3_monitoring",
    "data/raw/takeout",
    "data/raw/ytmusic",
    "data/interim",
    "data/processed",
    "dbt",
    "dashboards",
    "orchestration",
    "secrets",
]

files_with_default_content = {
    "README.md": """# YTMusic Analytics

Project structure aligned with Products & Epics:

- Product A – YT Music Library → `src/library/`
- Product B – Listening History → `src/history/`
- Product C – ETL Automation → `src/automation/`

See Jira epics A/B/C for detailed user stories.
""",
    ".env.example": """# Example environment variables
# Copy to .env and fill with your values

YT_PROJECT_ID=ytmusic-analytics-xxxxxx
YT_BQ_LOCATION=EU
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
""",
    ".gitignore": """# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.pkl

# Virtual env
venv/
.env

# VSCode
.vscode/

# Secrets
secrets/
*.json

# Data
data/interim/
data/processed/
""",
}

def main():
    print(f"Project root: {ROOT}")

    # Create directories
    for d in dirs:
        path = ROOT / d
        path.mkdir(parents=True, exist_ok=True)
        print(f"[DIR]  {path.relative_to(ROOT)}")

    # Create files if they don't exist
    for rel_path, content in files_with_default_content.items():
        file_path = ROOT / rel_path
        if file_path.exists():
            print(f"[SKIP] {rel_path} already exists")
            continue
        file_path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"[FILE] {rel_path} created")

    print("\n✅ Structure initialized.")

if __name__ == "__main__":
    main()
