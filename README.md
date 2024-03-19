# Eliminar Fondo de Imagen Pythone

Este repositorio contiene un script en Python que utiliza la biblioteca Tkinter para crear una interfaz gráfica de usuario (GUI) que permite cargar una imagen, seleccionar un color mediante un eyedropper, quitar el fondo de la imagen basado en el color seleccionado y guardar la imagen resultante. El proceso de eliminación del fondo se realiza utilizando OpenCV.

## Requisitos

- Python 3.x
- Tkinter
- OpenCV
- PIL (Python Imaging Library)
- NumPy

## Instalación

1. Clona el repositorio a tu sistema local:

    ```bash
    git clone https://github.com/pardalaco/remove-background-python.git
    ```

2. Instala las dependencias utilizando pip:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta el script `eliminar_fondo.py`:

    ```bash
    python eliminar_fondo.py
    ```

2. La interfaz gráfica se abrirá. Puedes cargar una imagen haciendo clic en el botón "Cargar Imagen". Luego, puedes utilizar el eyedropper para seleccionar un color en la imagen cargada.

3. Una vez seleccionado el color, haz clic en el botón "Quitar fondo" para eliminar el fondo de la imagen basado en el color seleccionado.

4. Para guardar la imagen resultante, haz clic en el botón de guardado y elige la ubicación y el formato de archivo deseado.

## Funcionalidades Principales

- Carga de imágenes en formatos jpg y png.
- Selección de color mediante eyedropper.
- Eliminación del fondo de la imagen basado en el color seleccionado.
- Guardado de la imagen resultante en formatos png y jpg.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, puedes realizar un fork del repositorio y enviar tus pull requests con las mejoras propuestas.

## Licencia

Este proyecto está bajo la licencia [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Esto significa que puedes usar y modificar el proyecto, incluso con fines comerciales, siempre y cuando des crédito al autor (pardalaco) y enlaces al repositorio original.
