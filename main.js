import { GameState } from './src/GameState.js';
import { GameRenderer } from './src/GameRenderer.js';
import { AStar } from './src/AStar.js';
import { BFS } from './src/BFS.js';
import { getLevel } from './src/Levels.js';

class LightBotGame {
    constructor() {
        this.currentLevelNumber = 1;
        this.gameState = null;
        this.renderer = new GameRenderer(document.getElementById('grid'));
        this.isAnimating = false;
        
        this.initializeEventListeners();
        this.loadLevel(1);
    }

    initializeEventListeners() {
        // Botones de nivel
        document.getElementById('level1').addEventListener('click', () => this.loadLevel(1));
        document.getElementById('level2').addEventListener('click', () => this.loadLevel(2));
        document.getElementById('level3').addEventListener('click', () => this.loadLevel(3));

        // Botones de algoritmos
        document.getElementById('solve-astar').addEventListener('click', () => this.solveWithAStar());
        document.getElementById('solve-bfs').addEventListener('click', () => this.solveWithBFS());
        document.getElementById('reset').addEventListener('click', () => this.resetLevel());
    }

    loadLevel(levelNumber) {
        if (this.isAnimating) return;

        this.currentLevelNumber = levelNumber;
        const level = getLevel(levelNumber);
        const [robotX, robotY] = level.robotStart;
        
        this.gameState = new GameState(level.grid, robotX, robotY);
        this.renderer.renderLevel(level, robotX, robotY);
        
        // Actualizar botones de nivel
        document.querySelectorAll('.level-btn').forEach(btn => btn.classList.remove('active'));
        document.getElementById(`level${levelNumber}`).classList.add('active');
        
        // Limpiar resultados anteriores
        this.clearResults();
    }

    async solveWithAStar() {
        if (this.isAnimating) return;
        
        this.setAnimating(true);
        const solver = new AStar(this.gameState);
        const result = await this.solveProblem(solver, 'astar');
        
        if (result.success) {
            await this.renderer.animateSolution(result.path, this.gameState);
        }
        
        this.setAnimating(false);
    }

    async solveWithBFS() {
        if (this.isAnimating) return;
        
        this.setAnimating(true);
        const solver = new BFS(this.gameState);
        const result = await this.solveProblem(solver, 'bfs');
        
        if (result.success) {
            await this.renderer.animateSolution(result.path, this.gameState);
        }
        
        this.setAnimating(false);
    }

    async solveProblem(solver, algorithmType) {
        const result = solver.solve();
        
        // Actualizar estadísticas
        document.getElementById(`${algorithmType}-nodes`).textContent = result.nodesExplored;
        document.getElementById(`${algorithmType}-steps`).textContent = result.steps;
        document.getElementById(`${algorithmType}-time`).textContent = `${result.executionTime.toFixed(2)}ms`;
        
        // Mostrar solución
        if (result.success) {
            this.displaySolution(result.path);
        } else {
            this.displayNoSolution();
        }
        
        return result;
    }

    displaySolution(path) {
        const container = document.getElementById('solution-steps');
        container.innerHTML = '';
        
        if (path.length === 0) {
            container.innerHTML = '<div class="no-solution">¡El robot ya está en la meta!</div>';
            return;
        }
        
        path.forEach((step, index) => {
            const stepElement = document.createElement('div');
            stepElement.className = 'step';
            stepElement.textContent = `${index + 1}. ${step}`;
            stepElement.style.animationDelay = `${index * 0.1}s`;
            container.appendChild(stepElement);
        });
    }

    displayNoSolution() {
        const container = document.getElementById('solution-steps');
        container.innerHTML = '<div class="no-solution">No se encontró solución</div>';
    }

    resetLevel() {
        if (this.isAnimating) return;
        
        this.loadLevel(this.currentLevelNumber);
    }

    clearResults() {
        // Limpiar estadísticas
        ['astar', 'bfs'].forEach(algorithm => {
            document.getElementById(`${algorithm}-nodes`).textContent = '-';
            document.getElementById(`${algorithm}-steps`).textContent = '-';
            document.getElementById(`${algorithm}-time`).textContent = '-';
        });
        
        // Limpiar solución
        document.getElementById('solution-steps').innerHTML = '';
    }

    setAnimating(isAnimating) {
        this.isAnimating = isAnimating;
        const gameSection = document.querySelector('.game-section');
        
        if (isAnimating) {
            gameSection.classList.add('solving');
        } else {
            gameSection.classList.remove('solving');
        }
    }
}

// Inicializar el juego cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    new LightBotGame();
});