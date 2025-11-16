#!/usr/bin/env python3
"""
Script to deduplicate similar ideas across multiple CSV files.
Consolidates ideas with the same or very similar names.
"""

import csv
import os
from collections import defaultdict
from difflib import SequenceMatcher

def normalize_idea_name(name):
    """Normalize idea name for comparison."""
    # Remove emoji and common prefixes
    name = name.replace('🚀', '').strip()
    name = name.lower()
    return name

def are_ideas_similar(name1, name2, threshold=0.85):
    """Check if two idea names are similar enough to be considered duplicates."""
    norm1 = normalize_idea_name(name1)
    norm2 = normalize_idea_name(name2)

    # Exact match after normalization
    if norm1 == norm2:
        return True

    # Check substring match (one is contained in the other)
    if norm1 in norm2 or norm2 in norm1:
        return True

    # Use sequence matcher for fuzzy matching
    ratio = SequenceMatcher(None, norm1, norm2).ratio()
    return ratio >= threshold

def read_csv_files(directory):
    """Read all CSV files from the directory."""
    csv_files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                csv_files[filename] = list(reader)
    return csv_files

def consolidate_ideas(csv_data):
    """Consolidate duplicate ideas across all CSV files."""
    # Group ideas by normalized name
    idea_groups = defaultdict(list)

    # First pass: collect all ideas
    for filename, rows in csv_data.items():
        for row in rows:
            if row.get('Idea'):
                idea_groups[row['Idea']].append({
                    'filename': filename,
                    'row': row
                })

    # Second pass: merge similar ideas
    consolidated = {}
    processed = set()

    idea_names = list(idea_groups.keys())
    for i, idea1 in enumerate(idea_names):
        if idea1 in processed:
            continue

        # Find all similar ideas
        similar_group = [idea1]
        for idea2 in idea_names[i+1:]:
            if idea2 not in processed and are_ideas_similar(idea1, idea2):
                similar_group.append(idea2)
                processed.add(idea2)

        processed.add(idea1)

        # Use the most common or shortest clean name
        canonical_name = min(similar_group, key=lambda x: (len(normalize_idea_name(x)), x))

        # Collect all instances
        all_instances = []
        for name in similar_group:
            all_instances.extend(idea_groups[name])

        # Consolidate the data
        scores = [float(inst['row']['Score']) for inst in all_instances if inst['row'].get('Score')]
        llm_sources = [inst['row']['LLM_Source'] for inst in all_instances if inst['row'].get('LLM_Source')]

        # Collect unique value props and explanations
        free_props = set()
        paid_props = set()
        why_scores = []

        for inst in all_instances:
            row = inst['row']
            if row.get('Free_Value_Prop'):
                free_props.add(row['Free_Value_Prop'].strip())
            if row.get('Paid_Value_Prop'):
                paid_props.add(row['Paid_Value_Prop'].strip())
            if row.get('Why_This_Score'):
                source = row.get('LLM_Source', 'Unknown')
                score = row.get('Score', 'N/A')
                why_scores.append(f"{source}: {score}\n{row['Why_This_Score']}")

        avg_score = sum(scores) / len(scores) if scores else 0

        consolidated[canonical_name] = {
            'Idea': canonical_name,
            'Score': round(avg_score, 1),
            'Free_Value_Prop': ' | '.join(sorted(free_props)) if free_props else '',
            'Paid_Value_Prop': ' | '.join(sorted(paid_props)) if paid_props else '',
            'Why_This_Score': f"{len(scores)} evals\n{'All: ' + str(round(avg_score, 1)) if len(scores) > 1 else ''}\n" +
                             (f"Used: {', '.join(str(s) for s in sorted(scores))}\n" if len(scores) > 1 else '') +
                             '\n---\n'.join(why_scores),
            'LLM_Source': f"Consolidated from: {', '.join(sorted(set(llm_sources)))}"
        }

    return consolidated

def write_consolidated_csv(consolidated_ideas, output_file):
    """Write consolidated ideas to a new CSV file."""
    fieldnames = ['Number', 'Idea', 'Score', 'Free_Value_Prop', 'Paid_Value_Prop', 'Why_This_Score', 'LLM_Source']

    # Sort by score descending
    sorted_ideas = sorted(consolidated_ideas.values(), key=lambda x: x['Score'], reverse=True)

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, idea in enumerate(sorted_ideas, 1):
            row = {'Number': i}
            row.update(idea)
            writer.writerow(row)

def main():
    directory = '/home/user/BI/Gen Era Business'

    print("Reading CSV files...")
    csv_data = read_csv_files(directory)
    print(f"Found {len(csv_data)} CSV files")

    print("\nConsolidating ideas...")
    consolidated = consolidate_ideas(csv_data)
    print(f"Consolidated to {len(consolidated)} unique ideas")

    print("\nWriting consolidated CSV...")
    output_file = os.path.join(directory, 'consolidated_ideas.csv')
    write_consolidated_csv(consolidated, output_file)
    print(f"Wrote consolidated ideas to {output_file}")

    # Print some statistics
    print("\n=== Consolidation Statistics ===")
    total_original = sum(len(rows) for rows in csv_data.values())
    print(f"Original total ideas (across all files): {total_original}")
    print(f"Unique ideas after consolidation: {len(consolidated)}")
    print(f"Duplicates removed: {total_original - len(consolidated)}")

    # Show top duplicated ideas
    print("\n=== Sample of Consolidated Ideas ===")
    for idea in sorted(consolidated.values(), key=lambda x: x['Score'], reverse=True)[:5]:
        num_evals = idea['Why_This_Score'].split('\n')[0]
        print(f"- {idea['Idea']}: {idea['Score']} ({num_evals})")

if __name__ == '__main__':
    main()
