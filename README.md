# Conventional Commit Toolkit

A collection of zero-dependency scripts to help you work with Conventional Commits.

This toolkit provides an interactive script to guide you in creating compliant commits and a powerful generator for creating beautiful changelogs and release notes from your commit history.

## Scripts

### Interactive Commit (`scripts/conventional-commit.sh`)

An interactive script to guide you in creating commits that follow the Conventional Commits specification.

- **Stages All Changes:** Automatically stages all tracked changes before committing.
- **Interactive Prompts:** Guides you through selecting the commit type, scope, description, body, and breaking changes.
- **Specification Compliant:** Ensures your commit messages adhere to the Conventional Commits standard.
- **Zero-Dependency:** Runs anywhere with just Bash.

### Changelog & Notes Generator (`scripts/generate-notes.sh`)

A flexible script for generating beautiful changelog and release notes from your commit history.

- **Automatic `CHANGELOG.md` Mode:** Intelligently creates and prepends to a `CHANGELOG.md` file.
- **Standalone Release Notes Mode:** Generate notes for a specific version, branch, or commit range.
- **Smart Initialization:** Avoids dumping the entire project history on the first run by default.
- **Conventional Commit Parsing:** Automatically categorizes commits into sections like `Features`, `Bug Fixes`, etc.
- **Automatic Linking:** Links commits to your web repository (GitHub, GitLab, etc.).
- **Portable:** Requires only Git and Python 3.

## Prerequisites

- **For `conventional-commit.sh`:**
  - Bash
- **For `generate-notes.sh`:**
  - Git
  - Python 3.6+

## Usage

Both scripts should be run from the root of the Git repository.

### `scripts/conventional-commit.sh`

Run this script to start an interactive session that helps you build a Conventional Commit message.

```bash
./scripts/conventional-commit.sh
```

The script will guide you through the following steps:
1.  **Stage Changes:** Automatically stages all new and modified files.
2.  **Select Type:** Choose the commit type (e.g., `feat`, `fix`, `chore`).
3.  **Define Scope:** Optionally provide a scope for the change.
4.  **Write Description:** Enter a short, imperative description.
5.  **Add Body:** Provide a more detailed, optional body.
6.  **Mark Breaking Change:** Flag the commit as a breaking change if necessary and describe it.

### `scripts/generate-notes.sh`

This script generates changelogs or release notes. It has two main modes of operation.

#### Changelog Mode (Default)

This is the primary mode for maintaining a `CHANGELOG.md` file.

**To update the changelog:**

Simply run the script with no arguments. It will intelligently find the last commit recorded in `CHANGELOG.md` and append any new commits since.

```bash
./scripts/generate-notes.sh
```

**To initialize a changelog with the *entire* project history:**

```bash
# Ensure CHANGELOG.md does not exist
rm CHANGELOG.md

# Run with the --full-history flag
./scripts/generate-notes.sh --full-history
```

#### Release Notes Mode

This mode generates a standalone file without modifying `CHANGELOG.md`. It is activated by the `--output` flag.

**To generate notes for a specific version tag:**

```bash
./scripts/generate-notes.sh --version v1.2.3 --output release-v1.2.3.md --repo-url "https://github.com/user/repo"
```

**To generate notes for an arbitrary commit range:**

```bash
./scripts/generate-notes.sh --start-ref main --end-ref develop --output changes-for-develop.md
```

#### All Options

| Flag | Description |
| :--- | :--- |
| `--output <file>` | Activates "Release Notes" mode and directs all output to the specified file. |
| `--repo-url <url>` | The base URL of your repository. Used to create clickable links for each commit hash. |
| `--version <tag>` | (Release Notes Mode) Generates notes for the specified version tag. |
| `--start-ref <ref>` | (Release Notes Mode) Specifies the starting commit, tag, or branch for the range. |
| `--end-ref <ref>` | (Release Notes Mode) Specifies the ending commit, tag, or branch for the range. |
| `--full-history` | (Changelog Mode) On the very first run, forces the script to generate a changelog for the entire project history instead of using its smart default. |