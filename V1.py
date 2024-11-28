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

z_left = np.exp(-((x - 0.3)**2 + (y - 0.5)**2) * 20) + np.exp(-((x - 0.7)**2 + (y - 0.8)**2) * 20)
z_right = np.exp(-((x - 0.4)**2 + (y - 0.5)**2) * 20) + np.exp(-((x - 0.6)**2 + (y - 0.7)**2) * 20)

z_left = gaussian_filter(z_left, sigma=5)
z_right = gaussian_filter(z_right, sigma=5)

# Función de inicio de sesión
def iniciar_sesion():
    usuario = usuario_var.get()
    contrasena = contrasena_var.get()
    
    if usuario == "x" and contrasena == "x":
        ventana_login.destroy()
        mostrar_interfaz_principal() 
    else:
        messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

# Función para generar el archivo PDF
def generar_pdf(fig):
    nombre = nombre_var.get()
    edad = edad_var.get()
    sexo = sexo_var.get()
    peso = peso_var.get()
    altura = altura_var.get()
    diagnostico = diagnostico_var.get()
    actividad = actividad_var.get()

    # Crear el PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Información del paciente
    pdf.cell(0, 10, "Informe de Presión Plantar", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(0, 10, f"Nombre: {nombre}", ln=True)
    pdf.cell(0, 10, f"Edad: {edad}", ln=True)
    pdf.cell(0, 10, f"Sexo: {sexo}", ln=True)
    pdf.cell(0, 10, f"Peso: {peso} kg", ln=True)
    pdf.cell(0, 10, f"Altura: {altura} cm", ln=True)
    pdf.cell(0, 10, f"Diagnóstico previo: {diagnostico}", ln=True)
    pdf.cell(0, 10, f"Actividad física habitual: {actividad}", ln=True)
    pdf.ln(10)

    # Guardar las gráficas como imágenes
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = Image.open(buf)
    img_path = "presion_plantar.png"
    img.save(img_path)

    # Agregar la gráfica al PDF
    pdf.image(img_path, x=10, y=90, w=190)
    pdf.output("informe_presion_plantar.pdf")
    messagebox.showinfo("PDF Generado", "El informe se ha generado como 'informe_presion_plantar.pdf'")

# Función para mostrar la información ingresada
def mostrar_informacion():
    nombre = nombre_var.get()
    edad = edad_var.get()
    sexo = sexo_var.get()
    peso = peso_var.get()
    altura = altura_var.get()
    diagnostico = diagnostico_var.get()
    actividad = actividad_var.get()

    info_text = (
        f"Nombre: {nombre}\n"
        f"Edad: {edad}\n"
        f"Sexo: {sexo}\n"
        f"Peso: {peso} kg\n"
        f"Altura: {altura} cm\n"
        f"Diagnóstico previo: {diagnostico}\n"
        f"Actividad física habitual: {actividad}"
    )
    messagebox.showinfo("Información del Paciente", info_text)

# Función para mostrar la interfaz principal
def mostrar_interfaz_principal():
    app = tk.Tk()
    app.title("Distribución de Presión Plantar")

    global nombre_var, edad_var, sexo_var, peso_var, altura_var, diagnostico_var, actividad_var

    nombre_var = tk.StringVar()
    edad_var = tk.StringVar()
    sexo_var = tk.StringVar()
    peso_var = tk.StringVar()
    altura_var = tk.StringVar()
    diagnostico_var = tk.StringVar()
    actividad_var = tk.StringVar()

    frame_top = tk.Frame(app)
    frame_top.pack(pady=10)

    ##################################################################################################################################################

    # Cuadros de texto para información del paciente

    # Nombre
    tk.Label(frame_top, text="Nombre", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    nombre_entry = tk.Entry(frame_top, textvariable=nombre_var, font=("Arial", 10))
    nombre_entry.grid(row=0, column=1, columnspan=3, sticky="we", padx=10, pady=5)

    # Edad, Sexo, Peso, Altura
    tk.Label(frame_top, text="Edad", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(frame_top, textvariable=edad_var, font=("Arial", 10), width=5).grid(row=1, column=1, sticky="w", padx=5, pady=5)

    tk.Label(frame_top, text="Sexo", font=("Arial", 10)).grid(row=1, column=2, sticky="w", padx=10, pady=5)
    tk.Entry(frame_top, textvariable=sexo_var, font=("Arial", 10), width=10).grid(row=1, column=3, sticky="w", padx=5, pady=5)

    tk.Label(frame_top, text="Peso (kg)", font=("Arial", 10)).grid(row=1, column=4, sticky="w", padx=10, pady=5)
    tk.Entry(frame_top, textvariable=peso_var, font=("Arial", 10), width=5).grid(row=1, column=5, sticky="w", padx=5, pady=5)

    tk.Label(frame_top, text="Altura (cm)", font=("Arial", 10)).grid(row=1, column=6, sticky="w", padx=10, pady=5)
    tk.Entry(frame_top, textvariable=altura_var, font=("Arial", 10), width=5).grid(row=1, column=7, sticky="w", padx=5, pady=5)

    # Diagnóstico previo
    tk.Label(frame_top, text="Diagnóstico previo", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(frame_top, textvariable=diagnostico_var, font=("Arial", 10)).grid(row=2, column=1, columnspan=7, sticky="we", padx=10, pady=5)

    # Actividad física habitual
    tk.Label(frame_top, text="Actividad física habitual", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(frame_top, textvariable=actividad_var, font=("Arial", 10)).grid(row=3, column=1, columnspan=7, sticky="we", padx=10, pady=5)

    frame = tk.Frame(app)
    frame.pack()

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].imshow(z_left, cmap="jet", origin="lower", extent=(0, 1, 0, 1))
    axs[0].set_title("Pie Izquierdo")
    axs[0].axis("off")

    im2 = axs[1].imshow(z_right, cmap="jet", origin="lower", extent=(0, 1, 0, 1))
    axs[1].set_title("Pie Derecho")
    axs[1].axis("off")

    cbar = fig.colorbar(im2, ax=axs[1], fraction=0.046, pad=0.04)
    cbar.set_label("Presión (kPa)")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Botones
    tk.Button(app, text="Generar PDF", font=("Arial", 12), command=lambda: generar_pdf(fig)).pack(pady=10)
    tk.Button(app, text="Mostrar Información", font=("Arial", 12), command=mostrar_informacion).pack(pady=10)

    app.mainloop()

# Pantalla de inicio de sesión
ventana_login = tk.Tk()
ventana_login.title("Inicio de sesión")

usuario_var = tk.StringVar()
contrasena_var = tk.StringVar()

tk.Label(ventana_login, text="Nombre de usuario", font=("Arial", 12)).pack(pady=5)
usuario_entry = tk.Entry(ventana_login, textvariable=usuario_var, font=("Arial", 12))
usuario_entry.pack(pady=5)

tk.Label(ventana_login, text="Contraseña", font=("Arial", 12)).pack(pady=5)
contrasena_entry = tk.Entry(ventana_login, textvariable=contrasena_var, show="*", font=("Arial", 12))
contrasena_entry.pack(pady=5)

tk.Button(ventana_login, text="Iniciar sesión", font=("Arial", 12), command=iniciar_sesion).pack(pady=10)

ventana_login.mainloop()
