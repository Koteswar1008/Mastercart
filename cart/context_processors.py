# cart/context_processors.py
from .cart import Cart

def cart(request):
    """
    Adds cart information to the context for all templates.
    """
    
    
    return {'cart' : Cart(request)}
