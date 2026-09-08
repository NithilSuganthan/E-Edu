/**
 * circuit-ui.js
 * Manages the User Interface, SVG Rendering, and Interaction for the Circuit Lab.
 */

class CircuitUI {
    constructor(containerId, engine) {
        this.container = document.getElementById(containerId);
        this.engine = engine;
        this.isDragging = false;
        this.draggedComp = null;
        this.dragOffset = { x: 0, y: 0 };
        this.wiringMode = false;
        this.wireStart = null; // { compId, pinId }

        this.initDOM();
        this.setupEventListeners();
        this.renderLoop();
    }

    initDOM() {
        this.container.innerHTML = `
            <svg id="circuit-svg" width="100%" height="100%" style="position: absolute; top:0; left:0; z-index:1; pointer-events:none; overflow: visible;"></svg>
            <div id="components-layer" style="position: absolute; top:0; left:0; width:100%; height:100%; z-index:2;"></div>
            <div id="ui-overlay" style="position: absolute; top: 10px; right: 10px; z-index: 10; display: flex; gap: 10px;">
                <button id="clear-btn" class="bg-red-500 text-white px-3 py-1 rounded shadow text-sm font-bold">Clear Board</button>
            </div>
        `;
        this.svgLayer = document.getElementById('circuit-svg');
        this.compLayer = document.getElementById('components-layer');

        document.getElementById('clear-btn').addEventListener('click', () => {
            this.engine.components = [];
            this.engine.wires = [];
            this.render();
        });
    }

    setupEventListeners() {
        // Drop on Workbench
        this.container.addEventListener('dragover', (e) => e.preventDefault());
        this.container.addEventListener('drop', (e) => {
            e.preventDefault();
            const type = e.dataTransfer.getData('text/plain');
            const rect = this.container.getBoundingClientRect();
            const x = e.clientX - rect.left - 30; // centerish
            const y = e.clientY - rect.top - 30;

            if (type) {
                this.engine.addComponent(type, x, y);
                this.render();
            }
        });

        // Global Mouse Up (End Dragging)
        window.addEventListener('mouseup', () => {
            this.isDragging = false;
            this.draggedComp = null;
        });

        // Global Mouse Move (Drag Update)
        this.container.addEventListener('mousemove', (e) => {
            if (this.isDragging && this.draggedComp) {
                const rect = this.container.getBoundingClientRect();
                this.draggedComp.x = e.clientX - rect.left - this.dragOffset.x;
                this.draggedComp.y = e.clientY - rect.top - this.dragOffset.y;
                this.render(); // Re-render wires and position
            }

            // Draw temp wire
            if (this.wireStart) {
                this.renderWires(e); // Pass mouse event to draw dynamic line
            }
        });
    }

    // Add component visual to DOM
    render() {
        // 1. Evaluate Logic State
        this.engine.evaluate();

        // 2. Render Components
        this.compLayer.innerHTML = '';
        this.engine.components.forEach(comp => {
            const def = ComponentRegistry[comp.type];
            const el = document.createElement('div');
            el.className = 'absolute cursor-move select-none group';
            el.style.left = comp.x + 'px';
            el.style.top = comp.y + 'px';

            // SVG Content
            // We wrapper it to handle Pin Clicks separately
            let pinDots = '';
            def.pins.forEach(pin => {
                // Pin Visuals (invisible hitboxes over the SVG coordinates)
                pinDots += `<div class="absolute w-4 h-4 rounded-full cursor-crosshair z-20 hover:bg-blue-400/50" 
                    style="left: ${pin.x - 8}px; top: ${pin.y - 8}px;"
                    title="${pin.id}"
                    data-comp-id="${comp.id}" data-pin-id="${pin.id}"></div>`;
            });

            // Interactive Controls Overlay
            let controls = '';
            if (comp.type === 'switch_toggle' || comp.type === 'push_button') {
                controls = `<div class="absolute inset-0 cursor-pointer z-10" onclick="window.circuitApp.toggleComponent('${comp.id}')"></div>`;
            }
            if (comp.type.startsWith('sensor_')) {
                // Slider for sensor value
                controls = `
               <div class="absolute -bottom-6 left-0 w-full bg-slate-800 rounded px-1 py-0.5 z-30 opacity-0 group-hover:opacity-100 transition-opacity">
                 <input type="range" min="0" max="100" value="${comp.state.value}" 
                    class="w-full h-1 bg-slate-600 rounded-lg appearance-none cursor-pointer"
                    oninput="window.circuitApp.updateSensor('${comp.id}', this.value)">
               </div>`;
            }

            el.innerHTML = `
                <svg width="100" height="100" style="overflow: visible;">
                    ${def.render(comp.state)}
                </svg>
                ${pinDots}
                ${controls}
            `;

            // Drag Start
            el.addEventListener('mousedown', (e) => {
                // Ignore if clicked on a pin
                if (e.target.dataset.pinId) return;

                this.isDragging = true;
                this.draggedComp = comp;
                this.dragOffset = { x: e.offsetX, y: e.offsetY };
            });

            this.compLayer.appendChild(el);
        });

        // 3. Render Wires
        this.renderWires();

        // 4. Attach Pin Click Listeners
        document.querySelectorAll('[data-pin-id]').forEach(pinEl => {
            pinEl.addEventListener('click', (e) => {
                e.stopPropagation();
                const cId = pinEl.dataset.compId;
                const pId = pinEl.dataset.pinId;
                this.handlePinClick(cId, pId);
            });
        });
    }

    renderWires(mouseEvent = null) {
        let svgHtml = '';

        // Existing Wires
        this.engine.wires.forEach(w => {
            const c1 = this.engine.getComponent(w.fromComp);
            const c2 = this.engine.getComponent(w.toComp);
            if (!c1 || !c2) return;

            const p1Def = ComponentRegistry[c1.type].pins.find(p => p.id === w.fromPin);
            const p2Def = ComponentRegistry[c2.type].pins.find(p => p.id === w.toPin);

            const x1 = c1.x + p1Def.x;
            const y1 = c1.y + p1Def.y;
            const x2 = c2.x + p2Def.x;
            const y2 = c2.y + p2Def.y;

            // Check if wire is "active" (part of a hot/gnd net is hard to check loosely visually)
            // Just red/black based on connection? 
            // Let's make wires Standard Blue for now.
            const color = '#3b82f6';

            svgHtml += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="4" stroke-linecap="round" style="opacity: 0.8;"/>`;
        });

        // Temp Wire
        if (this.wireStart && mouseEvent) {
            const c1 = this.engine.getComponent(this.wireStart.compId);
            const p1Def = ComponentRegistry[c1.type].pins.find(p => p.id === this.wireStart.pinId);
            const x1 = c1.x + p1Def.x;
            const y1 = c1.y + p1Def.y;

            const rect = this.svgLayer.getBoundingClientRect();
            const x2 = mouseEvent.clientX - rect.left;
            const y2 = mouseEvent.clientY - rect.top;

            svgHtml += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#fbbf24" stroke-width="4" stroke-dasharray="8 4" stroke-linecap="round"/>`;
        }

        this.svgLayer.innerHTML = svgHtml;
    }

    handlePinClick(compId, pinId) {
        if (!this.wireStart) {
            // Start Wire
            this.wireStart = { compId, pinId };
        } else {
            // Complete Wire
            if (this.wireStart.compId !== compId) { // Basic check
                this.engine.addWire(this.wireStart.compId, this.wireStart.pinId, compId, pinId);
                this.render();
            }
            this.wireStart = null;
            this.renderWires(); // clear temp
        }
    }

    toggleComponent(id) {
        const comp = this.engine.getComponent(id);
        if (comp) {
            if (comp.type === 'switch_toggle' || comp.type === 'push_button') {
                comp.state.closed = !comp.state.closed;
                this.render();
            }
        }
    }

    updateSensor(id, val) {
        const comp = this.engine.getComponent(id);
        if (comp) {
            comp.state.value = parseInt(val);
            this.render(); // Re-calc logic potentially
        }
    }

    renderLoop() {
        // Optional animation loop for motors
        // Since we use CSS animations for motors, we don't need a heavy JS loop unless we want smooth physics.
        // We just need to trigger 'render' when things change.
    }
}

window.CircuitUI = CircuitUI;
