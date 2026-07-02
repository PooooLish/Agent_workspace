$ErrorActionPreference = 'Continue'

$targets = @(
    'C:\Program Files (x86)\QQMailPlugin',
    'C:\Program Files (x86)\yxq_nethelper',
    'C:\Program Files (x86)\360'
)

$logDir = 'D:\MaHong\agent_workspace\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logPath = Join-Path $logDir ("cleanup_old_c_drive_components_{0}.log" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))

function Write-Log {
    param([string]$Message)
    $line = "{0} {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message
    Add-Content -LiteralPath $logPath -Value $line -Encoding UTF8
}

Write-Log "Starting targeted cleanup."
Write-Log "Running as: $([System.Security.Principal.WindowsIdentity]::GetCurrent().Name)"

$current = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$grantTarget = ('{0}:(OI)(CI)F' -f $current)

foreach ($target in $targets) {
    if (-not (Test-Path -LiteralPath $target)) {
        Write-Log "Missing: $target"
        continue
    }

    $resolved = (Resolve-Path -LiteralPath $target).Path
    $allowed = $resolved -eq 'C:\Program Files (x86)\QQMailPlugin' -or
        $resolved -eq 'C:\Program Files (x86)\yxq_nethelper' -or
        $resolved -eq 'C:\Program Files (x86)\360'

    if (-not $allowed) {
        Write-Log "Refusing unexpected path: $resolved"
        continue
    }

    $sum = (Get-ChildItem -LiteralPath $resolved -Force -Recurse -File -ErrorAction SilentlyContinue |
        Measure-Object Length -Sum).Sum
    $sizeMb = [math]::Round($sum / 1MB, 1)
    Write-Log "Preparing to remove $resolved ($sizeMb MB)."

    & takeown.exe /F $resolved /R /D Y >> $logPath 2>&1
    & icacls.exe $resolved /grant $grantTarget /T /C >> $logPath 2>&1
    Remove-Item -LiteralPath $resolved -Recurse -Force -ErrorAction SilentlyContinue

    if (Test-Path -LiteralPath $resolved) {
        Write-Log "FAILED still exists: $resolved"
    } else {
        Write-Log "Removed: $resolved"
    }
}

Write-Log "Verification:"
foreach ($target in $targets) {
    Write-Log ("{0} StillExists={1}" -f $target, (Test-Path -LiteralPath $target))
}

Write-Log "Done."
