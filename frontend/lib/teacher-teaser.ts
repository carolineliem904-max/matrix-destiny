import type { MatrixPosition } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type TeacherTeaserPositionId =
  | "A"
  | "B"
  | "C"
  | "D"
  | "E"
  | "earth_line"
  | "sky_line"
  | "top_left"
  | "top_right"
  | "bottom_right"
  | "bottom_left";

export interface ExperimentalPersonalRequest {
  birth_date: string;
  name?: string;
}

export interface ExperimentalPersonRequest {
  name: string;
  birth_date: string;
}

export interface ExperimentalCompatibilityRequest {
  person_1: ExperimentalPersonRequest;
  person_2: ExperimentalPersonRequest;
}

export interface ExperimentalPersonalMatrix {
  name?: string | null;
  methodology_version: "teacher-teaser-v0.1";
  verified: false;
  birth_date: string;
  supported_positions: MatrixPosition[];
  unsupported_positions: string[];
  warnings: string[];
}

export interface ExperimentalCompatibilityResponse {
  methodology_version: "teacher-teaser-v0.1";
  verified: false;
  person_1: ExperimentalPersonalMatrix;
  person_2: ExperimentalPersonalMatrix;
  supported_compatibility_positions: MatrixPosition[];
  unsupported_positions: string[];
  warnings: string[];
}

async function experimentalRequest<T>(
  path: string,
  payload: unknown
): Promise<T> {
  const response = await fetch(
    `${API_BASE_URL}/api/experimental/teacher-teaser/${path}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    }
  );

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail = body?.detail;
    const message =
      typeof detail === "string"
        ? detail
        : "The experimental calculation is currently unavailable.";
    throw new Error(message);
  }

  return response.json();
}

export function calculateTeacherTeaserPersonal(
  payload: ExperimentalPersonalRequest
): Promise<ExperimentalPersonalMatrix> {
  return experimentalRequest("personal", payload);
}

export function calculateTeacherTeaserCompatibility(
  payload: ExperimentalCompatibilityRequest
): Promise<ExperimentalCompatibilityResponse> {
  return experimentalRequest("compatibility", payload);
}
