# PowerShell : crée un virtualenv, l'active proprement et installe les dépendances
Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)

# Crée le virtualenv si nécessaire
if (-not (Test-Path ".venv")) {
	python -m venv .venv
}

# Autorise l'exécution pour cette session si nécessaire
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Chemin du script d'activation
$activate = Join-Path -Path (Resolve-Path .venv) -ChildPath "Scripts\Activate.ps1"

if (Test-Path $activate) {
	. $activate
} else {
	Write-Error "Activation script introuvable : $activate"
	exit 1
}

python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Environnement créé et dépendances installées."
Write-Host "Activez-le plus tard (PowerShell) : . .venv\Scripts\Activate.ps1"
