import panel as pn

pn.extension(design="material")

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    message = f"Echoing {user}: {contents}"
    return message


chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send(
    "enetr a message and receive an echo!",
    user="System",
    respond=False,
)

chat_interface.servable()