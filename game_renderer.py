"""
Clase para mostrar el estado del juego en consola
"""

class GameRenderer:
    def __init__(self):
        self.symbols = {
            0: '.',  # Piso normal
            1: '#',  # Obstáculo
            2: 'L',  # Luz apagada
            'light_on': '✓',  # Luz encendida
            'robot': 'R',     # Robot
            'robot_on_light': '@'  # Robot en luz encendida
        }

    def render_level(self, level, robot_x, robot_y, light_states=None):
        """Renderiza un nivel en la consola"""
        grid = level['grid']
        rows = len(grid)
        cols = len(grid[0])
        
        # Si no se proporcionan estados de luces, todas están apagadas
        if light_states is None:
            light_count = self._count_lights(grid)
            light_states = [0] * light_count
        
        print(f"\n=== {level['name']} ===")
        print(f"Descripción: {level['description']}")
        print()
        
        # Crear representación visual
        display_grid = []
        for i in range(rows):
            row = []
            for j in range(cols):
                cell = self._get_cell_symbol(grid[i][j], i, j, robot_x, robot_y, light_states, grid)
                row.append(cell)
            display_grid.append(row)
        
        # Mostrar el tablero
        for row in display_grid:
            print(' '.join(f'{cell:^3}' for cell in row))
        
        print()
        self._show_legend()

    def _get_cell_symbol(self, cell_type, row, col, robot_x, robot_y, light_states, grid):
        """Determina el símbolo a mostrar en una celda"""
        # Si el robot está aquí
        if row == robot_x and col == robot_y:
            if cell_type == 2:  # Robot en una luz
                light_index = self._get_light_index(row, col, grid)
                if light_index is not None and light_states[light_index] == 1:
                    return self.symbols['robot_on_light']
                else:
                    return self.symbols['robot']
            else:
                return self.symbols['robot']
        else:
            # Celda sin robot
            if cell_type == 0:
                return self.symbols[0]
            elif cell_type == 1:
                return self.symbols[1]
            elif cell_type == 2:
                light_index = self._get_light_index(row, col, grid)
                if light_index is not None and light_states[light_index] == 1:
                    return self.symbols['light_on']
                else:
                    return self.symbols[2]

    def _get_light_index(self, row, col, grid):
        """Obtiene el índice de una luz en las posiciones de luces"""
        light_positions = self._get_light_positions(grid)
        for i, (lx, ly) in enumerate(light_positions):
            if lx == row and ly == col:
                return i
        return None

    def _get_light_positions(self, grid):
        """Obtiene todas las posiciones de luces en el nivel"""
        positions = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 2:
                    positions.append((i, j))
        return positions

    def _count_lights(self, grid):
        """Cuenta el número total de luces en el nivel"""
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 2:
                    count += 1
        return count

    def _show_legend(self):
        """Muestra la leyenda de símbolos"""
        print("Leyenda:")
        print(f"  {self.symbols[0]} = Piso normal")
        print(f"  {self.symbols[1]} = Obstáculo")
        print(f"  {self.symbols[2]} = Luz apagada")
        print(f"  {self.symbols['light_on']} = Luz encendida")
        print(f"  {self.symbols['robot']} = Robot")
        print(f"  {self.symbols['robot_on_light']} = Robot en luz encendida")
        print()

    def show_solution(self, path):
        """Muestra la solución encontrada"""
        if not path:
            print("¡El robot ya está en la meta!")
            return
        
        print("Solución encontrada:")
        for i, step in enumerate(path, 1):
            print(f"  {i}. {step}")
        print()

    def show_stats(self, astar_result, bfs_result):
        """Muestra las estadísticas de comparación"""
        print("\n" + "="*60)
        print("📊 COMPARACIÓN DE ALGORITMOS")
        print("="*60)
        print()
        print("A* (Heurística - Algoritmo Informado):")
        print(f"  Nodos explorados: {astar_result['nodes_explored']}")
        print(f"  Pasos solución: {astar_result['steps']}")
        print(f"  Tiempo: {astar_result['execution_time']:.2f}ms")
        print()
        print("BFS (Búsqueda Ciega - Sin información):")
        print(f"  Nodos explorados: {bfs_result['nodes_explored']}")
        print(f"  Pasos solución: {bfs_result['steps']}")
        print(f"  Tiempo: {bfs_result['execution_time']:.2f}ms")
        print()
    
        if astar_result['success'] and bfs_result['success']:
            print("=== ANÁLISIS DE EFICIENCIA ===")
            efficiency_nodes = ((bfs_result['nodes_explored'] - astar_result['nodes_explored']) / bfs_result['nodes_explored']) * 100
        
            # Evitar división por cero en tiempo
            if bfs_result['execution_time'] > 0 and astar_result['execution_time'] > 0:
                efficiency_time = ((bfs_result['execution_time'] - astar_result['execution_time']) / bfs_result['execution_time']) * 100
                print(f"📈 A* exploró {efficiency_nodes:.1f}% menos nodos que BFS")
                if efficiency_time > 0:
                    print(f"⚡ A* fue {efficiency_time:.1f}% más rápido que BFS")
                else:
                    print(f"🐢 BFS fue {abs(efficiency_time):.1f}% más rápido que A*")
            else:
                print(f"📈 A* exploró {efficiency_nodes:.1f}% menos nodos que BFS")
                print("⏱️  El tiempo de ejecución es muy rápido para comparar")

    def show_visited_path(self, level, visited_nodes, algorithm_name):
        """Muestra el recorrido de nodos visitados por el algoritmo"""
        print(f"\n" + "="*60)
        print(f"🗺️  RECORRIDO DE {algorithm_name} - {len(visited_nodes)} NODOS VISITADOS")
        print("="*60)
    
        # Crear grid para mostrar el recorrido
        grid = level['grid']
        rows = len(grid)
        cols = len(grid[0])
    
        # Matriz para almacenar el orden de visita
        visit_grid = [[0] * cols for _ in range(rows)]
    
        for node in visited_nodes:
            if 0 <= node.x < rows and 0 <= node.y < cols:
                visit_grid[node.x][node.y] = node.visited_order
    
        print("\nOrden de visita en cada celda (0 = no visitado):")
        print("-" * (cols * 4))
    
        for i in range(rows):
            row_display = []
            for j in range(cols):
                if grid[i][j] == 1:  # Obstáculo
                    row_display.append(" ### ")
                elif visit_grid[i][j] > 0:
                    row_display.append(f"{visit_grid[i][j]:>4d}")
                else:
                    row_display.append("   . ")
            print(" ".join(row_display))
    
        print("-" * (cols * 4))
        print(f"Total de nodos únicos visitados: {len(set((node.x, node.y) for node in visited_nodes))}")

    def show_algorithm_progress(self, level, result, algorithm_name):
        """Muestra el progreso completo del algoritmo"""
        print(f"\n" + "="*60)
        print(f"📊 {algorithm_name} - RESULTADOS DETALLADOS")
        print("="*60)
    
        if result['success']:
            print(f"✅ ¡Solución encontrada en {result['steps']} pasos!")
            print(f"🔍 Nodos explorados: {result['nodes_explored']}")
            print(f"⏱️  Tiempo: {result['execution_time']:.2f}ms")
        
            # Mostrar recorrido de visita
            self.show_visited_path(level, result['visited_nodes'], algorithm_name)
        
            # Mostrar camino solución
            print(f"\n🛣️  CAMINO SOLUCIÓN ({algorithm_name}):")
            self.show_solution(result['path'])
        else:
            print("❌ No se encontró solución")
            print(f"🔍 Nodos explorados: {result['nodes_explored']}")
            print(f"⏱️  Tiempo: {result['execution_time']:.2f}ms")
        
            # Mostrar recorrido de visita aunque no haya solución
            self.show_visited_path(level, result['visited_nodes'], algorithm_name)