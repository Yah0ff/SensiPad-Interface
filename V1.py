import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.ndimage import gaussian_filter
import io
from PIL import Image

# Datos simulados de presión plantar
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
x, y = np.meshgrid(x, y)

z_left = np.exp(-((x - 0.3)**2 + (y - 0.5)**2) * 20) + np.exp(-((x - 0.7)**2 + (y - 0.8)**2) * 30)
z_right = np.exp(-((x - 0.3)**2 + (y - 0.5)**2) * 30) + np.exp(-((x - 0.6)**2 + (y - 0.8)**2) * 20)
z_left = gaussian_filter(z_left, sigma=5)
z_right = gaussian_filter(z_right, sigma=5)


def generar_pdf():
    pdf = FPDF(orientation='P',unit='mm',format='A4')
    pdf.add_page()

    pdf.image('Logo.png',x=10,y=10,w=10,h=10)
    pdf.set_font('Arial','B',25)
    pdf.set_text_color(74, 136, 156)
    pdf.text(x=22,y=18,txt='Sensi')
    pdf.set_text_color(12, 50, 86)
    pdf.text(x=46,y=18,txt='Pad')

    pdf.set_line_width(0.5)
    pdf.set_draw_color(12, 50, 86)
    pdf.set_fill_color(12, 50, 86)
    pdf.rect(10,30,190,10,'F')

    pdf.ellipse(5,30,10,10,'F')
    pdf.ellipse(195,30,10,10,'F')

    pdf.set_font('Arial','B',15)
    pdf.set_text_color(255, 255, 255)
    pdf.text(x=75,y=37,txt='INFORME DE RESULTADOS')

    pdf.set_font('Arial','',8)
    pdf.set_text_color(12, 50, 86)
    pdf.text(x=20,y=47,txt='Nombre:')
    pdf.text(x=150,y=47,txt='Edad:')
    pdf.text(x=20,y=52,txt='Sexo:')
    pdf.text(x=95,y=52,txt='Peso:')
    pdf.text(x=150,y=52,txt='Estatura:')
    pdf.text(x=20,y=57,txt='Actividad física:')
    pdf.text(x=20,y=62,txt='Diagnóstico anterior:')

    pdf.set_line_width(0.2)
    pdf.line(33,47,140,47)
    pdf.line(160,47,190,47)
    pdf.line(30,52,90,52)
    pdf.line(105,52,145,52)
    pdf.line(165,52,190,52)
    pdf.line(43,57,190,57)
    pdf.line(50,62,190,62)

    pdf.set_line_width(0.5)
    pdf.line(10,65,200,65)

    pdf.image('temp_img.png',x=5,y=100,w=200,h=100)

    pdf.set_font('Arial','B',8)
    pdf.set_text_color(12, 50, 86)
    pdf.text(x=20,y=250,txt='SensiPad recomienda que todo resultado obtenido sea evaluado e interpretado por un médico')

    # Guardar el archivo PDF
    #nombre_archivo = f"Informe_{nombre_var.get()}.pdf"
    nombre_archivo = f"Info.pdf"
    pdf.output(nombre_archivo)
    messagebox.showinfo("Éxito", f"El PDF se ha generado correctamente: {nombre_archivo}")


def mostrar_informacion():
    info = tk.Toplevel(root)
    info.title("Información de Padecimientos")
    info.geometry("500x300")

    # Crear una tabla de información
    texto = (
        "1. Pie Plano: Arco del pie colapsado, común en niños y adultos.\n"
        "2. Fascitis Plantar: Inflamación del tejido en la planta del pie.\n"
        "3. Espolón Calcáneo: Crecimiento óseo en el talón, causado por tensión.\n"
        "4. Metatarsalgia: Dolor en la parte delantera del pie, asociado a sobrepeso.\n"
    )
    label_info = tk.Label(info, text=texto, justify="left", padx=10, pady=10)
    label_info.pack()

    boton_cerrar = tk.Button(info, text="Cerrar", command=info.destroy)
    boton_cerrar.pack()

def cerrar_aplicacion():
    root.destroy()

# Ventana de Inicio de Sesión
def iniciar_sesion():
    if usuario_var.get() == "admin" and contrasena_var.get() == "admin":
        ventana_inicio.destroy()
        crear_interfaz_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def crear_interfaz_principal():
    global root, nombre_var, edad_var, sexo_var, peso_var, altura_var, diagnostico_var, actividad_var

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Interfaz de Presión Plantar")
    root.geometry("800x600")
    root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

    # Variables para la información del paciente
    nombre_var = tk.StringVar()
    edad_var = tk.StringVar()
    sexo_var = tk.StringVar()
    peso_var = tk.StringVar()
    altura_var = tk.StringVar()
    diagnostico_var = tk.StringVar()
    actividad_var = tk.StringVar()

    # Cuadros de texto y labels organizados
    frame_info = tk.Frame(root)
    frame_info.pack(pady=10)

    # Fila 1 (Nombre)
    tk.Label(frame_info, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=nombre_var).grid(row=0, column=1, padx=5, pady=5)

    # Fila 2 (Edad, Sexo, Peso, Altura)
    tk.Label(frame_info, text="Edad:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=edad_var).grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_info, text="Sexo:").grid(row=1, column=2, padx=5, pady=5, sticky="e")    
    tk.Entry(frame_info, textvariable=sexo_var).grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_info, text="Peso:").grid(row=1, column=4, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=peso_var).grid(row=1, column=5, padx=5, pady=5)

    tk.Label(frame_info, text="Altura:").grid(row=1, column=6, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=altura_var).grid(row=1, column=7, padx=5, pady=5)

    # Fila 3 (Actividad física)
    tk.Label(frame_info, text="Actividad física:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=actividad_var).grid(row=2, column=1, columnspan=3, padx=5, pady=5)

    # Fila 4 (Diagnóstico previo)
    tk.Label(frame_info, text="Diagnóstico previo:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=diagnostico_var).grid(row=3, column=1, columnspan=3, padx=5, pady=5)

    # Botones
    tk.Button(root, text="Generar PDF", command=generar_pdf).pack(pady=10)
    tk.Button(root, text="Mostrar Información", command=mostrar_informacion).pack(pady=10)

    # Gráficas de presión plantar
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    c1 = axes[0].imshow(z_left, cmap='jet', interpolation='bilinear')
    axes[0].set_title('Pie Izquierdo')
    axes[0].axis('off')
    c2 = axes[1].imshow(z_right, cmap='jet', interpolation='bilinear')
    axes[1].set_title('Pie Derecho')
    axes[1].axis('off')
    fig.colorbar(c2, ax=axes[1], fraction=0.046, pad=0.04)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=10)
    canvas.draw()

    root.mainloop()

# Ventana de inicio de sesión
ventana_inicio = tk.Tk()
generar_pdf()
ventana_inicio.title("Inicio de Sesión")
ventana_inicio.geometry("400x250")

# Variables de inicio de sesión
usuario_var = tk.StringVar()
contrasena_var = tk.StringVar()

# Formulario de inicio de sesión
tk.Label(ventana_inicio, text="Usuario:").pack(pady=5)
tk.Entry(ventana_inicio, textvariable=usuario_var).pack(pady=5)
tk.Label(ventana_inicio, text="Contraseña:").pack(pady=5)
tk.Entry(ventana_inicio, textvariable=contrasena_var, show="*").pack(pady=5)

tk.Button(ventana_inicio, text="Iniciar sesión", command=iniciar_sesion).pack(pady=10)

ventana_inicio.mainloop()
