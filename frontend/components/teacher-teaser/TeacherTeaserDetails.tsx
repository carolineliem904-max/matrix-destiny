import type { MatrixPosition } from "@/lib/types";
import type {
  TeacherTeaserPositionId
} from "@/lib/teacher-teaser";
import {
  POSITION_CONFIG_BY_ID,
  UNSUPPORTED_NODE_CONFIG
} from "./config";

interface TeacherTeaserDetailsProps {
  positions: MatrixPosition[];
  selectedId: string | null;
  language: "en" | "id";
  mode: "personal" | "compatibility";
}

const COPY = {
  en: {
    prompt: "Select a supported node to inspect its evidence and trace.",
    unavailable: "Not available",
    unavailableBody:
      "No formula or calculated value is available for this future position.",
    positionId: "Position ID",
    value: "Value",
    formula: "Formula",
    inputValues: "Input values",
    trace: "Calculation Trace",
    evidence: "Evidence status",
    verification: "Verification",
    unverified: "Unverified",
    explicitlyStated: "Explicitly stated in supplied teaser material",
    reconstructed: "Reconstructed from teacher teaser examples",
    inferred: "Inferred; not confidently visible in the supplied source"
  },
  id: {
    prompt: "Pilih node yang didukung untuk memeriksa bukti dan jejaknya.",
    unavailable: "Belum Tersedia",
    unavailableBody:
      "Belum ada rumus atau nilai perhitungan untuk posisi masa depan ini.",
    positionId: "ID Posisi",
    value: "Nilai",
    formula: "Rumus",
    inputValues: "Nilai masukan",
    trace: "Jejak Perhitungan",
    evidence: "Status bukti",
    verification: "Verifikasi",
    unverified: "Belum diverifikasi",
    explicitlyStated: "Disebutkan langsung dalam materi teaser yang diberikan",
    reconstructed: "Direkonstruksi dari contoh teaser guru",
    inferred: "Disimpulkan; tidak terbaca dengan yakin pada sumber"
  }
};

export function TeacherTeaserDetails({
  positions,
  selectedId,
  language,
  mode
}: TeacherTeaserDetailsProps) {
  const copy = COPY[language];

  if (!selectedId) {
    return (
      <section
        aria-live="polite"
        className="border border-gold/30 bg-cream p-5 text-night"
      >
        <p className="text-base leading-7">{copy.prompt}</p>
      </section>
    );
  }

  const unsupported = UNSUPPORTED_NODE_CONFIG.some(
    (node) => node.id === selectedId
  );
  if (unsupported) {
    return (
      <section
        aria-live="polite"
        className="border border-cream/20 bg-cream p-5 text-night"
      >
        <p className="text-xs font-bold uppercase text-plum/60">
          {selectedId}
        </p>
        <h2 className="mt-2 text-xl font-bold">{copy.unavailable}</h2>
        <p className="mt-3 leading-7 text-night/70">{copy.unavailableBody}</p>
      </section>
    );
  }

  const position = positions.find((item) => item.id === selectedId);
  const config =
    POSITION_CONFIG_BY_ID[selectedId as TeacherTeaserPositionId];

  if (!position || !config) {
    return (
      <section
        aria-live="polite"
        className="border border-gold/30 bg-cream p-5 text-night"
      >
        <p className="text-base leading-7">{copy.prompt}</p>
      </section>
    );
  }

  const positionsById = new Map(
    positions.map((item) => [item.id, item])
  );
  const inputLines =
    mode === "personal" && selectedId === "E"
      ? [
          positionsById.get("earth_line")?.calculation_trace[0],
          positionsById.get("sky_line")?.calculation_trace[0],
          position.calculation_trace[0]
        ].filter((line): line is string => Boolean(line))
      : position.calculation_trace.slice(0, 1);

  const evidence =
    mode === "compatibility" &&
    (selectedId === "earth_line" || selectedId === "sky_line")
      ? copy.inferred
      : config.evidence === "explicitly_stated"
        ? copy.explicitlyStated
        : copy.reconstructed;

  return (
    <section
      aria-live="polite"
      className="border border-gold/30 bg-cream p-5 text-night"
    >
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="font-mono text-sm font-bold text-plum/65">
            {copy.positionId}: {position.id}
          </p>
          <h2 className="mt-2 text-2xl font-bold">
            {config.label[language]}
          </h2>
        </div>
        <div className="min-w-20 border border-gold/50 bg-white px-4 py-3 text-center">
          <p className="text-xs font-bold uppercase text-night/55">
            {copy.value}
          </p>
          <p className="text-3xl font-bold text-plum">{position.value}</p>
        </div>
      </div>

      <dl className="mt-6 grid gap-5 sm:grid-cols-2">
        <div>
          <dt className="text-xs font-bold uppercase text-night/50">
            {copy.formula}
          </dt>
          <dd className="mt-2 font-mono text-sm font-semibold">
            {mode === "compatibility"
              ? `normalize(person_1[${position.id}] + person_2[${position.id}])`
              : config.formula}
          </dd>
        </div>
        <div>
          <dt className="text-xs font-bold uppercase text-night/50">
            {copy.verification}
          </dt>
          <dd className="mt-2 font-semibold text-red-800">
            {copy.unverified}
          </dd>
        </div>
        <div className="sm:col-span-2">
          <dt className="text-xs font-bold uppercase text-night/50">
            {copy.inputValues}
          </dt>
          <dd className="mt-2 space-y-1 font-mono text-sm">
            {inputLines.map((line) => (
              <p key={line}>{line}</p>
            ))}
          </dd>
        </div>
        <div className="sm:col-span-2">
          <dt className="text-xs font-bold uppercase text-night/50">
            {copy.trace}
          </dt>
          <dd className="mt-2">
            <ol className="space-y-2 border-l-2 border-gold/55 pl-4 font-mono text-sm">
              {position.calculation_trace.map((line, index) => (
                <li key={`${index}-${line}`}>{line}</li>
              ))}
            </ol>
          </dd>
        </div>
        <div className="sm:col-span-2">
          <dt className="text-xs font-bold uppercase text-night/50">
            {copy.evidence}
          </dt>
          <dd className="mt-2 font-semibold">{evidence}</dd>
        </div>
      </dl>
    </section>
  );
}
