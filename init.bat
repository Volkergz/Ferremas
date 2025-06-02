@echo off
REM Este script inicializa los servicios necesarios para el proyecto.

REM Crea el ambiente virtual si no existe
if not exist venv (
    echo Creando el ambiente virtual...
    python -m venv venv
)

REM Activa el ambiente virtual
call venv\Scripts\activate.bat

REM Instala las dependencias del proyecto
echo Instalando dependencias...
pip install -r requirements.txt

REM Ejecuta el script de inicialización del servicio de autenticación
echo Iniciando el servicio de autenticación...
start "Serv. Autenticacion" cmd /k "py services\Autenticacion\main.py"

REM Ejecuta el script de inicialización del servicio de Banco Central
echo Iniciando el servicio de Banco Central...
start "Serv. Banco Central" cmd /k "py services\BancoCentral\main.py"

REM Ejecuta el script de inicialización del servicio de Compras
echo Iniciando el servicio de Compras...
start "Serv. Monedas" cmd /k "py services\Compras\main.py"

REM Ejecuta el script de inicialización del servicio de Compras
echo Iniciando el servicio de Inventario...
start "Serv. Inventario" cmd /k "py services\Inventario\main.py"

REM Ejecuta el script de inicialización del servicio de Transbank
echo Iniciando el servicio de Transbank...
start "Serv. Transbank" cmd /k "py services\Transbank\main.py"