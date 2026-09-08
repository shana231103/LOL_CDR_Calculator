/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        app: '#111215',
        surface: {
          DEFAULT: '#181A1F',
          hover: '#21242C',
          inset: '#131519',
        },
        border: {
          subtle: '#1F2228',
          default: '#2A2D35',
          active: '#4B5162',
        },
        accent: {
          ah: '#38BDF8',
          ult: '#F59E0B',
          summoner: '#A855F7',
          success: '#10B981',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
}
