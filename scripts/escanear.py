import os
import json
import shutil
import subprocess
import requests

ORG       = "huggingface"
MAX_REPOS = 10
TOKEN     = ""          # opcional: pega tu GitHub token aquí
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS_DIR = os.path.join(BASE_DIR, "repos")
OUT_DIR   = os.path.join(BASE_DIR, "resultados")
GITLEAKS  = shutil.which("gitleaks") or os.path.join(BASE_DIR, "gitleaks", "gitleaks.exe")

os.makedirs(REPOS_DIR, exist_ok=True)
os.makedirs(OUT_DIR,   exist_ok=True)

# ── 1. Listar repos via GitHub API ───────────────────────────
headers = {"User-Agent": "gitleaks-tarea"}
if TOKEN:
    headers["Authorization"] = f"token {TOKEN}"

resp = requests.get(
    f"https://api.github.com/orgs/{ORG}/repos",
    headers=headers,
    params={"per_page": 100, "sort": "updated", "type": "public"},
)
resp.raise_for_status()

repos = sorted(resp.json(), key=lambda r: r["stargazers_count"], reverse=True)[:MAX_REPOS]
print(f"Repos seleccionados ({len(repos)}):")
for r in repos:
    print(f"  - {r['name']} ({r['stargazers_count']} ⭐)")

# ── 2. Clonar + escanear ─────────────────────────────────────
all_findings = []

for repo in repos:
    name      = repo["name"]
    clone_url = repo["clone_url"]
    repo_path = os.path.join(REPOS_DIR, name)
    json_path = os.path.join(OUT_DIR, f"{name}.json")

    if not os.path.isdir(repo_path):
        print(f"\nClonando {name}...")
        subprocess.run(
            ["git", "clone", "--depth", "50", clone_url, repo_path],
            check=True, capture_output=True
        )
    else:
        print(f"\n{name} ya existe, saltando clone.")

    print(f"Escaneando {name}...")
    subprocess.run(
        [GITLEAKS, "git", repo_path,
         "--report-format", "json",
         "--report-path", json_path,
         "--exit-code", "0"],
        capture_output=True
    )

    if os.path.exists(json_path):
        with open(json_path, encoding="utf-8") as f:
            findings = json.load(f)
        if findings:
            for finding in findings:
                finding["Repository"] = name
            all_findings.extend(findings)
            print(f"  → {len(findings)} hallazgo(s)")
        else:
            print("  → 0 hallazgos")

# ── 3. Guardar JSON combinado ─────────────────────────────────
combined_path = os.path.join(OUT_DIR, "all_findings.json")
with open(combined_path, "w", encoding="utf-8") as f:
    json.dump(all_findings, f, ensure_ascii=False, indent=2)

print(f"\nTotal hallazgos: {len(all_findings)}")
print(f"Guardado en: {combined_path}")
