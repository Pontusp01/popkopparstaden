# Importera IIS-modulen
Import-Module WebAdministration

# Lägg till FastCGI-applikationen
New-WebHandler -Name "Python FastCGI Kopparstaden" -Path "*" -Verb "*" -Modules "FastCgiModule" -ScriptProcessor "C:\Program Files\Python311\python.exe|C:\Program Files\Python311\Lib\site-packages\wfastcgi.py" -ResourceType "Unspecified"

# Lägg till FastCGI-applikationen i IIS konfiguration
Add-WebConfiguration /system.webServer/fastCgi -Value @{
    fullPath = "C:\Program Files\Python311\python.exe";
    arguments = "C:\Program Files\Python311\Lib\site-packages\wfastcgi.py";
}