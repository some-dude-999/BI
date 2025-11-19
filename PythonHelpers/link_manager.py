#!/usr/bin/env python3
"""
Link Manager - Automated GitHub Pages URL Generator
Automatically finds all .html files and updates LINK.txt with GitHub Pages URLs
"""

import os
import subprocess
import urllib.parse
from pathlib import Path


def get_repo_info():
    """Get repository owner and name from git remote"""
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()

        # Parse GitHub URL (handles both HTTPS, SSH, and local proxy formats)
        # Examples:
        # https://github.com/owner/repo.git
        # git@github.com:owner/repo.git
        # http://local_proxy@127.0.0.1:34216/git/owner/repo
        if 'github.com' in remote_url:
            if remote_url.startswith('git@'):
                # SSH format: git@github.com:owner/repo.git
                parts = remote_url.split(':')[1].replace('.git', '').split('/')
            else:
                # HTTPS format: https://github.com/owner/repo.git
                parts = remote_url.split('github.com/')[1].replace('.git', '').split('/')

            owner = parts[0]
            repo = parts[1]
            return owner, repo
        elif '/git/' in remote_url:
            # Local proxy format: http://local_proxy@127.0.0.1:34216/git/owner/repo
            parts = remote_url.split('/git/')[1].replace('.git', '').split('/')
            owner = parts[0]
            repo = parts[1]
            return owner, repo
        else:
            raise ValueError("Not a GitHub repository")

    except subprocess.CalledProcessError:
        print("Error: Unable to get git remote. Are you in a git repository?")
        return None, None
    except (IndexError, ValueError) as e:
        print(f"Error parsing git remote URL: {e}")
        return None, None


def find_html_files(root_dir='.'):
    """Find all .html files in the repository"""
    html_files = []
    root_path = Path(root_dir)

    for html_file in root_path.rglob('*.html'):
        # Convert to relative path from root
        relative_path = html_file.relative_to(root_path)
        html_files.append(str(relative_path))

    # Sort for consistent ordering
    html_files.sort()
    return html_files


def load_existing_descriptions(link_file='LINK.txt'):
    """Load existing descriptions from LINK.txt"""
    descriptions = {}

    if not os.path.exists(link_file):
        return descriptions

    try:
        with open(link_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            # Look for lines with format: URL - Description
            if ' - ' in line and line.startswith('http'):
                parts = line.split(' - ', 1)
                url = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ''

                # Extract filename from URL for matching
                if '/' in url:
                    # Decode URL encoding to match filenames
                    decoded_url = urllib.parse.unquote(url)
                    filename = decoded_url.split('/')[-1]
                    descriptions[filename] = description

    except Exception as e:
        print(f"Warning: Could not read existing LINK.txt: {e}")

    return descriptions


def generate_github_pages_url(owner, repo, file_path):
    """Generate GitHub Pages URL for a file"""
    # URL encode the path (spaces become %20, etc.)
    encoded_path = urllib.parse.quote(file_path)

    base_url = f"https://{owner}.github.io/{repo}"
    full_url = f"{base_url}/{encoded_path}"

    return full_url


def update_link_file(owner, repo, html_files, link_file='LINK.txt'):
    """Update LINK.txt with all HTML file URLs"""

    # Load existing descriptions
    existing_descriptions = load_existing_descriptions(link_file)

    # Build new content
    lines = []
    lines.append("# GitHub Pages Links for HTML Files")
    lines.append("=" * 50)
    lines.append("")
    lines.append(f"Repository: {owner}/{repo}")
    lines.append(f"Base URL: https://{owner}.github.io/{repo}/")
    lines.append("")
    lines.append("HTML Files:")
    lines.append("-" * 50)
    lines.append("")

    for i, html_file in enumerate(html_files, 1):
        url = generate_github_pages_url(owner, repo, html_file)

        # Check for existing description
        filename = html_file.split('/')[-1]
        description = existing_descriptions.get(filename, f"[Add description for {filename}]")

        lines.append(f"{i}. {html_file}")
        lines.append(f"   {url} - {description}")
        lines.append("")

    # Write to file
    try:
        with open(link_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"✓ Successfully updated {link_file}")
        print(f"  Found {len(html_files)} HTML file(s)")
    except Exception as e:
        print(f"✗ Error writing to {link_file}: {e}")


def main():
    """Main execution function"""
    print("Link Manager - Automated GitHub Pages URL Generator")
    print("=" * 50)
    print()

    # Get repository information
    print("Getting repository information...")
    owner, repo = get_repo_info()

    if not owner or not repo:
        print("✗ Failed to get repository information")
        return 1

    print(f"✓ Repository: {owner}/{repo}")
    print()

    # Find all HTML files
    print("Finding HTML files...")
    html_files = find_html_files()

    if not html_files:
        print("✗ No HTML files found in repository")
        return 1

    print(f"✓ Found {len(html_files)} HTML file(s):")
    for html_file in html_files:
        print(f"  - {html_file}")
    print()

    # Update LINK.txt
    print("Updating LINK.txt...")
    update_link_file(owner, repo, html_files)
    print()

    print("=" * 50)
    print("Done! Please review LINK.txt and update descriptions as needed.")
    return 0


if __name__ == '__main__':
    exit(main())
