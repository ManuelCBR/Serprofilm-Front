

import reflex as rx
import requests as rq

#Clase para recibir los datos del formulario
class Contact_Form_State(rx.State):
    name_surname: str
    email: str
    subject: str
    message: str

    def set_name_surname(self, value):
        self.name_surname = value
    def set_email(self, value):
        self.email = value
    def set_subject(self, value):
        self.subject = value
    def set_message(self, value):
        self.message = value

    #Petición al post del backend
    @rx.background
    async def submit_form(self):
        print("Form submitted")
        response = rq.post(
                "http://localhost:8000/contact",
                json={
                    "name_surname": self.name_surname,
                    "email": self.email,
                    "subject": self.subject,
                    "message": self.message
                }
        )

        #Quitar al desplegar
        if response.status_code == 200:
            print("Data sent successfully:", response.json())
        else:
            print("Failed to send data:", response.status_code)
        
#En el index es donde se establecen los componentes de la page con el mismo nombre
def index() -> rx.Component:
    return rx.box(
        rx.center(
            rx.vstack(
                rx.heading("Formulario de contacto"),
                contact_form(),
                max_width="30em",
                width="100%",
                align="center",
                margin_y="10px"
            ),
        )      
    )

#Formulario (Poner los componentes en ficheros independientes)
def contact_form():
    return rx.form(
        rx.input(placeholder="Nombre y apellidos", on_change=Contact_Form_State.set_name_surname),
        rx.input(placeholder="Email", on_change=Contact_Form_State.set_email),
        rx.input(placeholder="Asunto", on_change=Contact_Form_State.set_subject),
        rx.text_area(placeholder="Mensaje", on_change=Contact_Form_State.set_message),
        rx.button("Enviar", on_click=Contact_Form_State.submit_form)
    )

app = rx.App()
app.add_page(index)
