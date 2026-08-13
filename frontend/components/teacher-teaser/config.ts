import type {
  TeacherTeaserPositionId
} from "@/lib/teacher-teaser";
import type { LanguageCode } from "@/lib/types";

export type EvidenceStatus =
  | "explicitly_stated"
  | "reconstructed"
  | "inferred";

interface PositionDisplayConfig {
  id: TeacherTeaserPositionId;
  chartLabel: string;
  x: number;
  y: number;
  label: Record<LanguageCode, string>;
  formula: string;
  evidence: EvidenceStatus;
  color: string;
  radius: number;
}

export const POSITION_CONFIG: PositionDisplayConfig[] = [
  {
    id: "A",
    chartLabel: "A",
    x: 100,
    y: 400,
    label: { en: "Birth Day / Left", id: "Hari Lahir / Kiri" },
    formula: "normalize(day)",
    evidence: "explicitly_stated",
    color: "#e76f51",
    radius: 54
  },
  {
    id: "B",
    chartLabel: "B",
    x: 400,
    y: 100,
    label: { en: "Birth Month / Top", id: "Bulan Lahir / Atas" },
    formula: "normalize(month)",
    evidence: "explicitly_stated",
    color: "#4ca6a8",
    radius: 54
  },
  {
    id: "C",
    chartLabel: "C",
    x: 700,
    y: 400,
    label: { en: "Birth Year / Right", id: "Tahun Lahir / Kanan" },
    formula: "normalize(sum(year digits))",
    evidence: "explicitly_stated",
    color: "#5c7cce",
    radius: 54
  },
  {
    id: "D",
    chartLabel: "D",
    x: 400,
    y: 700,
    label: { en: "Foundation / Bottom", id: "Fondasi / Bawah" },
    formula: "normalize(A + B + C)",
    evidence: "explicitly_stated",
    color: "#b06c9c",
    radius: 54
  },
  {
    id: "E",
    chartLabel: "E",
    x: 400,
    y: 400,
    label: { en: "Soul Searching / Center", id: "Pencarian Jiwa / Pusat" },
    formula: "normalize(earth_line + sky_line)",
    evidence: "reconstructed",
    color: "#d9b56d",
    radius: 62
  },
  {
    id: "top_left",
    chartLabel: "TL",
    x: 205,
    y: 205,
    label: { en: "Top Left", id: "Kiri Atas" },
    formula: "normalize(A + B)",
    evidence: "reconstructed",
    color: "#f4dfb3",
    radius: 42
  },
  {
    id: "top_right",
    chartLabel: "TR",
    x: 595,
    y: 205,
    label: { en: "Top Right", id: "Kanan Atas" },
    formula: "normalize(B + C)",
    evidence: "reconstructed",
    color: "#f4dfb3",
    radius: 42
  },
  {
    id: "bottom_right",
    chartLabel: "BR",
    x: 595,
    y: 595,
    label: { en: "Bottom Right", id: "Kanan Bawah" },
    formula: "normalize(C + D)",
    evidence: "reconstructed",
    color: "#f4dfb3",
    radius: 42
  },
  {
    id: "bottom_left",
    chartLabel: "BL",
    x: 205,
    y: 595,
    label: { en: "Bottom Left", id: "Kiri Bawah" },
    formula: "normalize(D + A)",
    evidence: "reconstructed",
    color: "#f4dfb3",
    radius: 42
  },
  {
    id: "earth_line",
    chartLabel: "EARTH",
    x: 400,
    y: 585,
    label: { en: "Earth Line", id: "Garis Bumi" },
    formula: "normalize(A + C)",
    evidence: "explicitly_stated",
    color: "#e8c980",
    radius: 38
  },
  {
    id: "sky_line",
    chartLabel: "SKY",
    x: 585,
    y: 400,
    label: { en: "Sky Line", id: "Garis Langit" },
    formula: "normalize(B + D)",
    evidence: "explicitly_stated",
    color: "#e8c980",
    radius: 38
  }
];

export const UNSUPPORTED_NODE_CONFIG = [
  { id: "future_top", x: 400, y: 285 },
  { id: "future_right", x: 515, y: 400 },
  { id: "future_bottom", x: 400, y: 515 },
  { id: "future_left", x: 285, y: 400 }
] as const;

export const POSITION_CONFIG_BY_ID = Object.fromEntries(
  POSITION_CONFIG.map((position) => [position.id, position])
) as Record<TeacherTeaserPositionId, PositionDisplayConfig>;
