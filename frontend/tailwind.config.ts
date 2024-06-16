import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      boxShadow: {
        loader: '24px 0 , -24px 0 ,  48px 0'
      },
      animation: {
        rotation: 'rotation 1s linear infinite'
      },
      keyframes: {
        rotation: {
          '0%': {
            transform: "rotate(0deg)",
          },
          "100%": {
            transform: "rotate(360deg)"
          }
        }
      },
      flex: {
        thumbnail: '0 0 calc(100% / 20)'
      }
    },
  },
  plugins: [],
};
export default config;
