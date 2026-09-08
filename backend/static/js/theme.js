document.addEventListener('alpine:init', () => {
    Alpine.data('theme', () => ({
        // Force dark mode for everyone
        darkMode: true,

        init() {
            // Always apply dark theme
            document.documentElement.classList.add('dark');
        },

        applyTheme() {
            // Always dark
            document.documentElement.classList.add('dark');
        }
    }));
});

// Immediately apply dark mode (before Alpine loads)
document.documentElement.classList.add('dark');
