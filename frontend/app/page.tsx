"use client";

import { useState } from "react";
import { BirthDateForm } from "@/components/BirthDateForm";
import { Disclaimer } from "@/components/Disclaimer";
import { ReadingSection } from "@/components/ReadingSection";
import { calculateMatrix } from "@/lib/api";
import type { LanguageCode, MatrixRequest, ReadingResponse } from "@/lib/types";

const COPY = {
  en: {
    eyebrow: "Bilingual Destiny Matrix MVP",
    title: "A calm, traceable matrix reading for reflection.",
    body: "Enter a birth date to generate a deterministic placeholder chart. The calculation engine is separate from interpretations, and every unverified position is clearly marked until the final methodology is supplied.",
    disclaimer:
      "For reflection, education, and entertainment only. This app does not present spiritual interpretations as scientific fact or guarantee future outcomes.",
    error: "Something went wrong."
  },
  id: {
    eyebrow: "MVP Destiny Matrix bilingual",
    title: "Bacaan matrix yang tenang, terlacak, dan reflektif.",
    body: "Masukkan tanggal lahir untuk membuat bagan placeholder deterministik. Mesin kalkulasi terpisah dari interpretasi, dan setiap posisi yang belum terverifikasi ditandai jelas sampai metodologi final diberikan.",
    disclaimer:
      "Hanya untuk refleksi, edukasi, dan hiburan. Aplikasi ini tidak menyatakan interpretasi spiritual sebagai fakta ilmiah atau menjamin hasil masa depan.",
    error: "Terjadi kesalahan."
  }
};

export default function Home() {
  const [language, setLanguage] = useState<LanguageCode>("en");
  const [reading, setReading] = useState<ReadingResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const copy = COPY[language];

  async function handleSubmit(payload: MatrixRequest) {
    setIsLoading(true);
    setError(null);
    try {
      const result = await calculateMatrix(payload);
      setReading(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : copy.error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto grid max-w-6xl gap-8 lg:grid-cols-[0.95fr_1.05fr] lg:items-start">
        <section className="space-y-6 pt-4 lg:sticky lg:top-8">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.18em] text-gold">
              {copy.eyebrow}
            </p>
            <h1 className="mt-4 max-w-3xl text-4xl font-bold leading-tight text-cream sm:text-5xl">
              {copy.title}
            </h1>
            <p className="mt-5 max-w-2xl text-lg leading-8 text-mist">
              {copy.body}
            </p>
          </div>
          <Disclaimer text={copy.disclaimer} />
          <BirthDateForm
            language={language}
            isLoading={isLoading}
            onLanguageChange={setLanguage}
            onSubmit={handleSubmit}
          />
          {error ? (
            <p role="alert" className="rounded-lg border border-red-300/50 bg-red-950/40 p-4 text-sm text-red-100">
              {error}
            </p>
          ) : null}
        </section>

        <section>
          {reading ? (
            <ReadingSection reading={reading} />
          ) : (
            <div className="rounded-lg border border-cream/15 bg-night/45 p-6 text-cream/78 shadow-glow">
              <div className="aspect-square rounded-lg border border-gold/25 bg-cream/5" />
              <p className="mt-5 text-base leading-7">
                The chart will appear here after calculation, including raw traces and draft interpretation records.
              </p>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
