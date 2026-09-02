<#
publish.ps1 — one owner per file, everything else is a publish-copy.

    .\publish.ps1            # copy owner -> mirrors, then verify parity
    .\publish.ps1 -Check     # verify only; exit 1 on any drift (run before every commit/tag)

OWNERS (council ruling 2026-09-01, docs/council-2026-09-01-trm-audit/SYNTHESIS.md):
    SPINE.md, SPINE-WIRING.md, dispatch SKILL.md  -> this repo (the Deck)
    CREW.md, PROVENANCE.md, trm SKILL.md          -> team-rocket-method (the hub; its root IS the /trm drop-in)
    SHOW.md, trto SKILL.md                        -> team-rocket-takes-over

Local skill folders are directory junctions into the owner repos, so an edit in an owner repo is live
on this box immediately; this script keeps the PUBLIC mirrors honest. Failure mode: nobody runs it.
That is why -Check exists and why the version lines are printed on every run.
#>
param([switch]$Check)

$Deck = $PSScriptRoot
$Hub  = Join-Path (Split-Path $Deck) "team-rocket-method-public"
$Trto = Join-Path (Split-Path $Deck) "team-rocket-takes-over"

# owner -> list of mirrors
$Map = @(
    @{ src = "$Deck\SPINE.md";         dst = @("$Hub\SPINE.md", "$Trto\SPINE.md") }
    @{ src = "$Deck\SPINE-WIRING.md";  dst = @("$Hub\SPINE-WIRING.md", "$Trto\SPINE-WIRING.md") }
    @{ src = "$Deck\SKILL.md";         dst = @("$Hub\dispatch-SKILL.md") }
    @{ src = "$Hub\CREW.md";           dst = @("$Trto\CREW.md") }
    @{ src = "$Trto\SHOW.md";          dst = @("$Hub\SHOW.md") }
    @{ src = "$Trto\SKILL.md";         dst = @("$Hub\trto-SKILL.md") }
)

function Hash($p) { if (Test-Path $p) { (Get-FileHash $p -Algorithm SHA256).Hash } else { "MISSING" } }
function Norm($p) { (Get-Content $p -Raw) -replace "`r`n", "`n" }

$drift = 0
foreach ($e in $Map) {
    foreach ($d in $e.dst) {
        if (-not $Check) { Copy-Item $e.src $d -Force }
        $same = (Test-Path $d) -and ((Norm $e.src) -eq (Norm $d))
        $mark = if ($same) { "OK   " } else { $drift++; "DRIFT" }
        "{0}  {1,-48} -> {2}" -f $mark, ($e.src -replace [regex]::Escape((Split-Path $Deck)), "."), ($d -replace [regex]::Escape((Split-Path $Deck)), ".")
    }
}

""
"VERSION LINES"
foreach ($f in "$Deck\SPINE.md", "$Deck\SPINE-WIRING.md", "$Hub\CREW.md", "$Trto\SHOW.md") {
    $v = (Select-String -Path $f -Pattern '`([a-zA-Z/-]+ v[0-9.]+ \([0-9-]+\))`' | Select-Object -First 1).Matches[0].Groups[1].Value
    "  {0,-52} {1}" -f ($f -replace [regex]::Escape((Split-Path $Deck)), "."), $v
}

""
"INVARIANT BLOCK (must be one hash everywhere)"
$blocks = @{}
foreach ($f in "$Deck\SPINE.md", "$Deck\SKILL.md", "$Deck\CLAUDE.md", "$Hub\SKILL.md", "$Trto\SKILL.md") {
    $t = Norm $f
    if ($t -match '(?s)TRM INVARIANTS.*?and merges\.') {
        $h = [BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes($Matches[0]))).Replace("-", "").Substring(0, 12)
    } else { $h = "MISSING" }
    $blocks[$f] = $h
    "  {0,-52} {1}" -f ($f -replace [regex]::Escape((Split-Path $Deck)), "."), $h
}
if (($blocks.Values | Sort-Object -Unique).Count -ne 1) { $drift++; "  DRIFT: invariant blocks differ" }

""
if ($drift) { "PARITY: $drift problem(s)"; exit 1 } else { "PARITY: clean"; exit 0 }
