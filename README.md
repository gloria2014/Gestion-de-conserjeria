
REQUISITOS
1. Este proyecto se ejecuta con python 3.9
2. mysql 8.0
3. Instalar la libreria para weasyprint


---- PASOS -------
1. instalar python 3.9
2. crear un nuevo entorno virtual con python 3.9

  - PS C:\Project-mios\Gestion-de-conserjeria>  py -3.9 -m venv entorno5

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
  8.3 Para migraciones posteriores, eliminar la carpeta de migracion inicial y volver a migrar

9. Crear el superusuario desde la terminal
  9.1 (entorno5) PS C:\Project-mios\Gestion-de-conserjeria> python manage.py createsuperuser
  9.2. ingresar user = admin, correo, y pass

10. Ingresar al panel de django 
  10.1 Ingresar los roles(1 admin, 2 conserje)    
  10.1 Crear al usuario administrador de condominio.
  

11. Ir a la base de datos
 11.1 Copiar la clave del admin al admin_condominio desde la bd
 12.2 Ingresar las regiones y comunas

 






### 👉 Set Up for `Windows` 

> Install modules via `VENV` (windows) 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />


SUBIR CAMBIOS DE MI RAMA
1. Añadir los cambios al área de preparación:
 desde mi rama local > git add . 
2. Confirmar los cambios
  git commit -m "Descripción de los cambios realizados"
3.  Subir la nueva rama al repositorio remoto
  git push origin nueva-rama
4. Fusionaar o hacer merge mi rama con la rama main

5. Ir al repositorio y hacer un pr. 

TRAER LA ULTIMA VERSIÓN DE LA RAMA MAIN A MI RAMA LOCAL
1. Si no estas en tu rama, cambiarse a tu rama local
  git checkout tu-rama-actual

2.Actualizar la rama main local con los últimos cambios del repositorio remoto:
  git fetch origin
  git checkout main
  git pull origin main

3. Cambiar de nuevo a tu rama actual:
  git checkout tu-rama-actual

4. Fusionar los cambios de la rama
  git merge main

------ ****** PASOS PARA CONECTARSE A LA BASE DE DATOS DE AZURE DESDE EL CLIENTE MYSQL  ******* ------

-> DESDE EL PORTAL
1. Ingresar al portal de azure y crear el servidor para mysql
2. crear la base de datos (vacia)
3. Descargar los certificados SSL de Azure para establecer la conexion segura 
  3.1. ir al recurso servidor 
  3.2. en el menu > configuracion > redes : Descargar certificado SSL 
  3.3. guardar el certificado en el equipo local

-> EN EL EQUIPO
1. Abrir mysql workbench
2. crear nueva conexion
3. ingresar las credenciales del servidor de azure
4. ir a la pestaña SSL y selccionar required, en CA file: ingresa la ruta del archivo DigiCertGlobalRootCA.crt.pem
5. probar la conexion Y se debe ver la base de datsoo que creamos en azure vacia obviamente poruqe aun no se ha migrado

-> MIGRAR EL MODELO A LA BASE DE DATOS DE AZURE A TRAVEZ DEL CLIENTE
1. Modificar la conexion en el setting.py
      DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nombre_base_de_datos_de_azure',
            'USER':'User_azure',
            'PASSWORD': 'xxxx',
            'HOST': 'nombre_servidor.mysql.database.azure.com',
            'PORT': '3306',
            'OPTIONS': {
                'ssl': {'ca': 'C:/turuta/DigiCertGlobalRootCA.crt.pem'}  # Ruta al certificado SSL
            }
        }
    }
  
  2. Migrar el modelo:
   2.1. acceder a mysql desde la aplicación: probar estos:
    - mysql -h azure@servidorconserjeria01 -u azure -p    
    - (entorno7) PS C:\Project-mios\Gestion-de-conserjeria> mysql -h servidorconserjeria01.mysql.database.azure.com -u azure@servidorconserjeria01 -p --ssl-mode=REQUIRED
    SINO RESULTA PROBAR DESDE LA SHELL -> ingresar a modo mysql asi: PS C:\Users\Gloria> mysql -u azure -p  
    y volver a ejcutar

  2.2. desde la terminal del proyecto, dentro del entorno virtual migrar:
    (entorno7) PS C:\Project-mios\Gestion-de-conserjeria> python manage.py makemigrations
    (entorno7) PS C:\Project-mios\Gestion-de-conserjeria> python manage.py migrate

-> Conéctate a tu base de datos MySQL en Azure:
1. Cargar el larchivo DigiCertGlobalRootCA.crt.pem a azure
  1.1 abrir la shell de azure y en la parte de arriba cargar archivo.
  1.2 validar si se cargó correcto: PS /home/gcastromerma> ls ~/ 
  1.3.COnectarse: PS /home/gcastromerma> mysql -h servidorconserjeria01.mysql.database.azure.com -u azure -p --ssl-ca=/home/gcastromerma/DigiCertGlobalRootCA.crt.pem 

                 PS /home/gcastromerma> mysql -h servidorconserjeria01.mysql.database.azure.com -u azure -p --ssl-ca=/home/gcastromerma/DigiCertGlobalRootCA.crt.pem 

  1.4 pide tu clave
  1.5 MySQL [(none)]> SHOW DATABASES; con este comando lista las bases de datos
    MySQL [(none)]> USE conserjeria_2
    MySQL [conserjeria_2]> SHOW TABLES;




----- ************** FIN ************* ---------------




--------- PASOS PARA MIGRAR LA BASE DE DATOS  CON BACKUP ---------------
Requisitos
- tener la base de datos local creada y con data

PASOS
Paso 1: Exportar la Base de Datos Local usando mysqldump
1. Hacer un backup .sql de la base de datos: 
  - Abrir la terminal de shell del equipo y escribir :
    mysqldump --verbose -u root -p conserjeria_2 > backup20241020.sql
    
  - Abrir el archivo backup.sql desde visual code y asgurarse que el encoding tenga UTF-8 si no lo tiene
    ir a la derecha inferior y cabmbiar el "encoding" a UTF-8 y guardar y cerrar.

  Paso 2: Conectar a Azure Database for MySQL e Importar la Base de Datos
  - van con las credenciales de azure
  - permitir mi ip en el firewall
  - ejecutar el siguiente comando:
  mysql -u azure@servidorconserjeria01 -p -h servidorconserjeria01.mysql.database.azure.com conserjeria_2



-------- ********** CREAR O DAR TODOS LOS PRIVILEGIOS AL USUARIO ********** ------------

IMPORTANTE: 
1. DEBES SABER TU IP PUBLICA
- para ver mi ip publica desde la shell
(Invoke-WebRequest -uri "http://ifconfig.me/ip").Content
 en mi caso, la ip de mi equipo es : 181.43.248.16'

2. DEBES crear un usuario con los permisos para onectarse al servidor de azure:
2.1. entrar a la shell del equipo y conectarse a mysql
  - ejecuta>  mysql -u root -p e ingresa tu pass y ya estas en modo sql
  1.
  CREATE USER 'azure@servidorconserjeria01'@'181.43.248.16' IDENTIFIED BY 'Estrella.23';

  2.Otorgar permisos al usuario:
  GRANT USAGE ON *.* TO 'azure@servidorconserjeria01'@'181.43.248.16';

  GRANT ALL PRIVILEGES ON *.* TO 'azure@servidorconserjeria01'@'181.43.248.16';

  FLUSH PRIVILEGES;

  -------------- *************** FIN **************** ----------------

  CONECTARME A MI BASE DA DEATOS DESDE LA SHELL DE AZURE
  1. conectar a azure e ir al servidor y abrir shell
  2. escribir mysql -h servidorconserjeria01.mysql.database.azure.com -u azure@servidorconserjeria01 -p


----- ******************** COPIAR LOS REGISTROS DE LOCAL A AZURE **********----

1. Exporta los datos desde la base de datos local utilizando mysqldump y guárdalos en un archivo SQL en tu máquina local:
  abrir shell en tu local y ejecutar:
  PS C:\Users\Gloria> mysqldump -h localhost -P 3306 -u root -p conserjeria_2 > clientealfa_backup.sql

2. en PowerShell, puedes usar Get-Content para leer el archivo y canalizarlo hacia mysql:
    Get-Content clientealfa_backup.sql | mysql -h servidorconserjeria01.mysql.database.azure.com -P 3306 -u azure -p conserjeria_2

3. Ver que las tablas se hayan caragdo con registros en la bd de azure


----**************** EXPORTAR E IMPORTAR VARIAS TABLAS CON REGISTROS ENTRE 2 BASES DE DEATOS EN EL
 MISMO SERVIDOR *************-----------

REQUISITO: debe estar conectada a ambos servidores y tener permisos privilegiados
1. Guardar para exportar la data
desde la shell:
mysqldump -h servidorconserjeria01.mysql.database.azure.com -P 3306 -u azure -p conserjeria_2 > clientealfa_backup.sql

2. luego ejecutar el siguiente comando para Importar y copiar la data a la base de datos destino
desde la shell:
Get-Content clientealfa_backup.sql | mysql -h servidorconserjeria01.mysql.database.azure.com -P 3306 -u azure -p conserjeria_2


















  