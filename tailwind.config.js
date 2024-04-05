/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html"
  ],
  
  theme: {
    typography: {
      DEFAULT: { 
        css: {
          color: "#eeeeee",
        }
      }
    },
    extend: {
      colors:{
        "primary": "#91a375",
        "background": "#212121",
        "text": "#eeeeee",
        "seconday": "#121212",
        "accent": "#76885b",
      },
      fontFamily: {
        roboto: ["Roboto", "sans-serif"],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}