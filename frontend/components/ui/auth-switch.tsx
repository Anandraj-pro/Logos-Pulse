"use client";

import { cn } from "@/lib/utils";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Eye,
  EyeOff,
  Mail,
  Lock,
  User,
  ArrowRight,
  Loader2,
} from "lucide-react";

// ─────────────────────────────────────────────────────────────
//  Types
// ─────────────────────────────────────────────────────────────
type Mode = "signin" | "signup";

interface AuthSwitchProps {
  onSignIn?: (email: string, password: string) => Promise<void>;
  onSignUp?: (name: string, email: string, password: string) => Promise<void>;
  className?: string;
}

// ─────────────────────────────────────────────────────────────
//  Scripture fragments that float in the background
// ─────────────────────────────────────────────────────────────
const FRAGMENTS = [
  "In the beginning was the Word",
  "The Lord is my shepherd",
  "I can do all things through Christ",
  "Your word is a lamp to my feet",
  "Be still and know that I am God",
  "The peace of God surpasses all understanding",
  "Trust in the Lord with all your heart",
  "Seek first the Kingdom of God",
  "For I know the plans I have for you",
  "His mercies are new every morning",
  "The joy of the Lord is my strength",
  "Draw near to God and He will draw near",
];

// ─────────────────────────────────────────────────────────────
//  FloatingVerses — drifting scripture backdrop
// ─────────────────────────────────────────────────────────────
function FloatingVerses() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none select-none">
      {FRAGMENTS.map((frag, i) => {
        const top = 4 + (i * 8.2) % 92;
        const left = (i * 19 + 5) % 85;
        const rot = -12 + (i % 5) * 6;
        const dur = 20 + i * 4;
        const delay = i * 2.1;
        const gold = i % 3 === 0;
        return (
          <span
            key={i}
            className="absolute whitespace-nowrap text-[11px] tracking-wider"
            style={{
              fontFamily: "'EB Garamond', Georgia, serif",
              color: gold ? "#C9982A" : "#9E96AB",
              opacity: 0.035,
              top: `${top}%`,
              left: `${left}%`,
              transform: `rotate(${rot}deg)`,
              animation: `verse-drift ${dur}s ease-in-out ${delay}s infinite`,
            }}
          >
            {frag}
          </span>
        );
      })}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
//  CrossIcon — pure SVG gold cross for the logo
// ─────────────────────────────────────────────────────────────
function CrossIcon() {
  return (
    <svg width="24" height="28" viewBox="0 0 24 28" fill="none" aria-hidden>
      <defs>
        <linearGradient id="cross-grad" x1="0" y1="0" x2="24" y2="28" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor="#EDD68A" />
          <stop offset="100%" stopColor="#C9982A" />
        </linearGradient>
      </defs>
      <rect x="10" y="0" width="4" height="28" rx="2" fill="url(#cross-grad)" />
      <rect x="0" y="8" width="24" height="4" rx="2" fill="url(#cross-grad)" />
    </svg>
  );
}

// ─────────────────────────────────────────────────────────────
//  FloatingInput — animated floating-label input
// ─────────────────────────────────────────────────────────────
interface FloatingInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  icon?: React.ReactNode;
  suffix?: React.ReactNode;
}

function FloatingInput({ label, icon, suffix, className, ...props }: FloatingInputProps) {
  const [focused, setFocused] = useState(false);
  const hasValue = String(props.value ?? "").length > 0;
  const lifted = focused || hasValue;

  return (
    <div
      className="relative flex items-center rounded-xl transition-all duration-200"
      style={{
        background: "rgba(255,255,255,0.035)",
        border: `1.5px solid ${focused ? "rgba(201,152,42,0.55)" : "rgba(255,255,255,0.07)"}`,
        boxShadow: focused
          ? "0 0 0 3px rgba(201,152,42,0.09), inset 0 1px 0 rgba(255,255,255,0.04)"
          : "inset 0 1px 0 rgba(255,255,255,0.03)",
      }}
    >
      {/* Leading icon */}
      {icon && (
        <div
          className="pl-4 flex-shrink-0 transition-colors duration-200"
          style={{ color: focused ? "#C9982A" : "rgba(158,150,171,0.45)" }}
        >
          {icon}
        </div>
      )}

      {/* Label + input */}
      <div className="flex-1 relative">
        <label
          className="absolute left-3 pointer-events-none transition-all duration-200 font-semibold"
          style={{
            fontFamily: "'Nunito', sans-serif",
            fontSize: lifted ? "9.5px" : "13.5px",
            top: lifted ? "9px" : "50%",
            transform: lifted ? "none" : "translateY(-50%)",
            color: focused ? "rgba(201,152,42,0.75)" : "rgba(158,150,171,0.45)",
            letterSpacing: lifted ? "1px" : "0.2px",
            textTransform: lifted ? "uppercase" : "none",
          }}
        >
          {label}
        </label>
        <input
          {...props}
          onFocus={(e) => { setFocused(true); props.onFocus?.(e); }}
          onBlur={(e) => { setFocused(false); props.onBlur?.(e); }}
          className={cn(
            "w-full bg-transparent outline-none pt-5 pb-2.5 px-3 text-sm font-medium",
            className
          )}
          style={{
            fontFamily: "'Nunito', sans-serif",
            color: "rgba(255,255,255,0.88)",
            caretColor: "#C9982A",
          }}
        />
      </div>

      {/* Trailing suffix */}
      {suffix && <div className="pr-4 flex-shrink-0">{suffix}</div>}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
//  AuthSwitch — main exported component
// ─────────────────────────────────────────────────────────────
export const Component = ({ onSignIn, onSignUp, className }: AuthSwitchProps) => {
  const [mode, setMode] = useState<Mode>("signin");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const switchMode = (m: Mode) => { setMode(m); setError(""); };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "signin") await onSignIn?.(email, password);
      else await onSignUp?.(name, email, password);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Inject keyframes + fonts once */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=EB+Garamond:ital,wght@0,400;1,400&family=Nunito:wght@400;500;600;700;800&display=swap');

        @keyframes verse-drift {
          0%,100% { transform: translateY(0px) rotate(var(--rot,0deg)); opacity:0.035; }
          33%      { transform: translateY(-14px) rotate(var(--rot,0deg)); opacity:0.05; }
          66%      { transform: translateY(8px) rotate(var(--rot,0deg)); opacity:0.028; }
        }

        @keyframes lp-shimmer {
          0%   { background-position: -200% 0; }
          100% { background-position:  200% 0; }
        }

        @keyframes lp-glow-pulse {
          0%,100% { box-shadow: 0 0 20px rgba(59,47,142,0.3); }
          50%      { box-shadow: 0 0 36px rgba(59,47,142,0.5); }
        }

        .lp-btn-shimmer {
          background: linear-gradient(
            135deg,
            #3B2F8E 0%,
            #5B4FC4 40%,
            #7B6FD4 50%,
            #5B4FC4 60%,
            #3B2F8E 100%
          );
          background-size: 200% 100%;
          animation: lp-shimmer 3s linear infinite, lp-glow-pulse 4s ease-in-out infinite;
        }

        .lp-btn-shimmer:hover {
          animation: lp-shimmer 1.5s linear infinite;
        }
      `}</style>

      <div
        className={cn(
          "relative min-h-screen flex items-center justify-center overflow-hidden",
          className
        )}
      >
        {/* ── Background ── */}
        <div className="absolute inset-0 bg-[#060410]">
          {/* Radial gradient mesh */}
          <div
            className="absolute inset-0"
            style={{
              background: `
                radial-gradient(ellipse at 18% 18%, rgba(59,47,142,0.30) 0%, transparent 52%),
                radial-gradient(ellipse at 82% 82%, rgba(201,152,42,0.14) 0%, transparent 50%),
                radial-gradient(ellipse at 60% 10%, rgba(91,79,196,0.12) 0%, transparent 44%),
                radial-gradient(ellipse at 30% 90%, rgba(155,95,168,0.08) 0%, transparent 42%)
              `,
            }}
          />

          {/* Subtle grid */}
          <div
            className="absolute inset-0 opacity-[0.025]"
            style={{
              backgroundImage: `
                linear-gradient(rgba(201,152,42,0.6) 1px, transparent 1px),
                linear-gradient(90deg, rgba(201,152,42,0.6) 1px, transparent 1px)
              `,
              backgroundSize: "60px 60px",
            }}
          />

          {/* Floating scripture */}
          <FloatingVerses />

          {/* Noise grain */}
          <div
            className="absolute inset-0 opacity-[0.04]"
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
            }}
          />
        </div>

        {/* ── Card ── */}
        <motion.div
          initial={{ opacity: 0, y: 28, scale: 0.96 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.75, ease: [0.22, 1, 0.36, 1] }}
          className="relative z-10 w-full max-w-[420px] mx-4"
        >
          <div
            className="relative rounded-[26px] overflow-hidden"
            style={{
              background: "rgba(8, 5, 20, 0.82)",
              backdropFilter: "blur(28px) saturate(1.4)",
              WebkitBackdropFilter: "blur(28px) saturate(1.4)",
              border: "1px solid rgba(201,152,42,0.16)",
              boxShadow: `
                0 40px 90px rgba(0,0,0,0.70),
                0 8px 24px rgba(0,0,0,0.40),
                0 0 0 1px rgba(255,255,255,0.04),
                inset 0 1px 0 rgba(255,255,255,0.06),
                inset 0 -1px 0 rgba(0,0,0,0.15)
              `,
            }}
          >
            {/* Gold top line */}
            <div
              className="absolute top-0 left-[12%] right-[12%] h-px"
              style={{
                background:
                  "linear-gradient(90deg, transparent, rgba(201,152,42,0.8) 40%, rgba(232,197,96,0.9) 50%, rgba(201,152,42,0.8) 60%, transparent)",
              }}
            />

            <div className="px-8 py-10 sm:px-10">
              {/* ── Logo ── */}
              <motion.div
                initial={{ opacity: 0, y: -12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.18, duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
                className="text-center mb-8"
              >
                {/* Icon badge */}
                <div className="inline-flex items-center justify-center w-[58px] h-[58px] rounded-2xl mb-4"
                  style={{
                    background: "linear-gradient(135deg, rgba(59,47,142,0.45), rgba(201,152,42,0.18))",
                    border: "1px solid rgba(201,152,42,0.28)",
                    boxShadow: "0 4px 20px rgba(59,47,142,0.35), inset 0 1px 0 rgba(255,255,255,0.08)",
                  }}
                >
                  <CrossIcon />
                </div>

                <h1
                  className="text-[28px] font-bold tracking-[0.04em] leading-tight"
                  style={{
                    fontFamily: "'Cinzel', serif",
                    background: "linear-gradient(135deg, #F5EAC4 0%, #E8C560 35%, #C9982A 65%, #F5EAC4 100%)",
                    backgroundSize: "200% 100%",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                    backgroundClip: "text",
                    animation: "lp-shimmer 6s linear infinite",
                  }}
                >
                  Logos Pulse
                </h1>

                <p
                  className="text-[10px] mt-1.5 tracking-[3px] uppercase font-bold"
                  style={{
                    fontFamily: "'Nunito', sans-serif",
                    color: "rgba(158,150,171,0.5)",
                  }}
                >
                  Spiritual Growth Tracker
                </p>
              </motion.div>

              {/* ── Mode toggle ── */}
              <motion.div
                initial={{ opacity: 0, scale: 0.97 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.28, duration: 0.45 }}
                className="relative flex gap-1 p-1 rounded-xl mb-7"
                style={{
                  background: "rgba(255,255,255,0.035)",
                  border: "1px solid rgba(255,255,255,0.06)",
                }}
              >
                {/* Sliding pill */}
                <motion.div
                  className="absolute top-1 bottom-1 rounded-lg"
                  style={{
                    width: "calc(50% - 6px)",
                    background: "linear-gradient(135deg, rgba(59,47,142,0.65), rgba(91,79,196,0.45))",
                    border: "1px solid rgba(201,152,42,0.22)",
                    boxShadow: "0 2px 14px rgba(59,47,142,0.45)",
                  }}
                  animate={{ x: mode === "signin" ? 4 : "calc(100% + 4px)" }}
                  transition={{ type: "spring", stiffness: 420, damping: 38 }}
                />

                {(["signin", "signup"] as Mode[]).map((m) => (
                  <button
                    key={m}
                    type="button"
                    onClick={() => switchMode(m)}
                    className="relative z-10 flex-1 py-2.5 text-[13px] font-bold rounded-lg transition-colors duration-200"
                    style={{
                      fontFamily: "'Nunito', sans-serif",
                      color: mode === m ? "rgba(255,255,255,0.95)" : "rgba(158,150,171,0.55)",
                    }}
                  >
                    {m === "signin" ? "Sign In" : "Create Account"}
                  </button>
                ))}
              </motion.div>

              {/* ── Form ── */}
              <form onSubmit={handleSubmit}>
                <div className="space-y-3.5">
                  {/* Name field — only in signup */}
                  <AnimatePresence initial={false}>
                    {mode === "signup" && (
                      <motion.div
                        key="name"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.32, ease: [0.22, 1, 0.36, 1] }}
                        style={{ overflow: "hidden" }}
                      >
                        <FloatingInput
                          icon={<User size={14} />}
                          label="Your Name"
                          type="text"
                          value={name}
                          onChange={(e) => setName(e.target.value)}
                          required={mode === "signup"}
                          autoComplete="name"
                        />
                      </motion.div>
                    )}
                  </AnimatePresence>

                  <FloatingInput
                    icon={<Mail size={14} />}
                    label="Email Address"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    autoComplete="email"
                  />

                  <FloatingInput
                    icon={<Lock size={14} />}
                    label="Password"
                    type={showPw ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete={mode === "signin" ? "current-password" : "new-password"}
                    suffix={
                      <button
                        type="button"
                        onClick={() => setShowPw(!showPw)}
                        className="transition-colors duration-150 p-0.5"
                        style={{ color: showPw ? "#C9982A" : "rgba(158,150,171,0.45)" }}
                        tabIndex={-1}
                      >
                        {showPw ? <EyeOff size={14} /> : <Eye size={14} />}
                      </button>
                    }
                  />
                </div>

                {/* Forgot password */}
                <AnimatePresence>
                  {mode === "signin" && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="text-right mt-2"
                    >
                      <button
                        type="button"
                        className="text-[11.5px] font-bold transition-colors duration-150"
                        style={{
                          fontFamily: "'Nunito', sans-serif",
                          color: "rgba(158,150,171,0.45)",
                        }}
                        onMouseEnter={(e) => (e.currentTarget.style.color = "#C9982A")}
                        onMouseLeave={(e) => (e.currentTarget.style.color = "rgba(158,150,171,0.45)")}
                      >
                        Forgot password?
                      </button>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Error */}
                <AnimatePresence>
                  {error && (
                    <motion.p
                      initial={{ opacity: 0, y: -6 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -6 }}
                      className="mt-4 text-[12.5px] font-semibold text-center py-2.5 px-4 rounded-xl"
                      style={{
                        fontFamily: "'Nunito', sans-serif",
                        color: "#EF9A9A",
                        background: "rgba(229,115,115,0.09)",
                        border: "1px solid rgba(229,115,115,0.18)",
                      }}
                    >
                      {error}
                    </motion.p>
                  )}
                </AnimatePresence>

                {/* Submit button */}
                <motion.button
                  type="submit"
                  disabled={loading}
                  whileHover={{ scale: 1.015 }}
                  whileTap={{ scale: 0.985 }}
                  className="lp-btn-shimmer w-full mt-6 py-3.5 rounded-xl font-bold text-[14.5px] text-white flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
                  style={{
                    fontFamily: "'Nunito', sans-serif",
                    border: "1px solid rgba(201,152,42,0.18)",
                    boxShadow: "inset 0 1px 0 rgba(255,255,255,0.12), 0 4px 20px rgba(59,47,142,0.45)",
                    letterSpacing: "0.3px",
                  }}
                >
                  <AnimatePresence mode="wait">
                    {loading ? (
                      <motion.span
                        key="loading"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="flex items-center gap-2"
                      >
                        <Loader2 size={17} className="animate-spin" />
                        <span>One moment…</span>
                      </motion.span>
                    ) : (
                      <motion.span
                        key="label"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="flex items-center gap-2"
                      >
                        <span>
                          {mode === "signin" ? "Enter the Sanctuary" : "Begin Your Journey"}
                        </span>
                        <ArrowRight size={16} />
                      </motion.span>
                    )}
                  </AnimatePresence>
                </motion.button>
              </form>

              {/* Switch mode link */}
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.55 }}
                className="text-center text-[12px] mt-5"
                style={{
                  fontFamily: "'Nunito', sans-serif",
                  color: "rgba(87,79,110,0.8)",
                }}
              >
                {mode === "signin" ? "New to Logos Pulse? " : "Already have an account? "}
                <button
                  type="button"
                  onClick={() => switchMode(mode === "signin" ? "signup" : "signin")}
                  className="font-bold transition-colors duration-150"
                  style={{ color: "#C9982A" }}
                  onMouseEnter={(e) => (e.currentTarget.style.color = "#E8C560")}
                  onMouseLeave={(e) => (e.currentTarget.style.color = "#C9982A")}
                >
                  {mode === "signin" ? "Create account →" : "Sign in →"}
                </button>
              </motion.p>
            </div>

            {/* Gold bottom shimmer line */}
            <div
              className="absolute bottom-0 left-[30%] right-[30%] h-px"
              style={{
                background: "linear-gradient(90deg, transparent, rgba(201,152,42,0.35), transparent)",
              }}
            />
          </div>

          {/* Scripture quote below card */}
          <motion.p
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.85, duration: 0.5 }}
            className="text-center text-[12.5px] italic mt-5 px-4"
            style={{
              fontFamily: "'EB Garamond', Georgia, serif",
              color: "rgba(158,150,171,0.38)",
              lineHeight: 1.65,
            }}
          >
            "Your word is a lamp for my feet, a light on my path."
            <span
              className="not-italic text-[11px] block mt-0.5 tracking-widest uppercase font-semibold"
              style={{
                fontFamily: "'Nunito', sans-serif",
                color: "rgba(201,152,42,0.35)",
                letterSpacing: "2px",
              }}
            >
              — Psalm 119 : 105
            </span>
          </motion.p>
        </motion.div>
      </div>
    </>
  );
};

export default Component;
