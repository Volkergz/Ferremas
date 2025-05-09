
# Ferremas

Ferremas es un sistema informatico desarollado para navegadores, compatible con dispositivos Desktop, Nothebook y Mobile, este proyecto tiene como objetivo principal facilitar el proceso de compra de productos de ferremas a los consumidores.

## 👨‍💻 Instalación

Sigue estos pasos para configurar y ejecutar el proyecto **Ferremas** en tu entorno local.

### Pre-requisitos

Asegúrate de tener instalado lo siguiente en tu máquina:

- [Python](https://www.python.org/) (v3.13.3 o superior)
- [Git](https://git-scm.com/)

### Revisar versiones

```bash
npm --version
```
```bash
py --version
```
```bash
py -m pip --version
```

## si pip django no está instalado en su ambiente virtual usar
```pip install django
```

### Pasos a seguir

Primero, abre una terminal o cmd (windows).
* Clone el repositorio del proyecto desde GitHub.

```bash
git clone https://github.com/Volkergz/Ferremas/tree/main
```

*  Accede al directorio del proyecto clonado

```bash
cd Ferremas
```

* Instalar ambiente virtual 
```bash
pip -m venv venv
```

* Crear ambiente virtual en cmd
```bash
python -m venv venv
```

* Activar ambiente virtual en cmd
```bash
.\venv\Scripts\activate
```
Nota: si esta usando otra terminal, consulte la documentacion de [VirtualEnviroment](https://docs.python.org/3/library/venv.html#how-venvs-work)

## 💻 Ejecución

### Servicio de Cliente

Si ya activo el ambiente virtual, ejecute el siguiente comando

* Correr el servidor
py frontend\manage.py runserver

### Servicio de Autenticación

* Correr el servidor
py services\Autenticacion\manage.py runserver


#### El servidor se ejecutará en http://127.0.0.1:8000/. Abre esta URL en tu navegador para ver el proyecto en acción.




## 👀 Team Members

* Haleym Hidalgo
* Angel Perugini
* Martin Nuñez
