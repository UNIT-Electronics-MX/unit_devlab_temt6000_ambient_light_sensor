#!/bin/bash

# Build the static hardware documentation site.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is required." >&2
    exit 1
fi

python3 .github/scripts/copy_hardware_docs.py

if [[ ! -s docs/index.html || ! -s docs/hardware/index.html ]]; then
    echo "Error: documentation output was not generated." >&2
    exit 1
fi

shopt -s nullglob
product_reference_pdfs=(build/product-reference/*.pdf)
if [[ "${#product_reference_pdfs[@]}" -eq 0 ]]; then
    echo "Error: no generated product-reference PDF was found." >&2
    exit 1
fi

for source_pdf in "${product_reference_pdfs[@]}"; do
    published_pdf="docs/hardware/$(basename "$source_pdf")"
    if [[ ! -s "$published_pdf" ]]; then
        echo "Error: generated product reference was not published: $published_pdf" >&2
        exit 1
    fi
done

echo "Hardware documentation built successfully."
echo "Open docs/hardware/index.html in a browser to review it."
