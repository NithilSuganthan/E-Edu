/**
 * circuit-engine.js
 * The logic engine that simulates circuit behavior.
 */

class CircuitEngine {
    constructor() {
        this.components = []; // { id, type, x, y, state }
        this.wires = [];      // { fromComp, fromPin, toComp, toPin }
        this.nextId = 1;
    }

    addComponent(type, x, y) {
        const def = ComponentRegistry[type];
        if (!def) return null;

        const id = 'comp_' + this.nextId++;
        const component = {
            id: id,
            type: type,
            x: x,
            y: y,
            state: { on: false, ...def.defaultState } // active state
        };
        this.components.push(component);
        return component;
    }

    addWire(fromId, fromPin, toId, toPin) {
        // Prevent duplicate wires
        const exists = this.wires.find(w =>
            (w.fromComp === fromId && w.fromPin === fromPin && w.toComp === toId && w.toPin === toPin) ||
            (w.fromComp === toId && w.fromPin === toPin && w.toComp === fromId && w.toPin === fromPin)
        );
        if (exists) return false;

        // Basic validation: Cannot connect same component to itself
        if (fromId === toId) return false;

        this.wires.push({ fromComp: fromId, fromPin: fromPin, toComp: toId, toPin: toPin });
        return true;
    }

    removeComponent(id) {
        this.components = this.components.filter(c => c.id !== id);
        this.wires = this.wires.filter(w => w.fromComp !== id && w.toComp !== id);
    }

    // The heart of the simulation: Rule-based logic
    // Simplified Topological Check:
    // 1. Find Power Sources.
    // 2. Trace "Hot" paths (connected to Pos).
    // 3. Trace "Ground" paths (connected to Neg).
    // 4. A component is powered if it touches both Hot and Ground.
    evaluate() {
        // Reset all output states
        this.components.forEach(c => {
            if (ComponentRegistry[c.type].type === 'output') {
                c.state.on = false;
            }
        });

        const powerSources = this.components.filter(c => ComponentRegistry[c.type].type === 'source');

        powerSources.forEach(source => {
            // Find Hot Net (Connected recursively to Positive terminal)
            const hotNodes = this.traceNet(source.id, 'pos');
            // Find Ground Net (Connected recursively to Negative terminal)
            const gndNodes = this.traceNet(source.id, 'neg');

            // Check every component: Is it bridging Hot and Ground?
            this.components.forEach(comp => {
                if (comp.id === source.id) return; // Skip battery itself

                const def = ComponentRegistry[comp.type];

                // Special handling for RGB LED
                if (comp.type === 'led_rgb') {
                    const rHot = hotNodes.has(`${comp.id}:r`);
                    const gHot = hotNodes.has(`${comp.id}:g`);
                    const bHot = hotNodes.has(`${comp.id}:b`);
                    const commonGnd = gndNodes.has(`${comp.id}:gnd`);

                    if (commonGnd) {
                        comp.state.r = !!rHot;
                        comp.state.g = !!gHot;
                        comp.state.b = !!bHot;
                    } else {
                        comp.state.r = false;
                        comp.state.g = false;
                        comp.state.b = false;
                    }
                    return;
                }

                // Special Handling for Sensors (Require VCC and GND)
                if (comp.type.startsWith('sensor_')) {
                    const vccHot = hotNodes.has(`${comp.id}:vcc`);
                    const gndGnd = gndNodes.has(`${comp.id}:gnd`);

                    if (vccHot && gndGnd) {
                        // Sensor is powered
                        // For simplicity in this demo, it "works" if powered
                        // Actual logic (e.g. triggering output) depends on interaction
                    } else {
                        // Reset?
                    }
                    return;
                }

                // Default 2-pin Logic (Motor, LED, Buzzer, simple Resistor)
                if (def.pins.length >= 2) {
                    // Try to find reasonable pair. Usually 0 and 1.
                    // Or check specific named pins if defined?
                    // Let's stick to 0 and 1 for simple components.
                    const pin1 = def.pins[0].id;
                    const pin2 = def.pins[1].id;

                    const p1Hot = hotNodes.has(`${comp.id}:${pin1}`);
                    const p1Gnd = gndNodes.has(`${comp.id}:${pin1}`);
                    const p2Hot = hotNodes.has(`${comp.id}:${pin2}`);
                    const p2Gnd = gndNodes.has(`${comp.id}:${pin2}`);

                    // Condition for flow: One pin is Hot, other is Ground
                    if ((p1Hot && p2Gnd) || (p2Hot && p1Gnd)) {
                        comp.state.on = true;
                    }
                }
            });
        });
    }

    // BFS to find all connected pins from a start point
    // Respects Open Switches (stops traversal)
    traceNet(startCompId, startPinId) {
        const visited = new Set();
        const queue = [{ c: startCompId, p: startPinId }];
        visited.add(`${startCompId}:${startPinId}`);

        while (queue.length > 0) {
            const current = queue.shift();

            // 1. Find wires connected to this pin
            const connectedWires = this.wires.filter(w =>
                (w.fromComp === current.c && w.fromPin === current.p) ||
                (w.toComp === current.c && w.toPin === current.p)
            );

            connectedWires.forEach(w => {
                const neighborCompId = (w.fromComp === current.c) ? w.toComp : w.fromComp;
                const neighborPinId = (w.fromComp === current.c) ? w.toPin : w.fromPin;
                const key = `${neighborCompId}:${neighborPinId}`;

                if (!visited.has(key)) {
                    visited.add(key);
                    queue.push({ c: neighborCompId, p: neighborPinId });

                    // 2. Traverse THROUGH the component to its other pins?
                    // ONLY if the component is conductive internally.
                    // - Wires/Nodes: Yes (but we don't have breadboard nodes yet, simplified to direct wire)
                    // - Resistors/LEDs: Yes, they conduct.
                    // - Switches: Only if CLOSED.
                    // - Batteries: No, they are the source/sink bound.

                    const neighborComp = this.components.find(c => c.id === neighborCompId);
                    if (neighborComp) {
                        const type = neighborComp.type;
                        // Conduct through...
                        if (type === 'switch_toggle' || type === 'push_button') {
                            if (neighborComp.state.closed) {
                                this.addAllOtherPins(neighborComp, neighborPinId, visited, queue);
                            }
                        } else if (type === 'battery9v') {
                            // Do not conduct through battery
                        } else {
                            // Resistors, LEDs, Motors -> Assume conductive for net tracing
                            this.addAllOtherPins(neighborComp, neighborPinId, visited, queue);
                        }
                    }
                }
            });
        }
        return visited;
    }

    addAllOtherPins(comp, entryPin, visited, queue) {
        const def = ComponentRegistry[comp.type];
        def.pins.forEach(pin => {
            if (pin.id !== entryPin) {
                const key = `${comp.id}:${pin.id}`;
                if (!visited.has(key)) {
                    visited.add(key);
                    queue.push({ c: comp.id, p: pin.id });
                }
            }
        });
    }

    getComponent(id) {
        return this.components.find(c => c.id === id);
    }
}

window.CircuitEngine = CircuitEngine;
