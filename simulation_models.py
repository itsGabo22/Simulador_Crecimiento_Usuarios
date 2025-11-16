# simulation_models.py

import numpy as np
from scipy.integrate import solve_ivp

def logistic_model(t, U, r, K):
    """Define la ecuación diferencial logística de primer orden."""
    return r * U[0] * (1 - U[0] / K)

def social_acceleration_model(t, y, r, K, a):
    """
    Define el sistema de EDOs para el modelo de segundo orden.
    y[0] = U (usuarios), y[1] = dU/dt (velocidad).
    """
    y0, y1 = y
    dy0_dt = y1
    dy1_dt = r * y0 * (1 - y0 / K) - a * y1
    return [dy0_dt, dy1_dt]

def run_simulations(r, K, U0, a, t_max):
    """
    Ejecuta las simulaciones para ambos modelos y devuelve los resultados.
    Esta función NO dibuja, solo calcula los datos.
    """
    t_span = [0, t_max]
    t_eval = np.linspace(t_span[0], t_span[1], 500)

    # --- Simulación del Modelo 1 (Logístico) ---
    sol_logistic = solve_ivp(
        fun=logistic_model,
        t_span=t_span,
        y0=[U0],
        args=(r, K),
        t_eval=t_eval
    )
    
    # --- Simulación del Modelo 2 (Aceleración Social) ---
    U_prime_0 = r * U0 * (1 - U0 / K) # Velocidad inicial
    initial_conditions_2nd_order = [U0, U_prime_0]

    sol_social = solve_ivp(
        fun=social_acceleration_model,
        t_span=t_span,
        y0=initial_conditions_2nd_order,
        args=(r, K, a),
        t_eval=t_eval
    )

    # Empaquetar resultados en un diccionario para fácil acceso
    results = {
        "t_eval": t_eval,
        "logistic": {
            "U": sol_logistic.y[0],
            "dU_dt": r * sol_logistic.y[0] * (1 - sol_logistic.y[0] / K)
        },
        "social": {
            "U": sol_social.y[0],
            "dU_dt": sol_social.y[1]
        }
    }
    
    return results
