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
        sans:     ["Nunito", "system-ui", "sans-serif"],
        display:  ["Cinzel", "Georgia", "serif"],
        serif:    ["Cinzel", "Georgia", "serif"],
        spectral: ["Spectral", "Georgia", "serif"],
      },
      colors: {
        indigo: {
          DEFAULT: "#2A1D7E",
          light:   "#4B3DC0",
          dark:    "#170F4A",
        },
        gold: {
          DEFAULT: "#C4902A",
          light:   "#E8C050",
          deep:    "#8A6018",
          pale:    "#FAF0D8",
        },
        parchment: "#F3F0E8",
        surface:   "#FEFCF8",
        ink: {
          DEFAULT: "#140F1A",
          soft:    "#3A3255",
          muted:   "#8A85A0",
          faint:   "#B0ADB8",
        },
        success: "#1E5E3E",
        warning: "#A84C16",
        danger:  "#9C2424",
      },
      keyframes: {
        riseUp: {
          "0%":   { opacity: "0", transform: "translateY(18px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        fadeUp: {
          "0%":   { opacity: "0", transform: "translateY(14px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        breathe: {
          "0%, 100%": { opacity: "0.03" },
          "50%":       { opacity: "0.06" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        aureate: {
          "0%, 100%": { boxShadow: "0 4px 20px rgba(196,144,42,0.10)" },
          "50%":       { boxShadow: "0 4px 30px rgba(196,144,42,0.26), 0 0 0 3px rgba(196,144,42,0.07)" },
        },
      },
      animation: {
        riseUp:  "riseUp 0.7s cubic-bezier(0.22,1,0.36,1) both",
        fadeUp:  "fadeUp 0.6s cubic-bezier(0.22,1,0.36,1) both",
        breathe: "breathe 4s ease-in-out infinite",
        shimmer: "shimmer 2.5s linear infinite",
        aureate: "aureate 3.5s ease-in-out infinite",
      },
      boxShadow: {
        indigo:  "0 6px 28px rgba(42,29,126,0.22)",
        gold:    "0 6px 28px rgba(196,144,42,0.20)",
        card:    "0 2px 10px rgba(42,29,126,0.06), 0 1px 4px rgba(20,15,26,0.04)",
        feather: "0 8px 40px -8px rgba(42,29,126,0.12)",
        deep:    "0 14px 44px rgba(42,29,126,0.12), 0 4px 12px rgba(20,15,26,0.06)",
      },
    },
  },
  plugins: [],
};

export default config;
