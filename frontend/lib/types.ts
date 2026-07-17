export type LanguageCode = "en" | "id";

export interface ChartCoordinates {
  x: number;
  y: number;
}

export interface MatrixPosition {
  id: string;
  label: string;
  value: number;
  verified: boolean;
  calculation_trace: string[];
  coordinates?: ChartCoordinates | null;
  interpretation_key?: string | null;
}

export interface EnergyInterpretation {
  energy: number;
  name: string;
  keywords: string[];
  core_meaning: string;
  positive_expression: string[];
  shadow_expression: string[];
  relationships: string;
  career: string;
  money: string;
  growth_advice: string[];
  source_status: "draft" | "reviewed" | "verified";
}

export interface PositionInterpretation {
  id: string;
  label: string;
  description: string;
  source_status: "draft" | "reviewed" | "verified";
}

export interface InterpretedPosition {
  position: MatrixPosition;
  role?: PositionInterpretation | null;
  energy?: EnergyInterpretation | null;
}

export interface ReadingResponse {
  methodology_version: string;
  birth_date: string;
  language: LanguageCode;
  name?: string | null;
  focus?: string | null;
  positions: InterpretedPosition[];
  summary: string;
  warnings: string[];
  disclaimer: string;
}

export interface MatrixRequest {
  birth_date: string;
  language: LanguageCode;
  name?: string;
  focus?: string;
}
