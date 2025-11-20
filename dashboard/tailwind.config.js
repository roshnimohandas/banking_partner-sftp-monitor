/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand-primary': '#667eea',
        'brand-secondary': '#764ba2',
      }
    },
  },
  plugins: [],
}
