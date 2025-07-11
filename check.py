import os
import platform
import sys
import colorama
from colorama import Fore, Style, init
import asyncio
import aiohttp
import re
import difflib

init(autoreset=True)

# ──────────────────────────────────────────────────────────
# SETUP
# ──────────────────────────────────────────────────────────

if platform.system() == "Windows":
    os.system("title dsoal artifacts check")
    os.system("mode con: cols=132 lines=24")

GITHUB_TOKEN = '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'
REPO_OWNER = 'kcat'

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
                print(f"{Fore.RED}Error fetching {url}, Status: {resp.status}{Style.RESET_ALL}")
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

        for run in runs_data.get('workflow_runs', []):
            rid = run['id']
            art_url = f"https://api.github.com/repos/{REPO_OWNER}/{repo_name}/actions/runs/{rid}/artifacts"
            error, art_data = await fetch_json(session, art_url)
            if error is None and art_data.get('artifacts'):
                for artifact in art_data['artifacts']:
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

        artifacts = [(a['name'], a['archive_download_url'], a['id'], a['workflow_run']['id']) for a in sorted(
            data.get('artifacts', []),
            key=lambda x: x.get('workflow_run', {}).get('id', 0),
            reverse=True)[:2]]

        if data.get('artifacts'):
            run_id = data['artifacts'][0].get('workflow_run', {}).get('id')
            if run_id is None:
                run_id = ''

    if not artifacts:
        print(f"{Fore.YELLOW}No artifacts found for {repo_name}{Style.RESET_ALL}")
    
    output_lines = []
    for name, url, artifact_id, run_id in artifacts:
        artifact_url = f"https://github.com/{REPO_OWNER}/{repo_name}/actions/runs/{run_id}/artifacts/{artifact_id}"
        colored_name = f"{Fore.GREEN}{name}{Style.RESET_ALL}"
        output_lines.append(f"{colored_name} - {artifact_url}")

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
            ("dsoal", None, None, 'dsoal'),
            ("openal-soft", "ci.yml", lambda name: 'Win' in name and name.endswith('-Release'), 'soft_oal'),
            ("openal-soft", "utils.yml", None, 'openal_soft')
        ]

        tasks = [fetch_artifacts(session, repo, workflow, art_filter) for repo, workflow, art_filter, _ in sections]
        results = await asyncio.gather(*tasks)

        for (repo, workflow, _, run_key), (label, error, output, run_id) in zip(sections, results):
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
