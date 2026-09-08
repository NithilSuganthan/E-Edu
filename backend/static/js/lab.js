function labData() {
    return {
        activeTab: 'code',
        // Coding Logic
        languages: [
            { id: 'python', name: 'Python', filename: 'main.py', code: 'def main():\n    print("Hello, Inventobots!")\n\nif __name__ == "__main__":\n    main()' },
            { id: 'java', name: 'Java', filename: 'Main.java', code: 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, Inventobots!");\n    }\n}' },
            { id: 'c', name: 'C', filename: 'main.c', code: '#include <stdio.h>\n\nint main() {\n    printf("Hello, Inventobots!\\n");\n    return 0;\n}' },
            { id: 'cpp', name: 'C++', filename: 'main.cpp', code: '#include <iostream>\n\nint main() {\n    std::cout << "Hello, Inventobots!" << std::endl;\n    return 0;\n}' }
        ],
        currentLang: {},
        codeContent: '',
        output: '> Ready to compile...',

        init() {
            this.setLanguage('python');
        },
        setLanguage(id) {
            this.currentLang = this.languages.find(l => l.id === id);
            this.codeContent = this.currentLang.code;
            this.output = '> Ready to compile ' + this.currentLang.name + '...';
        },
        runCode() {
            this.output = '<span class="text-yellow-400">Compiling...</span>';
            setTimeout(() => {
                this.output = `> Running ${this.currentLang.filename}...\n<span class="text-green-400">Hello, Inventobots!</span>\n\n[Process exited with code 0]`;
            }, 800);
        },

        // Circuit Logic
        circuitOn: false,
        toggleCircuit() {
            this.circuitOn = !this.circuitOn;
        },

        // Abacus Logic (Simple Style Toggle)
        toggleBead(event) {
            const bead = event.target;
            const col = bead.closest('.relative');
            const isHeaven = bead.hasAttribute('data-heaven');

            if (isHeaven) {
                // Heaven Bead Logic (Toggle)
                bead.classList.toggle('active-heaven');
            } else {
                // Earth Bead Logic (Stacking)
                // Get all earth beads in this column
                const earthBeads = Array.from(col.querySelectorAll('.bead[data-earth]'));
                const index = earthBeads.indexOf(bead);

                // Check current state of clicked bead
                const isActive = bead.classList.contains('active-earth');

                if (!isActive) {
                    // Move this UP. Requirement: All beads ABOVE (index < clickedIndex) must also be UP.
                    for (let i = 0; i <= index; i++) {
                        earthBeads[i].classList.add('active-earth');
                    }
                } else {
                    // Move this DOWN. Requirement: All beads BELOW (index > clickedIndex) must also be DOWN.
                    for (let i = index; i < earthBeads.length; i++) {
                        earthBeads[i].classList.remove('active-earth');
                    }
                }
            }
        }
    }
}
