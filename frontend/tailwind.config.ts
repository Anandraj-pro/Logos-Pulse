import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Nunito", "system-ui", "sans-serif"],
        serif: ["Playfair Display", "Georgia", "serif"],
        garamond: ["EB Garamond", "Georgia", "serif"],
      },
      colors: {
        indigo: {
          DEFAULT: "#3B2F8E",
          light: "#5B4FC4",
          dark: "#1E1733",
        },
        gold: {
          DEFAULT: "#C9982A",
          light: "#f0d98a",
          deep: "#9e7420",
        },
        parchment: "#F8F7FF",
        ink: {
          DEFAULT: "#1A1A2E",
          soft: "#374151",
          muted: "#6B7280",
          faint: "#9CA3AF",
        },
        success: "#2D6A4F",
        warning: "#C26B2C",
        danger: "#B5383C",
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        breathe: {
          "0%, 100%": { opacity: "0.03" },
          "50%": { opacity: "0.06" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        fadeUp: "fadeUp 0.6s ease-out both",
        breathe: "breathe 4s ease-in-out infinite",
        shimmer: "shimmer 2.5s linear infinite",
      },
      boxShadow: {
        indigo: "0 4px 20px rgba(59,47,142,0.35)",
        card: "0 2px 12px rgba(59,47,142,0.08)",
        feather: "0 8px 40px -8px rgba(59,47,142,0.12)",
      },
    },
  },
  plugins: [],
};

export default config;
