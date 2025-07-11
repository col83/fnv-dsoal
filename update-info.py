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
    os.system("title dsoal artifacts update")
    os.system("mode con: cols=132 lines=41")

GITHUB_TOKEN = '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'
REPO_OWNER = 'kcat'
file_name = 'README.md'

HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# CONSTANTS (PREFIXES)
DSOAL_LINE_FILTER = "DSOAL - "
SOFT_OAL_LINE_FILTER = "soft_oal-Win*-Release - "
OPENAL_SOFT_LINE_FILTER = "openal-soft (utils) (x64) - "

# Empty map for ID
run_id_map = {
    'dsoal': '',
    'soft_oal': '',
    'openal_soft': ''
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
# HIGHLIGHT DIFFERENTS
# ──────────────────────────────────────────────────────────

def highlight_diff(old, new):
    highlighted_old = ""
    highlighted_new = ""
    seq = difflib.SequenceMatcher(None, old, new)
    for tag, i1, i2, j1, j2 in seq.get_opcodes():
        if tag == 'equal':
            highlighted_old += old[i1:i2]
            highlighted_new += new[j1:j2]
        elif tag == 'replace' or tag == 'delete':
            highlighted_old += f"{Fore.RED}{old[i1:i2]}{Style.RESET_ALL}"
        if tag == 'replace' or tag == 'insert':
            highlighted_new += f"{Fore.GREEN}{new[j1:j2]}{Style.RESET_ALL}"
    return highlighted_old, highlighted_new

# ──────────────────────────────────────────────────────────
# README.md LINK UPDATE
# ──────────────────────────────────────────────────────────

def update_readme(run_id_map):
    if not os.path.exists(file_name):
        print("")
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} File '{file_name}' not found!")
        print("")
        input("Press Enter to exit...")
        sys.exit(1)

    line_filters = {
        3: (DSOAL_LINE_FILTER, f"https://github.com/kcat/dsoal/actions/runs/{run_id_map['dsoal']}"),
        4: (SOFT_OAL_LINE_FILTER, f"https://github.com/kcat/openal-soft/actions/runs/{run_id_map['soft_oal']}"),
        5: (OPENAL_SOFT_LINE_FILTER, f"https://github.com/kcat/openal-soft/actions/runs/{run_id_map['openal_soft']}")
    }

    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line_number, (prefix, new_url) in line_filters.items():
        idx = line_number - 1
        if 0 <= idx < len(lines):
            original_line = lines[idx]

            if prefix in original_line:
                after_part = ""
                match = re.search(rf"({re.escape(prefix)})(.*?)(<p>|$)", original_line)
                if match:
                    after_part = match.group(3) if match.group(3) else ""

                new_line = f"{prefix}{new_url} {after_part}".rstrip() + '\n'
                lines[idx] = new_line

                diff_old, diff_new = highlight_diff(original_line.rstrip(), new_line.rstrip())

                print(f"\n{Fore.CYAN}Updating line {line_number}:{Style.RESET_ALL}")
                print(f"  {Fore.RED}- BEFORE:{Style.RESET_ALL} {diff_old}")
                print(f"  {Fore.GREEN}+ AFTER :{Style.RESET_ALL} {diff_new}")

    with open(file_name, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("")
    print(
        "Updated README.md with new run IDs: " +
        ", ".join(f"{key}: {Fore.YELLOW}{run_id}{Style.RESET_ALL}" for key, run_id in run_id_map.items())
    )

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
                print("")
                if run_id:
                    run_id_map[run_key] = str(run_id)
                else:
                    print(f"{Fore.RED}Warning: run_id is None or empty for {label}{Style.RESET_ALL}")

        update_readme(run_id_map)

if __name__ == "__main__":
    asyncio.run(main())
    print("")
    input("Press Enter to exit...")
