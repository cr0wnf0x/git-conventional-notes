#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from datetime import datetime
import re

def run_command(command):
    """Executes a shell command and returns its output, handling errors."""
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def get_last_commit_from_changelog(changelog_path):
    """Reads the changelog to find the most recent commit hash."""
    if not os.path.exists(changelog_path):
        return None
    with open(changelog_path, 'r') as f:
        for line in f:
            match = re.search(r"Changes up to commit ([0-9a-fA-F]{7,40})", line)
            if match:
                return match.group(1)
    return None

def parse_commits(start_commit, end_commit, repo_url):
    """Parses git log and returns categorized commits."""
    log_format = "%h%x00%H%x00%s%x00%b%x00%an%x01"
    command = ["git", "log", f"--pretty=format:{log_format}", f"{start_commit}...{end_commit}"]
    raw_log = run_command(command)
    categorized = { "feat": [], "fix": [], "docs": [], "style": [], "refactor": [], "perf": [], "test": [], "build": [], "ci": [], "chore": [], "misc": [] }
    breaking_changes = []
    for commit_str in raw_log.split('\x01'):
        if not commit_str.strip(): continue
        fields = commit_str.strip().split('\x00')
        if len(fields) < 5: continue
        short_hash, full_hash, subject, body, author = fields
        commit_id = f"({short_hash})"
        if repo_url:
            clean_repo_url = repo_url.rstrip('/')
            commit_id = f"([{short_hash}]({clean_repo_url}/commit/{full_hash}))"
        match = re.match(r"^([a-zA-Z]+)(\(.*\))?(!)?: (.*)$", subject)
        formatted_commit = f"* {subject} {commit_id} by {author}"
        is_breaking = "BREAKING CHANGE:" in body
        if match:
            type, scope, is_breaking_subject, description = match.groups()
            scope_str = f"**{scope}** " if scope else ""
            formatted_commit = f"* {scope_str}{description} {commit_id} by {author}"
            if type == "upd": type = "refactor"
            if type in categorized: categorized[type].append(formatted_commit)
            else: categorized["misc"].append(formatted_commit)
            if is_breaking_subject: is_breaking = True
        else:
            categorized["misc"].append(formatted_commit)
        if is_breaking:
            breaking_changes.append(formatted_commit)
    return categorized, breaking_changes

def generate_markdown(categorized, breaking_changes):
    """Generates the markdown content for the notes."""
    content = []
    headers = {
        "feat": "## ✨ Features", "fix": "## 🐛 Bug Fixes", "docs": "## 📚 Documentation", "style": "## 💅 Styles",
        "refactor": "## 🔨 Refactoring", "perf": "## 🚀 Performance Improvements", "test": "## ✅ Testing",
        "build": "## 📦 Build System", "ci": "## 🤖 Continuous Integration", "chore": "## 🧹 Chores", "misc": "## 📄 Miscellaneous"
    }
    if breaking_changes:
        content.append("## 💥 BREAKING CHANGES")
        content.extend(breaking_changes)
    for type, header in headers.items():
        if categorized[type]:
            content.append(f"\n{header}")
            content.extend(categorized[type])
    return "\n".join(content)

def main():
    parser = argparse.ArgumentParser(description="Generate release notes or update a changelog from Conventional Commits.")
    parser.add_argument("--version", help="Generate notes for a specific version/tag.")
    parser.add_argument("--start-ref", help="Generate notes for a specific commit range.")
    parser.add_argument("--end-ref", help="Generate notes for a specific commit range.")
    parser.add_argument("--output", help="Output to a specific file (Release Notes mode). If omitted, updates CHANGELOG.md.")
    parser.add_argument("--repo-url", help="The base URL of the repository for creating commit links.")
    parser.add_argument("--full-history", action="store_true", help="On first run, generate changelog for the entire project history.")
    args = parser.parse_args()

    changelog_mode = not args.output
    output_file = "CHANGELOG.md" if changelog_mode else args.output

    print("Determining commit range...")
    start_commit, end_commit, release_title = "", "HEAD", ""

    if not changelog_mode:
        if args.version:
            end_commit = args.version
            release_title = f"Version {args.version}"
            start_commit = run_command(["git", "describe", "--abbrev=0", "--tags", f"{args.version}^" ]) or run_command(["git", "rev-list", "--max-parents=0", "HEAD"])
        elif args.start_ref and args.end_ref:
            start_commit, end_commit = args.start_ref, args.end_ref
            release_title = f"Changes from {start_commit} to {end_commit}"
        else:
            current_branch = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
            upstream_branch = run_command(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
            if not upstream_branch:
                print(f"Error: The current branch '{current_branch}' does not have a remote tracking branch.", file=sys.stderr)
                sys.exit(1)
            start_commit, end_commit = upstream_branch, "HEAD"
            release_title = f"Unreleased Changes for Branch '{current_branch}'"
    else: # Changelog Mode
        print("Mode: Updating CHANGELOG.md")
        start_commit = get_last_commit_from_changelog(output_file)
        if not start_commit:
            if args.full_history:
                print("No previous commit found. Initializing with full project history as requested.")
                start_commit = run_command(["git", "rev-list", "--max-parents=0", "HEAD"])
            else:
                print("No previous commit found. Initializing from last tag or latest commit.")
                start_commit = run_command(["git", "describe", "--tags", "--abbrev=0"]) or run_command(["git", "rev-parse", "HEAD~1"])

    print(f"Range: {start_commit}...{end_commit}")
    commit_count_str = run_command(["git", "rev-list", "--count", f"{start_commit}...{end_commit}"])
    if not commit_count_str or int(commit_count_str) == 0:
        print(f"Warning: No new commits found since {start_commit}. Nothing to do.")
        sys.exit(0)

    print("Parsing commits and generating content...")
    categorized, breaking_changes = parse_commits(start_commit, end_commit, args.repo_url)
    new_content = generate_markdown(categorized, breaking_changes)

    if changelog_mode:
        print(f"Updating {output_file}...")
        latest_commit_hash = run_command(["git", "rev-parse", "--short", end_commit])
        dt = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        header = f"---\n### *Changes up to commit {latest_commit_hash} ({dt})*\n---"
        old_content = ""
        if os.path.exists(output_file):
            with open(output_file, 'r') as f: old_content = "".join(f.readlines()[1:])
        full_content = f"# Changelog\n\n{header}\n{new_content}\n{old_content}"
        with open(output_file, 'w') as f: f.write(full_content)
        print(f"Done. {output_file} has been updated.")
    else:
        print(f"Generating release notes at {output_file}...")
        with open(output_file, 'w') as f: f.write(f"# {release_title}\n\n{new_content}\n")
        print("Done.")

if __name__ == "__main__":
    main()