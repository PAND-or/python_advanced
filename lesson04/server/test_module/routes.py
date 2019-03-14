from .controllers import send_presence


routes = [
    {'action': 'presence', 'controller': send_presence}
]