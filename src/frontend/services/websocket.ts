export class WebSocketService {
    private socket: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private reconnectDelay = 1000; // Start with 1 second delay
    private messageHandlers: Map<string, ((data: any) => void)[]> = new Map();

    constructor(private url: string) {}

    connect() {
        try {
            this.socket = new WebSocket(this.url);
            this.setupEventHandlers();
        } catch (error) {
            console.error('WebSocket connection error:', error);
            this.handleDisconnect();
        }
    }

    private setupEventHandlers() {
        if (!this.socket) return;

        this.socket.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
            this.reconnectDelay = 1000;
        };

        this.socket.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                this.handleMessage(message);
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };

        this.socket.onclose = () => {
            console.log('WebSocket disconnected');
            this.handleDisconnect();
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }

    private handleDisconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            setTimeout(() => {
                console.log(`Attempting to reconnect (${this.reconnectAttempts + 1}/${this.maxReconnectAttempts})`);
                this.connect();
                this.reconnectAttempts++;
                this.reconnectDelay *= 2; // Exponential backoff
            }, this.reconnectDelay);
        }
    }

    subscribe(messageType: string, handler: (data: any) => void) {
        const handlers = this.messageHandlers.get(messageType) || [];
        handlers.push(handler);
        this.messageHandlers.set(messageType, handlers);
    }

    unsubscribe(messageType: string, handler: (data: any) => void) {
        const handlers = this.messageHandlers.get(messageType) || [];
        const index = handlers.indexOf(handler);
        if (index !== -1) {
            handlers.splice(index, 1);
            this.messageHandlers.set(messageType, handlers);
        }
    }

    private handleMessage(message: { type: string; data: any }) {
        const handlers = this.messageHandlers.get(message.type) || [];
        handlers.forEach(handler => handler(message.data));
    }

    send(messageType: string, data: any) {
        if (this.socket?.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({ type: messageType, data }));
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }
} 