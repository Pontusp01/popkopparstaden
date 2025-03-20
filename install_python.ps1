# Skapa en temporär mapp om den inte finns
$tempPath = "C:\temp"
if (!(Test-Path -Path $tempPath)) {
    New-Item -ItemType Directory -Path $tempPath
}

# Ladda ner senaste Python-versionen (64-bit installer)
$pythonInstaller = "python-3.11.6-amd64.exe"
$downloadUrl = "https://www.python.org/ftp/python/3.11.6/$pythonInstaller"
$downloadPath = "$tempPath\$pythonInstaller"

# Ladda ner Python installationsfilen
Invoke-WebRequest -Uri $downloadUrl -OutFile $downloadPath

# Kör installationsfilen tyst och lägg till Python i PATH
Start-Process -FilePath $downloadPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

# Kontrollera om Python är installerat och i PATH
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($pythonPath) {
    Write-Output "Python är installerat på: $pythonPath"
} else {
    Write-Output "Python verkar inte vara i PATH, lägger till manuellt."
    $pythonInstallPath = "C:\Program Files\Python311"
    [System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";$pythonInstallPath", [System.EnvironmentVariableTarget]::Machine)
    $env:Path += ";$pythonInstallPath"
    Write-Output "Python har lagts till i PATH manuellt."
}

# Verifiera Python-installationen
$pythonCheck = python --version
if ($pythonCheck) {
    Write-Output "Python har installerats korrekt: $pythonCheck"
} else {
    Write-Output "Python-installationen misslyckades."
    exit
}

# Installera wfastcgi
pip install wfastcgi

# Aktivera wfastcgi för IIS
wfastcgi-enable
