
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
py --version
```
```bash
py -m pip --version
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

* Instalar "Virtual Enviroment" 
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
```bash
py frontend\manage.py runserver
```

### Servicio de Autenticación

* Correr el servidor
```bash
py services\Autenticacion\main.py
```
#### El servicio se ejecutará en http://127.0.0.1:5000/.
Nota: Para probar los EndPoints use [Postman](https://www.postman.com/)

### Servicio de Transbank

* Correr el servidor
```bash
py services\Transbank\main.py
```
#### El servicio se ejecutará en http://127.0.0.1:5001/.
Nota: Para probar los EndPoints use [Postman](https://www.postman.com/)

## 👀 Team Members

* Haleym Hidalgo
* Angel Perugini
* Martin Nuñez
