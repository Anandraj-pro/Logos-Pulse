import React from "react";
import AuthSwitch from "./components/ui/auth-switch";

export default function Demo() {
  const handleSignIn = async (email: string, password: string) => {
    // Simulate async auth — replace with your Supabase call
    await new Promise((r) => setTimeout(r, 1200));
    console.log("Sign in →", email, password);
  };

  const handleSignUp = async (name: string, email: string, password: string) => {
    await new Promise((r) => setTimeout(r, 1400));
    console.log("Sign up →", name, email, password);
  };

  return (
    <AuthSwitch
      onSignIn={handleSignIn}
      onSignUp={handleSignUp}
    />
  );
}
