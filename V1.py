import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.ndimage import gaussian_filter
import io
from tkinter import PhotoImage
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from tkinter import font

load_dotenv()

#Tamaño de pantalla
password = os.getenv("PASSWORD")

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
    pdf.text(x=70,y=37,txt='INFORME DE RESULTADOS')

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
    pdf.line(33,48,140,48)
    pdf.line(160,48,190,48)
    pdf.line(30,53,90,53)
    pdf.line(105,53,145,53)
    pdf.line(165,53,190,53)
    pdf.line(43,58,190,58)
    pdf.line(50,63,190,63)

    pdf.text(x=33,y=47,txt=nombre_var.get())
    pdf.text(x=160,y=47,txt=edad_var.get())
    pdf.text(x=30,y=52,txt=sexo_var.get())
    pdf.text(x=105,y=52,txt=peso_var.get())
    pdf.text(x=165,y=52,txt=altura_var.get())
    pdf.text(x=43,y=57,txt=actividad_var.get())
    pdf.text(x=50,y=62,txt=diagnostico_var.get())

    pdf.image('presion.png',x=5,y=100,w=200,h=100)

    pdf.set_font('Arial','B',8)
    pdf.set_text_color(12, 50, 86)
    pdf.text(x=12,y=265,txt='SensiPad recomienda que todo resultado obtenido sea evaluado e interpretado por un médico')

    pdf.rect(10,270,190,10,'F')

    pdf.set_text_color(255, 255, 255)
    pdf.text(x=97,y=276,txt='www.sensipad.com')

    # Guardar el archivo PDF
    nombre_archivo = f"Informe_{nombre_var.get()}.pdf"
    pdf.output(nombre_archivo)

def enviar_correo():
    generar_pdf()
    try:
        # Dirección del remitente y destinatario
        remitente = "ggroproy@gmail.com"
        destinatario = f"{destinatario_var.get()}"
        
        # Obtener el nombre del archivo desde la variable de entrada
        nombre_archivo = f"Informe_{nombre_var.get()}.pdf"  # Aquí tomamos el nombre de la entrada
        
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = f'Informe de resultados plantares {nombre_var.get()}'
        
        cuerpo = f"""<html>
                <body>
                    <p>Estimado/a {nombre_var.get()},</p>
                    <p>Espero que este mensaje le encuentre bien. Adjunto encontrará el informe con los resultados de su evaluación plantar.</p>
                    <p>Es importante que siga las recomendaciones indicadas en el informe para mejorar su bienestar y evitar posibles complicaciones en el futuro. Si tiene alguna duda o necesita realizar alguna consulta adicional, no dude en contactarme.</p>
                    <p>Recuerde que la prevención es clave para mantener una buena salud y calidad de vida.</p>
                    <p>Saludos cordiales,</p>
                    <p>Dr. Alejandro Rivera<br>Ortopedista</p>
                    <p><em>"Cuidamos de tu bienestar, para que sigas dando los mejores pasos."</em></p>
                </body>
            </html>"""
        msg.attach(MIMEText(cuerpo, 'html'))


        # Ruta del archivo
        archivo_path = nombre_archivo  # Usamos el nombre definido dinámicamente
        attachment = open(archivo_path, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {nombre_archivo}')
        
        msg.attach(part)
        
        # Conectar con el servidor SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente,password)  # Usa tu contraseña o una contraseña de aplicación si es necesario

        # Enviar el correo
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        
        messagebox.showinfo("Éxito", "El archivo se ha enviado correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")
        print(f"Error detallado: {e}")


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

def abrir_recuperar_contrasena():
    # Crear una nueva ventana para recuperar contraseña
    ventana_recuperar = tk.Toplevel(ventana_inicio)
    ventana_recuperar.title("Recuperar Contraseña")
    ventana_recuperar.geometry("300x200")
    ventana_recuperar.config(bg="#484454")
    
    tk.Label(ventana_recuperar, text="Recuperar Contraseña", font=("Arial", 16, "bold"), bg="#484454", fg="white").pack(pady=20)
    tk.Label(ventana_recuperar, text="Introduce tu correo electrónico para restablecer\n tu contraseña.", font=("Arial", 12), bg="#484454", fg="white", justify="center").pack(pady=10)
    tk.Entry(ventana_recuperar, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana_recuperar, text="Enviar", font=("Arial", 12, "bold"), bg="#0b3d91", fg="white").pack(pady=20)

# Crear la ventana principal

def crear_interfaz_principal():
    global root, nombre_var, edad_var, sexo_var, peso_var, altura_var, diagnostico_var, actividad_var , destinatario_var

    # Crear la ventana principal
    root = tk.Tk()
    root.title("SensiPad")
    root.geometry("900x900")
    root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

    # Variables para la información del paciente
    nombre_var = tk.StringVar()
    edad_var = tk.StringVar()
    sexo_var = tk.StringVar()
    peso_var = tk.StringVar()
    altura_var = tk.StringVar()
    diagnostico_var = tk.StringVar()
    actividad_var = tk.StringVar()
    destinatario_var = tk.StringVar()

    # Cuadros de texto y labels organizados
    frame_info = tk.Frame(root)
    frame_info.pack(pady=10)

    # Fila 1 (Nombre,Edad)
    tk.Label(frame_info, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=nombre_var, width=30).grid(row=0, column=1, columnspan=3, sticky="ew", padx=5, pady=5)


    tk.Label(frame_info, text="Edad:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=edad_var).grid(row=0, column=5, padx=5, pady=5)

   # Fila 2 (Sexo, Peso, Altura)
    tk.Label(frame_info, text="Sexo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")    
    tk.Entry(frame_info, textvariable=sexo_var).grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_info, text="Peso:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=peso_var).grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_info, text="Altura:").grid(row=1, column=4, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=altura_var).grid(row=1, column=5, padx=5, pady=5)

    # Fila 3 (Actividad física)
    tk.Label(frame_info, text="Actividad física:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=actividad_var).grid(row=2, column=1, columnspan=5, sticky="ew",padx=5, pady=5)

    # Fila 4 (Diagnóstico previo)
    tk.Label(frame_info, text="Diagnóstico previo:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=diagnostico_var).grid(row=3, column=1, columnspan=5, sticky="ew",padx=5, pady=5)

    # Fila 5 (Correo)
    tk.Label(frame_info, text="Correo:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=destinatario_var).grid(row=4, column=1, columnspan=5, sticky="ew",padx=5, pady=5)

    # Botones
    tk.Button(frame_info, text="Generar PDF", command=generar_pdf).grid(row=5, column=1, padx=5, pady=5, sticky="e")
    tk.Button(frame_info, text="Mostrar Información", command=mostrar_informacion).grid(row=5, column=2, padx=5, pady=5, sticky="e")
    tk.Button(frame_info, text="Correo", command=enviar_correo).grid(row=5, column=3, padx=5, pady=5, sticky="e")


    fig, axes = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [1, 1.1]})
# Nota: el ajuste en `width_ratios` permite compensar el espacio de la barra de color.

# Subplot del pie izquierdo
    c1 = axes[0].imshow(z_left, cmap='jet', interpolation='bilinear')
    axes[0].set_title('Pie Izquierdo')
    axes[0].axis('off')

# Subplot del pie derecho
    c2 = axes[1].imshow(z_right, cmap='jet', interpolation='bilinear')
    axes[1].set_title('Pie Derecho')
    axes[1].axis('off')

# Barra de color para el segundo gráfico
    fig.colorbar(c2, ax=axes[1], fraction=0.046, pad=0.04)

# Ajustar el diseño para que los subplots queden alineados
    plt.tight_layout()
    fig.savefig('presion.png', dpi=100, bbox_inches='tight')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=10)
    canvas.draw()

    root.mainloop()

def mover_ventana(event):
    # Calculamos la diferencia entre la posición del puntero y la posición inicial del clic
    nueva_x = ventana_inicio.winfo_x() + event.x - offset_x
    nueva_y = ventana_inicio.winfo_y() + event.y - offset_y
    ventana_inicio.geometry(f"+{nueva_x}+{nueva_y}")

def iniciar_arrastre(event):
    # Guardamos la diferencia entre la posición del puntero y la esquina superior izquierda de la ventana
    global offset_x, offset_y
    offset_x = event.x
    offset_y = event.y

# Ventana de inicio de sesión
ventana_inicio = tk.Tk()
ventana_inicio.title("Inicio de Sesión")
ventana_width = 500
ventana_height = 350
pantalla_width = ventana_inicio.winfo_screenwidth()
pantalla_height = ventana_inicio.winfo_screenheight()
pos_x = (pantalla_width // 2) - (ventana_width // 2)
pos_y = (pantalla_height // 2) - (ventana_height // 2)
ventana_inicio.geometry(f"{ventana_width}x{ventana_height}+{pos_x}+{pos_y}")
ventana_inicio.configure(bg="#484454")
ventana_inicio.resizable(False, False)
ventana_inicio.overrideredirect(True)


barra_titulo = tk.Frame(ventana_inicio, bg="#484454", relief="raised", bd=0)
barra_titulo.pack(fill="x", pady=5)
# Crear un Label en la barra de título
titulo = tk.Label(barra_titulo, text="Login", fg="white", bg="#484454")
titulo.pack(side="left", padx=10)

# Permitir mover la ventana con la barra de título
barra_titulo.bind("<Button-1>", iniciar_arrastre)  # Iniciar el arrastre
barra_titulo.bind("<B1-Motion>", mover_ventana)  # Mover la ventana

# Variables de inicio de sesión
usuario_var = tk.StringVar()
contrasena_var = tk.StringVar()

# Encabezado
encabezado = tk.Label(ventana_inicio, text="USER LOGIN", font=("Code Saver",35), bg="#484454", fg="white")
encabezado.pack(pady=1)
subtitulo = tk.Label(ventana_inicio, text="Bienvenido a SensiPad", font=("Modern Sans", 14), bg="#484454", fg="white")
subtitulo.pack(pady=1)


# Crear marco con esquinas redondeadas
def create_rounded_frame(parent, width, height, radius=20, bg_color="#605c74"):
    canvas = tk.Canvas(parent, width=width, height=height, bg=ventana_inicio.cget("bg"), highlightthickness=0)

    # Dibujar esquinas redondeadas y fondo del marco
    canvas.create_arc((0, 0, radius * 2, radius * 2), start=90, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_arc((width - radius * 2, 0, width, radius * 2), start=0, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_arc((0, height - radius * 2, radius * 2, height), start=180, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_arc((width - radius * 2, height - radius * 2, width, height), start=270, extent=90, fill=bg_color, outline=bg_color)
    canvas.create_rectangle((radius, 0, width - radius, height), fill=bg_color, outline=bg_color)
    canvas.create_rectangle((0, radius, width, height - radius), fill=bg_color, outline=bg_color)

    # Retornar canvas
    return canvas


# Marco del formulario
frame_width = 400
frame_height = 100
rounded_frame = create_rounded_frame(ventana_inicio, width=frame_width, height=frame_height, radius=20, bg_color="#605c74")
rounded_frame.pack(pady=10)

# Agregar un Frame dentro del Canvas para widgets
frame_form = tk.Frame(rounded_frame, bg="#605c74")
frame_form.place(x=10, y=10, width=frame_width - 20, height=frame_height - 20)

# Campo de Usuario
tk.Label(frame_form, text="Usuario:", font=("Modern Sans", 12), bg="#605c74", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(frame_form, textvariable=usuario_var, font=("Arial", 12), width=25, bg="#c0bccc", fg="#000000").grid(row=0, column=1, padx=10, pady=10)


# Campo de Contraseña
tk.Label(frame_form, text="Contraseña:", font=("Modern Sans", 12), bg="#605c74", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
tk.Entry(frame_form, textvariable=contrasena_var, font=("Arial", 12), width=25, bg="#c0bccc", fg="#000000").grid(row=1, column=1, padx=10, pady=10)

# Botón Iniciar Sesión
boton_login = tk.Button(ventana_inicio, text="Login", font=("Modern Sans", 12), bg="#605c74", fg="white", command=iniciar_sesion)
boton_login.pack(pady=20)

texto_olvido = tk.Label(ventana_inicio, text="¿Olvidaste tu contraseña?", font=("Modern Sans", 12), bg="#484454", fg="white", cursor="hand2")
texto_olvido.pack(pady=1)
texto_olvido.bind("<Button-1>", lambda e: abrir_recuperar_contrasena())


ventana_inicio.iconphoto(True,PhotoImage(file="Logo.png"))

ventana_inicio.mainloop()
