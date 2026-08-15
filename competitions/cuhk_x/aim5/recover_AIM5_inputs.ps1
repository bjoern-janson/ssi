param(
    [Parameter(Mandatory=$false)]
    [string[]]$Roots = @("$HOME\Downloads", "$HOME\Documents", "$HOME\Desktop"),

    [Parameter(Mandatory=$false)]
    [string]$OutDir = "$HOME\Desktop\CUHKX_AIM5_RECOVERED"
)

$ErrorActionPreference = "Stop"

$targets = @(
    @{ Name = "Training-20260813T154030Z-1-002.zip"; Sha256 = "667a00cb03ec67e1eeb49a744cb4fc764878fadae0b35ea873e25c2f7b3868bc"; Rel = "Training-20260813T154030Z-1-002.zip" },
    @{ Name = "features.npz"; Sha256 = "e9699696af7d886896df7fa1e52d2b28ecfbb8abeef71a6b3b2ee04a68abb5db"; Rel = "cuhkx_v7_ir_dinov2_cache\features.npz" },
    @{ Name = "features.npz"; Sha256 = "d7e609a5e8a9ebc4bbdda92f8fe601d8b0c6ccfd4a2757f9a632a1ac9211b89a"; Rel = "cuhkx_b2_hau_pose_cache\features.npz" },
    @{ Name = "features.npz"; Sha256 = "8c4656e2c76029783c18d0b76f92f58fa8165a786a7049c3be7bf90a28aa0234"; Rel = "cuhkx_b4_imu_v2_cache\features.npz" }
)

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$remaining = @{}
foreach ($t in $targets) { $remaining[$t.Sha256] = $t }

Write-Host "AIM5 exact-byte recovery"
Write-Host "Output: $OutDir"
Write-Host "Roots: $($Roots -join ', ')"
Write-Host ""

foreach ($root in $Roots) {
    if ($remaining.Count -eq 0) { break }
    if (-not (Test-Path $root)) {
        Write-Host "SKIP missing root: $root"
        continue
    }

    Write-Host "Scanning $root ..."

    # Restrict by filenames to avoid hashing every file on disk.
    $candidates = Get-ChildItem -Path $root -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -eq "features.npz" -or $_.Name -eq "Training-20260813T154030Z-1-002.zip" }

    foreach ($f in $candidates) {
        if ($remaining.Count -eq 0) { break }
        try {
            $sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $f.FullName).Hash.ToLowerInvariant()
        } catch {
            Write-Host "WARN hash failed: $($f.FullName)"
            continue
        }

        if ($remaining.ContainsKey($sha)) {
            $t = $remaining[$sha]
            $dest = Join-Path $OutDir $t.Rel
            New-Item -ItemType Directory -Force -Path (Split-Path $dest -Parent) | Out-Null
            Copy-Item -LiteralPath $f.FullName -Destination $dest -Force
            Write-Host "FOUND $($t.Rel)"
            Write-Host "  source: $($f.FullName)"
            Write-Host "  sha256: $sha"
            $remaining.Remove($sha)
        }
    }
}

Write-Host ""
if ($remaining.Count -eq 0) {
    Write-Host "RECOVERY = COMPLETE"
    Write-Host "All four frozen AIM5 inputs were recovered byte-identically."
    exit 0
}

Write-Host "RECOVERY = INCOMPLETE"
Write-Host "Missing frozen objects:"
foreach ($kv in $remaining.GetEnumerator()) {
    Write-Host "  $($kv.Value.Rel)"
    Write-Host "    sha256: $($kv.Key)"
}
Write-Host ""
Write-Host "Re-run with additional roots, e.g.:"
Write-Host '  .\recover_AIM5_inputs.ps1 -Roots @("C:\", "D:\", "E:\")'
exit 2
