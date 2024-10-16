
REQUISITOS
1. Este proyecto se ejecuta con python 3.8
2. mysql
3. Instalar la libreria para weasyprint


---- PASOS -------
1. instalar python 3.8
2. crear un nuevo entorno virtual con python 3.8
  - PS C:\Project-mios\Gestion-de-conserjeria>  py -3.8 -m venv entorno5

3. instalar las dependencias necesarias para weasyprint. 
   3.1. Descargar e instalar GTK de esta url
  - https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases

   3.2 Agregar la libreria "weasyprint" en el archivo requirements.txt 
   3.3 Instalar weasyprint con el entorno activado 
 - (entorno5) PS C:\Project-mios\Gestion-de-conserjeria> pip install weasyprint
   3.4 Reiniciar el equipo

4. Instalar el archivo requirements.txt
  - (entorno5) PS C:\Project-mios\Gestion-de-conserjeria> pip install -r requirements.txt


6. recuerda tener levantada la base de datos y la conexion debe estar correcta 

7. Levantar el proyecto con python manage.py runserver 8081
. Aqui va a decir que falta migraciones. no importa igual levanta.

8. Hacer las migraciones
  8.1 (entorno5) PS C:\Project-mios\Gestion-de-conserjeria> python manage.py makemigrations
  8.2. (entorno5) PS C:\Project-mios\Gestion-de-conserjeria> python manage.py migrate

9. Crear el superusuario desde la terminal
  9.1 (entorno5) PS C:\Project-mios\Gestion-de-conserjeria> python manage.py createsuperuser
  9.2. ingresar user = admin, correo, y pass

10. Ingresar al panel de django e ingresar los roles y crear al usuario administrador de condominio.

11. volver a la bd e ingresar las regiones y comunas

 






### 👉 Set Up for `Windows` 

> Install modules via `VENV` (windows) 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

