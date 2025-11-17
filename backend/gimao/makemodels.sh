#!/bin/sh

INPUT_FILE="models.py"
OUTPUT_DIR="models"

# Créer dossier s'il n'existe pas
mkdir -p "$OUTPUT_DIR"

# Extraire les noms de classes du fichier
grep -E "^class [A-Za-z0-9_]+\(" "$INPUT_FILE" | while read -r line; do

    # Récupérer le nom du modèle
    class_name=$(echo "$line" | sed -n 's/class \([A-Za-z0-9_]\+\).*/\1/p')

    # Nom du fichier en snake_case
    file_name=$(echo "$class_name" | sed -r 's/([A-Z])/_\L\1/g' | sed 's/^_//').py

    file_path="$OUTPUT_DIR/$file_name"

    # Créer fichier avec squelette
    echo "from django.db import models" > "$file_path"
    echo "" >> "$file_path"
    echo "class $class_name(models.Model):" >> "$file_path"
    echo "    pass" >> "$file_path"

    echo "Créé : $file_path"

done

echo "Terminé."
