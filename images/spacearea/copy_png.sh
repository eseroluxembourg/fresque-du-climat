#!/bin/bash

# Traverse all subdirectories
find . -type f -name "en-GB.png" | while read -r file; do
    # Get the directory of the PNG file
    dir=$(dirname "$file")
    
    # Define the target file path
    target="$dir/de-DE.png"
    
    # Check if fr-FR.png already exists to avoid overwriting
    if [[ ! -f "$target" ]]; then
        # Copy the PNG file to fr-FR.png in the same directory
        cp "$file" "$target"
        echo "Copied $file to $target"
    else
        echo "File $target already exists. Skipping..."
    fi
done
