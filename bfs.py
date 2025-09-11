"""
Implementación del algoritmo BFS (Búsqueda en Anchura)
"""
import time
from collections import deque

class BFS:
    def __init__(self, game_state):
        self.game_state = game_state
        self.nodes_explored = 0

    def solve(self):
        """Ejecuta el algoritmo BFS para encontrar la solución"""
        self.nodes_explored = 0
        start_time = time.time()
        
        initial_node = self.game_state.get_initial_node()
        queue = deque([initial_node])
        visited = set()

        while queue:
            current_node = queue.popleft()
            self.nodes_explored += 1

            # Verificar si llegamos a la meta
            if self.game_state.is_goal(current_node):
                end_time = time.time()
                return {
                    'success': True,
                    'path': current_node.get_path(),
                    'nodes_explored': self.nodes_explored,
                    'execution_time': (end_time - start_time) * 1000,  # en ms
                    'steps': current_node.cost
                }

            current_key = current_node.get_key()
            if current_key in visited:
                continue
            
            visited.add(current_key)

            # Generar sucesores
            successors = self.game_state.get_successors(current_node)
            
            for successor in successors:
                successor_key = successor.get_key()
                
                if successor_key not in visited:
                    queue.append(successor)

        end_time = time.time()
        return {
            'success': False,
            'path': [],
            'nodes_explored': self.nodes_explored,
            'execution_time': (end_time - start_time) * 1000,
            'steps': 0
        }