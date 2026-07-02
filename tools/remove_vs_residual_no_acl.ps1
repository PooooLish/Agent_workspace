$ErrorActionPreference = 'Continue'

$target = 'C:\Program Files (x86)\Microsoft Visual Studio'
$logDir = 'D:\MaHong\agent_workspace\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logPath = Join-Path $logDir ("remove_vs_residual_no_acl_{0}.log" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))

function Write-Log {
    param([string]$Message)
    Add-Content -LiteralPath $logPath -Value ("{0} {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message) -Encoding UTF8
}

Write-Log "Starting VS residual removal without ACL changes."
Write-Log "Running as: $([System.Security.Principal.WindowsIdentity]::GetCurrent().Name)"

if (Test-Path -LiteralPath $target) {
    $resolved = (Resolve-Path -LiteralPath $target).Path
    if ($resolved -eq 'C:\Program Files (x86)\Microsoft Visual Studio') {
        $sum = (Get-ChildItem -LiteralPath $resolved -Force -Recurse -File -ErrorAction SilentlyContinue |
            Measure-Object Length -Sum).Sum
        Write-Log ("Removing {0} ({1} MB)" -f $resolved, [math]::Round($sum / 1MB, 1))
        Remove-Item -LiteralPath $resolved -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        Write-Log "Refusing unexpected path: $resolved"
    }
} else {
    Write-Log "Target missing before removal."
}

Write-Log ("StillExists={0}" -f (Test-Path -LiteralPath $target))
