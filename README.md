# Git Changelog & Release Notes Generator

A flexible, zero-dependency script for generating beautiful changelogs and release notes from your Conventional Commit history.

This tool analyzes your Git history and automatically produces structured, human-readable Markdown, perfect for maintaining a project changelog or creating release-specific notes.

## Features

- **Automatic `CHANGELOG.md` Mode:** Intelligently creates and prepends to a `CHANGELOG.md` file, using the changelog itself as the source of truth to prevent duplicate entries.
- **Standalone Release Notes Mode:** Generate notes for a specific version, branch, or commit range into a separate file.
- **Smart Initialization:** Avoids dumping the entire project history on the first run by default; starts from the most recent tag for a clean, concise changelog.
- **Conventional Commit Parsing:** Automatically categorizes commits into sections like `Features`, `Bug Fixes`, etc., complete with fitting emojis.
- **Graceful Fallback:** Commits that don't follow the conventional standard are neatly collected under a "Miscellaneous" section.
- **Automatic Linking:** Automatically links commits to your web repository (GitHub, GitLab, Azure DevOps, etc.) when a URL is provided.
- **Portable & Zero-Dependency:** The script is self-contained and can be run on any Git repository, requiring only Git and Python 3.

## Prerequisites

- Git
- Python 3.6+

## Usage

The main script is located at `scripts/generate-notes.sh`. It should be run from the root of the Git repository you wish to analyze.

### Changelog Mode (Default)

This is the primary mode for maintaining a `CHANGELOG.md` file in your repository.

**To update the changelog:**

Simply run the script with no arguments.

```bash
./scripts/generate-notes.sh
```

On its first run, it will create a `CHANGELOG.md` starting from the most recent tag. On subsequent runs, it will read the changelog to find the last commit it recorded and will add only the new commits since that point.

**To initialize a changelog with the *entire* project history:**

If you want to generate a complete changelog for an existing project, delete the current `CHANGELOG.md` (if it exists) and run the script with the `--full-history` flag.

```bash
# Make sure CHANGELOG.md does not exist
rm CHANGELOG.md

# Run with the full history flag
./scripts/generate-notes.sh --full-history
```

### Release Notes Mode

This mode is for generating a standalone file for a specific purpose, without modifying the project's main `CHANGELOG.md`. To use this mode, you must provide the `--output` flag.

**To generate notes for unpushed commits on your current branch:**

```bash
./scripts/generate-notes.sh --output my-unpushed-changes.md
```

**To generate notes for a specific version tag:**

This will create a file containing all changes between the specified tag and the tag that came before it.

```bash
./scripts/generate-notes.sh --version v1.2.3 --output release-v1.2.3.md --repo-url "https://github.com/user/repo"
```

**To generate notes for an arbitrary commit range:**

```bash
./scripts/generate-notes.sh --start-ref main --end-ref develop --output changes-for-develop.md
```

### All Options

| Flag | Description |
| :--- | :--- |
| `--output <file>` | Activates "Release Notes" mode and directs all output to the specified file. |
| `--repo-url <url>` | The base URL of your repository. Used to create clickable links for each commit hash. |
| `--version <tag>` | (Release Notes Mode) Generates notes for the specified version tag. |
| `--start-ref <ref>` | (Release Notes Mode) Specifies the starting commit, tag, or branch for the range. |
| `--end-ref <ref>` | (Release Notes Mode) Specifies the ending commit, tag, or branch for the range. |
| `--full-history` | (Changelog Mode) On the very first run, forces the script to generate a changelog for the entire project history instead of using its smart default. |