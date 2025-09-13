"""
Implementación del algoritmo A*
"""
import time
from priority_queue import PriorityQueue

class AStar:
    def __init__(self, game_state):
        self.game_state = game_state
        self.nodes_explored = 0
        self.visited_nodes = []

    def solve(self):
        """Ejecuta el algoritmo A* para encontrar la solución"""
        self.nodes_explored = 0
        self.visited_nodes = []
        start_time = time.perf_counter()
    
        initial_node = self.game_state.get_initial_node()
        initial_node.heuristic = self.game_state.heuristic(initial_node)
        initial_node.total_cost = initial_node.cost + initial_node.heuristic

        open_set = PriorityQueue()
        closed_set = set()
    
        open_set.enqueue(initial_node)
        visit_counter = 0

        while not open_set.is_empty():
            current_node = open_set.dequeue()
            self.nodes_explored += 1
            visit_counter += 1
            current_node.visited_order = visit_counter
            self.visited_nodes.append(current_node)

            # Verificar si llegamos a la meta
            if self.game_state.is_goal(current_node):
                end_time = time.perf_counter()
                return {
                    'success': True,
                    'path': current_node.get_path(),
                    'nodes_explored': self.nodes_explored,
                    'execution_time': (end_time - start_time) * 1000,
                    'steps': current_node.cost,
                    'visited_nodes': self.visited_nodes,
                    'final_node': current_node
                }

            current_key = current_node.get_key()
            if current_key in closed_set:
                continue
        
            closed_set.add(current_key)

            # Generar sucesores
            successors = self.game_state.get_successors(current_node)
        
            for successor in successors:
                successor_key = successor.get_key()
            
                if successor_key not in closed_set:
                    successor.heuristic = self.game_state.heuristic(successor)
                    successor.total_cost = successor.cost + successor.heuristic
                    open_set.enqueue(successor)

        end_time = time.perf_counter()
        return {
            'success': False,
            'path': [],
            'nodes_explored': self.nodes_explored,
            'execution_time': (end_time - start_time) * 1000,
            'steps': 0,
            'visited_nodes': self.visited_nodes,
            'final_node': None
        }