/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Space Grotesk"', "Inter", "system-ui", "sans-serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      colors: {
        // Earthy severity scale (savanna): sage → gold → terracotta → deep red
        sev: {
          none: "#6f9b6e",
          watch: "#e0b341",
          warning: "#d9863c",
          alert: "#c0442e",
        },
        // Warm accent (ochre/terracotta) to replace generic sky-blue
        ochre: {
          400: "#e3a15a",
          500: "#d9863c",
          600: "#c06f2c",
        },
      },
    },
  },
  plugins: [],
};
