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
                <button onclick="document.querySelector('[x-data]').__x.$data.saveProject()" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded shadow text-sm font-bold flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
                    Save
                </button>
                <button id="clear-btn" class="bg-red-500 text-white px-3 py-1 rounded shadow text-sm font-bold">Clear Board</button>
            </div>
            <div id="trash-zone" style="position: absolute; bottom: 20px; right: 20px; width: 60px; height: 60px; border-radius: 50%; background-color: #fee2e2; border: 2px dashed #ef4444; display: flex; align-items: center; justify-content: center; z-index: 5; transition: all 0.3s;" title="Drag here to delete">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
            </div>
        `;
        this.svgLayer = document.getElementById('circuit-svg');
        this.compLayer = document.getElementById('components-layer');
        this.trashZone = document.getElementById('trash-zone');

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

        // Global Mouse Up (End Dragging / Wiring)
        window.addEventListener('mouseup', (e) => {
            // Wiring Logic: End
            if (this.wireStart) {
                // Check if we dropped on a valid pin
                // We need to check if the target is a pin div
                const pinEl = e.target.closest('[data-pin-id]');
                if (pinEl) {
                    const compId = pinEl.dataset.compId;
                    const pinId = pinEl.dataset.pinId;

                    // Don't connect to self or start pin
                    if (compId !== this.wireStart.compId || pinId !== this.wireStart.pinId) {
                        this.engine.addWire(this.wireStart.compId, this.wireStart.pinId, compId, pinId);
                        this.render();
                    }
                }

                this.wireStart = null;
                this.renderWires(); // Clear temp wire
            }

            // Component Dragging Logic: End
            if (this.isDragging && this.draggedComp) {
                // Check if dropped in trash zone
                const trashRect = this.trashZone.getBoundingClientRect();
                if (e.clientX >= trashRect.left && e.clientX <= trashRect.right &&
                    e.clientY >= trashRect.top && e.clientY <= trashRect.bottom) {

                    // Delete Component
                    this.engine.removeComponent(this.draggedComp.id);
                    this.render();
                }
            }
            this.isDragging = false;
            this.draggedComp = null;
            this.trashZone.style.transform = 'scale(1)';
            this.trashZone.style.backgroundColor = '#fee2e2';
        });

        // Global Mouse Move (Drag Update)
        this.container.addEventListener('mousemove', (e) => {
            if (this.isDragging && this.draggedComp) {
                const rect = this.container.getBoundingClientRect();
                this.draggedComp.x = e.clientX - rect.left - this.dragOffset.x;
                this.draggedComp.y = e.clientY - rect.top - this.dragOffset.y;
                this.render(); // Re-render wires and position

                // Highlight Trash Zone if hovering
                const trashRect = this.trashZone.getBoundingClientRect();
                if (e.clientX >= trashRect.left && e.clientX <= trashRect.right &&
                    e.clientY >= trashRect.top && e.clientY <= trashRect.bottom) {
                    this.trashZone.style.transform = 'scale(1.2)';
                    this.trashZone.style.backgroundColor = '#fecaca';
                } else {
                    this.trashZone.style.transform = 'scale(1)';
                    this.trashZone.style.backgroundColor = '#fee2e2';
                }
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

            // Right Click to Delete
            el.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                if (confirm('Delete this component?')) {
                    this.engine.removeComponent(comp.id);
                    this.render();
                }
            });

            this.compLayer.appendChild(el);
        });

        // 3. Render Wires
        this.renderWires();

        // 4. Attach Pin Listeners (Mousedown for Drag Wiring)
        document.querySelectorAll('[data-pin-id]').forEach(pinEl => {
            pinEl.addEventListener('mousedown', (e) => {
                e.stopPropagation(); // Don't drag component
                e.preventDefault();  // Stop text selection
                const cId = pinEl.dataset.compId;
                const pId = pinEl.dataset.pinId;

                // Start Dragging Wire
                this.wireStart = { compId: cId, pinId: pId };
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
