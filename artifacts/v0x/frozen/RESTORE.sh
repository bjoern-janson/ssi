#!/usr/bin/env bash
set -euo pipefail

here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"

archive="v0x_frozen_artifacts.tar.xz"
b64="${archive}.b64"

cat \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-00 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-01 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-02 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-03 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-04 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-05 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-06 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-07 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-08 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-09 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-10a \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-10b \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-10c \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-10d \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-11 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-12 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-13 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-14 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-15 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-16 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-17 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-18 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-19 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-20 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-21 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-22 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-23 \
  transport/v0x_frozen_artifacts.tar.xz.b64.part-24 \
  > "$b64"

base64 --decode "$b64" > "$archive"
printf '%s  %s\n' \
  '9fc212811ff8b98e385e490a46145dbe995a8f7931e8c64854342f4af8dc2ca9' \
  "$archive" | sha256sum -c -

rm -rf restored
mkdir restored
tar -xJf "$archive" -C restored

if [[ -f restored/generative_probe_benchmark_v0_1.py ]]; then
  (cd restored && sha256sum -c ../SHA256SUMS.recovered)
else
  mapfile -t roots < <(find restored -mindepth 1 -maxdepth 1 -type d -print)
  if [[ ${#roots[@]} -ne 1 ]]; then
    echo 'Unexpected archive layout; refusing to guess verification root.' >&2
    exit 1
  fi
  (cd "${roots[0]}" && sha256sum -c ../../SHA256SUMS.recovered)
fi

echo 'Recovered V0.x payload verified: 25/25 present recovered files match the frozen checksum ledger.'
echo 'Manifest-listed v0_8_evidence_to_authority_scientific_runner.py remains intentionally absent; it was not reconstructed.'
