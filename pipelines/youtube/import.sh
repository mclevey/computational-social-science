#!/bin/bash

TARGET_DIR="./_import_"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --source) shift; SOURCES+=("$@"); break ;;
        --target) TARGET_DIR="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$SOURCES" ]; then
    echo "No source files or directories provided."
    exit 1
fi

mkdir -p "$TARGET_DIR"

for src in "${SOURCES[@]}"; do
    if [ -e "$src" ]; then
        cp -r "$src" "$TARGET_DIR"
        echo "Copied $src to $TARGET_DIR"
    else
        echo "Source $src does not exist."
    fi
done

# e.g., `bash import.sh --source config.yaml <datasets> <whatever>`
