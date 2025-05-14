/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
  extend: {
    colors: {
      dark: '#0e0e10',
      light: '#1a1a1d',
      accent: '#3f8efc',
    },fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
      },
  }
}
,
  plugins: [],
}
