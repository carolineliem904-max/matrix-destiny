import type { MatrixRequest, ReadingResponse } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function calculateMatrix(payload: MatrixRequest): Promise<ReadingResponse> {
  const response = await fetch(`${API_BASE_URL}/api/matrix/calculate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? "Unable to calculate matrix.");
  }

  return response.json();
}
