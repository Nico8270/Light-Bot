/**
 * Clase que representa un nodo en el espacio de estados del juego LightBot
 */
export class Node {
    constructor(x, y, lights, parent = null, action = null, cost = 0) {
        this.x = x;                    // Posición X del robot
        this.y = y;                    // Posición Y del robot
        this.lights = lights;          // Tupla con estado de las luces (0=apagada, 1=encendida)
        this.parent = parent;          // Nodo padre para reconstruir el camino
        this.action = action;          // Acción que llevó a este estado
        this.cost = cost;              // Costo acumulado (g en A*)
        this.heuristic = 0;            // Valor heurístico (h en A*)
        this.totalCost = 0;            // Costo total (f = g + h en A*)
    }

    /**
     * Genera una clave única para este estado
     */
    getKey() {
        return `${this.x},${this.y},${this.lights.join(',')}`;
    }

    /**
     * Verifica si dos nodos representan el mismo estado
     */
    equals(other) {
        return this.x === other.x && 
               this.y === other.y && 
               this.lights.every((light, i) => light === other.lights[i]);
    }

    /**
     * Crea una copia del nodo con nuevos valores
     */
    copy(newX = this.x, newY = this.y, newLights = [...this.lights]) {
        return new Node(newX, newY, newLights, this.parent, this.action, this.cost);
    }

    /**
     * Reconstruye el camino desde el nodo inicial hasta este nodo
     */
    getPath() {
        const path = [];
        let current = this;
        
        while (current.parent !== null) {
            path.unshift(current.action);
            current = current.parent;
        }
        
        return path;
    }
}