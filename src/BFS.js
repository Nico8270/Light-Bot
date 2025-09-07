/**
 * Implementación del algoritmo BFS (Búsqueda en Anchura)
 */
export class BFS {
    constructor(gameState) {
        this.gameState = gameState;
        this.nodesExplored = 0;
    }

    /**
     * Ejecuta el algoritmo BFS para encontrar la solución
     */
    solve() {
        this.nodesExplored = 0;
        const startTime = performance.now();
        
        const initialNode = this.gameState.getInitialNode();
        const queue = [initialNode];
        const visited = new Set();

        while (queue.length > 0) {
            const currentNode = queue.shift();
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
            if (visited.has(currentKey)) {
                continue;
            }
            
            visited.add(currentKey);

            // Generar sucesores
            const successors = this.gameState.getSuccessors(currentNode);
            
            for (const successor of successors) {
                const successorKey = successor.getKey();
                
                if (!visited.has(successorKey)) {
                    queue.push(successor);
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