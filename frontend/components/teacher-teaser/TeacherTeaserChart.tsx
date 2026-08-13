"use client";

import type { KeyboardEvent } from "react";
import type { MatrixPosition } from "@/lib/types";
import type {
  TeacherTeaserPositionId
} from "@/lib/teacher-teaser";
import {
  POSITION_CONFIG,
  UNSUPPORTED_NODE_CONFIG
} from "./config";

interface TeacherTeaserChartProps {
  positions: MatrixPosition[];
  language: "en" | "id";
  selectedId: string | null;
  onSelect: (positionId: string) => void;
  viewLabel: string;
}

const COPY = {
  en: {
    chartTitle: "Teacher teaser supported-position chart",
    chartDescription:
      "An experimental matrix showing eleven supported positions. Small outlined circles are unavailable future positions and contain no calculated values.",
    position: "Position",
    displayName: "Display name",
    value: "Value",
    verification: "Verification",
    unverified: "Unverified",
    unsupported: "Not available",
    select: "Select",
    noValue: "No value"
  },
  id: {
    chartTitle: "Bagan posisi yang didukung teaser guru",
    chartDescription:
      "Matriks eksperimental dengan sebelas posisi yang didukung. Lingkaran kecil hanya penanda posisi masa depan, belum tersedia, dan tidak memiliki nilai.",
    position: "Posisi",
    displayName: "Nama tampilan",
    value: "Nilai",
    verification: "Verifikasi",
    unverified: "Belum diverifikasi",
    unsupported: "Belum tersedia",
    select: "Pilih",
    noValue: "Tanpa nilai"
  }
};

export function TeacherTeaserChart({
  positions,
  language,
  selectedId,
  onSelect,
  viewLabel
}: TeacherTeaserChartProps) {
  const copy = COPY[language];
  const positionsById = new Map(
    positions.map((position) => [position.id, position])
  );

  function handleKeyDown(
    event: KeyboardEvent<SVGGElement>,
    positionId: string
  ) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onSelect(positionId);
    }
  }

  return (
    <div className="min-w-0 max-w-full overflow-hidden space-y-5">
      <figure className="teacher-chart overflow-hidden border border-gold/25 bg-night/70 p-3 sm:p-5">
        <svg
          viewBox="0 0 800 800"
          role="img"
          aria-labelledby="teacher-chart-title teacher-chart-description"
          className="aspect-square w-full"
        >
          <title id="teacher-chart-title" suppressHydrationWarning>
            {`${copy.chartTitle}: ${viewLabel}`}
          </title>
          <desc id="teacher-chart-description" suppressHydrationWarning>
            {copy.chartDescription}
          </desc>

          <circle
            cx="400"
            cy="400"
            r="300"
            fill="rgba(255,247,232,0.025)"
            stroke="rgba(255,247,232,0.12)"
            strokeWidth="2"
          />
          <path
            d="M100 400 L205 205 L400 100 L595 205 L700 400 L595 595 L400 700 L205 595 Z"
            fill="rgba(217,181,109,0.035)"
            stroke="#d9b56d"
            strokeOpacity="0.78"
            strokeWidth="3"
          />
          <path
            d="M100 400 H700 M400 100 V700"
            stroke="#d9b56d"
            strokeOpacity="0.48"
            strokeWidth="3"
          />
          <path
            d="M205 205 L595 595 M595 205 L205 595"
            stroke="#d9b56d"
            strokeDasharray="8 10"
            strokeOpacity="0.25"
            strokeWidth="2"
          />
          <text
            x="150"
            y="388"
            className="fill-gold text-[18px] font-semibold"
          >
            {language === "en" ? "EARTH" : "BUMI"}
          </text>
          <text
            x="414"
            y="156"
            className="fill-gold text-[18px] font-semibold"
            transform="rotate(90 414 156)"
          >
            {language === "en" ? "SKY" : "LANGIT"}
          </text>

          {UNSUPPORTED_NODE_CONFIG.map((node) => {
            const isSelected = selectedId === node.id;
            return (
              <g
                key={node.id}
                role="button"
                tabIndex={0}
                aria-label={`${copy.unsupported}: ${copy.noValue}`}
                aria-pressed={isSelected}
                className="teacher-node cursor-pointer outline-none"
                onClick={() => onSelect(node.id)}
                onKeyDown={(event) => handleKeyDown(event, node.id)}
              >
                <circle
                  className="teacher-node-focus"
                  cx={node.x}
                  cy={node.y}
                  r="25"
                  fill="rgba(255,247,232,0.025)"
                  stroke={isSelected ? "#fff7e8" : "rgba(255,247,232,0.24)"}
                  strokeDasharray="5 5"
                  strokeWidth={isSelected ? 4 : 2}
                />
                <text
                  x={node.x}
                  y={node.y + 5}
                  textAnchor="middle"
                  className="pointer-events-none fill-cream/45 text-[18px]"
                >
                  ?
                </text>
              </g>
            );
          })}

          {POSITION_CONFIG.map((config) => {
            const position = positionsById.get(config.id);
            const isSelected = selectedId === config.id;
            const available = Boolean(position);
            return (
              <g
                key={config.id}
                role={available ? "button" : undefined}
                tabIndex={available ? 0 : undefined}
                aria-label={
                  available
                    ? `${config.id}, ${config.label[language]}, ${copy.value} ${position?.value}, ${copy.unverified}`
                    : undefined
                }
                aria-pressed={available ? isSelected : undefined}
                className={
                  available
                    ? "teacher-node cursor-pointer outline-none"
                    : "opacity-35"
                }
                onClick={available ? () => onSelect(config.id) : undefined}
                onKeyDown={
                  available
                    ? (event) => handleKeyDown(event, config.id)
                    : undefined
                }
              >
                <circle
                  className="teacher-node-focus"
                  cx={config.x}
                  cy={config.y}
                  r={config.radius}
                  fill={available ? config.color : "rgba(255,247,232,0.05)"}
                  fillOpacity={available ? 0.98 : 1}
                  stroke={isSelected ? "#ffffff" : "#d9b56d"}
                  strokeWidth={isSelected ? 6 : 3}
                />
                <text
                  x={config.x}
                  y={config.y - (available ? 10 : 2)}
                  textAnchor="middle"
                  className="pointer-events-none fill-night text-[18px] font-bold"
                >
                  {config.chartLabel}
                </text>
                {available ? (
                  <text
                    x={config.x}
                    y={config.y + 24}
                    textAnchor="middle"
                    className="pointer-events-none fill-night text-[30px] font-bold"
                  >
                    {position?.value}
                  </text>
                ) : null}
              </g>
            );
          })}
        </svg>
        <figcaption className="border-t border-cream/10 px-2 pt-4 text-sm leading-6 text-mist/75">
          {copy.chartDescription}
        </figcaption>
      </figure>

      <div className="w-full max-w-full overflow-x-auto border border-cream/15 bg-night/55">
        <table className="w-full min-w-[580px] border-collapse text-left text-sm">
          <caption className="sr-only">{copy.chartDescription}</caption>
          <thead className="border-b border-gold/25 text-cream/65">
            <tr>
              <th className="px-4 py-3 font-semibold">{copy.position}</th>
              <th className="px-4 py-3 font-semibold">{copy.displayName}</th>
              <th className="px-4 py-3 font-semibold">{copy.value}</th>
              <th className="px-4 py-3 font-semibold">{copy.verification}</th>
              <th className="px-4 py-3 text-right font-semibold">
                <span className="sr-only">{copy.select}</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {POSITION_CONFIG.map((config) => {
              const position = positionsById.get(config.id);
              return (
                <tr
                  key={config.id}
                  className="border-b border-cream/10 last:border-0"
                >
                  <td className="px-4 py-3 font-mono text-gold">{config.id}</td>
                  <td className="px-4 py-3 text-cream">
                    {config.label[language]}
                  </td>
                  <td className="px-4 py-3 text-lg font-bold text-cream">
                    {position?.value ?? "—"}
                  </td>
                  <td className="px-4 py-3 text-cream/65">
                    {position ? copy.unverified : copy.noValue}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button
                      type="button"
                      disabled={!position}
                      onClick={() => onSelect(config.id)}
                      className="min-h-11 border border-gold/35 px-3 py-2 font-semibold text-gold transition hover:bg-gold/10 focus:outline-none focus:ring-2 focus:ring-gold disabled:cursor-not-allowed disabled:opacity-35"
                    >
                      {copy.select}
                    </button>
                  </td>
                </tr>
              );
            })}
            {UNSUPPORTED_NODE_CONFIG.map((node) => (
              <tr
                key={node.id}
                className="border-b border-cream/10 text-cream/45 last:border-0"
              >
                <td className="px-4 py-3 font-mono">{node.id}</td>
                <td className="px-4 py-3">{copy.unsupported}</td>
                <td className="px-4 py-3" aria-label={copy.noValue}>
                  —
                </td>
                <td className="px-4 py-3">{copy.unsupported}</td>
                <td className="px-4 py-3 text-right">
                  <button
                    type="button"
                    onClick={() => onSelect(node.id)}
                    className="min-h-11 border border-cream/20 px-3 py-2 font-semibold text-cream/65 transition hover:bg-cream/5 focus:outline-none focus:ring-2 focus:ring-gold"
                  >
                    {copy.select}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
