/**
 * Implementación de una cola de prioridad usando un heap binario
 */
export class PriorityQueue {
    constructor(compareFn) {
        this.items = [];
        this.compare = compareFn || ((a, b) => a - b);
    }

    /**
     * Agrega un elemento a la cola
     */
    enqueue(item) {
        this.items.push(item);
        this.heapifyUp(this.items.length - 1);
    }

    /**
     * Remueve y retorna el elemento con mayor prioridad
     */
    dequeue() {
        if (this.isEmpty()) {
            return null;
        }

        const root = this.items[0];
        const lastItem = this.items.pop();

        if (!this.isEmpty()) {
            this.items[0] = lastItem;
            this.heapifyDown(0);
        }

        return root;
    }

    /**
     * Verifica si la cola está vacía
     */
    isEmpty() {
        return this.items.length === 0;
    }

    /**
     * Retorna el tamaño de la cola
     */
    size() {
        return this.items.length;
    }

    /**
     * Reorganiza el heap hacia arriba
     */
    heapifyUp(index) {
        if (index === 0) return;

        const parentIndex = Math.floor((index - 1) / 2);
        
        if (this.compare(this.items[index], this.items[parentIndex]) < 0) {
            this.swap(index, parentIndex);
            this.heapifyUp(parentIndex);
        }
    }

    /**
     * Reorganiza el heap hacia abajo
     */
    heapifyDown(index) {
        const leftChild = 2 * index + 1;
        const rightChild = 2 * index + 2;
        let smallest = index;

        if (leftChild < this.items.length && 
            this.compare(this.items[leftChild], this.items[smallest]) < 0) {
            smallest = leftChild;
        }

        if (rightChild < this.items.length && 
            this.compare(this.items[rightChild], this.items[smallest]) < 0) {
            smallest = rightChild;
        }

        if (smallest !== index) {
            this.swap(index, smallest);
            this.heapifyDown(smallest);
        }
    }

    /**
     * Intercambia dos elementos en el array
     */
    swap(i, j) {
        [this.items[i], this.items[j]] = [this.items[j], this.items[i]];
    }
}