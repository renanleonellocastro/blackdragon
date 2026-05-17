import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'bd-bg': {
          primary: '#050505',
          secondary: '#0A0A0A',
          panel: '#111111',
          surface: '#181818',
        },
        'bd-border': {
          DEFAULT: '#2A2A2A',
          accent: '#3A3A3A',
        },
        'bd-text': {
          primary: '#E5E5E5',
          secondary: '#9CA3AF',
          muted: '#6B7280',
        },
        'bd-accent': {
          DEFAULT: '#6B7280',
          highlight: '#D1D5DB',
          metallic: '#8B8B8B',
        },
        'bd-chrome': {
          light: '#C0C0C0',
          mid: '#808080',
          dark: '#404040',
        },
        'bd-success': '#10B981',
        'bd-warning': '#F59E0B',
        'bd-error': '#EF4444',
      },
      boxShadow: {
        'bd-glow': '0 0 12px rgba(107, 114, 128, 0.3)',
        'bd-glow-accent': '0 0 16px rgba(209, 213, 219, 0.2)',
        'bd-emboss':
          'inset 0 1px 0 rgba(192, 192, 192, 0.05), 0 2px 8px rgba(0, 0, 0, 0.6), 0 1px 2px rgba(0, 0, 0, 0.4)',
        'bd-node':
          '0 0 0 1px rgba(42, 42, 42, 1), 0 4px 12px rgba(0, 0, 0, 0.5)',
      },
      backgroundImage: {
        'bd-metallic':
          'linear-gradient(135deg, #404040 0%, #808080 50%, #404040 100%)',
        'bd-chrome':
          'linear-gradient(180deg, #C0C0C0 0%, #808080 50%, #404040 100%)',
        'bd-hero':
          'radial-gradient(ellipse at center top, #111111 0%, #050505 70%)',
      },
      fontFamily: {
        'bd-sans': ['"Exo 2"', 'system-ui', 'sans-serif'],
        'bd-mono': ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
      animation: {
        'bd-pulse-glow': 'bd-pulse-glow 2s ease-in-out infinite',
      },
      keyframes: {
        'bd-pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 8px rgba(107, 114, 128, 0.2)' },
          '50%': { boxShadow: '0 0 16px rgba(107, 114, 128, 0.4)' },
        },
      },
    },
  },
  plugins: [],
}

export default config
