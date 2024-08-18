"""
Implementación de un procesador de imagenes que aplica filtros básicos.

Curso de proceso digital de imagenes - semestre 2025-1

Profesores:
Manuel Cristobal López Michelone
Yessica Martínez Reyes
César Hernández Solis

Versión 1.0
"""

from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os

# Carga la imagen a editar.
def cargar_imagen():
    # Exploramos en búsqueda de un archivo .png ó .jpg
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Selecciona la imagen", filetypes=(("JPG file","*.jpg"), ("PNG file", "*.png")))
    
    if filename:
        #Carga y muestra 2 instancias de la imagen, la vista original y la que muestra el filtro aplicado
        global img_original, img_editada
        img_original = Image.open(filename)
        img_editada = img_original.copy() 

        mostrar_imagen_original()
        mostrar_imagen_editada()

# Se encarga de que las imagenes mostradas queden dentró de los limites del marco
# así como de redimensionarlas para que se muestren completas.
def ajustar_imagen(img, label):
    # Obtener el tamaño del frame correspondiente
    frame_width = label.winfo_width()
    frame_height = label.winfo_height()

    # Redimensionar la imagen al tamaño del frame, manteniendo la relación de aspecto
    img.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)

    # Convertir la imagen redimensionada a un objeto ImageTk
    img_tk = ImageTk.PhotoImage(img)

    label.configure(image=img_tk)
    label.image = img_tk  # Guardar la referencia a la imagen para que no la elimine el recolector de basura.

# Vista de las imagenes.

def mostrar_imagen_original():
    if img_original:
        ajustar_imagen(img_original, lbl_original)

def mostrar_imagen_editada():
    if img_editada:
        ajustar_imagen(img_editada, lbl_editado)

# Función que implementa 2 filtros de escala de grises.
def escala_grises(version):
    if img_original:
        # Crear una nueva imagen en modo RGB para almacenar el resultado del filtro
        img_grises = Image.new("RGB", img_original.size)

        # Obtener los datos de píxeles de la imagen original
        pixels = img_original.load()
        pixels_grises = img_grises.load()

        # Recorre la imagen pixel a pixel y les aplica la formula de la media ó de la media
        # ponderada para convertir a escala de grises.        
        for i in range(img_original.width):
            for j in range(img_original.height):
                r, g, b = pixels[i, j]
                gris = (r + g + b) // 3
                if version == 2:
                    gris = int(r*0.299 + g*0.587 + b*0.114)
                pixels_grises[i, j] = (gris, gris, gris)

        global img_editada
        img_editada = img_grises
        mostrar_imagen_editada()  # Mostrar la imagen editada después de aplicar el filtro

# Función que aplica el filtro de mica, es decir, cambia la paleta de colores 
# de la imagen por una que toma como base a un sólo color RGB.
def mica_RGB(version):
    if img_original:
        # Crear una nueva imagen en modo RGB para almacenar el resultado del filtro
        img_mica = Image.new("RGB", img_original.size)

        # Obtener los datos de píxeles de la imagen original
        pixels = img_original.load()
        pixels_rgb = img_mica.load()

        # Recorre la imagen pixel a pixel y mantiene únicamente un valor de los bytes RGB
        # los 2 restantes los establece en cero.  
        for i in range(img_original.width):
            for j in range(img_original.height):
                r, g, b = pixels[i, j]
                if version == 1:
                    pixels_rgb[i, j] = (r, 0, 0)
                elif version == 2:
                    pixels_rgb[i, j] = (0, g, 0)
                else:
                    pixels_rgb[i, j] = (0, 0, b)

        global img_editada
        img_editada = img_mica
        mostrar_imagen_editada()  # Mostrar la imagen editada después de aplicar el filtro

# Función que controla el menú de filtros disponibles.
def opcion_seleccionada(opcion):
    global submenu_abierto
    # Ocultar el submenú previamente abierto si hay uno
    if submenu_abierto:
        submenu_abierto.unpost()
    
    if opcion == "Escala de grises":
        submenu_grises.post(root.winfo_pointerx(), root.winfo_pointery())
        submenu_abierto = submenu_grises
    elif opcion == "Mica RGB":
        submenu_RGB.post(root.winfo_pointerx(), root.winfo_pointery())
        submenu_abierto = submenu_RGB

# Auxiliares para llamar a cada filtro en su respectivo submenú.
def escala_grises_estandar():
    escala_grises(1)

def escala_grises_ponderada():
    escala_grises(2)

def mica_R():
    mica_RGB(1)

def mica_G():
    mica_RGB(2)

def mica_B():
    mica_RGB(3)

# Función para evitar que más de un submenú se despliegue al mismo tiempo.
def ocultar_submenu(event=None):
    global submenu_abierto
    if submenu_abierto:
        submenu_abierto.unpost()
        submenu_abierto = None

if __name__ == "__main__":
    global root, img_original, img_editada, submenu_grises, submenu_RGB, submenu_abierto
    root = Tk()    
    root.title("Editor Morsa")    
    
    window_width = 1000
    window_height = 500

    # Obtener el tamaño de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Despliega la ventana principal a razón de 1/2 en el ancho y 1/3 en la altura 
    root.geometry(f"{window_width}x{window_height}+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 3}")

    # Frame para las imágenes (lado izquierdo de la ventana)
    frame_imagenes = Frame(root)
    frame_imagenes.pack(side=LEFT, fill=BOTH, expand=True)

    # Frame para la imagen original (izquierda del frame de imágenes)
    frame_original = Frame(frame_imagenes)
    frame_original.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    # Frame para la imagen editada (derecha del frame de imágenes)
    frame_editado = Frame(frame_imagenes)
    frame_editado.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    # Label para mostrar la imagen original
    lbl_original = Label(frame_original)
    lbl_original.pack(expand=True, fill=BOTH)

    # Label para mostrar la imagen editada
    lbl_editado = Label(frame_editado)
    lbl_editado.pack(expand=True, fill=BOTH)

    # Frame para los botones (lado derecho)
    frame_boton = Frame(root)
    frame_boton.pack(side=RIGHT, fill=Y, padx=15, pady=15)

    # Botón para seleccionar la imagen
    btn2 = Button(frame_boton, text="Selecciona la imagen", command=cargar_imagen)
    btn2.pack(side=tk.TOP, fill=tk.X, pady=5)

    # Crear el menú principal
    menu = Menu(root)
    root.config(menu=menu)

    # Submenú para "Escala de grises"
    submenu_grises = Menu(menu, tearoff=0)
    submenu_grises.add_command(label="Escala estandar", command=escala_grises_estandar)
    submenu_grises.add_command(label="Escala ponderada", command=escala_grises_ponderada)

    # Submenú para "Mica RGB"
    submenu_RGB = Menu(menu, tearoff=0)
    submenu_RGB.add_command(label="Mica roja", command=mica_R)
    submenu_RGB.add_command(label="Mica verde", command=mica_G)
    submenu_RGB.add_command(label="Mica azul", command=mica_B)

    # Agregar opciones al menú principal
    menu.add_command(label="Escala de grises", command=lambda: opcion_seleccionada("Escala de grises"))
    menu.add_command(label="Mica RGB", command=lambda: opcion_seleccionada("Mica RGB"))

    # Variable global para almacenar la imagen original
    img_original = None
    img_editada = None
    submenu_abierto = None  # Variable global para rastrear el submenú abierto

    # Bind para ocultar el submenú al hacer clic en cualquier parte de la ventana
    root.bind("<Button-1>", ocultar_submenu)

    root.mainloop()