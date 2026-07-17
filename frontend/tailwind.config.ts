import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        night: "#101426",
        plum: "#25152d",
        gold: "#d9b56d",
        cream: "#fff7e8",
        mist: "#d7d5e7"
      },
      boxShadow: {
        glow: "0 0 40px rgba(217, 181, 109, 0.24)"
      }
    }
  },
  plugins: []
};

export default config;
