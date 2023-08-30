/** @type {import('tailwindcss').Config} */
module.exports = {
  // darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
    },
    fontFamily: {
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: true,
    logs: false,
  },
}

