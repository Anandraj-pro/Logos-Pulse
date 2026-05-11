"use client";

import React, { useState, useRef, forwardRef } from "react";
import HTMLFlipBook from "react-pageflip";
import { ChevronLeft, ChevronRight, BookOpen, Bookmark } from "lucide-react";

// ── Types ────────────────────────────────────────────────────────────────────
interface BibleVerse {
  number: number;
  text: string;
}

interface BiblePage {
  book: string;
  chapter: number;
  testament: "Old" | "New";
  verses: BibleVerse[];
  bgAccent: string;
}

// ── Sample Bible content ──────────────────────────────────────────────────────
const BIBLE_PAGES: BiblePage[] = [
  {
    book: "Genesis",
    chapter: 1,
    testament: "Old",
    bgAccent: "#C48A1C",
    verses: [
      { number: 1, text: "In the beginning God created the heavens and the earth." },
      { number: 2, text: "Now the earth was formless and empty, darkness was over the surface of the deep, and the Spirit of God was hovering over the waters." },
      { number: 3, text: "And God said, \"Let there be light,\" and there was light." },
      { number: 4, text: "God saw that the light was good, and he separated the light from the darkness." },
      { number: 5, text: "God called the light \"day,\" and the darkness he called \"night.\" And there was evening, and there was morning — the first day." },
      { number: 6, text: "And God said, \"Let there be a vault between the waters to separate water from water.\"" },
    ],
  },
  {
    book: "Psalm",
    chapter: 23,
    testament: "Old",
    bgAccent: "#2B5A3E",
    verses: [
      { number: 1, text: "The Lord is my shepherd, I lack nothing." },
      { number: 2, text: "He makes me lie down in green pastures, he leads me beside quiet waters," },
      { number: 3, text: "he refreshes my soul. He guides me along the right paths for his name's sake." },
      { number: 4, text: "Even though I walk through the darkest valley, I will fear no evil, for you are with me; your rod and your staff, they comfort me." },
      { number: 5, text: "You prepare a table before me in the presence of my enemies. You anoint my head with oil; my cup overflows." },
      { number: 6, text: "Surely your goodness and love will follow me all the days of my life, and I will dwell in the house of the Lord forever." },
    ],
  },
  {
    book: "Proverbs",
    chapter: 3,
    testament: "Old",
    bgAccent: "#B85A30",
    verses: [
      { number: 1, text: "My son, do not forget my teaching, but keep my commands in your heart," },
      { number: 2, text: "for they will prolong your life many years and bring you peace and prosperity." },
      { number: 3, text: "Let love and faithfulness never leave you; bind them around your neck, write them on the tablet of your heart." },
      { number: 5, text: "Trust in the Lord with all your heart and lean not on your own understanding;" },
      { number: 6, text: "in all your ways submit to him, and he will make your paths straight." },
      { number: 7, text: "Do not be wise in your own eyes; fear the Lord and shun evil." },
    ],
  },
  {
    book: "John",
    chapter: 3,
    testament: "New",
    bgAccent: "#1565C0",
    verses: [
      { number: 14, text: "Just as Moses lifted up the snake in the wilderness, so the Son of Man must be lifted up," },
      { number: 15, text: "that everyone who believes may have eternal life in him." },
      { number: 16, text: "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life." },
      { number: 17, text: "For God did not send his Son into the world to condemn the world, but to save the world through him." },
      { number: 18, text: "Whoever believes in him is not condemned, but whoever does not believe stands condemned already because they have not believed in the name of God's one and only Son." },
    ],
  },
  {
    book: "Romans",
    chapter: 8,
    testament: "New",
    bgAccent: "#7B1FA2",
    verses: [
      { number: 1, text: "Therefore, there is now no condemnation for those who are in Christ Jesus," },
      { number: 2, text: "because through Christ Jesus the law of the Spirit who gives life has set you free from the law of sin and death." },
      { number: 28, text: "And we know that in all things God works for the good of those who love him, who have been called according to his purpose." },
      { number: 37, text: "No, in all these things we are more than conquerors through him who loved us." },
      { number: 38, text: "For I am convinced that neither death nor life, neither angels nor demons, neither the present nor the future, nor any powers," },
      { number: 39, text: "neither height nor depth, nor anything else in all creation, will be able to separate us from the love of God that is in Christ Jesus our Lord." },
    ],
  },
  {
    book: "Philippians",
    chapter: 4,
    testament: "New",
    bgAccent: "#C48A1C",
    verses: [
      { number: 4, text: "Rejoice in the Lord always. I will say it again: Rejoice!" },
      { number: 6, text: "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God." },
      { number: 7, text: "And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus." },
      { number: 8, text: "Finally, brothers and sisters, whatever is true, whatever is noble, whatever is right, whatever is pure, whatever is lovely, whatever is admirable — if anything is excellent or praiseworthy — think about such things." },
      { number: 13, text: "I can do all this through him who gives me strength." },
    ],
  },
];

// ── Page components (forwarded refs required by react-pageflip) ───────────────
const CoverPage = forwardRef<HTMLDivElement>((_, ref) => (
  <div
    ref={ref}
    className="relative overflow-hidden select-none"
    style={{
      width: "100%",
      height: "100%",
      background: "linear-gradient(160deg, #1A1208 0%, #2A1A08 40%, #3A2A10 100%)",
    }}
  >
    {/* Grain texture */}
    <div
      className="absolute inset-0 opacity-20"
      style={{
        backgroundImage:
          "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")",
      }}
    />

    {/* Gold orb */}
    <div
      className="absolute top-0 right-0 w-64 h-64 rounded-full opacity-20"
      style={{
        background: "radial-gradient(circle, rgba(196,138,28,0.8) 0%, transparent 70%)",
        transform: "translate(30%, -30%)",
      }}
    />

    {/* Cross ornament */}
    <div className="absolute inset-0 flex items-center justify-center">
      <div className="flex flex-col items-center gap-6">
        <div className="relative">
          <div
            className="w-1 h-20 rounded-full mx-auto"
            style={{ background: "linear-gradient(180deg, #C48A1C, #DFA830)" }}
          />
          <div
            className="absolute top-6 left-1/2 -translate-x-1/2 h-1 w-12 rounded-full"
            style={{ background: "linear-gradient(90deg, #C48A1C, #DFA830)" }}
          />
        </div>

        <div className="text-center px-8">
          <p className="text-xs tracking-[0.35em] uppercase mb-3" style={{ color: "rgba(196,138,28,0.7)", fontFamily: "Jost, sans-serif" }}>
            The Holy
          </p>
          <h1
            className="text-4xl font-light text-white leading-none"
            style={{ fontFamily: "Cormorant, Georgia, serif", letterSpacing: "0.08em" }}
          >
            Bible
          </h1>
          <div className="mt-4 w-16 h-px mx-auto" style={{ background: "linear-gradient(90deg, transparent, #C48A1C, transparent)" }} />
          <p className="mt-4 text-xs tracking-widest uppercase" style={{ color: "rgba(240,228,210,0.4)", fontFamily: "Jost, sans-serif" }}>
            New International Version
          </p>
        </div>

        <div className="flex gap-2 items-center">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="w-1 h-1 rounded-full" style={{ background: "#C48A1C", opacity: 0.4 + i * 0.1 }} />
          ))}
        </div>
      </div>
    </div>

    {/* Bottom text */}
    <div className="absolute bottom-6 inset-x-0 text-center">
      <p className="text-xs tracking-[0.3em] uppercase" style={{ color: "rgba(196,138,28,0.5)", fontFamily: "Jost, sans-serif" }}>
        Logos Pulse · Sanctuary
      </p>
    </div>
  </div>
));
CoverPage.displayName = "CoverPage";

const TextPage = forwardRef<HTMLDivElement, { page: BiblePage; isLeft: boolean }>(
  ({ page, isLeft }, ref) => (
    <div
      ref={ref}
      className="relative overflow-hidden select-none"
      style={{
        width: "100%",
        height: "100%",
        background: isLeft
          ? "linear-gradient(to right, #F9F5EF, #F3EFE7)"
          : "linear-gradient(to left, #F9F5EF, #F3EFE7)",
      }}
    >
      {/* Subtle page lines */}
      {[...Array(18)].map((_, i) => (
        <div
          key={i}
          className="absolute left-8 right-8"
          style={{
            top: `${72 + i * 22}px`,
            height: "1px",
            background: "rgba(26,18,8,0.04)",
          }}
        />
      ))}

      {/* Gold accent top bar */}
      <div
        className="absolute top-0 inset-x-0 h-1"
        style={{ background: `linear-gradient(90deg, transparent, ${page.bgAccent}, transparent)`, opacity: 0.6 }}
      />

      {/* Content */}
      <div className="relative z-10 flex flex-col h-full px-8 pt-8 pb-6">
        {/* Header */}
        <div className="flex items-baseline justify-between mb-5 pb-3 border-b border-black/5">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.2em] mb-0.5" style={{ color: page.bgAccent, fontFamily: "Jost, sans-serif" }}>
              {page.testament} Testament
            </p>
            <h2 className="text-xl font-light leading-none" style={{ color: "#1A1208", fontFamily: "Cormorant, Georgia, serif", fontWeight: 600 }}>
              {page.book}
            </h2>
          </div>
          <div
            className="flex items-center justify-center w-9 h-9 rounded-full text-sm font-bold"
            style={{
              background: `${page.bgAccent}18`,
              color: page.bgAccent,
              fontFamily: "Jost, sans-serif",
              border: `1px solid ${page.bgAccent}30`,
            }}
          >
            {page.chapter}
          </div>
        </div>

        {/* Chapter label */}
        <p className="text-[9px] font-700 uppercase tracking-[0.25em] mb-4" style={{ color: "#A09080", fontFamily: "Jost, sans-serif" }}>
          Chapter {page.chapter}
        </p>

        {/* Verses */}
        <div className="flex-1 overflow-hidden space-y-3">
          {page.verses.map((verse) => (
            <div key={verse.number} className="flex gap-2.5">
              <span
                className="flex-shrink-0 text-[9px] font-bold mt-1 w-4 text-right"
                style={{ color: page.bgAccent, fontFamily: "Jost, sans-serif", opacity: 0.8 }}
              >
                {verse.number}
              </span>
              <p
                className="text-sm leading-relaxed flex-1"
                style={{
                  color: "#1A1208",
                  fontFamily: "Cormorant, Georgia, serif",
                  fontSize: "13.5px",
                  lineHeight: "1.75",
                }}
              >
                {verse.text}
              </p>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-auto pt-3 flex items-center justify-between border-t border-black/5">
          <p className="text-[9px] uppercase tracking-widest" style={{ color: "#A09080", fontFamily: "Jost, sans-serif" }}>
            {page.book} {page.chapter}
          </p>
          <div className="flex gap-1">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="w-1 h-1 rounded-full" style={{ background: page.bgAccent, opacity: 0.3 }} />
            ))}
          </div>
        </div>
      </div>

      {/* Page shadow edge */}
      <div
        className="absolute inset-y-0"
        style={{
          [isLeft ? "right" : "left"]: 0,
          width: "20px",
          background: isLeft
            ? "linear-gradient(to left, rgba(26,18,8,0.04), transparent)"
            : "linear-gradient(to right, rgba(26,18,8,0.04), transparent)",
        }}
      />
    </div>
  )
);
TextPage.displayName = "TextPage";

const BackCover = forwardRef<HTMLDivElement>((_, ref) => (
  <div
    ref={ref}
    className="relative overflow-hidden select-none"
    style={{
      width: "100%",
      height: "100%",
      background: "linear-gradient(160deg, #1A1208 0%, #2A1A08 40%, #3A2A10 100%)",
    }}
  >
    <div className="absolute inset-0 flex items-center justify-center">
      <div className="text-center px-10">
        <div
          className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4"
          style={{ background: "rgba(196,138,28,0.15)", border: "1px solid rgba(196,138,28,0.3)" }}
        >
          <BookOpen size={20} color="#C48A1C" />
        </div>
        <p
          className="text-sm leading-relaxed mb-6 italic"
          style={{ color: "rgba(240,228,210,0.6)", fontFamily: "Cormorant, Georgia, serif", fontSize: "15px" }}
        >
          &ldquo;Your word is a lamp to my feet and a light to my path.&rdquo;
        </p>
        <p className="text-xs" style={{ color: "rgba(196,138,28,0.6)", fontFamily: "Jost, sans-serif" }}>
          Psalm 119:105
        </p>
      </div>
    </div>
  </div>
));
BackCover.displayName = "BackCover";

// ── Main component ────────────────────────────────────────────────────────────
export function BibleBookSlider() {
  const bookRef = useRef<HTMLElement>(null);
  const [currentPage, setCurrentPage] = useState(0);
  const totalPages = BIBLE_PAGES.length + 2; // cover + content + back

  const goNext = () => (bookRef.current as any)?.pageFlip()?.flipNext();
  const goPrev = () => (bookRef.current as any)?.pageFlip()?.flipPrev();

  return (
    <div className="flex flex-col items-center gap-6">
      {/* Book */}
      <div className="relative">
        {/* Book shadow */}
        <div
          className="absolute -bottom-4 left-4 right-4 h-8 rounded-full blur-xl opacity-30"
          style={{ background: "#1A1208" }}
        />

        <HTMLFlipBook
          ref={bookRef as any}
          width={340}
          height={480}
          maxShadowOpacity={0.4}
          drawShadow={true}
          showCover={true}
          size="fixed"
          onFlip={(e: any) => setCurrentPage(e.data)}
          className="rounded-sm overflow-hidden"
          style={{}}
          startPage={0}
          minWidth={340}
          maxWidth={340}
          minHeight={480}
          maxHeight={480}
          flippingTime={700}
          usePortrait={false}
          startZIndex={0}
          autoSize={false}
          clickEventForward={true}
          useMouseEvents={true}
          swipeDistance={30}
          showPageCorners={true}
          disableFlipByClick={false}
          mobileScrollSupport={true}
        >
          {/* Front cover */}
          <CoverPage />

          {/* Bible pages */}
          {BIBLE_PAGES.map((page, i) => (
            <TextPage key={i} page={page} isLeft={i % 2 === 0} />
          ))}

          {/* Back cover */}
          <BackCover />
        </HTMLFlipBook>
      </div>

      {/* Controls */}
      <div className="flex items-center gap-4">
        <button
          onClick={goPrev}
          disabled={currentPage === 0}
          className="flex items-center justify-center w-9 h-9 rounded-full transition-all duration-200 disabled:opacity-30"
          style={{
            background: "rgba(184,90,48,0.08)",
            border: "1px solid rgba(184,90,48,0.20)",
            color: "#B85A30",
          }}
        >
          <ChevronLeft size={18} />
        </button>

        {/* Page indicators */}
        <div className="flex gap-1.5 items-center">
          {[...Array(totalPages)].map((_, i) => (
            <div
              key={i}
              className="rounded-full transition-all duration-300"
              style={{
                width: i === currentPage ? "20px" : "5px",
                height: "5px",
                background: i === currentPage ? "#B85A30" : "rgba(26,18,8,0.15)",
              }}
            />
          ))}
        </div>

        <button
          onClick={goNext}
          disabled={currentPage === totalPages - 1}
          className="flex items-center justify-center w-9 h-9 rounded-full transition-all duration-200 disabled:opacity-30"
          style={{
            background: "rgba(184,90,48,0.08)",
            border: "1px solid rgba(184,90,48,0.20)",
            color: "#B85A30",
          }}
        >
          <ChevronRight size={18} />
        </button>
      </div>

      {/* Page label */}
      <p className="text-xs uppercase tracking-widest" style={{ color: "#A09080", fontFamily: "Jost, sans-serif" }}>
        {currentPage === 0
          ? "Cover"
          : currentPage > BIBLE_PAGES.length
          ? "End"
          : `${BIBLE_PAGES[currentPage - 1]?.book} ${BIBLE_PAGES[currentPage - 1]?.chapter}`}
      </p>
    </div>
  );
}

export default BibleBookSlider;
