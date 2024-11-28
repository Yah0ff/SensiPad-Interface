from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


# Pantalla de inicio de sesión
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.username_input = TextInput(hint_text="Usuario", multiline=False)
        self.password_input = TextInput(hint_text="Contraseña", password=True, multiline=False)
        login_button = Button(text="Iniciar Sesión", size_hint=(0.5, None), height=40)
        login_button.bind(on_press=self.verificar_credenciales)

        self.message_label = Label(text="", color=(1, 0, 0, 1))  # Mensaje de error o éxito

        layout.add_widget(Label(text="Inicio de Sesión"))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(self.message_label)

        self.add_widget(layout)

    def verificar_credenciales(self, instance):
        usuario_correcto = "X"
        contraseña_correcta = "X"

        if (self.username_input.text == usuario_correcto and
                self.password_input.text == contraseña_correcta):
            self.manager.current = "info"  # Cambia a la pantalla de información
        else:
            self.message_label.text = "Usuario o contraseña incorrectos"


# Pantalla de información
class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=2, padding=20, spacing=10)

        # Campos de texto
        campos = [
            ("Nombre", "Ingrese el nombre"),
            ("Edad", "Ingrese la edad"),
            ("Sexo", "Ingrese el sexo"),
            ("Peso", "Ingrese el peso (kg)"),
            ("Altura", "Ingrese la altura (cm)"),
            ("Diagnóstico Previo", "Ingrese el diagnóstico previo")
        ]

        self.inputs = {}

        for label_text, hint in campos:
            layout.add_widget(Label(text=label_text))
            input_field = TextInput(hint_text=hint, multiline=False)
            layout.add_widget(input_field)
            self.inputs[label_text] = input_field

        guardar_button = Button(text="Guardar", size_hint=(0.5, None), height=40)
        guardar_button.bind(on_press=self.guardar_datos)

        self.mensaje = Label(text="")  # Mensaje de confirmación

        layout.add_widget(guardar_button)
        layout.add_widget(self.mensaje)

        self.add_widget(layout)

    def guardar_datos(self, instance):
        datos = {campo: self.inputs[campo].text for campo in self.inputs}
        self.mensaje.text = f"Datos guardados:\n{datos}"


# Administrador de pantallas
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LoginScreen(name="login"))
        self.add_widget(InfoScreen(name="info"))


# Clase principal de la aplicación
class MyApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    MyApp().run()
