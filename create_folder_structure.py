"""
Script to create folder structure based on JSON files in schemes/json directory.
Each JSON file becomes a subfolder with its name (without .json extension).
"""

import os
import json
from pathlib import Path

def create_folders_from_json_files(json_base_path: str, output_base_path: str) -> None:
    """
    Create folder structure based on JSON files found in json_base_path.
    
    Args:
        json_base_path: Path to the schemes/json directory
        output_base_path: Path where the folder structure will be created
    """
    json_base = Path(json_base_path)
    output_base = Path(output_base_path)
    
    if not json_base.exists():
        print(f"Error: JSON base path does not exist: {json_base}")
        return
    
    # Create output base directory if it doesn't exist
    output_base.mkdir(parents=True, exist_ok=True)
    
    # Find all JSON files
    json_files = sorted(json_base.rglob("*.json"))
    
    if not json_files:
        print(f"No JSON files found in {json_base}")
        return
    
    created_folders = []
    
    for json_file in json_files:
        # Get relative path from json_base to maintain category structure
        relative_path = json_file.relative_to(json_base)
        category = relative_path.parts[0]  # First directory (biocatalyst, components, etc.)
        file_name_without_ext = json_file.stem  # Filename without .json
        
        # Create output folder path
        output_folder = output_base / category / file_name_without_ext
        
        try:
            output_folder.mkdir(parents=True, exist_ok=True)
            created_folders.append(str(output_folder))
            print(f"✓ Created: {output_folder}")
        except Exception as e:
            print(f"✗ Error creating {output_folder}: {e}")
    
    print(f"\nTotal folders created: {len(created_folders)}")
    
    # Summary by category
    categories = {}
    for folder_path in created_folders:
        parts = Path(folder_path).parts
        if len(parts) > 0:
            category = parts[-2]  # Get category name
            categories[category] = categories.get(category, 0) + 1
    
    print("\nSummary by category:")
    for category in sorted(categories.keys()):
        print(f"  {category}: {categories[category]} folders")


if __name__ == "__main__":
    # Define paths
    current_dir = Path(__file__).parent
    json_base_path = current_dir / "schemes" / "json"
    output_base_path = current_dir / "generated_structure"
    
    print(f"Creating folder structure from JSON files...")
    print(f"Source: {json_base_path}")
    print(f"Output: {output_base_path}")
    print("-" * 60)
    
    create_folders_from_json_files(str(json_base_path), str(output_base_path))
