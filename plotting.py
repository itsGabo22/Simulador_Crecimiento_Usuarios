# plotting.py

import matplotlib.pyplot as plt

def create_plots(results, r, K, a):
    """
    Genera las figuras de Matplotlib a partir de los resultados de la simulación.
    Devuelve el objeto 'figure' para que Streamlit pueda mostrarlo.
    """
    t_eval = results["t_eval"]
    U_logistic = results["logistic"]["U"]
    dU_dt_logistic = results["logistic"]["dU_dt"]
    U_social = results["social"]["U"]
    dU_dt_social = results["social"]["dU_dt"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfica 1: Crecimiento de Usuarios U(t)
    ax1.plot(t_eval, U_logistic, label='Modelo Logístico (1er Orden)', color='blue')
    ax1.plot(t_eval, U_social, label=f'Modelo Social (2do Orden, a={a:.2f})', color='red', linestyle='--')
    ax1.axhline(y=K, color='gray', linestyle=':', label=f'Capacidad Máxima (K={K})')
    ax1.set_title('Crecimiento de Usuarios U(t)')
    ax1.set_xlabel('Tiempo (días)')
    ax1.set_ylabel('Número de Usuarios (U)')
    ax1.legend()
    ax1.grid(True, linestyle='--', linewidth=0.5)
    ax1.set_ylim(0, K * 1.5)

    # Gráfica 2: Velocidad de Crecimiento dU/dt
    ax2.plot(t_eval, dU_dt_logistic, label='Velocidad Logística', color='blue')
    ax2.plot(t_eval, dU_dt_social, label=f'Velocidad Social (a={a:.2f})', color='red', linestyle='--')
    ax2.set_title('Velocidad de Crecimiento dU/dt')
    ax2.set_xlabel('Tiempo (días)')
    ax2.set_ylabel('Nuevos Usuarios por Día (dU/dt)')
    ax2.legend()
    ax2.grid(True, linestyle='--', linewidth=0.5)

    fig.tight_layout()
    
    return fig
