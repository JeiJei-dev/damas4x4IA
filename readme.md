## Damas 4x4

Este proyecto es un juego de Damas en un tablero de 4x4, implementado en Python utilizando la biblioteca Pygame. El juego permite a un jugador humano competir contra una inteligencia artificial que utiliza el algoritmo Minimax para decidir sus movimientos.

### Requisitos

Para ejecutar este proyecto, necesitarás tener Python y Pygame instalados en tu sistema. A continuación, se detallan los pasos necesarios para instalar las dependencias y ejecutar el juego.

### Instalación

1. **Instalar Python**: Asegúrate de tener Python instalado en tu máquina. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).

2. **Instalar Pygame**: Una vez que Python esté instalado, abre una terminal o línea de comandos y ejecuta el siguiente comando para instalar Pygame:

   ```bash
   pip install pygame
   ```

### Ejecución del Programa

Una vez que hayas instalado Pygame, puedes ejecutar el juego siguiendo estos pasos:

1. **Navegar al directorio del proyecto**: Usa la terminal o línea de comandos para navegar hasta el directorio donde se encuentra el archivo `main.py`.

2. **Ejecutar el juego**: Ejecuta el programa con el siguiente comando:

   ```bash
   python main.py
   ```

### Controles del Juego

- **Seleccionar pieza**: Haz clic en una pieza de tu color (azul).
- **Mover pieza**: Haz clic en una casilla vacía en diagonal o en una casilla donde puedas capturar una pieza del oponente (roja).
- El juego alterna turnos entre el jugador humano y el cpu

### Descripción del Código

El archivo `main.py` contiene toda la lógica del juego, incluyendo:

- Inicialización de Pygame y configuración de la pantalla.
- Definición del tablero y las piezas.
- Funciones para dibujar el tablero, mover piezas, verificar movimientos válidos y determinar ganadores.
- Implementación del algoritmo Minimax para la IA.
