"use client";

import BibleReader from "@/components/ui/bible-reader";

export default function Demo() {
  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center py-10 px-4"
      style={{ background: "#F3EFE7" }}
    >
      {/* Header */}
      <div className="text-center mb-8">
        <p
          style={{
            fontFamily: "Jost, sans-serif",
            fontSize: 10,
            fontWeight: 700,
            textTransform: "uppercase",
            letterSpacing: "0.3em",
            color: "#B85A30",
            marginBottom: 6,
          }}
        >
          Scripture Reading
        </p>
        <h1
          style={{
            fontFamily: "Cormorant Garamond, Cormorant, Georgia, serif",
            fontSize: 32,
            fontWeight: 400,
            color: "#1A1208",
            letterSpacing: "0.04em",
          }}
        >
          The Holy Bible
        </h1>
        <div
          className="mx-auto mt-3"
          style={{
            width: 60,
            height: 1,
            background: "linear-gradient(90deg, transparent, #C48A1C, transparent)",
          }}
        />
      </div>

      {/* Bible reader with default John 3 */}
      <BibleReader defaultBook="John" defaultChapter={3} />
    </div>
  );
}
