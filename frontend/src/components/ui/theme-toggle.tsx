"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Sun, Moon, Sparkles } from "lucide-react";
import { useTheme, type Theme } from "@/lib/theme-provider";

const themes: { id: Theme; label: string; icon: React.ReactNode }[] = [
  { id: "light",  label: "Light",  icon: <Sun  className="h-3.5 w-3.5" /> },
  { id: "dark",   label: "Dark",   icon: <Moon className="h-3.5 w-3.5" /> },
  { id: "prisma", label: "Prisma", icon: <Sparkles className="h-3.5 w-3.5" /> },
];

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="theme-toggle-wrap fixed bottom-6 right-6 z-50">
      <div
        className="flex items-center gap-1 rounded-full border p-1 backdrop-blur-md shadow-lg"
        style={{
          background: "var(--toggle-bg)",
          borderColor: "var(--toggle-border)",
        }}
      >
        {themes.map((t) => {
          const active = theme === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setTheme(t.id)}
              className="relative flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-medium transition-colors"
              style={{
                color: active ? "var(--toggle-active-text)" : "var(--toggle-text)",
              }}
              aria-pressed={active}
            >
              {active && (
                <motion.span
                  layoutId="theme-pill"
                  className="absolute inset-0 rounded-full"
                  style={{ background: "var(--toggle-active-bg)" }}
                  transition={{ type: "spring", stiffness: 400, damping: 30 }}
                />
              )}
              <span className="relative z-10 flex items-center gap-1.5">
                {t.icon}
                {t.label}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}