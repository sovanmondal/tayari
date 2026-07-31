const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export type Severity = "none" | "watch" | "warning" | "alert";

export interface District {
  id: string;
  name: string;
  country: string;
  lon: number;
  lat: number;
  population: number;
  cdi_class: number;
  cdi_label: string;
  severity: Severity;
  triggered: boolean;
  population_exposed: number;
  as_of: string;
}

export interface EvidenceLink { step: string; detail: string; source?: string; }

export interface Ibf {
  admin: { id: string; name: string; country: string };
  as_of: string;
  cdi_class: number;
  cdi_label: string;
  severity: Severity;
  narrative: string;
  impact: {
    total_population_exposed: number;
    by_livelihood: { livelihood: string; population: number }[];
    method: string;
  };
  trigger: { rationale: string; triggered: boolean };
  provenance: { source: string; url?: string; role: string; stale?: boolean }[];
}

export interface Recommendation {
  rank: number;
  action: string;
  lead_time_days: number;
  cost_band: string;
  actor: string;
  window: string;
  evidence: EvidenceLink[];
}

export interface Message {
  audience: string;
  language: string;
  channel: string;
  admin_id: string;
  text: string;
  sms_segments: string[];
  voice_script: string;
}

async function get<T>(path: string): Promise<T> {
  const r = await fetch(`${API_BASE}${path}`);
  if (!r.ok) throw new Error(`${r.status} ${path}`);
  return r.json();
}
async function post<T>(path: string, body: unknown): Promise<T> {
  const r = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`${r.status} ${path}`);
  return r.json();
}

export const api = {
  base: API_BASE,
  districts: () => get<District[]>("/districts"),
  ibf: (id: string) => get<Ibf>(`/ibf/${id}`),
  recommendations: (id: string) => get<Recommendation[]>(`/recommendations/${id}`),
  message: (body: { admin_id: string; audience: string; language: string; channel: string }) =>
    post<Message>("/messages", body),
  dispatch: (body: { admin_id: string; audience: string; language: string; channel: string }) =>
    post<{ message: Message; dispatch: { status: string; provider_id?: string } }>("/dispatch", body),
};
