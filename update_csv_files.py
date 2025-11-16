#!/usr/bin/env python3
"""
Script to replace all individual CSV files with the consolidated, deduplicated data.
"""

import csv
import os
import shutil
from datetime import datetime

def backup_original_files(directory):
    """Create backups of original CSV files."""
    backup_dir = os.path.join(directory, f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    os.makedirs(backup_dir, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.endswith('.csv') and filename != 'consolidated_ideas.csv':
            src = os.path.join(directory, filename)
            dst = os.path.join(backup_dir, filename)
            shutil.copy2(src, dst)
            print(f"Backed up: {filename}")

    return backup_dir

def read_consolidated_ideas(filepath):
    """Read the consolidated ideas."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def update_csv_file(filepath, consolidated_ideas):
    """Update a CSV file with consolidated ideas."""
    fieldnames = ['Number', 'Idea', 'Score', 'Free_Value_Prop', 'Paid_Value_Prop', 'Why_This_Score', 'LLM_Source']

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in consolidated_ideas:
            writer.writerow(row)

def main():
    directory = '/home/user/BI/Gen Era Business'
    consolidated_file = os.path.join(directory, 'consolidated_ideas.csv')

    print("=== Updating CSV Files with Consolidated Data ===\n")

    # Backup original files
    print("Step 1: Backing up original files...")
    backup_dir = backup_original_files(directory)
    print(f"Backups created in: {backup_dir}\n")

    # Read consolidated ideas
    print("Step 2: Reading consolidated ideas...")
    consolidated_ideas = read_consolidated_ideas(consolidated_file)
    print(f"Loaded {len(consolidated_ideas)} unique ideas\n")

    # Update each CSV file
    print("Step 3: Updating individual CSV files...")
    updated_count = 0
    for filename in os.listdir(directory):
        if filename.endswith('.csv') and filename != 'consolidated_ideas.csv' and not filename.startswith('backup_'):
            filepath = os.path.join(directory, filename)
            update_csv_file(filepath, consolidated_ideas)
            print(f"Updated: {filename}")
            updated_count += 1

    print(f"\n=== Summary ===")
    print(f"Updated {updated_count} CSV files")
    print(f"Each file now contains {len(consolidated_ideas)} unique, deduplicated ideas")
    print(f"Original files backed up to: {backup_dir}")

if __name__ == '__main__':
    main()
