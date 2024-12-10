#!/bin/bash

# Check if the user provided two arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <source_directory> <target_directory>"
  exit 1
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"

# Check if the source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: Source directory '$SOURCE_DIR' does not exist."
  exit 1
fi

# Find and copy index.md files while preserving the directory structure
find "$SOURCE_DIR" -type f -name "index.md" | while read -r file; do
  # Get the relative path of the file from the source directory
  REL_PATH="${file#$SOURCE_DIR/}"
  
  # Create the same directory structure in the target directory
  #mkdir -p "$TARGET_DIR/$(dirname "$REL_PATH")"
  
  # Copy the file to the target directory
  cp "$file" "$TARGET_DIR/$REL_PATH"
done

echo "All index.md files have been copied from '$SOURCE_DIR' to '$TARGET_DIR'."
