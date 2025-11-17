#!/bin/bash

# Vérifie qu'un argument est fourni
if [ $# -eq 0 ]; then
    echo "Usage: $0 <dossier>"
    exit 1
fi

DIR="$1"

# Vérifie que le dossier existe
if [ ! -d "$DIR" ]; then
    echo "Erreur : le dossier '$DIR' n'existe pas."
    exit 1
fi

# Fonction récursive pour afficher l'arborescence
function tree() {
    local prefix="$1"
    local folder="$2"

    # Liste des fichiers et dossiers, triés
    local entries=("$folder"/*)
    
    for entry in "${entries[@]}"; do
        local name=$(basename "$entry")
        if [ -d "$entry" ]; then
            echo "${prefix}├─ $name/"
            tree "│  $prefix" "$entry"
        else
            echo "${prefix}├─ $name"
        fi
    done
}

echo "$DIR"
tree "" "$DIR"
