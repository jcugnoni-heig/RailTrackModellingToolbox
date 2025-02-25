#!/bin/bash

echo "Scanning for .tmplt files to restore..."

# Recherche tous les fichiers avec l'extension .tmplt
find . -type f -name "*.tmplt" | while IFS= read -r tmplt_file; do
    # Retire l'extension .tmplt pour obtenir le nom du fichier original
    original_file="${tmplt_file%.tmplt}"

    # Si le fichier original existe, le supprimer
    if [ -f "$original_file" ]; then
        echo "Deleting original file: $original_file"
        rm "$original_file"
    else
        echo "Original file $original_file does not exist."
    fi

    # Renomme le fichier .tmplt en fichier original
    echo "Renaming $tmplt_file to $original_file"
    mv "$tmplt_file" "$original_file"
done

echo "Restoration complete."
