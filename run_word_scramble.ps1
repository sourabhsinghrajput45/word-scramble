<#
    Smart Auto-Run Script for Poetry Project
    ----------------------------------------
    • Installs Poetry if missing
    • Installs dependencies if not yet installed
    • Runs "poetry run word-scramble"
    • Works from any folder
    • Optional -Loop for restart mode
#>

param(
    [switch]$Loop
)

$ProjectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$Command     = "poetry run word-scramble"
$LogFile     = Join-Path $ProjectPath "run_log.txt"
$ErrorActionPreference = "Stop"

function Log($msg, $color="Gray") {
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $line = "[$timestamp] $msg"
    Write-Host $line -ForegroundColor $color
    Add-Content -Path $LogFile -Value $line
}

function Pause-OnExit {
    Write-Host ""
    Write-Host "Press any key to close..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Set-Location $ProjectPath
Log "Project path: $ProjectPath" "Cyan"

# ---------- Install Poetry if missing ----------
try {
    poetry --version | Out-Null
    Log " Poetry is installed." "Green"
} catch {
    Log " Poetry not found. Installing..." "Yellow"
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    $env:Path += ";$env:APPDATA\pypoetry\venv\Scripts"
    Log " Poetry installed successfully." "Green"
}

# ---------- Install project dependencies if needed ----------
try {
    if (Test-Path "$ProjectPath\poetry.lock") {
        Log " Dependencies already locked. Skipping install." "Gray"
    } else {
        Log " Installing dependencies..." "Yellow"
        poetry install
        Log " Dependencies installed." "Green"
    }
} catch {
    Write-Host " Error installing dependencies: $($_.Exception.Message)" -ForegroundColor Red
    Log " Dependency installation failed." "Red"
    Pause-OnExit
    exit 1
}

# ---------- Run game ----------
try {
    if ($Loop) {
        while ($true) {
            Log "Launching Word Scramble..." "Cyan"
            & poetry run word-scramble
            Log " Restarting in 5 seconds..." "DarkYellow"
            Start-Sleep -Seconds 5
        }
    } else {
        Log "Launching Word Scramble (single run)..." "Cyan"
        & poetry run word-scramble
        Log " Game closed normally." "Green"
    }
} catch {
    Write-Host "`n Error running game:`n$($_.Exception.Message)" -ForegroundColor Red
    Log " Runtime error: $($_.Exception.Message)" "Red"
} finally {
    Pause-OnExit
}
