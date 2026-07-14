#!/usr/bin/env bash
# install-git-hooks.sh — copy scripts/hooks/* into .git/hooks/ and make
# them executable. Idempotent (safe to re-run). Prompts before overwriting
# an existing hook that isn't identical to the source.
#
# Usage:
#   ./scripts/install-git-hooks.sh          # interactive
#   ./scripts/install-git-hooks.sh --force  # overwrite without prompting

set -eu

repo_root="$(git rev-parse --show-toplevel)"
src_dir="${repo_root}/scripts/hooks"
dst_dir="${repo_root}/.git/hooks"

if [ ! -d "${src_dir}" ]; then
  echo "ERROR: ${src_dir} does not exist. Are you in the plugin repo root?" >&2
  exit 1
fi

force=0
if [ "${1:-}" = "--force" ]; then
  force=1
fi

installed=0
skipped=0

for src in "${src_dir}"/*; do
  [ -f "${src}" ] || continue
  name="$(basename "${src}")"
  dst="${dst_dir}/${name}"

  if [ -f "${dst}" ]; then
    if cmp -s "${src}" "${dst}"; then
      skipped=$((skipped + 1))
      continue
    fi
    if [ "${force}" -eq 0 ]; then
      echo "Hook ${name} exists at ${dst} and differs from source."
      read -r -p "Overwrite? [y/N] " reply
      case "${reply}" in
        y|Y|yes|YES) ;;
        *) echo "  skipped ${name}"; skipped=$((skipped + 1)); continue ;;
      esac
    fi
  fi

  cp "${src}" "${dst}"
  chmod +x "${dst}"
  echo "  installed ${name}"
  installed=$((installed + 1))
done

echo ""
echo "Done: ${installed} hook(s) installed, ${skipped} skipped/unchanged."
