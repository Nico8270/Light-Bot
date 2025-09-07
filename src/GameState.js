import { Node } from './Node.js';

/**
 * Clase que maneja el estado del juego y las reglas
 */
export class GameState {
    constructor(level, robotX, robotY) {
        this.level = level;
        this.rows = level.length;
        this.cols = level[0].length;
        this.robotX = robotX;
        this.robotY = robotY;
        
        // Encontrar posiciones de las luces
        this.lightPositions = [];
        for (let i = 0; i < this.rows; i++) {
            for (let j = 0; j < this.cols; j++) {
                if (level[i][j] === 2) {
                    this.lightPositions.push([i, j]);
                }
            }
        }
        
        // Estado inicial: todas las luces apagadas
        this.initialLights = new Array(this.lightPositions.length).fill(0);
    }

    /**
     * Verifica si una posición está dentro del tablero
     */
    isValidPosition(x, y) {
        return x >= 0 && x < this.rows && y >= 0 && y < this.cols;
    }

    /**
     * Verifica si el robot puede moverse a una posición
     */
    canMoveTo(x, y) {
        return this.isValidPosition(x, y) && this.level[x][y] !== 1;
    }

    /**
     * Verifica si el robot puede encender una luz en su posición actual
     */
    canTurnOnLight(x, y, lights) {
        // Buscar si hay una luz en esta posición
        const lightIndex = this.lightPositions.findIndex(([lx, ly]) => lx === x && ly === y);
        
        // Puede encender si hay una luz y está apagada
        return lightIndex !== -1 && lights[lightIndex] === 0;
    }

    /**
     * Genera todos los sucesores posibles de un nodo
     */
    getSuccessors(node) {
        const successors = [];
        const directions = [
            [-1, 0, 'ARRIBA'],
            [1, 0, 'ABAJO'],
            [0, -1, 'IZQUIERDA'],
            [0, 1, 'DERECHA']
        ];

        // Intentar movimientos en las 4 direcciones
        for (const [dx, dy, action] of directions) {
            const newX = node.x + dx;
            const newY = node.y + dy;

            if (this.canMoveTo(newX, newY)) {
                const successor = new Node(
                    newX, 
                    newY, 
                    [...node.lights], 
                    node, 
                    action, 
                    node.cost + 1
                );
                successors.push(successor);
            }
        }

        // Intentar encender luz en la posición actual
        if (this.canTurnOnLight(node.x, node.y, node.lights)) {
            const lightIndex = this.lightPositions.findIndex(([lx, ly]) => lx === node.x && ly === node.y);
            const newLights = [...node.lights];
            newLights[lightIndex] = 1;

            const successor = new Node(
                node.x, 
                node.y, 
                newLights, 
                node, 
                'ENCENDER', 
                node.cost + 1
            );
            successors.push(successor);
        }

        return successors;
    }

    /**
     * Verifica si un nodo representa el estado meta (todas las luces encendidas)
     */
    isGoal(node) {
        return node.lights.every(light => light === 1);
    }

    /**
     * Calcula la heurística para A*
     * Heurística = número de luces apagadas + distancia a la luz más cercana
     */
    heuristic(node) {
        const lightsOff = node.lights.filter(light => light === 0).length;
        
        if (lightsOff === 0) {
            return 0;
        }

        // Encontrar distancia a la luz apagada más cercana
        let minDistance = Infinity;
        
        for (let i = 0; i < this.lightPositions.length; i++) {
            if (node.lights[i] === 0) {
                const [lx, ly] = this.lightPositions[i];
                const distance = Math.abs(node.x - lx) + Math.abs(node.y - ly);
                minDistance = Math.min(minDistance, distance);
            }
        }

        return lightsOff + minDistance;
    }

    /**
     * Crea el nodo inicial
     */
    getInitialNode() {
        return new Node(this.robotX, this.robotY, [...this.initialLights]);
    }
}