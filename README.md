# Stale Branch Cleanup

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight CLI tool to identify and clean up fully merged local git branches. It safely checks against your repository's default branch.

## Features
- **Git Native**: Relies entirely on `git branch --merged` for safety.
- **Interactive Mode**: Prompts before deleting any branches.
- **Auto-Detection**: Automatically identifies your default branch (`main` / `master`) from the `origin` remote.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/gbvk312/stale-branch-cleanup.git
   ```
2. Navigate into the directory:
   ```bash
   cd stale-branch-cleanup
   ```
3. Make the tool executable:
   ```bash
   chmod +x stale_branch_cleanup.py
   ```
   *Tip: Add it to your `$PATH` for easy access from anywhere.*

## Usage
Simply run it in any git repository:
```bash
./stale_branch_cleanup.py
```

To automatically accept deletion without prompting:
```bash
./stale_branch_cleanup.py --yes
```

To compare against a specific target branch:
```bash
./stale_branch_cleanup.py --branch develop
```
