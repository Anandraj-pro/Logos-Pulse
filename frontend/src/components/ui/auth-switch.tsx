"use client";

import { cn } from "@/lib/utils";
import { useState, useRef, useEffect } from "react";
import { Eye, EyeOff, Mail, Lock, User, Users, ChevronRight, BookOpen } from "lucide-react";

type AuthMode = "login" | "register";

interface FormField {
  id: string;
  label: string;
  type: string;
  placeholder: string;
  icon: React.ReactNode;
  autoComplete?: string;
}

const LOGIN_FIELDS: FormField[] = [
  {
    id: "email",
    label: "Email Address",
    type: "email",
    placeholder: "you@church.org",
    icon: <Mail size={16} />,
    autoComplete: "email",
  },
  {
    id: "password",
    label: "Password",
    type: "password",
    placeholder: "••••••••",
    icon: <Lock size={16} />,
    autoComplete: "current-password",
  },
];

const REGISTER_FIELDS: FormField[] = [
  {
    id: "firstName",
    label: "First Name",
    type: "text",
    placeholder: "Ananda",
    icon: <User size={16} />,
    autoComplete: "given-name",
  },
  {
    id: "lastName",
    label: "Last Name",
    type: "text",
    placeholder: "Raj",
    icon: <User size={16} />,
    autoComplete: "family-name",
  },
  {
    id: "email",
    label: "Email Address",
    type: "email",
    placeholder: "you@church.org",
    icon: <Mail size={16} />,
    autoComplete: "email",
  },
  {
    id: "pastor",
    label: "Your Pastor",
    type: "select",
    placeholder: "Select your pastor",
    icon: <Users size={16} />,
  },
  {
    id: "password",
    label: "Password",
    type: "password",
    placeholder: "Create a strong password",
    icon: <Lock size={16} />,
    autoComplete: "new-password",
  },
];

const DAILY_VERSES = [
  { text: "Your word is a lamp to my feet and a light to my path.", ref: "Psalm 119:105" },
  { text: "The Lord is my shepherd; I shall not want.", ref: "Psalm 23:1" },
  { text: "Be still, and know that I am God.", ref: "Psalm 46:10" },
  { text: "I can do all things through Christ who strengthens me.", ref: "Philippians 4:13" },
];

// ── Vine / botanical SVG decoration ──────────────────────────────────────────
function VineDecoration() {
  return (
    <svg
      className="absolute inset-0 w-full h-full pointer-events-none"
      viewBox="0 0 440 700"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden
    >
      {/* Main stem */}
      <path
        d="M220 700 C220 700 180 550 170 400 C160 250 200 120 220 0"
        stroke="url(#vineGold)"
        strokeWidth="1.2"
        fill="none"
        opacity="0.5"
      />
      {/* Branch left */}
      <path
        d="M200 500 C160 470 120 480 80 450"
        stroke="url(#vineGold)"
        strokeWidth="0.8"
        fill="none"
        opacity="0.35"
      />
      <path
        d="M190 350 C140 320 110 340 70 310"
        stroke="url(#vineGold)"
        strokeWidth="0.8"
        fill="none"
        opacity="0.3"
      />
      {/* Branch right */}
      <path
        d="M235 450 C275 420 320 435 360 405"
        stroke="url(#vineGold)"
        strokeWidth="0.8"
        fill="none"
        opacity="0.35"
      />
      <path
        d="M230 280 C280 250 330 265 380 235"
        stroke="url(#vineGold)"
        strokeWidth="0.8"
        fill="none"
        opacity="0.3"
      />
      {/* Leaf shapes */}
      <ellipse cx="80" cy="450" rx="14" ry="8" fill="#c9982a" opacity="0.15" transform="rotate(-25 80 450)" />
      <ellipse cx="70" cy="310" rx="12" ry="7" fill="#c9982a" opacity="0.12" transform="rotate(-35 70 310)" />
      <ellipse cx="360" cy="405" rx="14" ry="8" fill="#c9982a" opacity="0.15" transform="rotate(20 360 405)" />
      <ellipse cx="380" cy="235" rx="12" ry="7" fill="#c9982a" opacity="0.12" transform="rotate(30 380 235)" />
      {/* Corner cross ornament */}
      <g opacity="0.18" transform="translate(30,30)">
        <rect x="18" y="8" width="4" height="24" rx="2" fill="#c9982a" />
        <rect x="10" y="16" width="20" height="4" rx="2" fill="#c9982a" />
      </g>
      <g opacity="0.12" transform="translate(390,640)">
        <rect x="8" y="0" width="3" height="18" rx="1.5" fill="#c9982a" />
        <rect x="2" y="6" width="15" height="3" rx="1.5" fill="#c9982a" />
      </g>
      {/* Small dot accents */}
      <circle cx="80" cy="450" r="2.5" fill="#c9982a" opacity="0.3" />
      <circle cx="70" cy="310" r="2" fill="#c9982a" opacity="0.25" />
      <circle cx="360" cy="405" r="2.5" fill="#c9982a" opacity="0.3" />
      <circle cx="380" cy="235" r="2" fill="#c9982a" opacity="0.25" />
      <defs>
        <linearGradient id="vineGold" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#c9982a" stopOpacity="0.6" />
          <stop offset="50%" stopColor="#f0d98a" stopOpacity="0.8" />
          <stop offset="100%" stopColor="#c9982a" stopOpacity="0.4" />
        </linearGradient>
      </defs>
    </svg>
  );
}

// ── Single input field ────────────────────────────────────────────────────────
interface FieldProps extends FormField {
  value: string;
  onChange: (val: string) => void;
}

function AuthField({ id, label, type, placeholder, icon, autoComplete, value, onChange }: FieldProps) {
  const [show, setShow] = useState(false);
  const [focused, setFocused] = useState(false);
  const isPassword = type === "password";
  const isSelect = type === "select";

  return (
    <div className="relative group">
      <label
        htmlFor={id}
        className={cn(
          "block text-[10px] font-semibold uppercase tracking-[0.12em] mb-1.5 transition-colors duration-200",
          focused ? "text-[#3B2F8E]" : "text-[#6B7280]"
        )}
      >
        {label}
      </label>
      <div className="relative flex items-center">
        <span
          className={cn(
            "absolute left-0 transition-colors duration-200",
            focused ? "text-[#3B2F8E]" : "text-[#6B7280]"
          )}
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
            className={cn(
              "w-full pl-6 pr-0 pb-2.5 pt-0.5 bg-transparent border-0 border-b text-sm text-[#1A1A2E] outline-none transition-all duration-200 appearance-none cursor-pointer",
              focused ? "border-[#3B2F8E]" : "border-[#e5e7eb]"
            )}
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
            className={cn(
              "w-full pl-6 pr-8 pb-2.5 pt-0.5 bg-transparent border-0 border-b text-sm text-[#1A1A2E] placeholder:text-[#9ca3af] outline-none transition-all duration-200",
              focused ? "border-[#3B2F8E]" : "border-[#e5e7eb]"
            )}
          />
        )}
        {isPassword && (
          <button
            type="button"
            tabIndex={-1}
            onClick={() => setShow((s) => !s)}
            className="absolute right-0 text-[#6B7280] hover:text-[#3B2F8E] transition-colors"
          >
            {show ? <EyeOff size={15} /> : <Eye size={15} />}
          </button>
        )}
      </div>
      {/* animated underline focus indicator */}
      <div
        className={cn(
          "absolute bottom-0 left-0 h-px bg-[#3B2F8E] transition-all duration-300 ease-out",
          focused ? "w-full opacity-100" : "w-0 opacity-0"
        )}
      />
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────
export const Component = () => {
  const [mode, setMode] = useState<AuthMode>("login");
  const [values, setValues] = useState<Record<string, string>>({});
  const [prayerGoal, setPrayerGoal] = useState(60);
  const [verseIdx] = useState(() => Math.floor(Math.random() * DAILY_VERSES.length));
  const [visible, setVisible] = useState(false);
  const formRef = useRef<HTMLDivElement>(null);

  const verse = DAILY_VERSES[verseIdx];
  const fields = mode === "login" ? LOGIN_FIELDS : REGISTER_FIELDS;

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 80);
    return () => clearTimeout(t);
  }, []);

  const handleField = (id: string, val: string) =>
    setValues((prev) => ({ ...prev, [id]: val }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // wire to actual auth
    console.log("Submit", mode, values, prayerGoal);
  };

  const switchMode = (m: AuthMode) => {
    setValues({});
    setMode(m);
  };

  return (
    <div
      className={cn(
        "min-h-screen flex font-sans transition-opacity duration-700",
        visible ? "opacity-100" : "opacity-0"
      )}
      style={{ fontFamily: "'Nunito', system-ui, sans-serif" }}
    >
      {/* ── Left: brand panel ── */}
      <div
        className="hidden lg:flex flex-col justify-between w-[420px] xl:w-[480px] flex-shrink-0 relative overflow-hidden px-12 py-10"
        style={{
          background: "linear-gradient(158deg, #1E1733 0%, #2a1f4a 45%, #1a1530 100%)",
        }}
      >
        <VineDecoration />

        {/* Glowing circle behind cross */}
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full pointer-events-none"
          style={{
            background:
              "radial-gradient(circle, rgba(201,152,42,0.07) 0%, transparent 70%)",
          }}
        />

        {/* Top: logo */}
        <div
          className="relative z-10 transition-all duration-700"
          style={{ transitionDelay: "0.1s" }}
        >
          <div className="flex items-center gap-3 mb-14">
            <div
              className="w-10 h-10 rounded-full border flex items-center justify-center flex-shrink-0"
              style={{ borderColor: "rgba(201,152,42,0.5)" }}
            >
              <BookOpen size={18} color="#c9982a" />
            </div>
            <div>
              <p
                className="text-white text-lg leading-none"
                style={{ fontFamily: "'Playfair Display', Georgia, serif" }}
              >
                Logos Pulse
              </p>
              <p className="text-[10px] uppercase tracking-[0.18em] mt-0.5" style={{ color: "rgba(201,152,42,0.6)" }}>
                Sanctuary
              </p>
            </div>
          </div>

          <h1
            className="text-white leading-tight mb-5"
            style={{
              fontFamily: "'Playfair Display', Georgia, serif",
              fontWeight: 300,
              fontSize: "clamp(28px, 3vw, 40px)",
            }}
          >
            Track your<br />
            <em style={{ color: "#f0d98a" }}>walk with God</em>
          </h1>

          <p className="text-sm leading-relaxed" style={{ color: "rgba(255,255,255,0.45)" }}>
            A sanctuary for daily prayer, scripture reading, and spiritual
            reflection — designed for the whole church family.
          </p>
        </div>

        {/* Middle: verse card */}
        <div
          className="relative z-10 transition-all duration-700"
          style={{ transitionDelay: "0.2s" }}
        >
          <div
            className="rounded-2xl p-6 border"
            style={{
              background: "rgba(255,255,255,0.04)",
              borderColor: "rgba(201,152,42,0.2)",
              backdropFilter: "blur(8px)",
            }}
          >
            <div className="flex items-center gap-2 mb-3">
              <div className="w-px h-8 self-stretch" style={{ background: "#c9982a", opacity: 0.6 }} />
              <p className="text-[10px] uppercase tracking-[0.16em]" style={{ color: "rgba(201,152,42,0.7)" }}>
                Verse of the Day
              </p>
            </div>
            <p
              className="text-white/75 leading-relaxed mb-3"
              style={{
                fontFamily: "'EB Garamond', Georgia, serif",
                fontStyle: "italic",
                fontSize: "17px",
                lineHeight: "1.75",
              }}
            >
              "{verse.text}"
            </p>
            <p
              className="text-sm font-medium"
              style={{ color: "#c9982a", fontFamily: "'Playfair Display', serif" }}
            >
              — {verse.ref}
            </p>
          </div>
        </div>

        {/* Bottom: tagline */}
        <p
          className="relative z-10 text-[10px] uppercase tracking-[0.2em]"
          style={{ color: "rgba(255,255,255,0.2)" }}
        >
          Prayer · Scripture · Reflection
        </p>
      </div>

      {/* ── Right: form panel ── */}
      <div
        className="flex-1 flex items-center justify-center px-6 py-10 overflow-y-auto"
        style={{ background: "#F8F7FF" }}
      >
        {/* Breathing cross watermark */}
        <div
          className="absolute right-12 top-1/2 -translate-y-1/2 pointer-events-none select-none hidden lg:block"
          style={{ opacity: 0.025 }}
          aria-hidden
        >
          <svg width="280" height="280" viewBox="0 0 280 280">
            <rect x="120" y="20" width="40" height="240" rx="20" fill="#3B2F8E" />
            <rect x="20" y="100" width="240" height="40" rx="20" fill="#3B2F8E" />
          </svg>
        </div>

        <div
          className="w-full max-w-md relative z-10 transition-all duration-700"
          style={{ transitionDelay: "0.15s" }}
          ref={formRef}
        >
          {/* Mobile logo */}
          <div className="lg:hidden flex items-center gap-2 mb-10">
            <BookOpen size={20} color="#3B2F8E" />
            <span
              className="text-lg text-[#1A1A2E]"
              style={{ fontFamily: "'Playfair Display', serif" }}
            >
              Logos Pulse
            </span>
          </div>

          {/* Heading */}
          <div className="mb-8">
            <h2
              className="text-[#1A1A2E] mb-1.5"
              style={{
                fontFamily: "'Playfair Display', Georgia, serif",
                fontWeight: 400,
                fontSize: "28px",
              }}
            >
              {mode === "login" ? "Welcome back" : "Join the sanctuary"}
            </h2>
            <p className="text-sm" style={{ color: "#6B7280" }}>
              {mode === "login"
                ? "Sign in to continue your spiritual journey"
                : "Create your account to get started"}
            </p>
          </div>

          {/* Mode toggle pill */}
          <div
            className="relative flex p-1 rounded-full mb-8 self-start w-fit"
            style={{ background: "#ede9f8" }}
          >
            {/* Sliding indicator */}
            <div
              className="absolute top-1 bottom-1 rounded-full transition-all duration-300 ease-out"
              style={{
                left: mode === "login" ? "4px" : "50%",
                width: "calc(50% - 4px)",
                background: "#3B2F8E",
                boxShadow: "0 2px 12px rgba(59,47,142,0.35)",
              }}
            />
            {(["login", "register"] as const).map((m) => (
              <button
                key={m}
                type="button"
                onClick={() => switchMode(m)}
                className={cn(
                  "relative z-10 px-5 py-2 text-sm font-semibold rounded-full transition-colors duration-300 capitalize",
                  mode === m ? "text-white" : "text-[#6B7280] hover:text-[#3B2F8E]"
                )}
              >
                {m === "login" ? "Sign In" : "Register"}
              </button>
            ))}
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit}>
            <div
              className={cn(
                "space-y-5 transition-all duration-500",
                mode === "register" ? "opacity-100" : "opacity-100"
              )}
            >
              {mode === "register" ? (
                <div className="grid grid-cols-2 gap-5">
                  {REGISTER_FIELDS.filter((f) => ["firstName", "lastName"].includes(f.id)).map(
                    (field) => (
                      <AuthField
                        key={field.id}
                        {...field}
                        value={values[field.id] ?? ""}
                        onChange={(v) => handleField(field.id, v)}
                      />
                    )
                  )}
                </div>
              ) : null}

              {fields
                .filter((f) => !["firstName", "lastName"].includes(f.id))
                .map((field) => (
                  <AuthField
                    key={field.id}
                    {...field}
                    value={values[field.id] ?? ""}
                    onChange={(v) => handleField(field.id, v)}
                  />
                ))}

              {/* Prayer goal slider — register only */}
              {mode === "register" && (
                <div className="pt-1">
                  <label className="block text-[10px] font-semibold uppercase tracking-[0.12em] text-[#6B7280] mb-3">
                    Daily Prayer Goal
                  </label>
                  <div className="flex items-center gap-4">
                    <input
                      type="range"
                      min={15}
                      max={195}
                      step={15}
                      value={prayerGoal}
                      onChange={(e) => setPrayerGoal(Number(e.target.value))}
                      className="flex-1 accent-[#3B2F8E] h-1.5 cursor-pointer"
                    />
                    <span
                      className="text-base font-bold w-20 text-right flex-shrink-0"
                      style={{ color: "#3B2F8E", fontFamily: "'Playfair Display', serif" }}
                    >
                      {prayerGoal} min
                    </span>
                  </div>
                  <div className="flex justify-between mt-1">
                    <span className="text-[10px] text-[#9ca3af]">15 min</span>
                    <span className="text-[10px] text-[#9ca3af]">195 min</span>
                  </div>
                </div>
              )}

              {/* Forgot password */}
              {mode === "login" && (
                <div className="text-right -mt-1">
                  <button
                    type="button"
                    className="text-xs text-[#6B7280] hover:text-[#3B2F8E] transition-colors underline-offset-2 hover:underline"
                  >
                    Forgot password?
                  </button>
                </div>
              )}

              {/* Submit button */}
              <button
                type="submit"
                className={cn(
                  "w-full py-3.5 rounded-xl text-white text-sm font-semibold",
                  "flex items-center justify-center gap-2",
                  "transition-all duration-200 hover:opacity-90 active:scale-[0.985]",
                  "mt-2"
                )}
                style={{
                  background:
                    "linear-gradient(135deg, #3B2F8E 0%, #5B4FC4 100%)",
                  boxShadow: "0 4px 20px rgba(59,47,142,0.35), inset 0 1px 0 rgba(255,255,255,0.15)",
                }}
              >
                {mode === "login" ? "Sign In" : "Create Account"}
                <ChevronRight size={16} />
              </button>
            </div>
          </form>

          {/* Divider */}
          <div className="flex items-center gap-3 my-6">
            <div className="flex-1 h-px" style={{ background: "#e5e7eb" }} />
            <span className="text-[11px] text-[#9ca3af] uppercase tracking-widest">or</span>
            <div className="flex-1 h-px" style={{ background: "#e5e7eb" }} />
          </div>

          {/* Secondary CTA */}
          <p className="text-center text-sm" style={{ color: "#6B7280" }}>
            {mode === "login" ? "New to Logos Pulse? " : "Already have an account? "}
            <button
              type="button"
              onClick={() => switchMode(mode === "login" ? "register" : "login")}
              className="font-semibold transition-colors hover:underline underline-offset-2"
              style={{ color: "#3B2F8E" }}
            >
              {mode === "login" ? "Register here" : "Sign in"}
            </button>
          </p>

          {/* Footer note */}
          <p className="text-center text-[11px] mt-6" style={{ color: "#9ca3af" }}>
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
