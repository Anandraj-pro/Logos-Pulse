"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  ChevronLeft,
  ChevronRight,
  BookOpen,
  Bookmark,
  BookMarked,
  Menu,
  X,
  Search,
} from "lucide-react";

// ─── Types ────────────────────────────────────────────────────────────────────
interface Verse {
  verse: number;
  text: string;
}

interface ChapterData {
  book: string;
  chapter: number;
  verses: Verse[];
}

// ─── Static Bible data (NIV-style) ───────────────────────────────────────────
const STATIC_CHAPTERS: Record<string, Record<number, Verse[]>> = {
  Genesis: {
    1: [
      { verse: 1, text: "In the beginning God created the heavens and the earth." },
      { verse: 2, text: "Now the earth was formless and empty, darkness was over the surface of the deep, and the Spirit of God was hovering over the waters." },
      { verse: 3, text: "And God said, \"Let there be light,\" and there was light." },
      { verse: 4, text: "God saw that the light was good, and he separated the light from the darkness." },
      { verse: 5, text: "God called the light \"day,\" and the darkness he called \"night.\" And there was evening, and there was morning — the first day." },
      { verse: 6, text: "And God said, \"Let there be a vault between the waters to separate water from water.\"" },
      { verse: 7, text: "So God made the vault and separated the water under the vault from the water above it. And it was so." },
      { verse: 8, text: "God called the vault \"sky.\" And there was evening, and there was morning — the second day." },
      { verse: 9, text: "And God said, \"Let the water under the sky be gathered to one place, and let dry ground appear.\" And it was so." },
      { verse: 10, text: "God called the dry ground \"land,\" and the gathered waters he called \"seas.\" And God saw that it was good." },
      { verse: 11, text: "Then God said, \"Let the land produce vegetation: seed-bearing plants and trees on the land that bear fruit with seed in it, according to their various kinds.\" And it was so." },
      { verse: 12, text: "The land produced vegetation: plants bearing seed according to their kinds and trees bearing fruit with seed in it according to their kinds. And God saw that it was good." },
      { verse: 26, text: "Then God said, \"Let us make mankind in our image, in our likeness, so that they may rule over the fish in the sea and the birds in the sky, over the livestock and all the wild animals, and over all the creatures that move along the ground.\"" },
      { verse: 27, text: "So God created mankind in his own image, in the image of God he created them; male and female he created them." },
      { verse: 31, text: "God saw all that he had made, and it was very good. And there was evening, and there was morning — the sixth day." },
    ],
    2: [
      { verse: 1, text: "Thus the heavens and the earth were completed in all their vast array." },
      { verse: 2, text: "By the seventh day God had finished the work he had been doing; so on the seventh day he rested from all his work." },
      { verse: 3, text: "Then God blessed the seventh day and made it holy, because on it he rested from all the work of creating that he had done." },
      { verse: 7, text: "Then the Lord God formed a man from the dust of the ground and breathed into his nostrils the breath of life, and the man became a living being." },
      { verse: 15, text: "The Lord God took the man and put him in the Garden of Eden to work it and take care of it." },
      { verse: 18, text: "The Lord God said, \"It is not good for the man to be alone. I will make a helper suitable for him.\"" },
      { verse: 24, text: "That is why a man leaves his father and mother and is united to his wife, and they become one flesh." },
    ],
    3: [
      { verse: 1, text: "Now the serpent was more crafty than any of the wild animals the Lord God had made. He said to the woman, \"Did God really say, 'You must not eat from any tree in the garden'?\"" },
      { verse: 8, text: "Then the man and his wife heard the sound of the Lord God as he was walking in the garden in the cool of the day, and they hid from the Lord God among the trees of the garden." },
      { verse: 9, text: "But the Lord God called to the man, \"Where are you?\"" },
      { verse: 15, text: "And I will put enmity between you and the woman, and between your offspring and hers; he will crush your head, and you will strike his heel." },
    ],
  },
  Psalm: {
    23: [
      { verse: 1, text: "The Lord is my shepherd, I lack nothing." },
      { verse: 2, text: "He makes me lie down in green pastures, he leads me beside quiet waters," },
      { verse: 3, text: "he refreshes my soul. He guides me along the right paths for his name's sake." },
      { verse: 4, text: "Even though I walk through the darkest valley, I will fear no evil, for you are with me; your rod and your staff, they comfort me." },
      { verse: 5, text: "You prepare a table before me in the presence of my enemies. You anoint my head with oil; my cup overflows." },
      { verse: 6, text: "Surely your goodness and love will follow me all the days of my life, and I will dwell in the house of the Lord forever." },
    ],
    119: [
      { verse: 1, text: "Blessed are those whose ways are blameless, who walk according to the law of the Lord." },
      { verse: 2, text: "Blessed are those who keep his statutes and seek him with all their heart—" },
      { verse: 9, text: "How can a young person stay on the path of purity? By living according to your word." },
      { verse: 11, text: "I have hidden your word in my heart that I might not sin against you." },
      { verse: 105, text: "Your word is a lamp for my feet, a light on my path." },
      { verse: 130, text: "The unfolding of your words gives light; it gives understanding to the simple." },
    ],
  },
  John: {
    1: [
      { verse: 1, text: "In the beginning was the Word, and the Word was with God, and the Word was God." },
      { verse: 2, text: "He was with God in the beginning." },
      { verse: 3, text: "Through him all things were made; without him nothing was made that has been made." },
      { verse: 4, text: "In him was life, and that life was the light of all mankind." },
      { verse: 5, text: "The light shines in the darkness, and the darkness has not overcome it." },
      { verse: 14, text: "The Word became flesh and made his dwelling among us. We have seen his glory, the glory of the one and only Son, who came from the Father, full of grace and truth." },
    ],
    3: [
      { verse: 14, text: "Just as Moses lifted up the snake in the wilderness, so the Son of Man must be lifted up," },
      { verse: 15, text: "that everyone who believes may have eternal life in him." },
      { verse: 16, text: "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life." },
      { verse: 17, text: "For God did not send his Son into the world to condemn the world, but to save the world through him." },
    ],
    14: [
      { verse: 1, text: "\"Do not let your hearts be troubled. You believe in God; believe also in me." },
      { verse: 2, text: "My Father's house has many rooms; if that were not so, would I have told you that I am going there to prepare a place for you?" },
      { verse: 6, text: "Jesus answered, \"I am the way and the truth and the life. No one comes to the Father except through me." },
      { verse: 27, text: "Peace I leave with you; my peace I give you. I do not give to you as the world gives. Do not let your hearts be troubled and do not be afraid." },
    ],
  },
  Romans: {
    8: [
      { verse: 1, text: "Therefore, there is now no condemnation for those who are in Christ Jesus," },
      { verse: 2, text: "because through Christ Jesus the law of the Spirit who gives life has set you free from the law of sin and death." },
      { verse: 28, text: "And we know that in all things God works for the good of those who love him, who have been called according to his purpose." },
      { verse: 37, text: "No, in all these things we are more than conquerors through him who loved us." },
      { verse: 38, text: "For I am convinced that neither death nor life, neither angels nor demons, neither the present nor the future, nor any powers," },
      { verse: 39, text: "neither height nor depth, nor anything else in all creation, will be able to separate us from the love of God that is in Christ Jesus our Lord." },
    ],
  },
  Philippians: {
    4: [
      { verse: 4, text: "Rejoice in the Lord always. I will say it again: Rejoice!" },
      { verse: 6, text: "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God." },
      { verse: 7, text: "And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus." },
      { verse: 8, text: "Finally, brothers and sisters, whatever is true, whatever is noble, whatever is right, whatever is pure, whatever is lovely, whatever is admirable — if anything is excellent or praiseworthy — think about such things." },
      { verse: 13, text: "I can do all this through him who gives me strength." },
      { verse: 19, text: "And my God will meet all your needs according to the riches of his glory in Christ Jesus." },
    ],
  },
};

const BOOKS = Object.keys(STATIC_CHAPTERS);
const BOOK_CHAPTERS: Record<string, number[]> = {
  Genesis: [1, 2, 3],
  Psalm: [23, 119],
  John: [1, 3, 14],
  Romans: [8],
  Philippians: [4],
};

// ─── Animation states ─────────────────────────────────────────────────────────
type AnimState = "idle" | "exit" | "enter";

// ─── Page component ───────────────────────────────────────────────────────────
function BookPage({
  verses,
  book,
  chapter,
  side,
}: {
  verses: Verse[];
  book: string;
  chapter: number;
  side: "left" | "right";
}) {
  const isLeft = side === "left";
  return (
    <div className="relative h-full flex flex-col overflow-hidden select-none"
      style={{
        background: isLeft
          ? "linear-gradient(to right, #EDE0C4, #F0E6CE, #F5EDD6)"
          : "linear-gradient(to left,  #EDE0C4, #F0E6CE, #F5EDD6)",
        boxShadow: isLeft
          ? "inset -8px 0 20px -8px rgba(74,46,26,0.18)"
          : "inset  8px 0 20px -8px rgba(74,46,26,0.18)",
      }}>
      {/* Grain overlay */}
      <div className="absolute inset-0 opacity-[0.035] pointer-events-none"
        style={{
          backgroundImage:
            "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")",
          backgroundSize: "256px",
        }} />

      {/* Ruled lines */}
      <div className="absolute inset-0 pointer-events-none" style={{ paddingTop: 80 }}>
        {[...Array(22)].map((_, i) => (
          <div key={i} className="absolute left-8 right-8"
            style={{ top: 80 + i * 24, height: 1, background: "rgba(74,46,26,0.055)" }} />
        ))}
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col h-full px-8 pt-8 pb-6">
        {/* Header */}
        <div className={`flex items-baseline mb-5 pb-3 ${isLeft ? "flex-row-reverse" : "flex-row"} justify-between`}
          style={{ borderBottom: "1px solid rgba(74,46,26,0.12)" }}>
          <span style={{
            fontFamily: "Cormorant Garamond, Cormorant, Georgia, serif",
            fontSize: 18, fontWeight: 600, color: "#1A1208", letterSpacing: "0.01em",
          }}>
            {book}
          </span>
          <span style={{
            fontFamily: "Jost, sans-serif", fontSize: 9,
            fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.25em",
            color: "#B85A30",
          }}>
            Chapter {chapter}
          </span>
        </div>

        {/* Verses */}
        <div className="flex-1 overflow-hidden space-y-2.5">
          {verses.map((v) => (
            <div key={v.verse} className="flex gap-2 group">
              <sup style={{
                fontFamily: "Jost, sans-serif", fontSize: 8,
                fontWeight: 700, color: "#B85A30",
                marginTop: 5, width: 14, flexShrink: 0,
                textAlign: "right", opacity: 0.75,
              }}>
                {v.verse}
              </sup>
              <p style={{
                fontFamily: "Cormorant Garamond, Cormorant, Georgia, serif",
                fontSize: 14.5, lineHeight: 1.78,
                color: "#1A1208", flex: 1,
              }}>
                {v.text}
              </p>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className={`mt-auto pt-3 flex items-center ${isLeft ? "flex-row-reverse" : "flex-row"} justify-between`}
          style={{ borderTop: "1px solid rgba(74,46,26,0.08)" }}>
          <span style={{
            fontFamily: "Jost, sans-serif", fontSize: 8,
            textTransform: "uppercase", letterSpacing: "0.2em", color: "#A09080",
          }}>
            {book} {chapter}
          </span>
          <div className="flex gap-1">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="w-1 h-1 rounded-full"
                style={{ background: "#B85A30", opacity: 0.2 + i * 0.1 }} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Chapter ornament ─────────────────────────────────────────────────────────
function ChapterOrnament({ chapter, book }: { chapter: number; book: string }) {
  return (
    <div className="flex flex-col items-center gap-2 py-6">
      <div className="flex items-center gap-4 w-full">
        <div className="flex-1 h-px" style={{ background: "linear-gradient(to right, transparent, rgba(196,138,28,0.4))" }} />
        <div className="flex flex-col items-center">
          <span style={{ fontFamily: "Cormorant Garamond, Cormorant, Georgia, serif", fontSize: 11, color: "#C48A1C", letterSpacing: "0.3em", textTransform: "uppercase" }}>
            {book}
          </span>
          <span style={{ fontFamily: "Cormorant Garamond, Cormorant, Georgia, serif", fontSize: 48, fontWeight: 300, color: "#1A1208", lineHeight: 1 }}>
            {chapter}
          </span>
          <div className="flex gap-1 mt-0.5">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="w-1 h-1 rounded-full" style={{ background: "#C48A1C", opacity: 0.15 + Math.abs(i - 2) * 0.08 }} />
            ))}
          </div>
        </div>
        <div className="flex-1 h-px" style={{ background: "linear-gradient(to left, transparent, rgba(196,138,28,0.4))" }} />
      </div>
    </div>
  );
}

// ─── Main BibleReader ─────────────────────────────────────────────────────────
export function BibleReader({
  defaultBook = "John",
  defaultChapter = 3,
}: {
  defaultBook?: string;
  defaultChapter?: number;
}) {
  const [book, setBook] = useState(defaultBook);
  const [chapter, setChapter] = useState(defaultChapter);
  const [displayBook, setDisplayBook] = useState(defaultBook);
  const [displayChapter, setDisplayChapter] = useState(defaultChapter);
  const [animState, setAnimState] = useState<AnimState>("idle");
  const [direction, setDirection] = useState<"next" | "prev">("next");
  const [showTOC, setShowTOC] = useState(false);
  const [singlePage, setSinglePage] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Detect narrow screens
  useEffect(() => {
    const check = () => setSinglePage(window.innerWidth < 720);
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  const verses = STATIC_CHAPTERS[displayBook]?.[displayChapter] ?? [];

  // Split verses for two-page spread
  const midpoint = Math.ceil(verses.length / 2);
  const leftVerses = singlePage ? [] : verses.slice(0, midpoint);
  const rightVerses = singlePage ? verses : verses.slice(midpoint);

  // Navigate
  const navigate = useCallback(
    (newBook: string, newChapter: number) => {
      if (animState !== "idle") return;
      const dir = newChapter > chapter || newBook !== book ? "next" : "prev";
      setDirection(dir);
      setAnimState("exit");

      setTimeout(() => {
        setDisplayBook(newBook);
        setDisplayChapter(newChapter);
        setBook(newBook);
        setChapter(newChapter);
        setAnimState("enter");
      }, 350);

      setTimeout(() => setAnimState("idle"), 750);
    },
    [animState, chapter, book]
  );

  const goNext = () => {
    const chapters = BOOK_CHAPTERS[book] ?? [];
    const idx = chapters.indexOf(chapter);
    if (idx < chapters.length - 1) navigate(book, chapters[idx + 1]);
    else {
      const bookIdx = BOOKS.indexOf(book);
      if (bookIdx < BOOKS.length - 1) {
        const nextBook = BOOKS[bookIdx + 1];
        navigate(nextBook, (BOOK_CHAPTERS[nextBook] ?? [1])[0]);
      }
    }
  };

  const goPrev = () => {
    const chapters = BOOK_CHAPTERS[book] ?? [];
    const idx = chapters.indexOf(chapter);
    if (idx > 0) navigate(book, chapters[idx - 1]);
    else {
      const bookIdx = BOOKS.indexOf(book);
      if (bookIdx > 0) {
        const prevBook = BOOKS[bookIdx - 1];
        const prevChaps = BOOK_CHAPTERS[prevBook] ?? [1];
        navigate(prevBook, prevChaps[prevChaps.length - 1]);
      }
    }
  };

  // Anim classes
  const pageClass = (() => {
    if (animState === "exit")
      return direction === "next"
        ? "animate-page-exit-forward"
        : "animate-page-exit-backward";
    if (animState === "enter")
      return direction === "next"
        ? "animate-page-enter-forward"
        : "animate-page-enter-backward";
    return "";
  })();

  const canNext = (() => {
    const chapters = BOOK_CHAPTERS[book] ?? [];
    const idx = chapters.indexOf(chapter);
    return idx < chapters.length - 1 || BOOKS.indexOf(book) < BOOKS.length - 1;
  })();

  const canPrev = (() => {
    const chapters = BOOK_CHAPTERS[book] ?? [];
    const idx = chapters.indexOf(chapter);
    return idx > 0 || BOOKS.indexOf(book) > 0;
  })();

  return (
    <>
      <div className="flex flex-col items-center gap-5 w-full" ref={containerRef}>
        {/* ── Book wrapper ── */}
        <div className="relative w-full" style={{ maxWidth: singlePage ? 380 : 740 }}>

          {/* Outer book shadow */}
          <div className="absolute -bottom-5 left-6 right-6 h-10 rounded-full blur-2xl opacity-40"
            style={{ background: "#1A1208" }} />

          {/* Book body */}
          <div className="relative rounded-sm overflow-hidden"
            style={{
              height: singlePage ? 520 : 480,
              boxShadow: "0 8px 40px rgba(26,18,8,0.22), 0 2px 8px rgba(26,18,8,0.14)",
            }}>

            {/* Pages spread */}
            <div className={`flex h-full ${pageClass}`} style={{ transformStyle: "preserve-3d" }}>

              {/* Left page (two-page only) */}
              {!singlePage && (
                <div className="flex-1 h-full">
                  <BookPage
                    verses={leftVerses}
                    book={displayBook}
                    chapter={displayChapter}
                    side="left"
                  />
                </div>
              )}

              {/* Book spine */}
              {!singlePage && (
                <div className="relative flex-shrink-0 flex flex-col items-center justify-center"
                  style={{
                    width: 22,
                    background: "linear-gradient(to right, #3A2010, #5C3A1E, #4A2E14, #3A2010)",
                    boxShadow: "inset -2px 0 6px rgba(0,0,0,0.25), inset 2px 0 6px rgba(0,0,0,0.25)",
                  }}>
                  {/* Spine lines */}
                  {[...Array(6)].map((_, i) => (
                    <div key={i} className="w-full my-0.5" style={{ height: 1, background: "rgba(196,138,28,0.15)" }} />
                  ))}
                </div>
              )}

              {/* Right page */}
              <div className="flex-1 h-full">
                <BookPage
                  verses={rightVerses}
                  book={displayBook}
                  chapter={displayChapter}
                  side="right"
                />
              </div>
            </div>

            {/* Turn shadow sweep overlay (appears during animation) */}
            {animState !== "idle" && (
              <div className="absolute inset-0 pointer-events-none shadow-sweep"
                style={{
                  background: direction === "next"
                    ? "linear-gradient(to right, transparent 0%, rgba(26,18,8,0.08) 45%, rgba(26,18,8,0.18) 50%, rgba(26,18,8,0.08) 55%, transparent 100%)"
                    : "linear-gradient(to left, transparent 0%, rgba(26,18,8,0.08) 45%, rgba(26,18,8,0.18) 50%, rgba(26,18,8,0.08) 55%, transparent 100%)",
                }} />
            )}

            {/* Page curl corners */}
            <div className="absolute bottom-0 right-0 w-10 h-10 pointer-events-none"
              style={{
                background: "linear-gradient(135deg, transparent 50%, rgba(74,46,26,0.12) 50%)",
              }} />
            {!singlePage && (
              <div className="absolute bottom-0 left-0 w-10 h-10 pointer-events-none"
                style={{
                  background: "linear-gradient(225deg, transparent 50%, rgba(74,46,26,0.12) 50%)",
                }} />
            )}
          </div>
        </div>

        {/* ── Chapter ornament / title ── */}
        <div className="ornament-animate w-full" style={{ maxWidth: singlePage ? 380 : 740 }}>
          <ChapterOrnament chapter={displayChapter} book={displayBook} />
        </div>

        {/* ── Navigation ── */}
        <div className="flex items-center gap-4">
          {/* Prev */}
          <button
            onClick={goPrev}
            disabled={!canPrev || animState !== "idle"}
            className="flex items-center gap-2 px-5 py-2.5 rounded-full transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed"
            style={{
              background: "rgba(184,90,48,0.07)",
              border: "1px solid rgba(184,90,48,0.22)",
              color: "#B85A30",
              fontFamily: "Jost, sans-serif",
              fontSize: 13, fontWeight: 600,
            }}
          >
            <ChevronLeft size={16} />
            <span>Prev</span>
          </button>

          {/* Chapter picker */}
          <button
            onClick={() => setShowTOC(!showTOC)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-full transition-all duration-200"
            style={{
              background: "#B85A30",
              color: "white",
              fontFamily: "Cormorant Garamond, Cormorant, Georgia, serif",
              fontSize: 15, fontWeight: 500,
              boxShadow: "0 3px 14px rgba(184,90,48,0.32)",
            }}
          >
            <BookOpen size={15} />
            <span>{book} {chapter}</span>
            <Menu size={13} />
          </button>

          {/* Next */}
          <button
            onClick={goNext}
            disabled={!canNext || animState !== "idle"}
            className="flex items-center gap-2 px-5 py-2.5 rounded-full transition-all duration-200 disabled:opacity-30 disabled:cursor-not-allowed"
            style={{
              background: "rgba(184,90,48,0.07)",
              border: "1px solid rgba(184,90,48,0.22)",
              color: "#B85A30",
              fontFamily: "Jost, sans-serif",
              fontSize: 13, fontWeight: 600,
            }}
          >
            <span>Next</span>
            <ChevronRight size={16} />
          </button>
        </div>

        {/* Keyboard hint */}
        <p style={{ fontFamily: "Jost, sans-serif", fontSize: 10, color: "#A09080", letterSpacing: "0.15em", textTransform: "uppercase" }}>
          Click Prev / Next to turn pages
        </p>

        {/* ── Table of Contents drawer ── */}
        {showTOC && (
          <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center"
            style={{ background: "rgba(26,18,8,0.5)", backdropFilter: "blur(8px)" }}
            onClick={() => setShowTOC(false)}>
            <div
              className="relative w-full max-w-md rounded-t-2xl sm:rounded-2xl overflow-hidden"
              style={{ background: "#F5EDD6", maxHeight: "70vh" }}
              onClick={(e) => e.stopPropagation()}>

              {/* Header */}
              <div className="flex items-center justify-between px-6 py-4"
                style={{ borderBottom: "1px solid rgba(74,46,26,0.12)" }}>
                <h3 style={{ fontFamily: "Cormorant Garamond, Cormorant, Georgia, serif", fontSize: 20, fontWeight: 600, color: "#1A1208" }}>
                  Contents
                </h3>
                <button onClick={() => setShowTOC(false)}
                  className="w-8 h-8 rounded-full flex items-center justify-center"
                  style={{ background: "rgba(74,46,26,0.08)", color: "#5A4A32" }}>
                  <X size={16} />
                </button>
              </div>

              {/* Books & chapters */}
              <div className="overflow-y-auto p-4 space-y-4" style={{ maxHeight: "calc(70vh - 70px)" }}>
                {BOOKS.map((b) => (
                  <div key={b}>
                    <p style={{ fontFamily: "Jost, sans-serif", fontSize: 9, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.2em", color: "#A09080", marginBottom: 8 }}>
                      {b}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {(BOOK_CHAPTERS[b] ?? []).map((ch) => {
                        const isActive = b === book && ch === chapter;
                        return (
                          <button
                            key={ch}
                            onClick={() => { navigate(b, ch); setShowTOC(false); }}
                            className="px-4 py-2 rounded-full transition-all duration-200"
                            style={{
                              background: isActive ? "#B85A30" : "rgba(74,46,26,0.08)",
                              color: isActive ? "white" : "#5A4A32",
                              fontFamily: "Cormorant Garamond, Cormorant, Georgia, serif",
                              fontSize: 15, fontWeight: isActive ? 600 : 400,
                              border: isActive ? "none" : "1px solid rgba(74,46,26,0.14)",
                              boxShadow: isActive ? "0 2px 10px rgba(184,90,48,0.28)" : "none",
                            }}>
                            Ch {ch}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default BibleReader;
