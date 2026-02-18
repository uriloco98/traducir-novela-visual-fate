# traducir-novela-visual-fate



markdown
# Fate/Stay Night - Script Translator & XP3 Packager 🛠️

Una herramienta de automatización de alto rendimiento diseñada para la localización y reconstrucción de archivos del motor **Kirikiri (KAG)**. Este proyecto automatiza el ciclo completo de traducción, desde la limpieza de scripts hasta el empaquetado final del parche `.xp3`.

## ✨ Características Principales

- **⚙️ Procesamiento Concurrente:** Implementación de `ThreadPoolExecutor` para la traducción multihilo, reduciendo drásticamente los tiempos de espera.
- **🛡️ Protección de Sintaxis KAG:** Algoritmo basado en **Regex** que identifica y protege etiquetas de motor (ej: `[l]`, `[r]`, `[wait]`) para evitar que el traductor las corrompa.
- **💾 Sistema de Caché Persistente:** Motor de memoria basado en JSON que evita traducciones duplicadas, optimizando el uso de la API y permitiendo reanudar procesos interrumpidos.
- **📂 Clonación de Recursos:** Gestión inteligente de archivos que diferencia entre scripts traducibles y activos multimedia (imágenes, audio, video), manteniendo la integridad de la estructura original.
- **📟 Interfaz de Usuario Moderna:** Experiencia en consola enriquecida mediante la librería `rich`, con barras de progreso dinámicas por archivo y estadísticas globales en tiempo real.
- **🏗️ Arquitectura Desacoplada:** Configuración gestionada mediante archivos `.ini`, separando la lógica del negocio de los datos del entorno.

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **Librerías Clave:** 
  - `deep-translator` (Motor de traducción)
  - `rich` (Interfaz CLI avanzada)
  - `configparser` (Gestión de configuración)
  - `re` (Procesamiento de patrones complejos)

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com
Usa el código con precaución.

Instalar dependencias:
bash
pip install deep-translator rich
Usa el código con precaución.

Configurar el entorno:
Edita el archivo config.ini con las rutas locales de tus carpetas de proyecto y la herramienta xp3.py.
Ejecutar:
bash
python main.py
Usa el código con precaución.

📊 Detalles Técnicos Destacables
Manejo de Codificación (Encoding)
El script garantiza la compatibilidad con el motor original mediante el forzado de codificación UTF-16 LE con BOM, asegurando que caracteres especiales como la ñ y tildes se rendericen correctamente en el juego.
Resiliencia de Red
Implementa un sistema de reintentos exponenciales para manejar errores de conexión o límites de tasa (Rate Limiting) de la API de traducción, asegurando que el proceso no se detenga ante fallos menores de red.
Desarrollado con ❤️ para la comunidad de Visual Novels.
