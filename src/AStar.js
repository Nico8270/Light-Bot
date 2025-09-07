import { PriorityQueue } from './PriorityQueue.js';

/**
 * Implementación del algoritmo A*
 */
export class AStar {
    constructor(gameState) {
        this.gameState = gameState;
        this.nodesExplored = 0;
    }

    /**
     * Ejecuta el algoritmo A* para encontrar la solución
     */
    solve() {
        this.nodesExplored = 0;
        const startTime = performance.now();
        
        const initialNode = this.gameState.getInitialNode();
        initialNode.heuristic = this.gameState.heuristic(initialNode);
        initialNode.totalCost = initialNode.cost + initialNode.heuristic;

        const openSet = new PriorityQueue((a, b) => a.totalCost - b.totalCost);
        const closedSet = new Set();
        
        openSet.enqueue(initialNode);

        while (!openSet.isEmpty()) {
            const currentNode = openSet.dequeue();
            this.nodesExplored++;

            // Verificar si llegamos a la meta
            if (this.gameState.isGoal(currentNode)) {
                const endTime = performance.now();
                return {
                    success: true,
                    path: currentNode.getPath(),
                    nodesExplored: this.nodesExplored,
                    executionTime: endTime - startTime,
                    steps: currentNode.cost
                };
            }

            const currentKey = currentNode.getKey();
            if (closedSet.has(currentKey)) {
                continue;
            }
            
            closedSet.add(currentKey);

            // Generar sucesores
            const successors = this.gameState.getSuccessors(currentNode);
            
            for (const successor of successors) {
                const successorKey = successor.getKey();
                
                if (!closedSet.has(successorKey)) {
                    successor.heuristic = this.gameState.heuristic(successor);
                    successor.totalCost = successor.cost + successor.heuristic;
                    openSet.enqueue(successor);
                }
            }
        }

        const endTime = performance.now();
        return {
            success: false,
            path: [],
            nodesExplored: this.nodesExplored,
            executionTime: endTime - startTime,
            steps: 0
        };
    }
}