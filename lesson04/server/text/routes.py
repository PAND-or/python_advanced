from .controllers import get_lower_text
from .controllers import get_upper_text



routes = [
    {'action': 'lower_text', 'controller': get_lower_text},
    {'action': 'upper_text', 'controller': get_upper_text}
]