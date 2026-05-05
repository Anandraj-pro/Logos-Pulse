import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Logos Pulse",
  description: "Track your walk with God",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
