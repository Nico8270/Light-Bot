"""
Juego LightBot - Comparación A* vs BFS
"""
from game_state import GameState
from game_renderer import GameRenderer
from astar import AStar
from bfs import BFS
from levels import get_level

class LightBotGame:
    def __init__(self):
        self.renderer = GameRenderer()
        self.current_level = None
        self.game_state = None

    def play(self):
        """Inicia el juego principal"""
        print("🤖 LIGHTBOT - Comparación de algoritmos A* vs BFS")
        print("=" * 50)
        
        while True:
            self._show_menu()
            choice = input("Selecciona una opción: ").strip()
            
            if choice == '1':
                self._play_level(1)
            elif choice == '2':
                self._play_level(2)
            elif choice == '3':
                self._play_level(3)
            elif choice == '4':
                self._compare_all_levels()
            elif choice == '5':
                self._manual_play()
            elif choice == '6':
                print("¡Gracias por jugar!")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")

    def _show_menu(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 50)
        print("MENÚ PRINCIPAL")
        print("=" * 50)
        print("1. Resolver Nivel 1 (Básico)")
        print("2. Resolver Nivel 2 (Intermedio)")
        print("3. Resolver Nivel 3 (Avanzado)")
        print("4. Comparar todos los niveles")
        print("5. Juego manual (adivinar camino)")
        print("6. Salir")
        print()

    def _play_level(self, level_number):
        """Resuelve un nivel específico con ambos algoritmos"""
        level = get_level(level_number)
        robot_x, robot_y = level['robot_start']
        
        self.game_state = GameState(level['grid'], robot_x, robot_y)
        self.renderer.render_level(level, robot_x, robot_y)
        
        print("Resolviendo con A*...")
        astar_solver = AStar(self.game_state)
        astar_result = astar_solver.solve()
        
        print("Resolviendo con BFS...")
        bfs_solver = BFS(self.game_state)
        bfs_result = bfs_solver.solve()
        
        # Mostrar resultados
        self.renderer.show_stats(astar_result, bfs_result)
        
        if astar_result['success']:
            self.renderer.show_solution(astar_result['path'])
        else:
            print("No se encontró solución.")

    def _compare_all_levels(self):
        """Compara el rendimiento en todos los niveles"""
        print("\n🔍 COMPARACIÓN COMPLETA DE TODOS LOS NIVELES")
        print("=" * 60)
        
        total_astar_nodes = 0
        total_bfs_nodes = 0
        total_astar_time = 0
        total_bfs_time = 0
        
        for level_num in [1, 2, 3]:
            level = get_level(level_num)
            robot_x, robot_y = level['robot_start']
            
            game_state = GameState(level['grid'], robot_x, robot_y)
            
            print(f"\n--- {level['name']} ---")
            
            # Resolver con A*
            astar_solver = AStar(game_state)
            astar_result = astar_solver.solve()
            
            # Resolver con BFS
            bfs_solver = BFS(game_state)
            bfs_result = bfs_solver.solve()
            
            # Acumular estadísticas
            total_astar_nodes += astar_result['nodes_explored']
            total_bfs_nodes += bfs_result['nodes_explored']
            total_astar_time += astar_result['execution_time']
            total_bfs_time += bfs_result['execution_time']
            
            # Mostrar resultados del nivel
            print(f"A*:  {astar_result['nodes_explored']:3d} nodos, {astar_result['steps']:2d} pasos, {astar_result['execution_time']:6.2f}ms")
            print(f"BFS: {bfs_result['nodes_explored']:3d} nodos, {bfs_result['steps']:2d} pasos, {bfs_result['execution_time']:6.2f}ms")
        
        # Mostrar resumen total
        print("\n" + "=" * 60)
        print("RESUMEN TOTAL:")
        print(f"A*:  {total_astar_nodes:3d} nodos totales, {total_astar_time:6.2f}ms totales")
        print(f"BFS: {total_bfs_nodes:3d} nodos totales, {total_bfs_time:6.2f}ms totales")
        
        efficiency_nodes = ((total_bfs_nodes - total_astar_nodes) / total_bfs_nodes) * 100
        efficiency_time = ((total_bfs_time - total_astar_time) / total_bfs_time) * 100
        
        print(f"\nA* fue {efficiency_nodes:.1f}% más eficiente en nodos explorados")
        print(f"A* fue {efficiency_time:.1f}% más rápido en tiempo de ejecución")

    def _manual_play(self):
        """Modo de juego manual donde el usuario adivina el camino"""
        print("\n🎮 MODO MANUAL - Adivina el camino")
        print("=" * 50)
        
        # Seleccionar nivel
        while True:
            try:
                level_num = int(input("Selecciona nivel (1-3): "))
                if 1 <= level_num <= 3:
                    break
                else:
                    print("Nivel debe estar entre 1 y 3")
            except ValueError:
                print("Por favor ingresa un número válido")
        
        level = get_level(level_num)
        robot_x, robot_y = level['robot_start']
        
        self.game_state = GameState(level['grid'], robot_x, robot_y)
        self.renderer.render_level(level, robot_x, robot_y)
        
        print("Comandos disponibles:")
        print("  ARRIBA, ABAJO, IZQUIERDA, DERECHA - para mover")
        print("  ENCENDER - para encender luz")
        print("  SOLUCION - para ver la solución con A*")
        print("  SALIR - para volver al menú")
        print()
        
        # Estado actual del juego
        current_node = self.game_state.get_initial_node()
        user_path = []
        
        while True:
            # Verificar si ganó
            if self.game_state.is_goal(current_node):
                print("🎉 ¡FELICITACIONES! ¡Has encendido todas las luces!")
                print(f"Tu solución: {' -> '.join(user_path)}")
                print(f"Pasos utilizados: {len(user_path)}")
                
                # Comparar con solución óptima
                astar_solver = AStar(self.game_state)
                optimal_result = astar_solver.solve()
                if optimal_result['success']:
                    print(f"Solución óptima: {optimal_result['steps']} pasos")
                    if len(user_path) == optimal_result['steps']:
                        print("🌟 ¡Encontraste la solución óptima!")
                    else:
                        print(f"Diferencia: +{len(user_path) - optimal_result['steps']} pasos")
                break
            
            # Mostrar estado actual
            self._render_current_state(level, current_node)
            
            # Obtener comando del usuario
            command = input("Comando: ").strip().upper()
            
            if command == 'SALIR':
                break
            elif command == 'SOLUCION':
                self._show_optimal_solution()
                continue
            
            # Intentar ejecutar el comando
            new_node = self._execute_command(current_node, command)
            if new_node:
                current_node = new_node
                user_path.append(command)
            else:
                print("❌ Movimiento inválido. Intenta de nuevo.")

    def _render_current_state(self, level, node):
        """Renderiza el estado actual del juego"""
        print("\n" + "-" * 30)
        self.renderer.render_level(level, node.x, node.y, list(node.lights))
        
        lights_on = sum(node.lights)
        total_lights = len(node.lights)
        print(f"Luces encendidas: {lights_on}/{total_lights}")

    def _execute_command(self, current_node, command):
        """Ejecuta un comando del usuario y retorna el nuevo nodo si es válido"""
        # Verificar movimientos
        if command in ['ARRIBA', 'ABAJO', 'IZQUIERDA', 'DERECHA']:
            directions = {
                'ARRIBA': (-1, 0),
                'ABAJO': (1, 0),
                'IZQUIERDA': (0, -1),
                'DERECHA': (0, 1)
            }
            
            dx, dy = directions[command]
            new_x = current_node.x + dx
            new_y = current_node.y + dy
            
            if self.game_state.can_move_to(new_x, new_y):
                return Node(new_x, new_y, list(current_node.lights), 
                          current_node, command, current_node.cost + 1)
        
        # Verificar encender luz
        elif command == 'ENCENDER':
            if self.game_state.can_turn_on_light(current_node.x, current_node.y, current_node.lights):
                light_index = None
                for i, (lx, ly) in enumerate(self.game_state.light_positions):
                    if lx == current_node.x and ly == current_node.y:
                        light_index = i
                        break
                
                new_lights = list(current_node.lights)
                new_lights[light_index] = 1
                
                return Node(current_node.x, current_node.y, new_lights,
                          current_node, command, current_node.cost + 1)
        
        return None

    def _show_optimal_solution(self):
        """Muestra la solución óptima usando A*"""
        astar_solver = AStar(self.game_state)
        result = astar_solver.solve()
        
        if result['success']:
            print("\n💡 SOLUCIÓN ÓPTIMA (A*):")
            self.renderer.show_solution(result['path'])
            print(f"Nodos explorados: {result['nodes_explored']}")
            print(f"Tiempo: {result['execution_time']:.2f}ms")
        else:
            print("❌ No se encontró solución.")

def main():
    """Función principal"""
    game = LightBotGame()
    game.play()

if __name__ == "__main__":
    main()