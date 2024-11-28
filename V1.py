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
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Agregar información al PDF
    pdf.cell(200, 10, txt="Reporte de Presión Plantar", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Nombre: {nombre_var.get()}", ln=True)
    pdf.cell(200, 10, txt=f"Edad: {edad_var.get()}", ln=True)
    pdf.cell(200, 10, txt=f"Sexo: {sexo_var.get()}", ln=True)
    pdf.cell(200, 10, txt=f"Peso: {peso_var.get()}", ln=True)
    pdf.cell(200, 10, txt=f"Altura: {altura_var.get()}", ln=True)
    pdf.cell(200, 10, txt=f"Diagnóstico previo: {diagnostico_var.get()}", ln=True)
    pdf.cell(200, 10, txt=f"Actividad física: {actividad_var.get()}", ln=True)

    # Generar las gráficas como imágenes
    buf = io.BytesIO()
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    c1 = axes[0].imshow(z_left, cmap='jet', interpolation='bilinear')
    axes[0].set_title('Pie Izquierdo')
    axes[0].axis('off')
    c2 = axes[1].imshow(z_right, cmap='jet', interpolation='bilinear')
    axes[1].set_title('Pie Derecho')
    axes[1].axis('off')
    fig.colorbar(c2, ax=axes[1], fraction=0.046, pad=0.04)
    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf)

    # Agregar la imagen al PDF
    img_path = "temp_img.png"
    img.save(img_path)
    pdf.image(img_path, x=10, y=80, w=180)

    # Guardar el PDF
    nombre_archivo = f"Informe_{nombre_var.get()}.pdf"
    pdf.output(nombre_archivo)
    messagebox.showinfo("Éxito", "El PDF se ha generado correctamente.")

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

    #  Fila 2 (Edad, Sexo, Peso, Altura)
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
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.mainloop()

# Ventana de inicio
ventana_inicio = tk.Tk()
ventana_inicio.title("Inicio de Sesión")
ventana_inicio.geometry("300x200")

usuario_var = tk.StringVar()
contrasena_var = tk.StringVar()

tk.Label(ventana_inicio, text="Usuario:").pack(pady=5)
tk.Entry(ventana_inicio, textvariable=usuario_var).pack(pady=5)
tk.Label(ventana_inicio, text="Contraseña:").pack(pady=5)
tk.Entry(ventana_inicio, textvariable=contrasena_var, show="*").pack(pady=5)
tk.Button(ventana_inicio, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=20)

ventana_inicio.protocol("WM_DELETE_WINDOW", ventana_inicio.destroy)
ventana_inicio.mainloop()
