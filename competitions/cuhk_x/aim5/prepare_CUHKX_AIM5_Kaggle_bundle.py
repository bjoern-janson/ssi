#!/usr/bin/env python3
"""Build the private input bundle for frozen CUHK-X AIM5.

Run from a working directory containing the exact frozen derived artifacts plus
copies of the frozen AIM4 helper and AIM5 executable from the SSI branch.
The organizer Training ZIP is intentionally excluded and attached separately.
"""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path.cwd()
OUT = ROOT / "cuhkx_aim5_private_inputs.zip"

FILES = {
    "cuhkx_submission1.py": ROOT / "cuhkx_submission1.py",
    "cuhkx_v7_ir_dinov2_cache/features.npz": ROOT / "cuhkx_v7_ir_dinov2_cache" / "features.npz",
    "cuhkx_b2_hau_pose_cache/features.npz": ROOT / "cuhkx_b2_hau_pose_cache" / "features.npz",
    "cuhkx_b4_imu_v2_cache/features.npz": ROOT / "cuhkx_b4_imu_v2_cache" / "features.npz",
    "cuhkx_v7_strong_ir_dinov2_results.zip": ROOT / "cuhkx_v7_strong_ir_dinov2_results.zip",
    "cuhkx_aim4_structured_set.py": ROOT / "cuhkx_aim4_structured_set.py",
    "cuhkx_aim5_conditional_setmap.py": ROOT / "cuhkx_aim5_conditional_setmap.py",
}

EXPECTED = {
    "cuhkx_submission1.py": "38152a54acde3e5241a15ab03d364e8f08164b7ae81ece86738ae45ebe2e594f",
    "cuhkx_v7_ir_dinov2_cache/features.npz": "e9699696af7d886896df7fa1e52d2b28ecfbb8abeef71a6b3b2ee04a68abb5db",
    "cuhkx_b2_hau_pose_cache/features.npz": "d7e609a5e8a9ebc4bbdda92f8fe601d8b0c6ccfd4a2757f9a632a1ac9211b89a",
    "cuhkx_b4_imu_v2_cache/features.npz": "8c4656e2c76029783c18d0b76f92f58fa8165a786a7049c3be7bf90a28aa0234",
    "cuhkx_v7_strong_ir_dinov2_results.zip": "af7687fad3c7a4d140707c09dd84edea79288abdd81f91e9755d21cb63aad088",
    "cuhkx_aim4_structured_set.py": "ba2ebfd73e9dfa3c7f0e597e9f24691551fd4d844e8a3c8049fe7c44c91eb1c5",
    "cuhkx_aim5_conditional_setmap.py": "620e35da4256e3368359e202729e45489b916687ef890e3f9d887e91f11a0605",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


manifest = {}
print("Checking frozen AIM5 private inputs...")
for arcname, src in FILES.items():
    if not src.exists():
        raise FileNotFoundError(src)
    got = sha256_file(src)
    exp = EXPECTED[arcname]
    if got != exp:
        raise RuntimeError(f"SHA mismatch for {arcname}: {got} != {exp}")
    manifest[arcname] = got
    print("  PASS", arcname, got)

if OUT.exists():
    OUT.unlink()

with zipfile.ZipFile(
    OUT,
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=6,
    allowZip64=True,
) as z:
    for arcname, src in FILES.items():
        if "\\" in arcname:
            raise RuntimeError(f"forbidden archive separator: {arcname}")
        z.write(src, arcname=arcname)
    z.writestr("bundle_manifest.json", json.dumps(manifest, indent=2, sort_keys=True))

with zipfile.ZipFile(OUT) as z:
    bad = [n for n in z.namelist() if "\\" in n]
    if bad:
        raise RuntimeError(f"forbidden backslash entries remain: {bad}")

print()
print("DONE")
print("PRIVATE_BUNDLE =", OUT)
print("SHA256 =", sha256_file(OUT))
print("Attach this private bundle plus the official Training ZIP in Kaggle.")
