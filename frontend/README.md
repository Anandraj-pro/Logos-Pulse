# Logos Pulse — Auth Switch Component

Beautiful login/signup toggle built with React, shadcn, Tailwind CSS, and Framer Motion.

## Setup

```bash
# 1. Create a new Next.js project (or use an existing one)
npx create-next-app@latest logos-pulse-web --typescript --tailwind --app
cd logos-pulse-web

# 2. Initialize shadcn
npx shadcn@latest init

# 3. Install dependencies
npm install framer-motion lucide-react clsx tailwind-merge

# 4. Copy component files
cp components/ui/auth-switch.tsx  <your-project>/components/ui/
cp lib/utils.ts                   <your-project>/lib/
cp demo.tsx                       <your-project>/app/page.tsx
```

## Fonts used

Add to your `app/layout.tsx` `<head>` or import in globals.css:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=EB+Garamond:ital,wght@0,400;1,400&family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

The component self-injects fonts via `<style>` if you skip this step.

## Usage

```tsx
import AuthSwitch from "@/components/ui/auth-switch";

export default function LoginPage() {
  return (
    <AuthSwitch
      onSignIn={async (email, password) => {
        // call your Supabase / API
        await supabase.auth.signInWithPassword({ email, password });
      }}
      onSignUp={async (name, email, password) => {
        await supabase.auth.signUp({ email, password, options: { data: { preferred_name: name } } });
      }}
    />
  );
}
```

## What's inside

| Feature | Detail |
|---|---|
| **Background** | Midnight `#060410` + 4-point radial gradient mesh + subtle gold grid + noise grain |
| **Floating scripture** | 12 verse fragments drift at varied angles and speeds |
| **Logo** | Pure-CSS gold cross SVG + Cinzel shimmer gradient text |
| **Mode toggle** | Spring-physics sliding pill (Framer Motion `type: "spring"`) |
| **Inputs** | Floating-label with gold focus glow, leading icon, password reveal |
| **Button** | Animated shimmer gradient + glow pulse, spring scale on hover/tap |
| **Animations** | Staggered entrance, `AnimatePresence` for name field & error, loading state |
| **Fonts** | Cinzel (logo) · EB Garamond (scripture) · Nunito (UI) |
