"""
Juego LightBot - Comparación A* vs BFS
"""
from game_state import GameState
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
                self._user_guess_mode()
            elif choice == '6':
                self._generate_readme()
            elif choice == '7':
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
        print("5. Modo adivinanza (ingresa tu solución)")
        print("6. Generar README.txt con resultados")
        print("7. Salir")
        print()

    def _play_level(self, level_number):
        """Resuelve un nivel específico con ambos algoritmos"""
        level = get_level(level_number)
        robot_x, robot_y = level['robot_start']
    
        self.game_state = GameState(level['grid'], robot_x, robot_y)
    
        print("\n" + "="*60)
        print("🎯 PRESENTACIÓN DEL PROBLEMA")
        print("="*60)
        self.renderer.render_level(level, robot_x, robot_y)
        
        # Mostrar explicación de la heurística
        initial_node = self.game_state.get_initial_node()
        self.renderer.show_heuristic_explanation(initial_node, self.game_state.light_positions)
    
        input("\nPresiona ENTER para ver la solución con A*...")
    
        print("\n" + "="*60)
        print("🔍 RESOLVIENDO CON A* (ALGORITMO INFORMADO)")
        print("="*60)
        astar_solver = AStar(self.game_state)
        astar_result = astar_solver.solve()
    
        # Mostrar progreso detallado de A*
        self.renderer.show_algorithm_progress(level, astar_result, "A*", show_heuristic=True)
    
        input("\nPresiona ENTER para ver la solución con BFS...")
    
        print("\n" + "="*60)
        print("🔍 RESOLVIENDO CON BFS (BÚSQUEDA CIEGA)")
        print("="*60)
        bfs_solver = BFS(self.game_state)
        bfs_result = bfs_solver.solve()
    
        # Mostrar progreso detallado de BFS
        self.renderer.show_algorithm_progress(level, bfs_result, "BFS")
    
        input("\nPresiona ENTER para ver la comparación...")
    
        # Mostrar comparación
        self.renderer.show_stats(astar_result, bfs_result)

    def _user_guess_mode(self):
        """Modo donde el usuario adivina la solución antes de ver los algoritmos"""
        print("\n🎮 MODO ADIVINANZA - Ingresa tu solución")
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
        
        # Mostrar el problema completo
        print("\n" + "="*60)
        print("🎯 PROBLEMA A RESOLVER")
        print("="*60)
        self.renderer.render_level(level, robot_x, robot_y)
        
        print("Comandos disponibles:")
        print("  ARRIBA, ABAJO, IZQUIERDA, DERECHA - para mover")
        print("  ENCENDER - para encender luz")
        print()
        
        # Solicitar solución del usuario
        user_path = []
        print("Ingresa tu solución paso a paso (escribe 'FIN' para terminar):")
        
        while True:
            step = input(f"Paso {len(user_path) + 1}: ").strip().upper()
            
            if step == 'FIN':
                break
            elif step in ['ARRIBA', 'ABAJO', 'IZQUIERDA', 'DERECHA', 'ENCENDER']:
                user_path.append(step)
                print(f"  ✅ Agregado: {step}")
            else:
                print("  ❌ Comando inválido. Usa: ARRIBA, ABAJO, IZQUIERDA, DERECHA, ENCENDER, FIN")
        
        if not user_path:
            print("No ingresaste ninguna solución.")
            return
        
        # Evaluar la solución del usuario
        is_correct, user_steps = self.renderer.evaluate_user_solution(level, (robot_x, robot_y), user_path)
        
        input("\nPresiona ENTER para ver las soluciones de los algoritmos...")
        
        # Resolver con algoritmos
        game_state = GameState(level['grid'], robot_x, robot_y)
        
        astar_solver = AStar(game_state)
        astar_result = astar_solver.solve()
        
        bfs_solver = BFS(game_state)
        bfs_result = bfs_solver.solve()
        
        # Mostrar comparación incluyendo solución del usuario
        print("\n" + "="*60)
        print("📊 COMPARACIÓN COMPLETA")
        print("="*60)
        print()
        print("Tu solución:")
        print(f"  Pasos: {user_steps}")
        print(f"  Correcta: {'✅ Sí' if is_correct else '❌ No'}")
        print()
        
        self.renderer.show_stats(astar_result, bfs_result)
        
        if is_correct and astar_result['success']:
            optimal_steps = astar_result['steps']
            if user_steps == optimal_steps:
                print("🌟 ¡FELICITACIONES! Encontraste la solución óptima!")
            elif user_steps > optimal_steps:
                print(f"📈 Tu solución usa {user_steps - optimal_steps} pasos adicionales")
            else:
                print("🤔 Esto es extraño, tu solución es mejor que la óptima...")

    def _compare_all_levels(self):
        """Compara el rendimiento en todos los niveles"""
        print("\n🔍 COMPARACIÓN COMPLETA DE TODOS LOS NIVELES")
        print("=" * 60)
        
        total_astar_nodes = 0
        total_bfs_nodes = 0
        total_astar_time = 0
        total_bfs_time = 0
        
        results_summary = []
        
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
            
            # Guardar resultados para README
            results_summary.append({
                'level': level_num,
                'level_name': level['name'],
                'astar': astar_result,
                'bfs': bfs_result
            })
            
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
        
        # Guardar resultados para uso posterior
        self.last_comparison_results = results_summary

    def _generate_readme(self):
        """Genera el archivo README.txt con los resultados"""
        print("\n📝 GENERANDO README.txt...")
        
        # Ejecutar comparación si no se ha hecho
        if not hasattr(self, 'last_comparison_results'):
            print("Ejecutando comparación de todos los niveles...")
            self._compare_all_levels()
        
        try:
            with open('README.txt', 'w', encoding='utf-8') as f:
                f.write("# LightBot Python - Comparación A* vs BFS\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("## Descripción del Proyecto\n\n")
                f.write("Este proyecto implementa una versión simplificada del juego LightBot\n")
                f.write("donde un robot debe encender todas las luces azules en un tablero.\n")
                f.write("Se compara la eficiencia de dos algoritmos de búsqueda:\n")
                f.write("- A* (con heurística)\n")
                f.write("- BFS (búsqueda ciega)\n\n")
                
                f.write("## Heurística Implementada\n\n")
                f.write("h(n) = luces_apagadas + distancia_a_luz_más_cercana\n\n")
                f.write("Esta heurística es optimista porque:\n")
                f.write("- Nunca sobreestima el costo real\n")
                f.write("- Considera el mínimo de acciones necesarias\n")
                f.write("- Usa distancia Manhattan (admisible)\n\n")
                
                f.write("## Resultados de Comparación\n\n")
                
                total_astar_nodes = 0
                total_bfs_nodes = 0
                total_astar_time = 0
                total_bfs_time = 0
                
                for result in self.last_comparison_results:
                    f.write(f"### {result['level_name']}\n")
                    f.write(f"- A*: {result['astar']['nodes_explored']} nodos, ")
                    f.write(f"{result['astar']['steps']} pasos, ")
                    f.write(f"{result['astar']['execution_time']:.2f}ms\n")
                    f.write(f"- BFS: {result['bfs']['nodes_explored']} nodos, ")
                    f.write(f"{result['bfs']['steps']} pasos, ")
                    f.write(f"{result['bfs']['execution_time']:.2f}ms\n\n")
                    
                    total_astar_nodes += result['astar']['nodes_explored']
                    total_bfs_nodes += result['bfs']['nodes_explored']
                    total_astar_time += result['astar']['execution_time']
                    total_bfs_time += result['bfs']['execution_time']
                
                f.write("## Resumen Total\n\n")
                f.write(f"- A*: {total_astar_nodes} nodos totales, {total_astar_time:.2f}ms totales\n")
                f.write(f"- BFS: {total_bfs_nodes} nodos totales, {total_bfs_time:.2f}ms totales\n\n")
                
                efficiency_nodes = ((total_bfs_nodes - total_astar_nodes) / total_bfs_nodes) * 100
                efficiency_time = ((total_bfs_time - total_astar_time) / total_bfs_time) * 100
                
                f.write("## Análisis de Eficiencia\n\n")
                f.write(f"- A* exploró {efficiency_nodes:.1f}% menos nodos que BFS\n")
                f.write(f"- A* fue {efficiency_time:.1f}% más rápido que BFS\n\n")
                
                f.write("## Conclusiones\n\n")
                f.write("Los resultados demuestran que A* es más eficiente que BFS\n")
                f.write("gracias al uso de información heurística que guía la búsqueda\n")
                f.write("hacia estados más prometedores, reduciendo el espacio de búsqueda.\n")
            
            print("✅ README.txt generado exitosamente!")
            
        except Exception as e:
            print(f"❌ Error al generar README.txt: {e}")

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
                from node import Node
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
                
                from node import Node
                return Node(current_node.x, current_node.y, new_lights,
                          current_node, command, current_node.cost + 1)
        
        return None

    def _show_optimal_solution(self):
        """Muestra la solución óptima usando A*"""
        astar_solver = AStar(self.game_state)
        result = astar_solver.solve()
        
        if result['success']:
            print("\n💡 SOLUCIÓN ÓPTIMA (A*):")
            self.renderer.show_solution(result['path'], "A*")
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