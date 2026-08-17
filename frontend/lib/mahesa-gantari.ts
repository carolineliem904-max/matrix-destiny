export type Sect = "day" | "night" | "unknown";

export interface Evidence {
  methodology_version: string;
  source_document: string;
  source_page: number;
  evidence_status: string;
  verified: false;
}

export interface CoursePoint {
  position_id: string;
  label: string;
  value: number;
  arcana_number: number;
  arcana_name: string;
  calculation_trace: string[];
  evidence: Evidence;
}

export interface CourseLine {
  line_id: string;
  ordered_point_ids: string[];
  values: number[];
  component_labels: string[];
  evidence: Evidence;
}

export interface MahesaGantariResult {
  methodology_version: string;
  status: string;
  verified: false;
  birth_date: string;
  points: CoursePoint[];
  money_line: CourseLine;
  relationship_line: CourseLine;
  karmic_tail: CourseLine;
  deepest_desire: CourseLine;
  male_generation: CourseLine;
  female_generation: CourseLine;
  purpose: {
    earth: CoursePoint;
    sky: CoursePoint;
    soul_searching: CoursePoint;
    male: CoursePoint;
    female: CoursePoint;
    socialization: CoursePoint;
    spiritual_knowledge: CoursePoint;
    age_range_metadata: Record<string, string>;
  };
  sect_context: {
    sect: Sect;
    source: string;
    weighting_rule_version: null;
    interpretation_modifier_active: false;
  };
  warnings: string[];
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function calculateMahesaGantari(
  birth_date: string,
  sect: Sect
): Promise<MahesaGantariResult> {
  const response = await fetch(`${API_BASE}/api/experimental/mahesa-gantari/personal`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ birth_date, sect })
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) throw new Error(body?.detail ?? "Unable to calculate the matrix.");
  return body;
}
