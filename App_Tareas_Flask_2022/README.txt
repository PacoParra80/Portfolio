APP TAREAS FLASK (2022)

Instrucciones de instalación:

La app viene por defecto sin entorno virtual.

# Instrucciones para configurar un entorno virtual y ejecutar el proyecto

Este proyecto utiliza un entorno virtual para gestionar sus dependencias. Sigue los pasos a continuación para configurar el entorno virtual en tu sistema:

1. Abre una terminal o línea de comandos en la raíz del proyecto.

2. Crea un nuevo entorno virtual utilizando `virtualenv`. Ejecuta el siguiente comando:

    ```
    virtualenv venv
    ```

   Esto creará una nueva carpeta llamada `venv` que contendrá el entorno virtual.

3. Activa el entorno virtual. Los comandos para activar el entorno virtual pueden variar según el sistema operativo. Aquí hay algunos ejemplos:

   - En Windows:

     ```
     venv\Scripts\activate
     ```

   - En macOS y Linux:

     ```
     source venv/bin/activate
     ```

4. Una vez activado el entorno virtual, instala las dependencias del proyecto ejecutando:

    ```
    pip install -r requirements.txt
    ```

   Esto instalará todas las bibliotecas y paquetes necesarios para ejecutar el proyecto.

5. Ahora estás listo para ejecutar el proyecto. Simplemente ejecuta el archivo principal main.py para iniciar la aplicación.
   Verás algo como 'Running on http://127.0.0.1:5000', sólo tienes que hacer click en el enlace.

¡Y eso es todo! Has configurado con éxito un entorno virtual para el proyecto y has instalado todas las dependencias necesarias. 

¡Un saludo!
