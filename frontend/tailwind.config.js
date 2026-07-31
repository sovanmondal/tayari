/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        sev: {
          none: "#4ade80",
          watch: "#facc15",
          warning: "#fb923c",
          alert: "#ef4444",
        },
      },
    },
  },
  plugins: [],
};
