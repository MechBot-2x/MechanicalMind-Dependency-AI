#!/bin/bash
cd "$(dirname "$0")/../docs/architecture/diagrams"
for f in *.mmd; do
    mmdc -i "$f" -o "${f%.*}.png"
done
