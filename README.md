# Sistema de Soporte a la Decisión (DSS) en Fútbol: Motor de Similitud de Jugadores

## 1. Descripción del Proyecto

Este proyecto es un Sistema de Soporte a la Decisión (DSS) basado en datos, diseñado para el ámbito del fútbol profesional. Su objetivo principal es identificar jugadores estilísticamente similares utilizando métricas estadísticas avanzadas y algoritmos de Machine Learning. El motor procesa datos brutos de rendimiento de jugadores y equipos, genera un conjunto avanzado de características (feature engineering) y emplea modelos matemáticos para calcular la similitud, permitiendo encontrar alternativas en el mercado de fichajes con una alta precisión.

**Autor:** Oscar López Andreu

---

## 2. Funcionamiento y Características Principales

El núcleo de la aplicación reside en su capacidad de aislar y contextualizar el rendimiento del jugador:

* **Normalización por 90 minutos:** Transforma estadísticas de volumen bruto en métricas per-90, permitiendo una comparación justa entre jugadores con diferentes minutos disputados.
* **Ajuste por Posesión (PAdj):** Contextualiza las acciones defensivas y ofensivas según la posesión del equipo. (Ej. No es lo mismo realizar 5 intercepciones en un equipo con 30% de posesión media que en uno con 70%).
* **Coeficiente UEFA (Ajuste por Liga):** Ajusta las estadísticas de cada jugador ponderando la dificultad de su liga nacional mediante los coeficientes históricos de la UEFA, homogenizando las comparativas entre ligas de diferente nivel competitivo.
* **Reducción de Dimensionalidad (PCA) y Similitud Vectorial:** Emplea Análisis de Componentes Principales (PCA) para limpiar el ruido de los datos y utiliza la similitud de coseno (o euclidiana/híbrida) en un espacio n-dimensional para medir la semejanza pura de perfiles y estilos de juego.

---

## 3. Origen de los Datos

El sistema se alimenta de fuentes de datos de primer nivel mediante un proceso ETL (Extracción, Transformación y Carga) automatizado:
1. **Kaggle Datasets:** Extracción de estadísticas individuales detalladas de rendimiento de los jugadores.
2. **FBref (vía `soccerdata`):** Extracción automatizada (web scraping) de datos a nivel de equipo, fundamentalmente estadísticas de posesión y contexto competitivo general.

---

## 4. Tecnologías Utilizadas

Este proyecto ha sido desarrollado utilizando un stack tecnológico enfocado en la ciencia de datos y el machine learning:

* **Lenguaje Core:** Python 3.8+
* **Procesamiento y Análisis de Datos:** Pandas, NumPy
* **Machine Learning:** Scikit-learn (PCA, StandardScaler, medidas de distancia vectoriales)
* **Adquisición de Datos (Scraping y APIs):** `soccerdata` (FBref scraping), `kagglehub`
* **Almacenamiento Eficiente:** PyArrow (para lectura/escritura en formato Parquet)
* **Frontend y Visualización:** Streamlit (interfaz gráfica UI), Plotly (radares y gráficos interactivos)

---

## 5. Estructura del Proyecto

```text
/
├── data/
│   ├── raw/           # Datos brutos descargados
│   └── processed/     # Datasets finales listos para el motor
├── src/
│   ├── data/          # Scripts de ingesta (Kaggle/FBref) y creación del dataset maestro
│   ├── features/      # Ingeniería de características (Per-90, PAdj, Coeficientes)
│   └── models/        # Motor de similitud matemática (ScoutEngine)
├── frontend/          # Interfaz gráfica de usuario en Streamlit (Páginas, Utilidades, i18n)
├── cli.py             # Interfaz de línea de comandos para análisis rápido en terminal
├── app.py             # Archivo principal de ejecución del frontend
└── requirements.txt   # Dependencias necesarias para ejecutar el proyecto
```

---

## 6. Instrucciones de Ejecución

### 6.1. Requisitos e Instalación

Es necesario disponer de **Python 3.8+**.
1. Clona el repositorio y sitúate en la raíz del proyecto.
2. (Recomendado) Crea un entorno virtual para no interferir con las librerías globales de tu sistema.
3. Instala todas las dependencias necesarias:
```sh
pip install -r requirements.txt
```
*(Nota: El archivo `requirements.txt` ya incluye todas las dependencias completas y actualizadas para procesar datos, entrenar modelos y desplegar el frontend como `pandas`, `scikit-learn`, `streamlit`, `plotly` y `soccerdata`).*

### 6.2. Construcción del Dataset (Data Pipeline)

Antes de buscar jugadores, se debe ejecutar el pipeline de datos para descargar, unificar y procesar la información. Ejecuta estos comandos en orden desde la raíz del proyecto:

```sh
# 1. Descargar datos brutos
python -m src.data.ingest_players
python -m src.data.ingest_possession

# 2. Unificar en un dataset maestro
python -m src.data.create_master

# 3. Aplicar ajustes estadísticos (Per-90, PAdj, Coeficiente UEFA)
python -m src.data.build_features
```
*Al finalizar, el archivo `scouting_dataset.parquet` se generará en la carpeta `data/processed/` y el motor estará listo para funcionar.*

### 6.3. Interfaz de Línea de Comandos (CLI)

Para realizar búsquedas y análisis directamente desde la terminal de forma rápida:

```sh
python cli.py
```
* Sigue las instrucciones interactivas por consola.
* Podrás aplicar filtros de minutos, ligas, y seleccionar métricas concretas o permitir que el algoritmo utilice PCA para búsquedas de similitud general.

### 6.4. Interfaz Gráfica Avanzada (Frontend UI)

El proyecto incluye una aplicación web interactiva desarrollada con Streamlit. Dispone de visualizaciones interactivas, radares de percentiles y tablas dinámicas para facilitar el análisis visual.

Para lanzarla, ejecuta:
```sh
streamlit run app.py
```
*Se abrirá automáticamente tu navegador web (por defecto en `http://localhost:8501`) con el DSS listo para usarse.*

---

## 7. Próximas Funcionalidades (Roadmap)

* 🚀 **Sistema de Simulación de Impacto en Equipos (Próximamente):** Se integrará un nuevo módulo avanzado capaz de simular y proyectar el impacto estadístico que tendría un jugador si fuera traspasado a un equipo diferente. Este sistema adaptará su perfil individual al ecosistema táctico y volumen de juego de su posible nuevo club.