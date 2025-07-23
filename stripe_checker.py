
import random

def check_card(number, month, year, cvc):
    # Simulación: Stripe test
    endings = {
        "0005": "Fondos insuficientes",
        "0101": "CVV incorrecto",
        "0003": "Tarjeta robada",
        "4242": "Aprobada",
    }

    ending = number[-4:]
    if ending in endings:
        return {
            "status": "LIVE" if ending == "4242" else "DEAD",
            "message": endings[ending]
        }
    return {
        "status": "DEAD",
        "message": "Tarjeta rechazada"
    }
