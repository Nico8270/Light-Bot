# LightBot - Comparación A* vs BFS

## Descripción del Proyecto

Este proyecto implementa una versión simplificada del juego LightBot donde un robot debe encender todas las luces azules en un tablero. El objetivo principal es comparar la eficiencia de dos algoritmos de búsqueda:

- **A*** (con heurística)
- **BFS** (búsqueda ciega)

## Reglas del Juego Simplificado

1. **Movimiento**: El robot puede moverse instantáneamente en 4 direcciones (arriba, abajo, izquierda, derecha) sin necesidad de girar.

2. **Objetivo**: Encender todas las luces azules del tablero.

3. **Acciones disponibles**:
   - **MOVER**: A una casilla adyacente (si no es obstáculo)
   - **ENCENDER**: La luz en la posición actual (si hay una luz apagada)

## Representación del Tablero

- **0**: Piso normal (el robot puede caminar)
- **1**: Obstáculo (el robot NO puede pasar)
- **2**: Casilla objetivo con luz azul (debe ser encendida)

## Algoritmos Implementados

### A* (A-Star)
- Utiliza una heurística optimista: `h(n) = luces_apagadas + distancia_a_luz_más_cercana`
- Explora nodos de manera inteligente priorizando los más prometedores
- Garantiza encontrar la solución óptima

### BFS (Breadth-First Search)
- Búsqueda ciega que explora todos los nodos nivel por nivel
- No utiliza información heurística
- Garantiza encontrar la solución óptima pero puede ser menos eficiente

## Estructura del Código

### Clases Principales

1. **Node**: Representa un estado del juego (posición del robot + estado de luces)
2. **GameState**: Maneja las reglas del juego y generación de sucesores
3. **AStar**: Implementación del algoritmo A*
4. **BFS**: Implementación del algoritmo BFS
5. **GameRenderer**: Renderizado visual del juego
6. **PriorityQueue**: Cola de prioridad para A*

### Niveles Incluidos

1. **Nivel 1**: Tablero 3x3 con 2 luces
2. **Nivel 2**: Tablero 4x4 con 3 luces y obstáculos
3. **Nivel 3**: Tablero 5x5 con 4 luces en laberinto complejo

## Cómo Usar

1. Selecciona un nivel usando los botones superiores
2. Haz clic en "Resolver con A*" o "Resolver con BFS"
3. Observa las estadísticas de rendimiento de cada algoritmo
4. Ve la animación de la solución encontrada

## Métricas de Comparación

Para cada algoritmo se muestran:
- **Nodos explorados**: Cantidad de estados visitados
- **Pasos de la solución**: Longitud del camino encontrado
- **Tiempo de ejecución**: Tiempo en milisegundos

## Resultados Esperados

Generalmente A* debería:
- Explorar menos nodos que BFS
- Encontrar la solución en menos tiempo
- Mantener la optimalidad de la solución

Esto demuestra la ventaja de usar información heurística en problemas de búsqueda.