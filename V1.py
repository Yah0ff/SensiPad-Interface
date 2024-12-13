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

estado = 0 

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
    messagebox.showinfo("Información", "El documento fue creado correctamente")

def enviar_correo():
    generar_pdf()
    try:
        # Dirección del remitente y destinatario
        remitente = "ggroproy@gmail.com"
        destinatario = f"{destinatario_var.get()}"
        
        # Obtener el nombre del archivo desde la variable de entrada
        nombre_archivo = f"Informe_{nombre_var.get()}.pdf" 
        
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
        archivo_path = nombre_archivo  
        attachment = open(archivo_path, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {nombre_archivo}')
        
        msg.attach(part)
        
        # Conectar con el servidor SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente,password) 

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
    info.geometry("700x800")
    info.configure(bg="#FFFFFF")

    encabezado = tk.Label(info, text="Padecimientos comunes", font=("Code Saver",35), bg="#FFFFFF", fg="#0C3256")
    encabezado.pack(pady=1)
 

    texto = (
        "1. Pie Plano: El pie plano se caracteriza por la pérdida del arco del pie, lo que causa que toda la planta del pie \n"
        "toque el suelo al caminar. Este trastorno es común tanto en niños como en adultos. El pie plano puede causar dolor \n"
        "en los talones y en la parte media del pie, así como dificultad para caminar largas distancias. Las personas con pie \n"
        "plano pueden experimentar problemas adicionales como la inestabilidad o el dolor en las rodillas.\n\n"
        
        "2. Fascitis Plantar: Es una de las principales causas de dolor en el talón. Se trata de una inflamación del tejido \n"
        "que conecta el talón con los dedos, conocido como la fascia plantar. Esta afección se desarrolla cuando la fascia se \n"
        "irrita o se lesiona debido a un uso excesivo, mala alineación al caminar o estar mucho tiempo de pie. Los síntomas incluyen \n"
        "dolor en el talón, especialmente al levantarse por la mañana, o después de estar mucho tiempo sentado.\n\n"
        
        "3. Espolón Calcáneo: Un espolón calcáneo es una protuberancia ósea que se forma en el talón como resultado de la tensión \n"
        "prolongada en la fascia plantar, lo que lleva a una acumulación de calcio. Aunque el espolón calcáneo no siempre causa dolor, \n"
        "cuando lo hace, generalmente se experimenta un dolor punzante en la base del talón al caminar o estar de pie por períodos largos. \n"
        "El tratamiento incluye el uso de plantillas ortopédicas, cambios en el calzado o, en casos severos, cirugía.\n\n"
        
        "4. Metatarsalgia: Se refiere a un dolor generalizado en la parte delantera del pie, particularmente en la zona de los dedos \n"
        "y la base de los metatarsos. Esta afección es común en personas que tienen sobrepeso, usan zapatos incómodos o realizan \n"
        "actividades de alto impacto. El dolor puede intensificarse al caminar o correr, y los síntomas incluyen inflamación y enrojecimiento \n"
        "de la zona afectada. El tratamiento puede incluir reposo, el uso de zapatos adecuados, y en algunos casos, la terapia física.\n\n"
        
        "5. Hallux Valgus (Juanete): Un juanete es una deformidad en la base del dedo gordo del pie, que puede causar dolor y \n"
        "dificultad para caminar. Se forma cuando el hueso o los tejidos blandos en la parte frontal del pie se desalinean, lo que \n"
        "resulta en un bulto en la zona. Los juanetes son más comunes en personas que usan zapatos apretados, pero también pueden \n"
        "ser causados por factores hereditarios o problemas en la estructura del pie. El tratamiento incluye ortesis, terapia física o \n"
        "cirugía en casos graves.\n\n"
        
        "6. Neuroma de Morton: Esta afección se caracteriza por la formación de un bulto benigno en los nervios entre los dedos \n"
        "del pie, generalmente entre el tercero y cuarto dedo. Puede causar dolor, hormigueo o sensación de ardor en los dedos del pie. \n"
        "El neuroma es más común en mujeres y puede ser provocado por el uso de zapatos estrechos. El tratamiento varía desde el uso de \n"
        "plantillas ortopédicas hasta cirugía en casos severos.\n\n"
        
        "7. Tendinitis Aquilea: Es la inflamación del tendón de Aquiles, que conecta el talón con los músculos de la pantorrilla. \n"
        "La tendinitis puede ser causada por el uso excesivo, especialmente en actividades deportivas que requieren mucho esfuerzo de \n"
        "la pantorrilla, como correr o saltar. Los síntomas incluyen dolor en la parte posterior del tobillo, hinchazón y rigidez. \n"
        "El tratamiento incluye reposo, terapia física y en algunos casos, cirugía.\n\n"
        
        "8. Síndrome de Túnel Tarsiano: Esta condición se produce cuando el nervio tibial se comprime en el túnel tarsiano, \n"
        "situado en el lado interno del tobillo. Los síntomas incluyen dolor, hormigueo y debilidad en el pie o los dedos. \n"
        "Este trastorno es menos común que el síndrome del túnel carpiano, pero puede ser igualmente debilitante. El tratamiento \n"
        "puede incluir el uso de férulas, medicamentos antiinflamatorios o cirugía en casos graves.\n\n"
    )

    # Crear un widget de texto con la información
    label_info = tk.Label(info, text=texto, justify="left", padx=10, pady=10, bg="#FFFFFF")
    label_info.pack(fill="both", expand=True)


def cerrar_aplicacion():
    root.destroy()

# Ventana de Inicio de Sesión
def iniciar_sesion():
    if usuario_var.get() == "x" and contrasena_var.get() == "x":
        ventana_inicio.destroy()
        crear_interfaz_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def abrir_recuperar_contrasena():
    
    ventana_recuperar = tk.Toplevel(ventana_inicio)
    ventana_recuperar.title("Recuperar Contraseña")
    ventana_recuperar.geometry("300x200")
    ventana_recuperar.config(bg="#484454")
    
    tk.Label(ventana_recuperar, text="Recuperar Contraseña", font=("Arial", 16, "bold"), bg="#484454", fg="white").pack(pady=20)
    tk.Label(ventana_recuperar, text="Introduce tu correo electrónico para restablecer\n tu contraseña.", font=("Arial", 12), bg="#484454", fg="white", justify="center").pack(pady=10)
    tk.Entry(ventana_recuperar, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana_recuperar, text="Enviar", font=("Arial", 12, "bold"), bg="#0b3d91", fg="white").pack(pady=20)

# Crear la ventana principal

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def cambio_VG():
    global root

    def on_resize(event):
        # Obtener el tamaño actual de la ventana
        width = event.width / 100
        height = event.height / 100
        # Ajustar el tamaño de la figura
        fig.set_size_inches(width, height)
        canvas.draw()

    # Ocultar la ventana principal
    root.withdraw()

    # Crear ventana de muestra
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Muestra")

    # Maximizar la ventana sin hacerlo de pantalla completa
    nueva_ventana.state('zoomed') 

    # Crear la figura de los gráficos
    fig, axes = plt.subplots(1, 2, figsize=(8, 5), gridspec_kw={'width_ratios': [1, 1.1]})

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

    # Agregar la figura al lienzo de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=nueva_ventana)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    # Vincular el evento de redimensionamiento
    nueva_ventana.bind('<Configure>', on_resize)

    # Volver a la ventana principal
    def cerrar_nueva_ventana():
        nueva_ventana.destroy()
        root.deiconify()

    nueva_ventana.protocol("WM_DELETE_WINDOW", cerrar_nueva_ventana)

def crear_interfaz_principal():
    global root, nombre_var, edad_var, sexo_var, peso_var, altura_var, diagnostico_var, actividad_var , destinatario_var 
    global barra_lateral, canvas

    # Crear la ventana principal
    root = tk.Tk()
    root.title("SensiPad")
    root.geometry("900x750")
    ventana_width = 900
    ventana_height = 750
    pantalla_width = root.winfo_screenwidth()
    pantalla_height = root.winfo_screenheight()
    pos_x = (pantalla_width // 2) - (ventana_width // 2)
    pos_y = (pantalla_height // 2) - (ventana_height // 2)
    root.geometry(f"{ventana_width}x{ventana_height}+{pos_x}+{pos_y}")
    root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
    root.configure(bg="#FFFFFF")

    # Variables para la información del paciente
    nombre_var = tk.StringVar()
    edad_var = tk.StringVar()
    sexo_var = tk.StringVar()
    peso_var = tk.StringVar()
    altura_var = tk.StringVar()
    diagnostico_var = tk.StringVar()
    actividad_var = tk.StringVar()
    destinatario_var = tk.StringVar()

    # Crear la barra lateral
    barra_lateral = tk.Frame(root, bg="#4A889C", width=200)
    barra_lateral.pack(side="left", fill="y")

# Cargar las imágenes
    img1 = tk.PhotoImage(file="PDF.png") 
    img2 = tk.PhotoImage(file="Correo.png") 
    img3 = tk.PhotoImage(file="Ques.png") 
    img4 = tk.PhotoImage(file="expan.png")  

# Crear botones con imágenes
    btn1 = tk.Button(barra_lateral, image=img1,command=generar_pdf, bg="#4A889C", bd=0)
    btn1.pack(pady=10, padx=10, fill="x")

    btn2 = tk.Button(barra_lateral, image=img2, command=enviar_correo, bg="#4A889C", bd=0)
    btn2.pack(pady=10, padx=10, fill="x")

    btn3 = tk.Button(barra_lateral, image=img3, command=mostrar_informacion, bg="#4A889C", bd=0)
    btn3.pack(pady=10, padx=10, fill="x")

    btn4 = tk.Button(barra_lateral, image=img4, command=cambio_VG, bg="#4A889C", bd=0)
    btn4.pack(pady=10, padx=10, fill="x")

    encabezado = tk.Label(root, text="SensiPad", font=("Code Saver",35), bg="#FFFFFF", fg="#0C3256")
    encabezado.pack(pady=1)
    subtitulo = tk.Label(root, text="Datos del usuario", font=("Modern Sans", 14), bg="#FFFFFF", fg="#0C3256")
    subtitulo.pack(pady=1)

    # Cuadros de texto y labels organizados
    frame_info = tk.Frame(root, bg="white")
    frame_info.pack(pady=10)

    # Fila 1 (Nombre,Edad)
    tk.Label(frame_info, text="Nombre:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=nombre_var, width=30).grid(row=0, column=1, columnspan=3, sticky="ew", padx=5, pady=5)


    tk.Label(frame_info, text="Edad:", bg="white").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=edad_var).grid(row=0, column=5, padx=5, pady=5)

   # Fila 2 (Sexo, Peso, Altura)
    tk.Label(frame_info, text="Sexo:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")    
    tk.Entry(frame_info, textvariable=sexo_var).grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_info, text="Peso:", bg="white").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=peso_var).grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_info, text="Altura:", bg="white").grid(row=1, column=4, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=altura_var).grid(row=1, column=5, padx=5, pady=5)

    # Fila 3 (Actividad física)
    tk.Label(frame_info, text="Actividad física:", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=actividad_var).grid(row=2, column=1, columnspan=5, sticky="ew",padx=5, pady=5)

    # Fila 4 (Diagnóstico previo)
    tk.Label(frame_info, text="Diagnóstico previo:", bg="white").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=diagnostico_var).grid(row=3, column=1, columnspan=5, sticky="ew",padx=5, pady=5)

    # Fila 5 (Correo)
    tk.Label(frame_info, text="Correo:", bg="white").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    tk.Entry(frame_info, textvariable=destinatario_var).grid(row=4, column=1, columnspan=5, sticky="ew",padx=5, pady=5)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [1, 1.1]})

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
    nueva_x = ventana_inicio.winfo_x() + event.x - offset_x
    nueva_y = ventana_inicio.winfo_y() + event.y - offset_y
    ventana_inicio.geometry(f"+{nueva_x}+{nueva_y}")

def iniciar_arrastre(event):
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
titulo = tk.Label(barra_titulo, text="Login", fg="white", bg="#484454")
titulo.pack(side="left", padx=10)

barra_titulo.bind("<Button-1>", iniciar_arrastre)  
barra_titulo.bind("<B1-Motion>", mover_ventana)  

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
