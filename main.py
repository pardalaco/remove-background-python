
#   _____              _       _                 
#  |  __ \            | |     | |                
#  | |__) |_ _ _ __ __| | __ _| | __ _  ___ ___  
#  |  ___/ _` | '__/ _` |/ _` | |/ _` |/ __/ _ \ 
#  | |  | (_| | | | (_| | (_| | | (_| | (_| (_) |
#  |_|   \__,_|_|  \__,_|\__,_|_|\__,_|\___\___/ 
#
# Repositorio de git: 
# https://github.com/pardalaco/remove-background-python.git
#
# Licencia:
# Creative Commons Attribution 4.0 International (CC BY 4.0)
                                               



import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
import numpy as np
import cv2

eyedropper_activo = False
imagen_pil = None
imagen_sin_fondo = None

def habilitar_deshabilitar_botones():
    if imagen_pil is None:
        boton_quitar_fondo.config(state=tk.DISABLED)
        boton_seleccionar_color.config(state=tk.DISABLED)
    else:
        boton_quitar_fondo.config(state=tk.NORMAL)
        boton_seleccionar_color.config(state=tk.NORMAL)

def habilitar_deshabilitar_boton_guardado():
    if imagen_sin_fondo is None:
        boton_guardado.config(state=tk.DISABLED)
    else:
        boton_guardado.config(state=tk.NORMAL)

# Luego, llamas a esta función después de cargar la imagen
def cargar_imagen():
    ruta_imagen = filedialog.askopenfilename(
        filetypes=(("Imagenes jpg", "*.jpg"), ("Imagenes png", "*.png"))
    )
    if ruta_imagen:
        global imagen_pil
        imagen_pil = Image.open(ruta_imagen)
        imagen_pil = imagen_pil.resize((300, 300))

        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        canvas_imagen.create_image(0, 0, anchor=tk.NW, image=imagen_tk)
        canvas_imagen.image = imagen_tk

        # Llama a la función para habilitar o deshabilitar el botón
        habilitar_deshabilitar_botones()

def guardar_en_ruta():
    ruta_de_guardado = filedialog.asksaveasfilename(
        title=("Guardar imagen como:"),
        filetypes=(("Imagen png", "*.png"), ("Imagen jpg", "*.jpg"))
        )
    if ruta_de_guardado:
        imagen_sin_fondo.save(ruta_de_guardado)

        

def obtener_color(event):
    if eyedropper_activo and imagen_pil:
        x, y = event.x, event.y
        color = imagen_pil.getpixel((x, y))
        vRed.set(color[0])
        vGreen.set(color[1])
        vBlue.set(color[2])
        actualizar_rgb()

def alternar_eyedropper():
    global eyedropper_activo
    eyedropper_activo = not eyedropper_activo
    if eyedropper_activo:
        ventana.config(cursor="plus")
    else:
        ventana.config(cursor="")
    etiqueta_r.config(text=f"Eyedropper activo: {eyedropper_activo}")


def quitar_fondo():
    global imagen_pil, imagen_sin_fondo
    color_rgb = np.array([vRed.get(), vGreen.get(), vBlue.get()])


    if imagen_pil is None:
        print("Primero carga una imagen.")
        return

    image = np.array(imagen_pil)  # Convertir la imagen PIL a una matriz NumPy
    color_to_replace = color_rgb
    threshold = 10

    # Definimos los rangos del color a reemplazar en formato HSV
    lower_color = np.array([color_to_replace[0] - threshold, color_to_replace[1] - threshold, color_to_replace[2] - threshold])
    upper_color = np.array([color_to_replace[0] + threshold, color_to_replace[1] + threshold, color_to_replace[2] + threshold])

    # Creamos una máscara del color a reemplazar
    mask = cv2.inRange(image, lower_color, upper_color)

    # Convertimos la imagen a formato RGBA (añadiendo canal alfa)
    rgba_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Aplicamos la máscara para hacer transparente el color a reemplazar
    rgba_image[mask == 255] = (0, 0, 0, 0)

    imagen_sin_fondo = Image.fromarray(rgba_image)

    imagen_tk_sin_fondo = ImageTk.PhotoImage(Image.fromarray(rgba_image))  # Convertir la matriz NumPy a una imagen PIL
    canvas_imagen_sin_fondo.create_image(0, 0, anchor=tk.NW, image=imagen_tk_sin_fondo)
    canvas_imagen_sin_fondo.image = imagen_tk_sin_fondo

    # Activar guardado de la nueva imagen
    habilitar_deshabilitar_boton_guardado()





# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Eliminar fondo de imagen")

# Variables para los valores RGB
vRed = tk.IntVar(value=0)
vGreen = tk.IntVar(value=0)
vBlue = tk.IntVar(value=0)

vBGR = (vBlue.get(), vGreen.get(), vRed.get())


# Función para actualizar etiquetas RGB
def actualizar_rgb():
    vBGR = (vBlue.get(), vGreen.get(), vRed.get())

    # Actualizar texto
    etiqueta_r_rgb.config(text=f"RGB\nR: {vRed.get():3}\nG: {vGreen.get():3}\nB: {vBlue.get():3}")

    # Actualizar Imagen RGB
    color_rgb_cv2 = np.zeros((30, 30, 3), dtype="uint8")
    cv2.rectangle(color_rgb_cv2, (0, 0), (30, 30), vBGR, -1)
    color_rgb_pil = Image.fromarray(cv2.cvtColor(color_rgb_cv2, cv2.COLOR_BGR2RGB))
    color_rgb_tk = ImageTk.PhotoImage(color_rgb_pil)
    canvas_color.create_image(1, 1, anchor=tk.NW, image=color_rgb_tk)
    canvas_color.image = color_rgb_tk


# Botón para cargar la imagen
boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
boton_cargar.grid(row=3, column=1)


# Etiquetas para los valores RGB
etiqueta_r_rgb = tk.Label(ventana, text=f"RGB\nR: {vRed.get():3}\nG: {vGreen.get():3}\nB: {vBlue.get():3}")
etiqueta_r_rgb.grid(column=0, row=0)

# Botón de selección de color (eyedropper)
imagen_colorselect = PhotoImage(file="./img/colorselect.png")
imagen_colorselect = imagen_colorselect.subsample(10, 10)

boton_seleccionar_color = tk.Button(ventana, image=imagen_colorselect, command=alternar_eyedropper)
boton_seleccionar_color.config(state=tk.DISABLED)
boton_seleccionar_color.grid(row=0, column=1)

# Crear un canvas para mostrar la color RGB
canvas_color = tk.Canvas(ventana, width=30, height=30)
canvas_color.grid(row=1, column=0)
color_rgb_cv2 = np.zeros((30, 30, 3), dtype="uint8")
cv2.rectangle(color_rgb_cv2, (0, 0), (30, 30), vBGR, -1)
color_rgb_pil = Image.fromarray(cv2.cvtColor(color_rgb_cv2, cv2.COLOR_BGR2RGB))
color_rgb_tk = ImageTk.PhotoImage(color_rgb_pil)
canvas_color.create_image(1, 1, anchor=tk.NW, image=color_rgb_tk)

# Botón de guardado
imagen_guardado = PhotoImage(file="./img/guardado.png")
imagen_guardado = imagen_guardado.subsample(10, 10)

boton_guardado = tk.Button(ventana, image=imagen_guardado, command=guardar_en_ruta)
boton_guardado.config(state=tk.DISABLED)
boton_guardado.grid(row=0, column=2)

# Etiqueta para mostrar el estado del eyedropper
etiqueta_r = tk.Label(ventana, text=f"Eyedropper activo: {eyedropper_activo}")
etiqueta_r.grid(column=1, row=1)

# Crear un canvas para mostrar la imagen
canvas_imagen = tk.Canvas(ventana, width=300, height=300)
canvas_imagen.grid(row=4, column=1, columnspan=3)
canvas_imagen.bind("<Button-1>", obtener_color)

# Botón de quitar fondo
boton_quitar_fondo = tk.Button(ventana, text="Quitar fondo", command=quitar_fondo)
boton_quitar_fondo.config(state=tk.DISABLED)
boton_quitar_fondo.grid(row=5, column=1)

# Crear un canvas para mostrar la imagen sin fondo
canvas_imagen_sin_fondo = tk.Canvas(ventana, width=300, height=300)
canvas_imagen_sin_fondo.grid(row=6, column=1, columnspan=3)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
