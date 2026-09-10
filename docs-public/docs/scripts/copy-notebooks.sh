#!/usr/bin/env bash
# Quarto post-render step: copy the raw tutorial notebooks into the built site
# at /downloads/notebooks/ so the per-page "Download this notebook" buttons
# (see javascript/notebook-downloads.js) have real .ipynb files to serve.
#
# Quarto runs post-render scripts from the project directory and sets
# QUARTO_PROJECT_OUTPUT_DIR to the output directory (relative to the project).
set -eu

OUT="${QUARTO_PROJECT_OUTPUT_DIR:-_site}"
SRC="tutorials/notebooks"
DEST="${OUT}/downloads/notebooks"

mkdir -p "${DEST}"
cp "${SRC}"/*.ipynb "${DEST}/"
echo "copy-notebooks: copied $(ls "${SRC}"/*.ipynb | wc -l | tr -d ' ') notebooks to ${DEST}"
