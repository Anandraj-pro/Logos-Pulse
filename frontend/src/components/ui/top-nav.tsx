"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Home, PenLine, CalendarDays, Flame, BookMarked, BookOpen,
  FileText, Heart, ShieldCheck, Utensils, Target, Star,
  Bell, User, Settings, ChevronDown, Menu, X,
  LayoutDashboard, Crown, Users, Wand2, LogOut, BookText,
} from "lucide-react";
import { cn } from "@/lib/utils";

/* ────────────────────────────────────────────────────────── Types */

export type Role = "admin" | "bishop" | "pastor" | "prayer_warrior";

export interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  description?: string;
  href: string;
}

export interface NavGroup {
  id: string;
  label: string;
  items: NavItem[];
}

export interface TopNavProps {
  role?: Role;
  currentPath?: string;
  userName?: string;
  unreadCount?: number;
  onNavigate?: (href: string) => void;
  onSignOut?: () => void;
}

/* ────────────────────────────────────────────────────────── Nav data */

const NAV_GROUPS: NavGroup[] = [
  {
    id: "daily",
    label: "Daily",
    items: [
      { id: "dashboard",   label: "Dashboard",    icon: <Home size={15} />,         description: "Your daily overview",        href: "/dashboard" },
      { id: "daily-entry", label: "Daily Entry",  icon: <PenLine size={15} />,      description: "Log today's disciplines",    href: "/daily-entry" },
      { id: "daily-log",   label: "Daily Log",    icon: <CalendarDays size={15} />, description: "Browse past entries",        href: "/daily-log" },
      { id: "streaks",     label: "Streaks & Stats", icon: <Flame size={15} />,     description: "Track your consistency",     href: "/streaks" },
    ],
  },
  {
    id: "scripture",
    label: "Scripture",
    items: [
      { id: "bible-plan",   label: "My Bible Plan",   icon: <BookMarked size={15} />, description: "Weekly reading assignment",  href: "/bible-plan" },
      { id: "reading-plan", label: "Reading Plan",    icon: <BookOpen size={15} />,   description: "Chapter-by-chapter plan",   href: "/reading-plan" },
      { id: "sermon-notes", label: "Sermon Notes",    icon: <FileText size={15} />,   description: "Record sermon insights",    href: "/sermon-notes" },
    ],
  },
  {
    id: "prayer",
    label: "Prayer",
    items: [
      { id: "prayer-journal",    label: "Prayer Journal",    icon: <Heart size={15} />,       description: "Your prayer life",           href: "/prayer-journal" },
      { id: "confession-plans",  label: "Confession Plans",  icon: <ShieldCheck size={15} />, description: "Guided confession tracks",   href: "/confession-plans" },
      { id: "fasting",           label: "Fasting Tracker",   icon: <Utensils size={15} />,    description: "Track fasting periods",      href: "/fasting" },
    ],
  },
  {
    id: "growth",
    label: "Growth",
    items: [
      { id: "goals",       label: "Personal Goals", icon: <Target size={15} />, description: "Set spiritual milestones",  href: "/goals" },
      { id: "testimonies", label: "Testimonies",    icon: <Star size={15} />,   description: "Share what God has done",   href: "/testimonies" },
    ],
  },
];

const LEADERSHIP_ITEMS: Record<Role, NavItem[]> = {
  admin: [
    { id: "admin",       label: "Admin Panel",        icon: <Crown size={15} />,         href: "/admin" },
    { id: "bishop",      label: "Bishop Dashboard",   icon: <LayoutDashboard size={15} />, href: "/bishop" },
    { id: "pastor",      label: "Pastor Dashboard",   icon: <Users size={15} />,           href: "/pastor" },
    { id: "assignments", label: "Custom Assignments", icon: <Wand2 size={15} />,           href: "/assignments" },
    { id: "member",      label: "Member Detail",      icon: <User size={15} />,            href: "/member" },
  ],
  bishop: [
    { id: "bishop",      label: "Bishop Dashboard",   icon: <LayoutDashboard size={15} />, href: "/bishop" },
    { id: "pastor",      label: "Pastor Dashboard",   icon: <Users size={15} />,           href: "/pastor" },
    { id: "assignments", label: "Custom Assignments", icon: <Wand2 size={15} />,           href: "/assignments" },
    { id: "member",      label: "Member Detail",      icon: <User size={15} />,            href: "/member" },
  ],
  pastor: [
    { id: "pastor",      label: "Pastor Dashboard",   icon: <Users size={15} />,  href: "/pastor" },
    { id: "assignments", label: "Custom Assignments", icon: <Wand2 size={15} />,  href: "/assignments" },
    { id: "member",      label: "Member Detail",      icon: <User size={15} />,   href: "/member" },
  ],
  prayer_warrior: [],
};

const ACCOUNT_ITEMS: NavItem[] = [
  { id: "profile",       label: "My Profile",   icon: <User size={15} />,     href: "/profile" },
  { id: "settings",      label: "Settings",     icon: <Settings size={15} />, href: "/settings" },
  { id: "notifications", label: "Notifications",icon: <Bell size={15} />,     href: "/notifications" },
];

/* ────────────────────────────────────────────────────────── Logo SVG */

function LogoMark() {
  return (
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="28" height="28" rx="7" fill="url(#lp-grad)" />
      <circle cx="14" cy="14" r="7" stroke="white" strokeWidth="1.5" strokeOpacity="0.9" fill="none" />
      <line x1="14" y1="9"  x2="14" y2="19" stroke="white" strokeWidth="1.5" strokeOpacity="0.9" strokeLinecap="round" />
      <line x1="9"  y1="14" x2="19" y2="14" stroke="white" strokeWidth="1.5" strokeOpacity="0.9" strokeLinecap="round" />
      <defs>
        <linearGradient id="lp-grad" x1="0" y1="0" x2="28" y2="28" gradientUnits="userSpaceOnUse">
          <stop offset="0%"   stopColor="#4A3FB0" />
          <stop offset="50%"  stopColor="#6B5FD4" />
          <stop offset="100%" stopColor="#C9982A" />
        </linearGradient>
      </defs>
    </svg>
  );
}

/* ────────────────────────────────────────────────────────── Dropdown */

interface DropdownProps {
  group: NavGroup;
  currentPath?: string;
  onNavigate?: (href: string) => void;
}

function GroupDropdown({ group, currentPath, onNavigate }: DropdownProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const isGroupActive = group.items.some(
    (i) => currentPath === i.href || currentPath?.startsWith(i.href + "/")
  );

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className={cn(
          "flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-150",
          isGroupActive
            ? "text-white"
            : "text-white/60 hover:text-white hover:bg-white/[0.06]"
        )}
      >
        {isGroupActive && (
          <motion.span
            layoutId="nav-active-bg"
            className="absolute inset-0 rounded-lg bg-white/[0.08]"
            transition={{ type: "spring", stiffness: 380, damping: 30 }}
          />
        )}
        <span className="relative">{group.label}</span>
        <motion.span
          className="relative"
          animate={{ rotate: open ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <ChevronDown size={13} />
        </motion.span>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -6, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -6, scale: 0.97 }}
            transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
            className="absolute top-full left-0 mt-2 w-64 rounded-2xl overflow-hidden z-50"
            style={{
              background: "#0E0B20",
              border: "1px solid rgba(255,255,255,0.07)",
              boxShadow: "0 16px 48px rgba(0,0,0,0.5), 0 2px 8px rgba(0,0,0,0.3)",
            }}
          >
            <div className="p-2">
              {group.items.map((item) => {
                const active =
                  currentPath === item.href ||
                  currentPath?.startsWith(item.href + "/");
                return (
                  <button
                    key={item.id}
                    onClick={() => { onNavigate?.(item.href); setOpen(false); }}
                    className={cn(
                      "w-full flex items-start gap-3 px-3 py-2.5 rounded-xl text-left transition-all duration-150",
                      active
                        ? "bg-[rgba(201,152,42,0.12)] text-white"
                        : "text-white/60 hover:bg-white/[0.05] hover:text-white"
                    )}
                  >
                    <span
                      className={cn(
                        "mt-0.5 flex-shrink-0",
                        active ? "text-[#C9982A]" : "text-white/40"
                      )}
                    >
                      {item.icon}
                    </span>
                    <div className="min-w-0">
                      <div
                        className="text-sm font-medium leading-tight"
                        style={active ? { color: "#E8C55A" } : {}}
                      >
                        {item.label}
                      </div>
                      {item.description && (
                        <div className="text-xs text-white/35 mt-0.5 leading-snug">
                          {item.description}
                        </div>
                      )}
                    </div>
                    {active && (
                      <span className="ml-auto flex-shrink-0 w-1 rounded-full self-stretch bg-[#C9982A] opacity-80" />
                    )}
                  </button>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/* ────────────────────────────────────────────────────────── Avatar dropdown */

interface AvatarDropdownProps {
  userName?: string;
  onNavigate?: (href: string) => void;
  onSignOut?: () => void;
}

function AvatarDropdown({ userName = "User", onNavigate, onSignOut }: AvatarDropdownProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const initial = userName[0]?.toUpperCase() ?? "U";

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white transition-transform hover:scale-105"
        style={{
          background: "linear-gradient(135deg,#B05A7A,#C9982A)",
          border: "2px solid rgba(201,152,42,0.3)",
        }}
        title={userName}
      >
        {initial}
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -6, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -6, scale: 0.97 }}
            transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
            className="absolute top-full right-0 mt-2 w-48 rounded-2xl overflow-hidden z-50"
            style={{
              background: "#0E0B20",
              border: "1px solid rgba(255,255,255,0.07)",
              boxShadow: "0 16px 48px rgba(0,0,0,0.5)",
            }}
          >
            <div className="px-4 py-3 border-b border-white/[0.06]">
              <p className="text-sm font-semibold text-white truncate">{userName}</p>
            </div>
            <div className="p-2">
              {ACCOUNT_ITEMS.map((item) => (
                <button
                  key={item.id}
                  onClick={() => { onNavigate?.(item.href); setOpen(false); }}
                  className="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-sm text-white/60 hover:text-white hover:bg-white/[0.05] transition-colors text-left"
                >
                  <span className="text-white/40">{item.icon}</span>
                  {item.label}
                </button>
              ))}
              <div className="my-1.5 border-t border-white/[0.06]" />
              <button
                onClick={() => { onSignOut?.(); setOpen(false); }}
                className="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-sm text-red-400/80 hover:text-red-400 hover:bg-red-400/[0.06] transition-colors text-left"
              >
                <LogOut size={15} />
                Sign out
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/* ────────────────────────────────────────────────────────── Leadership group */

interface LeadershipGroupProps {
  role: Role;
  currentPath?: string;
  onNavigate?: (href: string) => void;
}

function LeadershipGroup({ role, currentPath, onNavigate }: LeadershipGroupProps) {
  const items = LEADERSHIP_ITEMS[role];
  if (!items || items.length === 0) return null;

  const group: NavGroup = { id: "leadership", label: "Leadership", items };
  return <GroupDropdown group={group} currentPath={currentPath} onNavigate={onNavigate} />;
}

/* ────────────────────────────────────────────────────────── Mobile Overlay */

interface MobileOverlayProps {
  role?: Role;
  currentPath?: string;
  unreadCount?: number;
  onNavigate?: (href: string) => void;
  onSignOut?: () => void;
  onClose: () => void;
}

function MobileOverlay({
  role = "prayer_warrior",
  currentPath,
  unreadCount = 0,
  onNavigate,
  onSignOut,
  onClose,
}: MobileOverlayProps) {
  const handle = useCallback((href: string) => {
    onNavigate?.(href);
    onClose();
  }, [onNavigate, onClose]);

  const allGroups = [
    ...NAV_GROUPS,
    ...(LEADERSHIP_ITEMS[role]?.length
      ? [{ id: "leadership", label: "Leadership", items: LEADERSHIP_ITEMS[role] }]
      : []),
    { id: "account", label: "Account", items: ACCOUNT_ITEMS },
  ];

  return (
    <motion.div
      initial={{ x: "-100%" }}
      animate={{ x: 0 }}
      exit={{ x: "-100%" }}
      transition={{ type: "spring", stiffness: 280, damping: 28 }}
      className="fixed inset-0 z-[100] flex"
    >
      {/* Panel */}
      <div
        className="relative w-full max-w-xs h-full flex flex-col overflow-y-auto"
        style={{ background: "#0D0A1C", borderRight: "1px solid rgba(255,255,255,0.06)" }}
      >
        {/* Header */}
        <div
          className="flex items-center justify-between px-5 py-4 flex-shrink-0"
          style={{ borderBottom: "1px solid rgba(255,255,255,0.07)" }}
        >
          <div className="flex items-center gap-3">
            <LogoMark />
            <span
              className="text-base font-semibold text-white"
              style={{ fontFamily: "Cinzel, Georgia, serif" }}
            >
              Logos Pulse
            </span>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full flex items-center justify-center text-white/40 hover:text-white hover:bg-white/[0.08] transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Nav groups */}
        <div className="flex-1 px-3 py-4 space-y-5">
          {allGroups.map((group) => (
            <div key={group.id}>
              <p
                className="px-3 mb-1 text-[10px] font-bold uppercase tracking-[0.16em]"
                style={{ color: "rgba(201,152,42,0.55)" }}
              >
                {group.label}
              </p>
              <div className="space-y-0.5">
                {group.items.map((item) => {
                  const active =
                    currentPath === item.href ||
                    currentPath?.startsWith(item.href + "/");
                  const isSignOut = false;
                  return (
                    <button
                      key={item.id}
                      onClick={() => handle(item.href)}
                      className={cn(
                        "w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all text-left",
                        active
                          ? "bg-[rgba(201,152,42,0.1)] text-white font-semibold"
                          : "text-white/60 hover:text-white hover:bg-white/[0.05]"
                      )}
                    >
                      <span
                        className="flex-shrink-0"
                        style={{ color: active ? "#C9982A" : "rgba(255,255,255,0.35)" }}
                      >
                        {item.icon}
                      </span>
                      <span className="flex-1">{item.label}</span>
                      {item.id === "notifications" && unreadCount > 0 && (
                        <span
                          className="text-[10px] font-bold rounded-full w-5 h-5 flex items-center justify-center flex-shrink-0"
                          style={{ background: "#C9982A", color: "#0D0A1C" }}
                        >
                          {unreadCount}
                        </span>
                      )}
                      {active && (
                        <span className="w-1 rounded-full self-stretch flex-shrink-0 bg-[#C9982A]" />
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Sign out */}
        <div className="px-3 pb-6 flex-shrink-0" style={{ borderTop: "1px solid rgba(255,255,255,0.07)" }}>
          <button
            onClick={() => { onSignOut?.(); onClose(); }}
            className="mt-4 w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-red-400/70 hover:text-red-400 hover:bg-red-400/[0.06] transition-colors"
          >
            <LogOut size={15} />
            Sign out
          </button>
        </div>
      </div>

      {/* Backdrop */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
        className="flex-1 bg-black/60 backdrop-blur-sm"
      />
    </motion.div>
  );
}

/* ────────────────────────────────────────────────────────── TopNav */

export function TopNav({
  role = "prayer_warrior",
  currentPath = "/dashboard",
  userName = "User",
  unreadCount = 0,
  onNavigate,
  onSignOut,
}: TopNavProps) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      <header
        className="fixed top-0 left-0 right-0 z-50 flex items-center px-4 md:px-6"
        style={{
          height: "56px",
          background: "rgba(14,11,32,0.95)",
          borderBottom: "1px solid rgba(255,255,255,0.06)",
          backdropFilter: "blur(20px) saturate(150%)",
          WebkitBackdropFilter: "blur(20px) saturate(150%)",
          boxShadow: "0 1px 0 rgba(0,0,0,0.3), 0 4px 24px rgba(0,0,0,0.2)",
        }}
      >
        {/* Logo */}
        <button
          onClick={() => onNavigate?.("/dashboard")}
          className="flex items-center gap-2.5 mr-6 flex-shrink-0 group"
        >
          <LogoMark />
          <span
            className="text-white text-[15px] font-semibold hidden sm:block group-hover:text-white/90 transition-colors"
            style={{ fontFamily: "Cinzel, Georgia, serif", letterSpacing: "0.03em" }}
          >
            Logos Pulse
          </span>
        </button>

        {/* Desktop nav groups */}
        <nav className="hidden md:flex items-center gap-0.5 flex-1">
          {NAV_GROUPS.map((group) => (
            <GroupDropdown
              key={group.id}
              group={group}
              currentPath={currentPath}
              onNavigate={onNavigate}
            />
          ))}
          <LeadershipGroup
            role={role}
            currentPath={currentPath}
            onNavigate={onNavigate}
          />
        </nav>

        {/* Right side */}
        <div className="flex items-center gap-2 ml-auto">
          {/* Notification bell */}
          <button
            onClick={() => onNavigate?.("/notifications")}
            className="relative w-9 h-9 rounded-lg flex items-center justify-center text-white/50 hover:text-white hover:bg-white/[0.06] transition-all"
          >
            <Bell size={17} />
            {unreadCount > 0 && (
              <span
                className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full"
                style={{ background: "#C9982A", boxShadow: "0 0 0 1.5px #0E0B20" }}
              />
            )}
          </button>

          {/* Avatar (desktop) */}
          <div className="hidden md:block">
            <AvatarDropdown
              userName={userName}
              onNavigate={onNavigate}
              onSignOut={onSignOut}
            />
          </div>

          {/* Hamburger (mobile) */}
          <button
            onClick={() => setMobileOpen(true)}
            className="md:hidden w-9 h-9 rounded-lg flex items-center justify-center text-white/60 hover:text-white hover:bg-white/[0.06] transition-all"
            aria-label="Open menu"
          >
            <Menu size={20} />
          </button>
        </div>
      </header>

      {/* Spacer so content doesn't hide under fixed nav */}
      <div style={{ height: "56px" }} />

      {/* Mobile overlay */}
      <AnimatePresence>
        {mobileOpen && (
          <MobileOverlay
            role={role}
            currentPath={currentPath}
            unreadCount={unreadCount}
            onNavigate={onNavigate}
            onSignOut={onSignOut}
            onClose={() => setMobileOpen(false)}
          />
        )}
      </AnimatePresence>
    </>
  );
}

export default TopNav;