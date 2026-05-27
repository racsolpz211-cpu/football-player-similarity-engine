"""
Interfaz de Línea de Comandos (CLI) del Scouting Engine.

Proporciona un punto de entrada interactivo en terminal para interactuar con 
el motor matemático subyacente. Actúa como controlador (Controller en MVC)
conectando el input del usuario con los algoritmos del modelo (`ScoutEngine`).
Ideal para analistas de datos o pruebas rápidas sin levantar el Frontend completo.
"""
import warnings
import pandas as pd
from src.data.loader import DataLoader
from src.models.scouting_engine import ScoutEngine

# Silenciamos warnings estéticos de Pandas (e.g., SettingWithCopyWarning) 
# para garantizar que la salida estándar (STDOUT) de la terminal quede limpia para el usuario.
warnings.filterwarnings('ignore')

def main():
    """
    Bucle principal de ejecución del CLI interactivo (REPL - Read-Eval-Print Loop).
    """
    print("==================================================")
    print("🚀 INICIANDO TERMINAL DE SCOUTING (TFG IA) 🚀")
    print("==================================================")
    print("Cargando base de datos y motor matemático... (Esto puede tardar unos segundos)\n")

    # --- 1. FASE DE BOOTSTRAP (Carga en memoria) ---
    # Instanciamos el motor una sola vez antes del bucle interactivo para evitar 
    # la penalización de I/O (lectura de disco) en cada nueva búsqueda.
    try:
        loader = DataLoader()
        # Se asume que el pipeline ETL ya fue ejecutado y generó el parquet procesado.
        df_scouting = loader.load_processed_dataset("scouting_dataset.parquet")
        # El threshold de 200 mins previene errores matemáticos (outliers por varianza extrema) en el PCA.
        engine = ScoutEngine(df_scouting, base_min_minutes=200)
        print("✅ Motor cargado correctamente. ¡Listo para buscar!\n")
    except Exception as e:
        print(f"❌ Error crítico al arrancar: No se pudo levantar el motor. Detalle: {e}")
        return

    # --- 2. BUCLE INTERACTIVO INFINITO ---
    while True:
        print("--------------------------------------------------")
        print("💡 Escribe 'ver' para listar todas las métricas disponibles.")
        target = input("🔍 Nombre del jugador a buscar (o 'salir'): ").strip()

        # Condición de salida (Graceful shutdown)
        if target.lower() in ['salir', 'exit', 'quit']:
            print("👋 ¡Cerrando terminal de scouting! Buen trabajo.")
            break

        # Utilidad de descubrimiento: Imprime el Feature Space actual disponible en memoria
        if target.lower() == 'ver':
            print("\n📊 MÉTRICAS DISPONIBLES (Copia y pega las que quieras):")
            for i, col in enumerate(engine.all_numeric_features):
                print(f"{col:<35}", end="")
                if (i + 1) % 3 == 0: print()
            print("\n")
            continue

        if not target:
            continue

        # --- RECOLECCIÓN DE PARÁMETROS (Input Binding) ---
        target_season = input("📅 Temporada del jugador objetivo (ej. 2324) [Enter: más reciente]: ").strip()
        target_season = target_season if target_season else None

        result_season = input("⏱️  Temporada de los resultados (ej. 2425) [Enter: todas]: ").strip()
        result_seasons = [result_season] if result_season else None

        result_team = input("🛡️  Filtrar por equipo específico [Enter: todos]: ").strip()
        result_team = result_team if result_team else None

        min_mins_input = input("⏳ Minutos mínimos exigidos [Enter: 900]: ").strip()
        min_minutes = int(min_mins_input) if min_mins_input.isdigit() else 900

        # --- CONFIGURACIÓN DEL ESPACIO VECTORIAL (Feature Selection) ---
        print("\n🎯 SELECCIÓN DE ATRIBUTOS:")
        print("Escribe las métricas separadas por comas (ej: Performance_Gls_90, Standard_Sh_90)")
        attrs_input = input("👉 Atributos específicos [Enter para Búsqueda General con PCA]: ").strip()

        selected_features = None
        if attrs_input:
            # Parseo y validación estricta de las métricas ingresadas vs las disponibles en el engine
            raw_attrs = [a.strip() for a in attrs_input.split(',')]
            selected_features = [f for f in raw_attrs if f in engine.all_numeric_features]

            invalid_attrs = [a for a in raw_attrs if a not in engine.all_numeric_features]
            if invalid_attrs:
                print(f"⚠️  Aviso: Estas métricas no existen y serán ignoradas por seguridad: {invalid_attrs}")

            if not selected_features:
                print("❌ Ninguna de las métricas introducidas es válida. Cayendo de vuelta a Búsqueda General.")
                selected_features = None

        # --- SELECCIÓN DE ALGORITMO MATEMÁTICO ---
        print("\n📐 MÉTRICA DE DISTANCIA:")
        metric_input = input("Elige 'cosine' (estilo), 'euclidean' (volumen) o 'hybrid' (ambas) [Enter para hybrid]: ").strip().lower()
        metric_choice = metric_input if metric_input in ['cosine', 'euclidean', 'hybrid'] else 'hybrid'

        alpha_choice = 0.5
        if metric_choice == 'hybrid':
            alpha_input = input("🎛️  Introduce el peso Alfa para el Coseno (0.0 a 1.0) [Enter para 0.5]: ").strip()
            try:
                alpha_choice = float(alpha_input) if alpha_input else 0.5
                # Clamp del valor alfa entre 0 y 1 para que la ecuación no se rompa
                if not (0.0 <= alpha_choice <= 1.0): alpha_choice = 0.5
            except ValueError:
                alpha_choice = 0.5

        # --- EJECUCIÓN ALGORÍTMICA (Delegación al Modelo) ---
        modo_str = "BÚSQUEDA ESPECÍFICA (Raw Vecs)" if selected_features else "BÚSQUEDA GENERAL (PCA 90% Var)"
        print(f"\n⚙️  Analizando {modo_str} usando métrica '{metric_choice.upper()}'...")

        try:
            # Despachamos la carga matemática a ScoutEngine
            resultados = engine.find_similar_players(
                target_player_name=target,
                target_season=target_season,
                result_seasons=result_seasons,
                result_team=result_team,
                min_minutes=min_minutes,
                features=selected_features,
                metric=metric_choice,
                alpha=alpha_choice,
                top_n=5
            )

            if resultados.empty:
                print("⚠️ No se encontraron jugadores que cumplan matemáticamente todos los filtros de negocio.")
            else:
                print("\n🏆 RESULTADOS ENCONTRADOS:\n")
                # Volcado tabular usando Markdown para legibilidad en consola
                print(resultados.to_markdown())

        except ValueError as ve:
            print(f"❌ Aviso de Lógica de Negocio: {ve}")
        except Exception as e:
            print(f"❌ Error Técnico Inesperado: {e}")

        print("\n")

if __name__ == "__main__":
    import logging
    # Se silencian los logs técnicos del backend (INFO/DEBUG) para no ensuciar 
    # la interfaz limpia de la línea de comandos, manteniendo solo WARNING/ERROR.
    logging.getLogger('src.models.scouting_engine').setLevel(logging.WARNING)
    logging.getLogger('src.data.loader').setLevel(logging.WARNING)
    main()