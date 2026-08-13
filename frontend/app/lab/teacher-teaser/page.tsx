"use client";

import dynamic from "next/dynamic";
import { FormEvent, useMemo, useState } from "react";
import { TeacherTeaserDetails } from "@/components/teacher-teaser/TeacherTeaserDetails";
import {
  calculateTeacherTeaserCompatibility,
  calculateTeacherTeaserPersonal,
  type ExperimentalCompatibilityResponse,
  type ExperimentalPersonalMatrix
} from "@/lib/teacher-teaser";
import type { LanguageCode, MatrixPosition } from "@/lib/types";

const TeacherTeaserChart = dynamic(
  () =>
    import(
      "@/components/teacher-teaser/TeacherTeaserChart"
    ).then((module) => module.TeacherTeaserChart),
  {
    ssr: false,
    loading: () => (
      <div
        aria-hidden="true"
        className="aspect-square w-full border border-gold/20 bg-night/60"
      />
    )
  }
);

type LabTab = "personal" | "compatibility";
type CompatibilityView = "person_1" | "person_2" | "compatibility";

interface PersonalFormState {
  name: string;
  birthDate: string;
}

interface CompatibilityFormState {
  person1Name: string;
  person1BirthDate: string;
  person2Name: string;
  person2BirthDate: string;
}

const EMPTY_PERSONAL: PersonalFormState = { name: "", birthDate: "" };
const EMPTY_COMPATIBILITY: CompatibilityFormState = {
  person1Name: "",
  person1BirthDate: "",
  person2Name: "",
  person2BirthDate: ""
};

const COPY = {
  en: {
    title: "Teacher Teaser Preview",
    badge: "Experimental / Belum Diverifikasi Guru",
    intro:
      "A local inspection workspace for formulas supported by the supplied teaser material. This is not a complete Destiny Matrix and contains no interpretations or predictions.",
    personalTab: "Personal Matrix",
    compatibilityTab: "Compatibility Matrix",
    language: "Language",
    name: "Name or nickname",
    optional: "Optional",
    birthDate: "Birth date",
    person1Name: "Person 1 name",
    person1BirthDate: "Person 1 birth date",
    person2Name: "Person 2 name",
    person2BirthDate: "Person 2 birth date",
    calculate: "Calculate supported positions",
    calculateCompatibility: "Compare supported positions",
    clear: "Clear form",
    presetTaylor: "Taylor Swift",
    presetTravis: "Travis Kelce",
    presetPair: "Taylor Swift + Travis Kelce",
    presets: "Presets",
    required: "Complete the required birth date fields.",
    requiredNames: "Enter both names and birth dates.",
    loading: "Calculating supported positions…",
    empty:
      "Choose a preset or enter dates to populate the supported-position chart.",
    result: "Experimental result",
    person1: "Person 1",
    person2: "Person 2",
    compatibility: "Compatibility",
    unsupported: "Unsupported in this preview",
    unsupportedBody:
      "No values are generated for internal nodes, annual or monthly energy, age cycles, money or relationship outputs, or forecast charts.",
    warnings: "Methodology warnings",
    methodology: "teacher-teaser-v0.1",
    verification: "verified: false"
  },
  id: {
    title: "Pratinjau Teaser Guru",
    badge: "Eksperimental / Belum Diverifikasi Guru",
    intro:
      "Ruang inspeksi lokal untuk rumus yang didukung materi teaser yang diberikan. Ini bukan Destiny Matrix lengkap dan tidak berisi interpretasi atau prediksi.",
    personalTab: "Matriks Personal",
    compatibilityTab: "Matriks Kompatibilitas",
    language: "Bahasa",
    name: "Nama atau panggilan",
    optional: "Opsional",
    birthDate: "Tanggal lahir",
    person1Name: "Nama orang 1",
    person1BirthDate: "Tanggal lahir orang 1",
    person2Name: "Nama orang 2",
    person2BirthDate: "Tanggal lahir orang 2",
    calculate: "Hitung posisi yang didukung",
    calculateCompatibility: "Bandingkan posisi yang didukung",
    clear: "Kosongkan formulir",
    presetTaylor: "Taylor Swift",
    presetTravis: "Travis Kelce",
    presetPair: "Taylor Swift + Travis Kelce",
    presets: "Preset",
    required: "Lengkapi kolom tanggal lahir yang wajib.",
    requiredNames: "Masukkan kedua nama dan tanggal lahir.",
    loading: "Menghitung posisi yang didukung…",
    empty:
      "Pilih preset atau masukkan tanggal untuk mengisi bagan posisi yang didukung.",
    result: "Hasil eksperimental",
    person1: "Orang 1",
    person2: "Orang 2",
    compatibility: "Kompatibilitas",
    unsupported: "Belum didukung dalam pratinjau ini",
    unsupportedBody:
      "Tidak ada nilai untuk node internal, energi tahunan atau bulanan, siklus usia, keluaran uang atau relasi, maupun bagan prediksi.",
    warnings: "Peringatan metodologi",
    methodology: "teacher-teaser-v0.1",
    verification: "verified: false"
  }
};

const INPUT_CLASS =
  "mt-2 min-h-12 w-full border border-night/20 bg-white px-3 py-3 text-base text-night outline-none transition focus:border-plum focus:ring-2 focus:ring-gold";

export default function TeacherTeaserLabPage() {
  const [language, setLanguage] = useState<LanguageCode>("en");
  const [activeTab, setActiveTab] = useState<LabTab>("personal");
  const [personalForm, setPersonalForm] =
    useState<PersonalFormState>(EMPTY_PERSONAL);
  const [compatibilityForm, setCompatibilityForm] =
    useState<CompatibilityFormState>(EMPTY_COMPATIBILITY);
  const [personalResult, setPersonalResult] =
    useState<ExperimentalPersonalMatrix | null>(null);
  const [compatibilityResult, setCompatibilityResult] =
    useState<ExperimentalCompatibilityResponse | null>(null);
  const [compatibilityView, setCompatibilityView] =
    useState<CompatibilityView>("compatibility");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const copy = COPY[language];

  const displayedPositions = useMemo<MatrixPosition[]>(() => {
    if (activeTab === "personal") {
      return personalResult?.supported_positions ?? [];
    }
    if (!compatibilityResult) {
      return [];
    }
    if (compatibilityView === "person_1") {
      return compatibilityResult.person_1.supported_positions;
    }
    if (compatibilityView === "person_2") {
      return compatibilityResult.person_2.supported_positions;
    }
    return compatibilityResult.supported_compatibility_positions;
  }, [
    activeTab,
    compatibilityResult,
    compatibilityView,
    personalResult
  ]);

  const currentWarnings =
    activeTab === "personal"
      ? personalResult?.warnings
      : compatibilityResult?.warnings;

  const viewLabel =
    activeTab === "personal"
      ? personalResult?.name || copy.personalTab
      : compatibilityView === "person_1"
        ? compatibilityResult?.person_1.name || copy.person1
        : compatibilityView === "person_2"
          ? compatibilityResult?.person_2.name || copy.person2
          : copy.compatibility;

  function selectTab(tab: LabTab) {
    setActiveTab(tab);
    setError(null);
    setSelectedId(null);
  }

  async function submitPersonal(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!personalForm.birthDate) {
      setError(copy.required);
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const result = await calculateTeacherTeaserPersonal({
        birth_date: personalForm.birthDate,
        name: personalForm.name.trim() || undefined
      });
      setPersonalResult(result);
      setSelectedId("E");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : copy.required);
    } finally {
      setIsLoading(false);
    }
  }

  async function submitCompatibility(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const complete =
      compatibilityForm.person1Name.trim() &&
      compatibilityForm.person1BirthDate &&
      compatibilityForm.person2Name.trim() &&
      compatibilityForm.person2BirthDate;
    if (!complete) {
      setError(copy.requiredNames);
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const result = await calculateTeacherTeaserCompatibility({
        person_1: {
          name: compatibilityForm.person1Name.trim(),
          birth_date: compatibilityForm.person1BirthDate
        },
        person_2: {
          name: compatibilityForm.person2Name.trim(),
          birth_date: compatibilityForm.person2BirthDate
        }
      });
      setCompatibilityResult(result);
      setCompatibilityView("compatibility");
      setSelectedId("E");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : copy.requiredNames);
    } finally {
      setIsLoading(false);
    }
  }

  function chooseCompatibilityView(view: CompatibilityView) {
    setCompatibilityView(view);
    setSelectedId("E");
  }

  const detailMode =
    activeTab === "compatibility" && compatibilityView === "compatibility"
      ? "compatibility"
      : "personal";

  return (
    <main className="teacher-lab min-h-screen bg-[#12101d] px-4 py-6 text-cream sm:px-6 lg:px-8">
      <div className="mx-auto max-w-[1480px]">
        <header className="border-b border-gold/30 pb-6">
          <div className="flex flex-wrap items-start justify-between gap-5">
            <div className="max-w-4xl">
              <div className="inline-flex border border-gold/55 bg-gold/10 px-3 py-2 text-xs font-bold uppercase text-gold">
                {copy.badge}
              </div>
              <h1 className="mt-4 text-3xl font-bold text-cream sm:text-4xl">
                {copy.title}
              </h1>
              <p className="mt-3 max-w-3xl text-base leading-7 text-mist/80">
                {copy.intro}
              </p>
            </div>
            <div className="border border-cream/15 bg-night/80 p-3">
              <p className="text-xs font-bold uppercase text-cream/50">
                {copy.methodology}
              </p>
              <p className="mt-1 font-mono text-sm font-bold text-gold">
                {copy.verification}
              </p>
            </div>
          </div>
        </header>

        <div className="mt-6 flex flex-wrap items-center justify-between gap-4 border-b border-cream/15 pb-5">
          <div
            role="tablist"
            aria-label="Teacher teaser preview mode"
            className="inline-flex border border-cream/20 bg-night p-1"
          >
            {(["personal", "compatibility"] as const).map((tab) => (
              <button
                key={tab}
                id={`${tab}-tab`}
                type="button"
                role="tab"
                aria-selected={activeTab === tab}
                aria-controls={`${tab}-panel`}
                onClick={() => selectTab(tab)}
                className={`min-h-11 px-4 py-2 text-sm font-bold transition focus:outline-none focus:ring-2 focus:ring-gold ${
                  activeTab === tab
                    ? "bg-gold text-night"
                    : "text-cream/70 hover:bg-cream/10 hover:text-cream"
                }`}
              >
                {tab === "personal"
                  ? copy.personalTab
                  : copy.compatibilityTab}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <span className="text-sm font-semibold text-cream/65">
              {copy.language}
            </span>
            <div
              role="group"
              aria-label={copy.language}
              className="inline-flex border border-cream/20 bg-night p-1"
            >
              {(["en", "id"] as const).map((option) => (
                <button
                  key={option}
                  type="button"
                  aria-pressed={language === option}
                  onClick={() => setLanguage(option)}
                  className={`min-h-11 min-w-12 px-3 py-2 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-gold ${
                    language === option
                      ? "bg-cream text-night"
                      : "text-cream/70"
                  }`}
                >
                  {option.toUpperCase()}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-6 grid gap-6 xl:grid-cols-[360px_minmax(0,1fr)_390px] xl:items-start">
          <section
            id={`${activeTab}-panel`}
            role="tabpanel"
            aria-labelledby={`${activeTab}-tab`}
            className="border border-cream/15 bg-cream p-5 text-night xl:sticky xl:top-5"
          >
            {activeTab === "personal" ? (
              <form onSubmit={submitPersonal} className="space-y-5">
                <div>
                  <h2 className="text-xl font-bold">{copy.personalTab}</h2>
                  <p className="mt-1 text-sm text-night/60">{copy.presets}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() =>
                        setPersonalForm({
                          name: "Taylor Swift",
                          birthDate: "1989-12-13"
                        })
                      }
                      className="min-h-11 border border-plum/25 px-3 py-2 text-sm font-semibold hover:bg-plum/5 focus:outline-none focus:ring-2 focus:ring-plum"
                    >
                      {copy.presetTaylor}
                    </button>
                    <button
                      type="button"
                      onClick={() =>
                        setPersonalForm({
                          name: "Travis Kelce",
                          birthDate: "1989-10-05"
                        })
                      }
                      className="min-h-11 border border-plum/25 px-3 py-2 text-sm font-semibold hover:bg-plum/5 focus:outline-none focus:ring-2 focus:ring-plum"
                    >
                      {copy.presetTravis}
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setPersonalForm(EMPTY_PERSONAL);
                        setPersonalResult(null);
                        setSelectedId(null);
                      }}
                      className="min-h-11 border border-night/15 px-3 py-2 text-sm font-semibold text-night/65 hover:bg-night/5 focus:outline-none focus:ring-2 focus:ring-plum"
                    >
                      {copy.clear}
                    </button>
                  </div>
                </div>

                <label className="block">
                  <span className="text-sm font-bold">{copy.name}</span>
                  <span className="ml-2 text-xs text-night/50">
                    {copy.optional}
                  </span>
                  <input
                    value={personalForm.name}
                    onChange={(event) =>
                      setPersonalForm((current) => ({
                        ...current,
                        name: event.target.value
                      }))
                    }
                    className={INPUT_CLASS}
                    maxLength={80}
                    autoComplete="name"
                  />
                </label>
                <label className="block">
                  <span className="text-sm font-bold">{copy.birthDate}</span>
                  <input
                    type="date"
                    required
                    value={personalForm.birthDate}
                    onChange={(event) =>
                      setPersonalForm((current) => ({
                        ...current,
                        birthDate: event.target.value
                      }))
                    }
                    className={INPUT_CLASS}
                  />
                </label>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="min-h-12 w-full bg-night px-4 py-3 font-bold text-cream transition hover:bg-plum focus:outline-none focus:ring-4 focus:ring-gold disabled:cursor-wait disabled:opacity-55"
                >
                  {isLoading ? copy.loading : copy.calculate}
                </button>
              </form>
            ) : (
              <form onSubmit={submitCompatibility} className="space-y-5">
                <div>
                  <h2 className="text-xl font-bold">
                    {copy.compatibilityTab}
                  </h2>
                  <p className="mt-1 text-sm text-night/60">{copy.presets}</p>
                  <button
                    type="button"
                    onClick={() =>
                      setCompatibilityForm({
                        person1Name: "Taylor Swift",
                        person1BirthDate: "1989-12-13",
                        person2Name: "Travis Kelce",
                        person2BirthDate: "1989-10-05"
                      })
                    }
                    className="mt-3 min-h-11 border border-plum/25 px-3 py-2 text-sm font-semibold hover:bg-plum/5 focus:outline-none focus:ring-2 focus:ring-plum"
                  >
                    {copy.presetPair}
                  </button>
                </div>

                <label className="block">
                  <span className="text-sm font-bold">{copy.person1Name}</span>
                  <input
                    required
                    value={compatibilityForm.person1Name}
                    onChange={(event) =>
                      setCompatibilityForm((current) => ({
                        ...current,
                        person1Name: event.target.value
                      }))
                    }
                    className={INPUT_CLASS}
                    maxLength={80}
                  />
                </label>
                <label className="block">
                  <span className="text-sm font-bold">
                    {copy.person1BirthDate}
                  </span>
                  <input
                    type="date"
                    required
                    value={compatibilityForm.person1BirthDate}
                    onChange={(event) =>
                      setCompatibilityForm((current) => ({
                        ...current,
                        person1BirthDate: event.target.value
                      }))
                    }
                    className={INPUT_CLASS}
                  />
                </label>
                <label className="block">
                  <span className="text-sm font-bold">{copy.person2Name}</span>
                  <input
                    required
                    value={compatibilityForm.person2Name}
                    onChange={(event) =>
                      setCompatibilityForm((current) => ({
                        ...current,
                        person2Name: event.target.value
                      }))
                    }
                    className={INPUT_CLASS}
                    maxLength={80}
                  />
                </label>
                <label className="block">
                  <span className="text-sm font-bold">
                    {copy.person2BirthDate}
                  </span>
                  <input
                    type="date"
                    required
                    value={compatibilityForm.person2BirthDate}
                    onChange={(event) =>
                      setCompatibilityForm((current) => ({
                        ...current,
                        person2BirthDate: event.target.value
                      }))
                    }
                    className={INPUT_CLASS}
                  />
                </label>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="min-h-12 w-full bg-night px-4 py-3 font-bold text-cream transition hover:bg-plum focus:outline-none focus:ring-4 focus:ring-gold disabled:cursor-wait disabled:opacity-55"
                >
                  {isLoading ? copy.loading : copy.calculateCompatibility}
                </button>
              </form>
            )}

            {error ? (
              <p
                role="alert"
                className="mt-5 border border-red-700/40 bg-red-50 p-3 text-sm font-semibold text-red-900"
              >
                {error}
              </p>
            ) : null}
          </section>

          <section className="min-w-0">
            <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-xs font-bold uppercase text-gold">
                  {copy.result}
                </p>
                <h2 className="mt-1 text-xl font-bold text-cream">
                  {viewLabel}
                </h2>
              </div>
              {activeTab === "compatibility" && compatibilityResult ? (
                <div
                  role="group"
                  aria-label={copy.compatibilityTab}
                  className="inline-flex flex-wrap border border-cream/20 bg-night p-1"
                >
                  {(
                    [
                      ["person_1", copy.person1],
                      ["person_2", copy.person2],
                      ["compatibility", copy.compatibility]
                    ] as const
                  ).map(([view, label]) => (
                    <button
                      key={view}
                      type="button"
                      aria-pressed={compatibilityView === view}
                      onClick={() => chooseCompatibilityView(view)}
                      className={`min-h-11 px-3 py-2 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-gold ${
                        compatibilityView === view
                          ? "bg-gold text-night"
                          : "text-cream/70 hover:bg-cream/10"
                      }`}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              ) : null}
            </div>

            {displayedPositions.length === 0 ? (
              <p className="mb-4 border border-gold/20 bg-night/65 p-4 text-sm leading-6 text-mist/70">
                {copy.empty}
              </p>
            ) : null}

            <TeacherTeaserChart
              positions={displayedPositions}
              language={language}
              selectedId={selectedId}
              onSelect={setSelectedId}
              viewLabel={viewLabel}
            />
          </section>

          <aside className="space-y-5 xl:sticky xl:top-5">
            <TeacherTeaserDetails
              positions={displayedPositions}
              selectedId={selectedId}
              language={language}
              mode={detailMode}
            />

            <section className="border border-cream/15 bg-[#1d2936] p-5">
              <h2 className="text-base font-bold text-cream">
                {copy.unsupported}
              </h2>
              <p className="mt-2 text-sm leading-6 text-mist/70">
                {copy.unsupportedBody}
              </p>
            </section>

            {currentWarnings ? (
              <section className="border border-gold/25 bg-[#2b1a28] p-5">
                <h2 className="text-base font-bold text-gold">
                  {copy.warnings}
                </h2>
                <ul className="mt-3 space-y-2 text-sm leading-6 text-mist/75">
                  {currentWarnings.map((warning) => (
                    <li key={warning}>{warning}</li>
                  ))}
                </ul>
              </section>
            ) : null}
          </aside>
        </div>
      </div>
    </main>
  );
}
