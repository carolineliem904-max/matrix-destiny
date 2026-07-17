"use client";

import { FormEvent, useState } from "react";
import type { LanguageCode, MatrixRequest } from "@/lib/types";
import { LanguageSwitcher } from "./LanguageSwitcher";

interface BirthDateFormProps {
  language: LanguageCode;
  isLoading: boolean;
  onLanguageChange: (language: LanguageCode) => void;
  onSubmit: (payload: MatrixRequest) => void;
}

const COPY = {
  en: {
    name: "Name or nickname",
    birthDate: "Date of birth",
    focus: "Reading focus",
    optional: "Optional",
    submit: "Calculate Matrix",
    required: "Please enter your date of birth."
  },
  id: {
    name: "Nama atau panggilan",
    birthDate: "Tanggal lahir",
    focus: "Fokus bacaan",
    optional: "Opsional",
    submit: "Hitung Matrix",
    required: "Masukkan tanggal lahir."
  }
};

export function BirthDateForm({
  language,
  isLoading,
  onLanguageChange,
  onSubmit
}: BirthDateFormProps) {
  const [name, setName] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [focus, setFocus] = useState("");
  const [error, setError] = useState<string | null>(null);
  const copy = COPY[language];

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!birthDate) {
      setError(copy.required);
      return;
    }
    setError(null);
    onSubmit({
      birth_date: birthDate,
      language,
      name,
      focus
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 rounded-lg border border-cream/15 bg-cream/95 p-5 text-night shadow-glow">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-plum/70">
            Matrix Destiny
          </p>
          <h2 className="mt-1 text-2xl font-bold">MVP Reading</h2>
        </div>
        <LanguageSwitcher value={language} onChange={onLanguageChange} />
      </div>

      <label className="block">
        <span className="text-sm font-semibold">{copy.name}</span>
        <span className="ml-2 text-xs text-night/55">{copy.optional}</span>
        <input
          value={name}
          onChange={(event) => setName(event.target.value)}
          className="mt-2 w-full rounded-md border border-night/15 bg-white px-4 py-3 text-base outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/20"
          maxLength={80}
          autoComplete="name"
        />
      </label>

      <label className="block">
        <span className="text-sm font-semibold">{copy.birthDate}</span>
        <input
          type="date"
          value={birthDate}
          onChange={(event) => setBirthDate(event.target.value)}
          className="mt-2 w-full rounded-md border border-night/15 bg-white px-4 py-3 text-base outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/20"
          required
        />
      </label>

      <label className="block">
        <span className="text-sm font-semibold">{copy.focus}</span>
        <span className="ml-2 text-xs text-night/55">{copy.optional}</span>
        <input
          value={focus}
          onChange={(event) => setFocus(event.target.value)}
          className="mt-2 w-full rounded-md border border-night/15 bg-white px-4 py-3 text-base outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/20"
          maxLength={180}
        />
      </label>

      {error ? <p className="text-sm font-semibold text-red-700">{error}</p> : null}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full rounded-md bg-night px-5 py-3 text-base font-bold text-cream transition hover:bg-plum focus:outline-none focus:ring-4 focus:ring-gold/40 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isLoading ? "..." : copy.submit}
      </button>
    </form>
  );
}
