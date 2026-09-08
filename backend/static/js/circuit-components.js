/**
 * circuit-components.js
 * Definitions for all circuit components.
 * Includes behavior type, pin locations, and SVG rendering logic.
 */

const ComponentRegistry = {
    // --- Power Sources ---
    battery9v: {
        type: 'source',
        pins: [
            { id: 'pos', x: 15, y: 10 },
            { id: 'neg', x: 45, y: 10 }
        ],
        defaultState: {},
        render: (state) => `
            <rect x="5" y="10" width="50" height="70" rx="4" fill="#334155" stroke="#1e293b" stroke-width="2"/>
            <text x="30" y="50" text-anchor="middle" fill="#94a3b8" font-size="12" font-weight="bold" font-family="sans-serif">9V</text>
            <!-- Terminals -->
            <circle cx="15" cy="10" r="6" fill="#ef4444" stroke="#7f1d1d" stroke-width="2"/>
            <text x="15" y="22" text-anchor="middle" fill="#ef4444" font-size="10" font-weight="bold">+</text>
            <circle cx="45" cy="10" r="6" fill="#000000" stroke="#333" stroke-width="2"/>
            <text x="45" y="22" text-anchor="middle" fill="#64748b" font-size="10" font-weight="bold">-</text>
        `
    },
    battery5v: {
        type: 'source',
        pins: [
            { id: 'pos', x: 25, y: 10 },
            { id: 'neg', x: 25, y: 70 }
        ],
        defaultState: {},
        render: (state) => `
            <rect x="15" y="10" width="20" height="60" rx="2" fill="#eab308" stroke="#854d0e" stroke-width="2"/>
            <text x="25" y="45" text-anchor="middle" fill="#854d0e" font-size="10" font-weight="bold" transform="rotate(-90 25 45)">5V</text>
            <!-- Terminals -->
            <circle cx="25" cy="10" r="4" fill="#ef4444" />
            <circle cx="25" cy="70" r="4" fill="#000000" />
        `
    },

    // --- Outputs ---
    led_red: {
        type: 'output',
        pins: [
            { id: 'anode', x: 15, y: 50 },
            { id: 'cathode', x: 35, y: 50 }
        ],
        defaultState: { on: false },
        render: (state) => {
            const color = state.on ? '#ff3333' : '#7f1d1d';
            const filter = state.on ? 'drop-shadow(0 0 8px #ff0000)' : '';
            return `
                <path d="M15,50 L15,30 A10,10 0 1,1 35,30 L35,50 Z" fill="${color}" style="filter: ${filter}" stroke="#333" stroke-width="1"/>
                <line x1="15" y1="50" x2="15" y2="60" stroke="#94a3b8" stroke-width="2"/>
                <line x1="35" y1="50" x2="35" y2="60" stroke="#94a3b8" stroke-width="2"/>
                <!-- Glow effect usage could also be via class -->
            `;
        }
    },
    led_rgb: {
        type: 'output',
        pins: [
            { id: 'r', x: 10, y: 50 },
            { id: 'gnd', x: 25, y: 55 }, // Common Cathode usually longer, sticking out
            { id: 'g', x: 40, y: 50 },
            { id: 'b', x: 55, y: 50 }
        ],
        defaultState: { r: false, g: false, b: false },
        render: (state) => {
            let r = 50, g = 50, b = 50;
            if (state.r) r += 200;
            if (state.g) g += 200;
            if (state.b) b += 200;
            const fill = `rgb(${r},${g},${b})`;
            return `
                <circle cx="32" cy="30" r="15" fill="${fill}" stroke="#333" stroke-width="1"/>
                <line x1="10" y1="50" x2="20" y2="38" stroke="#94a3b8" stroke-width="1"/>
                <line x1="25" y1="55" x2="28" y2="40" stroke="#94a3b8" stroke-width="1"/>
                <line x1="40" y1="50" x2="36" y2="38" stroke="#94a3b8" stroke-width="1"/>
                <line x1="55" y1="50" x2="44" y2="38" stroke="#94a3b8" stroke-width="1"/>
                <text x="10" y="65" font-size="8" fill="#aaa">R</text>
                <text x="25" y="70" font-size="8" fill="#aaa">-</text>
                <text x="40" y="65" font-size="8" fill="#aaa">G</text>
                <text x="55" y="65" font-size="8" fill="#aaa">B</text>
            `;
        }
    },
    motor_dc: {
        type: 'output',
        pins: [
            { id: 'p1', x: 10, y: 50 },
            { id: 'p2', x: 50, y: 50 }
        ],
        defaultState: { on: false },
        render: (state) => `
            <circle cx="30" cy="30" r="20" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>
            <line x1="10" y1="50" x2="15" y2="40" stroke="#94a3b8" stroke-width="2"/>
            <line x1="50" y1="50" x2="45" y2="40" stroke="#94a3b8" stroke-width="2"/>
            <g transform="translate(30, 30)">
                <path d="M-15,0 L15,0 M0,-15 L0,15" stroke="#0f172a" stroke-width="4" class="${state.on ? 'motor-spin' : ''}" style="transform-origin: center;"/>
            </g>
        `
    },
    buzzer: {
        type: 'output',
        pins: [
            { id: 'p1', x: 10, y: 40 },
            { id: 'p2', x: 40, y: 40 }
        ],
        defaultState: { on: false },
        render: (state) => `
            <circle cx="25" cy="25" r="15" fill="#1e293b" stroke="#333" stroke-width="2"/>
            <circle cx="25" cy="25" r="4" fill="#000" fill-opacity="0.5"/>
            ${state.on ? '<circle cx="25" cy="25" r="20" stroke="orange" stroke-width="2" fill="none" opacity="0.5"><animate attributeName="r" from="15" to="25" dur="0.2s" repeatCount="indefinite"/><animate attributeName="opacity" from="0.8" to="0" dur="0.2s" repeatCount="indefinite"/></circle>' : ''}
            <line x1="10" y1="40" x2="15" y2="32" stroke="#94a3b8" stroke-width="2"/>
            <line x1="40" y1="40" x2="35" y2="32" stroke="#94a3b8" stroke-width="2"/>
        `
    },

    // --- Controls ---
    switch_toggle: {
        type: 'control',
        pins: [
            { id: 'p1', x: 10, y: 30 },
            { id: 'p2', x: 50, y: 30 }
        ],
        defaultState: { closed: false },
        render: (state) => `
            <rect x="15" y="15" width="30" height="30" fill="#94a3b8" rx="2"/>
            <rect x="20" y="20" width="20" height="20" fill="${state.closed ? '#22c55e' : '#ef4444'}" rx="1"/>
            <line x1="10" y1="30" x2="15" y2="30" stroke="#333" stroke-width="2"/>
            <line x1="45" y1="30" x2="50" y2="30" stroke="#333" stroke-width="2"/>
            <text x="30" y="12" font-size="8" text-anchor="middle">${state.closed ? 'ON' : 'OFF'}</text>
        `
    },
    push_button: {
        type: 'control',
        pins: [
            { id: 'p1', x: 10, y: 30 },
            { id: 'p2', x: 50, y: 30 }
        ],
        defaultState: { closed: false },
        render: (state) => `
            <rect x="15" y="15" width="30" height="30" fill="#333" rx="4"/>
            <circle cx="30" cy="30" r="10" fill="${state.closed ? '#ef4444' : '#ef4444'}" stroke="#991b1b" stroke-width="${state.closed ? 0 : 4}"/>
            <line x1="10" y1="30" x2="15" y2="30" stroke="#94a3b8" stroke-width="2"/>
            <line x1="45" y1="30" x2="50" y2="30" stroke="#94a3b8" stroke-width="2"/>
        `
    },
    resistor: {
        type: 'passive',
        pins: [
            { id: 'p1', x: 0, y: 15 },
            { id: 'p2', x: 60, y: 15 }
        ],
        defaultState: {},
        render: (state) => `
            <line x1="0" y1="15" x2="10" y2="15" stroke="#333" stroke-width="2"/>
            <path d="M10,15 L15,5 L25,25 L35,5 L45,25 L50,15" fill="none" stroke="#f59e0b" stroke-width="2"/>
            <line x1="50" y1="15" x2="60" y2="15" stroke="#333" stroke-width="2"/>
        `
    },
    potentiometer: {
        type: 'passive',
        pins: [
            { id: 'vcc', x: 10, y: 40 },
            { id: 'out', x: 30, y: 40 },
            { id: 'gnd', x: 50, y: 40 }
        ],
        defaultState: { value: 50 },
        render: (state) => `
            <circle cx="30" cy="20" r="15" fill="#ddd" stroke="#999" stroke-width="1"/>
            <line x1="30" y1="20" x2="30" y2="5" stroke="#333" stroke-width="2" transform="rotate(${state.value * 2.7 - 135} 30 20)"/>
            <line x1="10" y1="40" x2="20" y2="30" stroke="#94a3b8"/>
            <line x1="30" y1="40" x2="30" y2="35" stroke="#94a3b8"/>
            <line x1="50" y1="40" x2="40" y2="30" stroke="#94a3b8"/>
        `
    },

    // --- Sensors ---
    // Visual placeholder for sensors, assumed 3 pin (VCC, OUT, GND) or 4 pin
    sensor_ldr: {
        type: 'sensor',
        pins: [{ id: 'vcc', x: 10, y: 40 }, { id: 'out', x: 30, y: 40 }, { id: 'gnd', x: 50, y: 40 }],
        defaultState: { value: 0 },
        render: (state) => `
            <rect x="5" y="5" width="50" height="30" fill="#eab308" rx="2"/>
            <text x="30" y="25" text-anchor="middle" font-size="10" font-weight="bold">LDR</text>
            <line x1="10" y1="40" x2="10" y2="35" stroke="#333"/>
            <line x1="30" y1="40" x2="30" y2="35" stroke="#333"/>
            <line x1="50" y1="40" x2="50" y2="35" stroke="#333"/>
        `
    },
    sensor_ultrasonic: {
        type: 'sensor',
        pins: [{ id: 'vcc', x: 10, y: 40 }, { id: 'trig', x: 23, y: 40 }, { id: 'echo', x: 36, y: 40 }, { id: 'gnd', x: 50, y: 40 }],
        defaultState: { value: 0 },
        render: (state) => `
            <rect x="5" y="5" width="50" height="25" fill="#3b82f6" rx="2"/>
            <circle cx="15" cy="18" r="6" fill="#ddd" stroke="#333"/>
            <circle cx="45" cy="18" r="6" fill="#ddd" stroke="#333"/>
            <text x="30" y="12" text-anchor="middle" font-size="6" fill="#fff">HC-SR04</text>
        `
    },
    sensor_ir: {
        type: 'sensor',
        pins: [{ id: 'vcc', x: 10, y: 40 }, { id: 'out', x: 30, y: 40 }, { id: 'gnd', x: 50, y: 40 }],
        defaultState: { value: 0 },
        render: (state) => `
            <rect x="5" y="5" width="50" height="30" fill="#22c55e" rx="2"/>
            <text x="30" y="25" text-anchor="middle" font-size="10" font-weight="bold">IR</text>
        `
    },
    sensor_temp: {
        type: 'sensor',
        pins: [{ id: 'vcc', x: 10, y: 40 }, { id: 'out', x: 30, y: 40 }, { id: 'gnd', x: 50, y: 40 }],
        defaultState: { value: 0 },
        render: (state) => `
            <rect x="5" y="5" width="50" height="30" fill="#ef4444" rx="2"/>
            <text x="30" y="25" text-anchor="middle" font-size="10" font-weight="bold">LM35</text>
        `
    },
    sensor_pir: {
        type: 'sensor',
        pins: [{ id: 'vcc', x: 10, y: 40 }, { id: 'out', x: 30, y: 40 }, { id: 'gnd', x: 50, y: 40 }],
        defaultState: { value: 0 },
        render: (state) => `
            <rect x="5" y="5" width="50" height="30" fill="#a855f7" rx="2"/>
            <circle cx="30" cy="20" r="8" fill="#fff" opacity="0.8"/>
            <text x="30" y="25" text-anchor="middle" font-size="8" font-weight="bold">PIR</text>
        `
    }
};

window.ComponentRegistry = ComponentRegistry;
