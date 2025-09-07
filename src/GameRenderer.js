/**
 * Clase encargada de renderizar el juego en el DOM
 */
export class GameRenderer {
    constructor(gridElement) {
        this.gridElement = gridElement;
        this.currentLevel = null;
        this.robotPosition = null;
        this.lightStates = null;
    }

    /**
     * Renderiza un nivel en el grid
     */
    renderLevel(level, robotX, robotY, lightStates = null) {
        this.currentLevel = level;
        this.robotPosition = [robotX, robotY];
        
        // Si no se proporcionan estados de luces, todas están apagadas
        if (!lightStates) {
            const lightCount = this.countLights(level.grid);
            this.lightStates = new Array(lightCount).fill(0);
        } else {
            this.lightStates = [...lightStates];
        }

        const grid = level.grid;
        const rows = grid.length;
        const cols = grid[0].length;

        // Configurar el grid CSS
        this.gridElement.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
        this.gridElement.style.gridTemplateRows = `repeat(${rows}, 1fr)`;

        // Limpiar grid anterior
        this.gridElement.innerHTML = '';

        // Crear celdas
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                const cell = this.createCell(grid[i][j], i, j);
                this.gridElement.appendChild(cell);
            }
        }
    }

    /**
     * Crea una celda individual
     */
    createCell(cellType, row, col) {
        const cell = document.createElement('div');
        cell.className = 'cell';
        cell.dataset.row = row;
        cell.dataset.col = col;

        // Determinar el tipo de celda
        if (row === this.robotPosition[0] && col === this.robotPosition[1]) {
            // Robot está aquí
            if (cellType === 2) {
                // Robot en una luz
                const lightIndex = this.getLightIndex(row, col);
                if (this.lightStates[lightIndex] === 1) {
                    cell.classList.add('robot', 'on-light');
                    cell.textContent = '🤖';
                } else {
                    cell.classList.add('robot');
                    cell.textContent = '🤖';
                }
            } else {
                cell.classList.add('robot');
                cell.textContent = '🤖';
            }
        } else {
            // Celda sin robot
            switch (cellType) {
                case 0:
                    cell.classList.add('floor');
                    break;
                case 1:
                    cell.classList.add('obstacle');
                    cell.textContent = '🧱';
                    break;
                case 2:
                    const lightIndex = this.getLightIndex(row, col);
                    if (this.lightStates[lightIndex] === 1) {
                        cell.classList.add('light-on');
                        cell.textContent = '💡';
                    } else {
                        cell.classList.add('light-off');
                        cell.textContent = '🔵';
                    }
                    break;
            }
        }

        return cell;
    }

    /**
     * Obtiene el índice de una luz en las posiciones de luces
     */
    getLightIndex(row, col) {
        const lightPositions = this.getLightPositions(this.currentLevel.grid);
        return lightPositions.findIndex(([lx, ly]) => lx === row && ly === col);
    }

    /**
     * Obtiene todas las posiciones de luces en el nivel
     */
    getLightPositions(grid) {
        const positions = [];
        for (let i = 0; i < grid.length; i++) {
            for (let j = 0; j < grid[0].length; j++) {
                if (grid[i][j] === 2) {
                    positions.push([i, j]);
                }
            }
        }
        return positions;
    }

    /**
     * Cuenta el número total de luces en el nivel
     */
    countLights(grid) {
        let count = 0;
        for (let i = 0; i < grid.length; i++) {
            for (let j = 0; j < grid[0].length; j++) {
                if (grid[i][j] === 2) {
                    count++;
                }
            }
        }
        return count;
    }

    /**
     * Actualiza la posición del robot y estados de luces
     */
    updateGameState(robotX, robotY, lightStates) {
        this.robotPosition = [robotX, robotY];
        this.lightStates = [...lightStates];
        this.renderLevel(this.currentLevel, robotX, robotY, lightStates);
    }

    /**
     * Anima la ejecución de una secuencia de acciones
     */
    async animateSolution(path, gameState) {
        let currentNode = gameState.getInitialNode();
        
        for (let i = 0; i < path.length; i++) {
            const action = path[i];
            
            // Ejecutar la acción
            if (action === 'ENCENDER') {
                // Encender luz
                const lightIndex = gameState.lightPositions.findIndex(
                    ([lx, ly]) => lx === currentNode.x && ly === currentNode.y
                );
                if (lightIndex !== -1) {
                    currentNode.lights[lightIndex] = 1;
                }
            } else {
                // Movimiento
                switch (action) {
                    case 'ARRIBA':
                        currentNode.x -= 1;
                        break;
                    case 'ABAJO':
                        currentNode.x += 1;
                        break;
                    case 'IZQUIERDA':
                        currentNode.y -= 1;
                        break;
                    case 'DERECHA':
                        currentNode.y += 1;
                        break;
                }
            }

            // Actualizar visualización
            this.updateGameState(currentNode.x, currentNode.y, currentNode.lights);
            
            // Pausa para la animación
            await new Promise(resolve => setTimeout(resolve, 800));
        }
    }
}