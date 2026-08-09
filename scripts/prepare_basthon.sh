#!/usr/bin/env bash
set -Eeuo pipefail

out="${1:-_build/html/basthon}"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# Known-good Basthon package used by the Norwegian site. This is only a
# bootstrap fallback: once this repository has a gh-pages branch, subsequent
# builds reuse their own previously deployed Basthon files.
reference_url="https://raw.githubusercontent.com/andreasdh/programmering-i-kjemi/master/vendor/basthon/basthon-console-custom.tgz"
reference_sha256="b257e4b5fab334eaa38df8cb4abe0542cc64003d575f65ce184a27d98fd27eda"

valid() {
  [[ -f "$1/index.html" ]] && [[ -d "$1/assets" ]] &&
    find "$1/assets" -maxdepth 1 -type f -name 'main.*.js' ! -name '*.map' -print -quit | grep -q .
}

install_dir() {
  rm -rf "$out"
  mkdir -p "$out"
  cp -a "$1/." "$out/"
}

from_pages() {
  echo "Trying Basthon from this repository's previous GitHub Pages deployment"
  mkdir -p "$tmp/pages"
  git fetch origin gh-pages --depth=1 || return 1
  git archive --format=tar origin/gh-pages basthon 2>/dev/null |
    tar -xf - -C "$tmp/pages" 2>/dev/null || return 1
  valid "$tmp/pages/basthon" || return 1
  install_dir "$tmp/pages/basthon"
}

from_reference_backup() {
  echo "Trying known-good Basthon bootstrap package"
  archive="$tmp/basthon-reference.tgz"
  curl --fail --location --silent --show-error \
    --retry 5 --retry-all-errors --retry-delay 5 \
    --connect-timeout 20 --max-time 240 \
    -o "$archive" "$reference_url" || return 1

  printf '%s  %s\n' "$reference_sha256" "$archive" | sha256sum -c - >/dev/null || return 1
  tar -tzf "$archive" >/dev/null || return 1
  mkdir -p "$tmp/reference"
  tar -xzf "$archive" -C "$tmp/reference"
  valid "$tmp/reference" || return 1
  install_dir "$tmp/reference"
}

from_download() {
  echo "Downloading Basthon from the official server"
  archive="$tmp/basthon-console.tgz"
  curl --fail --location --silent --show-error \
    --retry 5 --retry-all-errors --retry-delay 5 \
    --connect-timeout 20 --max-time 240 \
    -o "$archive" https://console.basthon.fr/basthon-console.tgz
  tar -tzf "$archive" >/dev/null
  mkdir -p "$tmp/download"
  tar -xzf "$archive" -C "$tmp/download"
  valid "$tmp/download"
  install_dir "$tmp/download"
}

mkdir -p "$out"
if from_pages; then
  source_name="this repository's gh-pages branch"
elif from_reference_backup; then
  source_name="known-good bootstrap package"
elif from_download; then
  source_name="official Basthon download"
else
  echo "Could not prepare Basthon from any source" >&2
  exit 1
fi

basthon_js=$(find "$out/assets" -maxdepth 1 -type f -name 'main.*.js' ! -name '*.map' -print -quit)
test -n "$basthon_js"
python "$root/scripts/customize_basthon.py" "$out/index.html" "$basthon_js"

examples=("$root"/docs/_static/basthon_examples/*.py)
[[ -e "${examples[0]}" ]] || { echo "No Basthon examples found" >&2; exit 1; }
rm -rf "$out/examples"
mkdir -p "$out/examples"
cp "${examples[@]}" "$out/examples/"

echo "Basthon ready from $source_name"
