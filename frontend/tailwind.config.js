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
    themes: [
      {
        light: {
          ...require("daisyui/src/theming/themes")["[data-theme=light]"],
        },
        dark: {
          ...require("daisyui/src/theming/themes")["[data-theme=dark]"],
          "info": "#88b5dd",
          "success": "#2dcda8",
          "warning": "#fbae51",
          "error": "#eb7560",
        }
      }
    ],
    logs: false,
  },
}

