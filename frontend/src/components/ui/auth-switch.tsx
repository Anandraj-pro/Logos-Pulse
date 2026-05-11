"use client";

import { cn } from "@/lib/utils";
import { useState, useEffect } from "react";
import { Eye, EyeOff, Mail, Lock, User, Users, ArrowRight, BookOpen } from "lucide-react";

type AuthMode = "login" | "register";

const DAILY_VERSES = [
  { text: "Your word is a lamp to my feet and a light to my path.", ref: "Psalm 119:105" },
  { text: "The Lord is my shepherd; I shall not want.", ref: "Psalm 23:1" },
  { text: "Be still, and know that I am God.", ref: "Psalm 46:10" },
  { text: "I can do all things through Christ who strengthens me.", ref: "Philippians 4:13" },
];

// ── Left-panel ambient decorations ──────────────────────────────────────────
function PanelDecor() {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden" aria-hidden>
      {/* Soft radial glow behind cross */}
      <div
        className="absolute left-1/2 top-[42%] -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full"
        style={{ background: "radial-gradient(circle, rgba(196,144,42,0.10) 0%, transparent 68%)" }}
      />
      {/* Cross silhouette */}
      <div className="absolute left-1/2 top-[42%] -translate-x-1/2 -translate-y-1/2">
        <svg width="110" height="150" viewBox="0 0 110 150" fill="none">
          <defs>
            <linearGradient id="cg" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#C4902A" stopOpacity="0.2" />
              <stop offset="50%" stopColor="#E8C050" stopOpacity="0.55" />
              <stop offset="100%" stopColor="#C4902A" stopOpacity="0.15" />
            </linearGradient>
          </defs>
          <rect x="48" y="0" width="14" height="150" rx="7" fill="url(#cg)" />
          <rect x="0" y="48" width="110" height="14" rx="7" fill="url(#cg)" />
        </svg>
      </div>
      {/* Fine dot grid */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage: "radial-gradient(circle, rgba(255,255,255,0.08) 1px, transparent 1px)",
          backgroundSize: "36px 36px",
          opacity: 0.5,
        }}
      />
      {/* Thin border-glow top */}
      <div
        className="absolute top-0 left-8 right-8 h-px"
        style={{ background: "linear-gradient(90deg, transparent, rgba(201,152,42,0.35), transparent)" }}
      />
      {/* Bottom glow */}
      <div
        className="absolute bottom-0 left-8 right-8 h-px"
        style={{ background: "linear-gradient(90deg, transparent, rgba(201,152,42,0.2), transparent)" }}
      />
      {/* Corner accents */}
      <svg className="absolute top-6 left-6" width="24" height="24" viewBox="0 0 24 24" fill="none" opacity="0.2">
        <path d="M2 14 L2 2 L14 2" stroke="#C4902A" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
      <svg className="absolute bottom-6 right-6" width="24" height="24" viewBox="0 0 24 24" fill="none" opacity="0.2">
        <path d="M22 10 L22 22 L10 22" stroke="#C4902A" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    </div>
  );
}

// ── Input field ───────────────────────────────────────────────────────────────
interface FieldProps {
  id: string;
  label: string;
  type: string;
  placeholder: string;
  icon: React.ReactNode;
  autoComplete?: string;
  value: string;
  onChange: (v: string) => void;
}

function AuthField({ id, label, type, placeholder, icon, autoComplete, value, onChange }: FieldProps) {
  const [show, setShow] = useState(false);
  const [focused, setFocused] = useState(false);
  const isPassword = type === "password";
  const isSelect = type === "select";

  return (
    <div>
      <label
        htmlFor={id}
        className="block text-[10.5px] font-bold uppercase tracking-[0.11em] mb-2 transition-colors duration-200"
        style={{ color: focused ? "#2A1D7E" : "#8A85A0" }}
      >
        {label}
      </label>
      <div
        className="relative flex items-center rounded-[13px] transition-all duration-200"
        style={{
          background: focused ? "rgba(42,29,126,0.03)" : "#FDFAF5",
          border: focused
            ? "1.5px solid rgba(42,29,126,0.38)"
            : "1.5px solid rgba(180,170,145,0.35)",
          boxShadow: focused
            ? "0 0 0 3.5px rgba(42,29,126,0.07)"
            : "0 1px 3px rgba(0,0,0,0.04)",
        }}
      >
        <span
          className="absolute left-4 flex-shrink-0 transition-colors duration-200"
          style={{ color: focused ? "#2A1D7E" : "#B0ADB8" }}
        >
          {icon}
        </span>

        {isSelect ? (
          <select
            id={id}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            className="w-full pl-11 pr-4 py-3.5 bg-transparent text-[14px] text-[#1A1A2E] outline-none appearance-none cursor-pointer rounded-[13px]"
          >
            <option value="">Select your pastor</option>
            <option value="ps-samuel">Ps. Samuel Patta</option>
            <option value="bishop-samuel">Bishop Samuel Patta</option>
            <option value="ps-deepak">Ps. Deepak Avinash</option>
          </select>
        ) : (
          <input
            id={id}
            type={isPassword && show ? "text" : type}
            placeholder={placeholder}
            autoComplete={autoComplete}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            className="w-full pl-11 pr-11 py-3.5 bg-transparent text-[14px] text-[#1A1A2E] placeholder:text-[#C8C4D0] outline-none rounded-[13px]"
          />
        )}

        {isPassword && (
          <button
            type="button"
            tabIndex={-1}
            onClick={() => setShow((s) => !s)}
            className="absolute right-4 flex-shrink-0 transition-colors duration-200"
            style={{ color: show ? "#2A1D7E" : "#B0ADB8" }}
          >
            {show ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        )}
      </div>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────
export const Component = () => {
  const [mode, setMode] = useState<AuthMode>("login");
  const [values, setValues] = useState<Record<string, string>>({});
  const [prayerGoal, setPrayerGoal] = useState(60);
  const [verseIdx] = useState(() => Math.floor(Math.random() * DAILY_VERSES.length));
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const t0 = setTimeout(() => setPhase(1), 60);
    const t1 = setTimeout(() => setPhase(2), 220);
    const t2 = setTimeout(() => setPhase(3), 420);
    return () => { clearTimeout(t0); clearTimeout(t1); clearTimeout(t2); };
  }, []);

  const verse = DAILY_VERSES[verseIdx];

  const handleField = (id: string, val: string) =>
    setValues((prev) => ({ ...prev, [id]: val }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Submit", mode, values, prayerGoal);
  };

  const switchMode = (m: AuthMode) => {
    setValues({});
    setMode(m);
  };

  const loginFields: FieldProps[] = [
    { id: "email",    label: "Email Address", type: "email",    placeholder: "you@church.org",  icon: <Mail size={15} />, autoComplete: "email",            value: values.email    ?? "", onChange: (v) => handleField("email",    v) },
    { id: "password", label: "Password",      type: "password", placeholder: "••••••••",        icon: <Lock size={15} />, autoComplete: "current-password", value: values.password ?? "", onChange: (v) => handleField("password", v) },
  ];

  const registerFields: FieldProps[] = [
    { id: "email",    label: "Email Address", type: "email",    placeholder: "you@church.org",       icon: <Mail  size={15} />, autoComplete: "email",        value: values.email    ?? "", onChange: (v) => handleField("email",    v) },
    { id: "pastor",   label: "Your Pastor",   type: "select",   placeholder: "Select your pastor",    icon: <Users size={15} />,                               value: values.pastor   ?? "", onChange: (v) => handleField("pastor",   v) },
    { id: "password", label: "Password",      type: "password", placeholder: "Create a strong password", icon: <Lock size={15} />, autoComplete: "new-password", value: values.password ?? "", onChange: (v) => handleField("password", v) },
  ];

  const firstNameField: FieldProps = {
    id: "firstName", label: "First Name", type: "text", placeholder: "Ananda",
    icon: <User size={15} />, autoComplete: "given-name",
    value: values.firstName ?? "", onChange: (v) => handleField("firstName", v),
  };
  const lastNameField: FieldProps = {
    id: "lastName", label: "Last Name", type: "text", placeholder: "Raj",
    icon: <User size={15} />, autoComplete: "family-name",
    value: values.lastName ?? "", onChange: (v) => handleField("lastName", v),
  };

  const fields = mode === "login" ? loginFields : registerFields;

  // Shared entrance transition
  const enter = (minPhase: number, delay = 0) => ({
    opacity:    phase >= minPhase ? 1 : 0,
    transform:  phase >= minPhase ? "translateY(0px)" : "translateY(16px)",
    transition: `opacity 0.55s ease ${delay}s, transform 0.55s cubic-bezier(0.22,1,0.36,1) ${delay}s`,
  });

  return (
    <div
      className="h-screen overflow-hidden flex"
      style={{ fontFamily: "'Nunito', system-ui, sans-serif" }}
    >
      {/* ══════════════════════════════ LEFT PANEL ══════════════════════════════ */}
      <div
        className="hidden lg:flex flex-col justify-between flex-shrink-0 relative overflow-hidden"
        style={{
          width: "44%",
          maxWidth: "500px",
          padding: "52px 56px",
          background: "linear-gradient(148deg, #0F0930 0%, #1A1060 30%, #221574 60%, #2E1E88 100%)",
        }}
      >
        <PanelDecor />

        {/* Brand */}
        <div className="relative z-10" style={enter(1)}>
          <div className="flex items-center gap-3 mb-16">
            <div
              className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0"
              style={{
                background: "rgba(201,152,42,0.1)",
                border: "1px solid rgba(201,152,42,0.3)",
              }}
            >
              <BookOpen size={17} color="#c9982a" />
            </div>
            <div>
              <p
                className="text-white leading-none"
                style={{ fontFamily: "'Cinzel', serif", fontSize: "15px", letterSpacing: "0.05em" }}
              >
                Logos Pulse
              </p>
              <p
                className="text-[9px] uppercase mt-0.5"
                style={{ letterSpacing: "0.24em", color: "rgba(201,152,42,0.5)" }}
              >
                Sanctuary
              </p>
            </div>
          </div>

          <h1
            className="text-white mb-5 leading-[1.15]"
            style={{
              fontFamily: "'Cinzel', serif",
              fontWeight: 300,
              fontSize: "clamp(28px, 2.6vw, 42px)",
            }}
          >
            Track your<br />
            <span style={{ color: "#E8C050" }}>walk with God</span>
          </h1>

          <p
            className="text-sm leading-[1.85]"
            style={{ color: "rgba(255,255,255,0.38)", maxWidth: "280px" }}
          >
            A sanctuary for daily prayer, scripture reading, and spiritual
            reflection — built for the whole church family.
          </p>
        </div>

        {/* Verse card */}
        <div className="relative z-10" style={enter(2, 0.08)}>
          <div
            className="rounded-2xl p-6"
            style={{
              background: "rgba(255,255,255,0.03)",
              border: "1px solid rgba(201,152,42,0.16)",
              backdropFilter: "blur(16px)",
            }}
          >
            <div className="flex items-center gap-2.5 mb-4">
              <div
                className="h-5 rounded-full"
                style={{ width: "1.5px", background: "rgba(201,152,42,0.65)" }}
              />
              <p
                className="text-[9px] font-bold uppercase"
                style={{ letterSpacing: "0.2em", color: "rgba(201,152,42,0.6)" }}
              >
                Verse of the Day
              </p>
            </div>

            <p
              className="leading-[1.85] mb-4"
              style={{
                fontFamily: "'Spectral', Georgia, serif",
                fontStyle: "italic",
                fontSize: "16px",
                color: "rgba(255,255,255,0.68)",
              }}
            >
              "{verse.text}"
            </p>

            <p
              className="font-medium"
              style={{
                fontFamily: "'Cinzel', serif",
                fontSize: "11.5px",
                color: "#c9982a",
                letterSpacing: "0.04em",
              }}
            >
              — {verse.ref}
            </p>
          </div>
        </div>

        {/* Footer tagline */}
        <div className="relative z-10 flex items-center gap-5" style={enter(3, 0.1)}>
          {["Prayer", "Scripture", "Reflection"].map((word, i) => (
            <div key={word} className="flex items-center gap-5">
              {i > 0 && (
                <div
                  className="h-3 rounded-full"
                  style={{ width: "1px", background: "rgba(255,255,255,0.12)" }}
                />
              )}
              <span
                className="text-[9px] font-bold uppercase"
                style={{ letterSpacing: "0.22em", color: "rgba(255,255,255,0.18)" }}
              >
                {word}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* ══════════════════════════════ RIGHT PANEL ══════════════════════════════ */}
      <div
        className="flex-1 flex items-center justify-center overflow-y-auto relative"
        style={{ background: "#F5F1E9", padding: "48px 24px" }}
      >
        {/* Parchment texture */}
        <div className="absolute inset-0 pointer-events-none" aria-hidden>
          <div
            className="absolute inset-0"
            style={{
              backgroundImage: "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)'/%3E%3C/svg%3E\")",
              backgroundRepeat: "repeat",
              backgroundSize: "300px 300px",
              opacity: 0.022,
            }}
          />
          {/* Cross watermark — right side */}
          <div className="absolute right-14 top-1/2 -translate-y-1/2 opacity-[0.022]">
            <svg width="200" height="280" viewBox="0 0 200 280">
              <rect x="88"  y="0"   width="24" height="280" rx="12" fill="#2A1D7E" />
              <rect x="0"   y="92"  width="200" height="24" rx="12" fill="#2A1D7E" />
            </svg>
          </div>
        </div>

        {/* Form container */}
        <div
          className="w-full relative z-10"
          style={{ maxWidth: "400px", ...enter(1, 0.12) }}
        >
          {/* Mobile logo */}
          <div className="lg:hidden flex items-center gap-3 mb-10">
            <div
              className="w-9 h-9 rounded-full flex items-center justify-center"
              style={{
                background: "rgba(42,29,126,0.07)",
                border: "1px solid rgba(42,29,126,0.15)",
              }}
            >
              <BookOpen size={15} color="#2A1D7E" />
            </div>
            <span
              className="text-[15px] text-[#1A1A2E]"
              style={{ fontFamily: "'Cinzel', serif", letterSpacing: "0.04em" }}
            >
              Logos Pulse
            </span>
          </div>

          {/* Heading */}
          <div className="mb-7">
            <h2
              className="text-[#1A1A2E] mb-1.5"
              style={{
                fontFamily: "'Cinzel', serif",
                fontWeight: 400,
                fontSize: "26px",
                letterSpacing: "0.01em",
                lineHeight: 1.3,
              }}
            >
              {mode === "login" ? "Welcome back" : "Join the sanctuary"}
            </h2>
            <p className="text-[14px] leading-relaxed" style={{ color: "#8A85A0" }}>
              {mode === "login"
                ? "Sign in to continue your spiritual journey"
                : "Create your account to get started"}
            </p>
          </div>

          {/* Segmented mode toggle */}
          <div
            className="relative flex rounded-xl p-1 mb-7"
            style={{
              background: "rgba(42,29,126,0.07)",
              border: "1px solid rgba(42,29,126,0.09)",
            }}
          >
            {/* Sliding active pill — pixel-perfect alignment */}
            <div
              className="absolute top-1 bottom-1 rounded-[9px] transition-all duration-300 ease-[cubic-bezier(0.4,0,0.2,1)]"
              style={{
                left:     mode === "login" ? "4px" : "calc(50% + 2px)",
                width:    "calc(50% - 6px)",
                background: "linear-gradient(135deg, #2A1D7E 0%, #3D2DA0 100%)",
                boxShadow: "0 2px 10px rgba(42,29,126,0.30), inset 0 1px 0 rgba(255,255,255,0.12)",
              }}
            />
            {(["login", "register"] as const).map((m) => (
              <button
                key={m}
                type="button"
                onClick={() => switchMode(m)}
                className={cn(
                  "relative z-10 flex-1 py-2.5 text-[13px] font-bold rounded-[9px] transition-colors duration-250",
                  mode === m ? "text-white" : "text-[#8A85A0] hover:text-[#3A3255]"
                )}
              >
                {m === "login" ? "Sign In" : "Register"}
              </button>
            ))}
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Name row — register only */}
            {mode === "register" && (
              <div className="grid grid-cols-2 gap-3">
                <AuthField {...firstNameField} />
                <AuthField {...lastNameField}  />
              </div>
            )}

            {fields.map((field) => (
              <AuthField key={field.id} {...field} />
            ))}

            {/* Prayer goal slider — register only */}
            {mode === "register" && (
              <div>
                <label
                  className="block text-[10.5px] font-bold uppercase tracking-[0.11em] mb-2"
                  style={{ color: "#8A85A0" }}
                >
                  Daily Prayer Goal
                </label>
                <div
                  className="rounded-[13px] px-4 py-3.5"
                  style={{
                    background: "#FDFAF5",
                    border: "1.5px solid rgba(180,170,145,0.35)",
                    boxShadow: "0 1px 3px rgba(0,0,0,0.04)",
                  }}
                >
                  <div className="flex items-center gap-4">
                    <input
                      type="range"
                      min={15}
                      max={195}
                      step={15}
                      value={prayerGoal}
                      onChange={(e) => setPrayerGoal(Number(e.target.value))}
                      className="flex-1 cursor-pointer accent-[#2A1D7E]"
                      style={{ height: "5px" }}
                    />
                    <span
                      className="text-sm font-bold w-14 text-right flex-shrink-0"
                      style={{ color: "#2A1D7E", fontFamily: "'Cinzel', serif" }}
                    >
                      {prayerGoal}m
                    </span>
                  </div>
                  <div className="flex justify-between mt-2">
                    <span className="text-[10px]" style={{ color: "#C8C4D0" }}>15 min</span>
                    <span className="text-[10px]" style={{ color: "#C8C4D0" }}>195 min</span>
                  </div>
                </div>
              </div>
            )}

            {/* Forgot password */}
            {mode === "login" && (
              <div className="flex justify-end" style={{ marginTop: "-4px" }}>
                <button
                  type="button"
                  className="text-[12.5px] font-semibold transition-colors hover:underline underline-offset-2"
                  style={{ color: "#2A1D7E" }}
                >
                  Forgot password?
                </button>
              </div>
            )}

            {/* Submit button */}
            <button
              type="submit"
              className="w-full flex items-center justify-center gap-2 rounded-[13px] text-white text-[14px] font-bold transition-all duration-200 hover:opacity-90 active:scale-[0.984]"
              style={{
                marginTop: "8px",
                padding: "14px 20px",
                background: "linear-gradient(135deg, #2A1D7E 0%, #4B3DC0 100%)",
                boxShadow: "0 4px 20px rgba(42,29,126,0.32), inset 0 1px 0 rgba(255,255,255,0.14)",
              }}
            >
              {mode === "login" ? "Sign In" : "Create Account"}
              <ArrowRight size={15} strokeWidth={2.5} />
            </button>
          </form>

          {/* Divider */}
          <div className="flex items-center gap-4 my-5">
            <div className="flex-1 h-px" style={{ background: "rgba(0,0,0,0.08)" }} />
            <span
              className="text-[11px] font-bold uppercase tracking-widest"
              style={{ color: "#C8C4D0" }}
            >
              or
            </span>
            <div className="flex-1 h-px" style={{ background: "rgba(0,0,0,0.08)" }} />
          </div>

          {/* Switch mode link */}
          <p className="text-center text-[13.5px]" style={{ color: "#8A85A0" }}>
            {mode === "login" ? "New to Logos Pulse? " : "Already have an account? "}
            <button
              type="button"
              onClick={() => switchMode(mode === "login" ? "register" : "login")}
              className="font-bold transition-colors hover:underline underline-offset-2"
              style={{ color: "#2A1D7E" }}
            >
              {mode === "login" ? "Register here" : "Sign in"}
            </button>
          </p>

          {/* Footer note */}
          <p
            className="text-center leading-relaxed mt-5"
            style={{ fontSize: "11px", color: "#C8C4D0" }}
          >
            Accounts are created by your pastor or admin.
            <br />
            Contact your pastor if you need access.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Component;