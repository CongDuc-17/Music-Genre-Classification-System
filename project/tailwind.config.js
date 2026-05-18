/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html', './apps/**/templates/**/*.html', './static/**/*.js'],
  theme: {
    extend: {
      colors: {
        spotify: {
          bg: '#121212',
          surface: '#1F1F1F',
          elevated: '#282828',
          green: '#1ED760',
          greenHover: '#1DB954',
          text: '#FFFFFF',
          muted: '#B3B3B3',
        },
      },
      boxShadow: {
        lift: '0 8px 24px rgba(0,0,0,0.45)',
        card: '0 4px 16px rgba(0,0,0,0.35)',
      },
    },
  },
  plugins: [],
};
