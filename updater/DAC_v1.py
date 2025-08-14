import os
import platform
import sys
import colorama
from colorama import Fore, Style, init
import asyncio
import aiohttp

init(autoreset=True)

# ──────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────
CONSOLE_WIDTH = 132
CONSOLE_HEIGHT = 24
MAX_ARTIFACTS_TO_FETCH = 2
TOKEN_FILE = "gh_key.txt"
WINDOW_TITLE = "dsoal artifacts check"
REPO_OWNER = 'kcat'
REPO_DSOAL = "dsoal"
REPO_OPENAL_SOFT = "openal-soft"

# ──────────────────────────────────────────────────────────
# SETUP
# ──────────────────────────────────────────────────────────
if platform.system() == "Windows":
    os.system(f"title {WINDOW_TITLE}")
    os.system(f"mode con: cols={CONSOLE_WIDTH} lines={CONSOLE_HEIGHT}")

# Read GitHub token from file
def get_github_token():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        token_file_path = os.path.join(script_dir, TOKEN_FILE)
        
        with open(token_file_path, 'r') as file:
            token = file.read().strip()
            
        if not token:
            print(f"{Fore.RED}Error: Token file '{TOKEN_FILE}' is empty{Style.RESET_ALL}")
            sys.exit(1)
            
        # Validate token format
        valid_prefixes = ('ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_', 'github_pat_')
        if not any(token.startswith(prefix) for prefix in valid_prefixes):
            print(f"{Fore.RED}Error: Invalid GitHub token format. Token must start with one of: {', '.join(valid_prefixes)}{Style.RESET_ALL}")
            sys.exit(1)
            
        return token
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Token file '{TOKEN_FILE}' not found in script directory{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error reading token file: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

GITHUB_TOKEN = get_github_token()
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# ──────────────────────────────────────────────────────────
# FETCH ARTIFACTS
# ──────────────────────────────────────────────────────────
async def fetch_json(session, url):
    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                print(f"{Fore.RED}Error fetching {url}, Status: {resp.status}, Response: {error_text}{Style.RESET_ALL}")
                return resp.status, None
            return None, await resp.json()
    except Exception as e:
        print(f"{Fore.RED}Exception during fetch: {str(e)}{Style.RESET_ALL}")
        return -1, None

async def fetch_artifacts(session, repo_name, workflow_filename=None, artifact_filter=None):
    artifacts = []
    run_id = None
    
    if workflow_filename:
        runs_url = f"https://api.github.com/repos/{REPO_OWNER}/{repo_name}/actions/workflows/{workflow_filename}/runs"
        error, runs_data = await fetch_json(session, runs_url)
        if error:
            return (f"{repo_name} ({workflow_filename})", f"Failed to fetch workflow '{workflow_filename}' runs: {error}", [], None)
        
        if not isinstance(runs_data, dict) or 'workflow_runs' not in runs_data:
            return (f"{repo_name} ({workflow_filename})", "Invalid workflow runs data format", [], None)
            
        for run in runs_data.get('workflow_runs', []):
            if not isinstance(run, dict) or 'id' not in run:
                continue
                
            rid = run['id']
            art_url = f"https://api.github.com/repos/{REPO_OWNER}/{repo_name}/actions/runs/{rid}/artifacts"
            error, art_data = await fetch_json(session, art_url)
            
            if error is None and art_data and isinstance(art_data, dict) and 'artifacts' in art_data:
                for artifact in art_data['artifacts']:
                    if not isinstance(artifact, dict):
                        continue
                    name = artifact.get('name', '')
                    if not artifact_filter or artifact_filter(name):
                        artifacts.append((name, artifact.get('archive_download_url'), artifact.get('id'), rid))
                if artifacts:
                    run_id = rid
                    break
    else:
        artifacts_url = f"https://api.github.com/repos/{REPO_OWNER}/{repo_name}/actions/artifacts"
        error, data = await fetch_json(session, artifacts_url)
        if error:
            return (repo_name, f"Failed to fetch artifacts for {repo_name}: {error}", [], None)
            
        if not isinstance(data, dict) or 'artifacts' not in data:
            return (repo_name, "Invalid artifacts data format", [], None)
            
        # Get latest MAX_ARTIFACTS_TO_FETCH artifacts
        sorted_artifacts = sorted(
            data.get('artifacts', []),
            key=lambda x: x.get('workflow_run', {}).get('id', 0),
            reverse=True
        )[:MAX_ARTIFACTS_TO_FETCH]
        
        artifacts = []
        for a in sorted_artifacts:
            if not isinstance(a, dict):
                continue
            run_id_value = a.get('workflow_run', {}).get('id')
            artifacts.append((a['name'], a['archive_download_url'], a['id'], run_id_value))
            
        if artifacts:
            run_id = artifacts[0][3]  # Use artifacts list instead of sorted_artifacts
    
    artifacts.sort(key=lambda x: x[0])
    
    output_lines = []
    for name, url, artifact_id, run_id_val in artifacts:
        artifact_url = f"https://github.com/{REPO_OWNER}/{repo_name}/actions/runs/{run_id_val}/artifacts/{artifact_id}"
        colored_name = f"{Fore.GREEN}{name}{Style.RESET_ALL}"
        colored_artifact_url = f"{Fore.CYAN}{artifact_url}{Style.RESET_ALL}"
        output_lines.append(f"{colored_name} - {colored_artifact_url}")
    
    if run_id:
        build_url = f"https://github.com/{REPO_OWNER}/{repo_name}/actions/runs/{run_id}"
        colored_build_url = f"{Fore.YELLOW}{build_url}{Style.RESET_ALL}"
        output_lines.append(f"\nBuild log - {colored_build_url}")
    
    label = f"{repo_name} ({workflow_filename})" if workflow_filename else repo_name
    return (label, None, output_lines, run_id)

# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────
async def main():
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        sections = [
            (REPO_DSOAL, None, None),
            (REPO_OPENAL_SOFT, "ci.yml", lambda name: 'Win' in name and name.endswith('-Release')),
            (REPO_OPENAL_SOFT, "utils.yml", None)
        ]
        tasks = [fetch_artifacts(session, repo, workflow, art_filter) for repo, workflow, art_filter in sections]
        results = await asyncio.gather(*tasks)
        
        for (repo, workflow, art_filter), (label, error, output, _) in zip(sections, results):
            print("")
            print(f"=== Artifacts from {label} ===\n")
            if error:
                print(f"{Fore.RED}{error}{Style.RESET_ALL}\n")
            else:
                if output:
                    for line in output:
                        print(line)
                else:
                    print(f"{Fore.YELLOW}No artifacts found for {label}{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(main())
    print("")
    input("Press Enter to exit...")