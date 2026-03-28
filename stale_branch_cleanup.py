#!/usr/bin/env python3
"""
Stale Branch Cleanup CLI

Finds local git branches that have been merged into the main branch
and offers to delete them.
"""
import subprocess
import argparse
import sys

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()

def get_default_branch():
    # Attempt to find the default branch from remote
    try:
        remote_info = run_cmd("git remote show origin")
        for line in remote_info.split('\n'):
            if "HEAD branch:" in line:
                return line.split(":")[1].strip()
    except Exception:
        pass
    return "main"

def get_merged_branches(target_branch):
    stdout = run_cmd(f"git branch --merged {target_branch}")
    branches = []
    for line in stdout.split('\n'):
        line = line.strip()
        if not line or line.startswith('*'):
            continue
        if line == target_branch:
            continue
        branches.append(line)
    return branches

def main():
    parser = argparse.ArgumentParser(description="Clean up merged local branches.")
    parser.add_argument("-y", "--yes", action="store_true", help="Non-interactive deletion of branches.")
    parser.add_argument("-b", "--branch", help="Target branch to compare against (default: auto-detected, usually main).")
    args = parser.parse_args()

    try:
        run_cmd("git rev-parse --is-inside-work-tree")
    except RuntimeError:
        print("Error: Not inside a git repository", file=sys.stderr)
        sys.exit(1)

    default_branch = args.branch or get_default_branch()
    print(f"Target branch: {default_branch}")

    try:
        merged_branches = get_merged_branches(default_branch)
    except RuntimeError as e:
        print(f"Error fetching branches: {e}", file=sys.stderr)
        sys.exit(1)

    if not merged_branches:
        print("No merged branches to clean up.")
        return

    print("The following local branches have been merged:")
    for b in merged_branches:
        print(f" - {b}")

    if args.yes:
        confirm = "y"
    else:
        try:
            confirm = input("Delete these branches? (y/N): ").strip().lower()
        except EOFError:
            confirm = "n"

    if confirm == 'y':
        for b in merged_branches:
            try:
                run_cmd(f"git branch -d {b}")
                print(f"Deleted branch: {b}")
            except RuntimeError as e:
                print(f"Failed to delete {b}: {e}", file=sys.stderr)
    else:
        print("Aborted.")

if __name__ == "__main__":
    main()
