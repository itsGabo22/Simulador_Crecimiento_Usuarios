# analysis.py

import numpy as np

def generate_analysis_text(results, r, K, U0, a, t_max):
    """
    Analiza los resultados de la simulación y genera un texto de diagnóstico dinámico,
    emulando un análisis experto en tiempo real.
    """
    U_log = results["logistic"]["U"]
    dU_log = results["logistic"]["dU_dt"]
    U_soc = results["social"]["U"]
    dU_soc = results["social"]["dU_dt"]

    # --- Métricas Clave para el Diagnóstico ---
    final_U_log = U_log[-1]
    max_U_soc = np.max(U_soc)
    has_overshoot = max_U_soc > K * 1.01
    overshoot_percentage = ((max_U_soc - K) / K) * 100 if has_overshoot else 0
    has_churn = np.any(dU_soc < 0)
    min_dU_soc = np.min(dU_soc) if has_churn else 0
    
    # --- 1. DIAGNÓSTICO GENERAL ---
    diag_general = "### `[DIAGNÓSTICO GENERAL DEL SISTEMA]`\n\n"
    if final_U_log < K * 0.05 and r < 0.1:
        diag_general += "**Estado:** `Estancamiento`. El sistema muestra un crecimiento mínimo, casi imperceptible. La adquisición de usuarios es prácticamente nula."
    elif has_overshoot and overshoot_percentage > 10:
        diag_general += f"**Estado:** `Volatilidad Crítica`. Se detecta un sobreimpulso severo del **{overshoot_percentage:.1f}%** por encima de la capacidad. El sistema es inestable y propenso a ciclos de crecimiento y pérdida de usuarios."
    elif has_overshoot:
        diag_general += f"**Estado:** `Crecimiento Inestable`. El sistema exhibe un sobreimpulso moderado del **{overshoot_percentage:.1f}%**, indicando un 'momentum' viral que supera la capacidad sostenible antes de corregir."
    elif final_U_log > K * 0.9:
        diag_general += "**Estado:** `Saturación / Madurez`. El crecimiento se ha estabilizado cerca de la capacidad máxima. El sistema es predecible y ha alcanzado su madurez."
    else:
        diag_general += "**Estado:** `Crecimiento Activo`. La plataforma está en una fase de adquisición de usuarios saludable y manejable, evolucionando hacia su capacidad máxima."

    # --- 2. ANÁLISIS DE COMPORTAMIENTO ---
    analysis = "\n\n---\n### `[ANÁLISIS DE COMPORTAMIENTO]`\n\n"
    
    # Modelo Logístico (Baseline)
    analysis += "#### Modelo Logístico (Curva Azul - Baseline)\n"
    if final_U_log < K * 0.05:
        analysis += "**Observación:** Crecimiento **latente**. La curva es casi plana, indicando una fase inicial donde la adopción aún no ha despegado.\n"
    elif final_U_log < K * 0.8:
        analysis += "**Observación:** Fase de **aceleración**. La plataforma está ganando usuarios a un ritmo creciente. La curva 'S' está en pleno desarrollo, dirigiéndose hacia su punto de máxima velocidad.\n"
    else:
        analysis += "**Observación:** Fase de **saturación**. El crecimiento se desacelera notablemente al aproximarse al límite `K`, demostrando un mercado maduro o limitaciones de capacidad.\n"

    # Modelo Social (Sistema Dinámico)
    analysis += "\n#### Modelo Social (Curva Roja - Sistema Dinámico)\n"
    # Caracterización del sistema basado en 'a' (amortiguamiento)
    if a > 0.8:
        analysis += (
            f"**Caracterización:** Sistema **Sobreamortiguado** (`a={a:.2f}`). "
            "La alta fricción social elimina casi toda la inercia. El crecimiento es suave, estable y sin sorpresas, siguiendo de cerca al modelo logístico. Es un escenario de bajo riesgo."
        )
    elif a < 0.2 and has_overshoot:
        analysis += (
            f"**Caracterización:** Sistema **Subamortiguado** (`a={a:.2f}`). "
            "La baja fricción permite que la inercia del crecimiento domine, causando el sobreimpulso y las oscilaciones observadas. Este comportamiento es típico de fenómenos virales con correcciones posteriores."
        )
    else:
        analysis += (
            f"**Caracterización:** Sistema **Críticamente Amortiguado** (o cercano, `a={a:.2f}`). "
            "La fricción está balanceada con la inercia. Esto permite una estabilización rápida sin generar sobreimpulsos significativos, representando el escenario más eficiente para alcanzar la capacidad `K`."
        )

    # --- 3. ANÁLISIS DE VELOCIDAD (PULSO DEL SISTEMA) ---
    vel_analysis = "\n\n---\n### `[ANÁLISIS DE VELOCIDAD (dU/dt)]`\n\n"
    max_dU_log = np.max(dU_log)
    max_dU_soc = np.max(dU_soc)

    if max_dU_log < 10: # Umbral para estancamiento
        vel_analysis += (
            "**Diagnóstico de Velocidad:** `Estancada`. La tasa de adquisición es inferior a 10 usuarios/día. "
            "No se observan picos de demanda; la carga sobre el sistema es mínima y constante."
        )
    else:
        vel_analysis += (
            f"**Diagnóstico de Velocidad:** `Dinámica`. Se observa un pico de demanda claro. "
            f"El modelo social predice una demanda máxima de **{max_dU_soc:,.0f} usuarios/día**, "
            f"un **{((max_dU_soc - max_dU_log) / max_dU_log) * 100:+.1f}%** respecto al modelo base. "
            "Este es el punto de máxima carga para los servicios de registro y backend."
        )

    if has_churn:
        vel_analysis += (
            f"\n\n**Alerta de Churn:** Se detecta una fase de **pérdida de usuarios** con un mínimo de **{min_dU_soc:,.0f} usuarios/día**. "
            "Esto confirma la corrección post-viralidad y representa un riesgo para la retención a largo plazo."
        )

    # --- 4. IMPLICACIONES DE INGENIERÍA Y ESTRATEGIA ---
    conclusion = "\n\n---\n### `[IMPLICACIONES DE INGENIERÍA Y ESTRATEGIA]`\n\n"
    if has_overshoot:
        conclusion += (
            f"**Recomendación:** `Diseño para la Resiliencia`. El sobreimpulso del **{overshoot_percentage:.1f}%** exige una arquitectura elástica. "
            "Implementar **autoescalado, limitadores de tasa (rate limiting) y colas de mensajes** es crucial para absorber picos de demanda y evitar caídas del servicio. "
            f"El escenario (`r={r}`, `a={a:.2f}`) es de alto riesgo y alta recompensa."
        )
    elif final_U_log < K * 0.1 and r < 0.1:
        conclusion += (
            "**Recomendación:** `Estrategia de Activación`. El crecimiento está estancado. "
            "El foco de ingeniería debe ser la **optimización del 'onboarding' y la mejora del producto** para aumentar el valor intrínseco. "
            "Desde negocio, se requiere validar el 'product-market fit' antes de invertir en marketing (aumentar `r`)."
        )
    else:
        conclusion += (
            "**Recomendación:** `Optimización y Escalabilidad Sostenible`. El crecimiento es predecible. "
            "El foco de ingeniería debe ser la **optimización de costos de infraestructura, la mejora del rendimiento y la fiabilidad (SRE)**. "
            "Es el momento ideal para refactorizar deuda técnica y fortalecer la plataforma para el largo plazo."
        )

    return diag_general + analysis + vel_analysis + conclusion