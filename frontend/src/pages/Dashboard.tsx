import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import { MapView } from "../components/MapView";
import { IbfCard } from "../components/IbfCard";
import { Recommendations } from "../components/Recommendations";
import { MessagePanel } from "../components/MessagePanel";
import { SituationBriefing } from "../components/SituationBriefing";
import { DekadTimeline } from "../components/DekadTimeline";
import { SEV_COLOR, SEV_LABEL } from "../components/severity";

export function Dashboard() {
  const [dekad, setDekad] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);

  // Available real dekads; default to latest (real-time).
  const dekads = useQuery({ queryKey: ["dekads"], queryFn: api.dekads });
  useEffect(() => {
    if (!dekad && dekads.data?.latest) setDekad(dekads.data.latest);
  }, [dekads.data, dekad]);

  const districts = useQuery({
    queryKey: ["districts", dekad],
    queryFn: () => api.districts(dekad ?? undefined),
    enabled: !!dekad,
  });
  const briefing = useQuery({
    queryKey: ["briefing", dekad],
    queryFn: () => api.briefing(dekad ?? undefined),
    enabled: !!dekad,
  });

  // Auto-focus the worst-hit district whenever the dekad changes.
  useEffect(() => {
    if (districts.data?.length) {
      const worst = [...districts.data].sort((a, b) => b.cdi_class - a.cdi_class)[0];
      setSelected((prev) =>
        districts.data!.some((d) => d.id === prev) && prev ? prev : worst.id
      );
    }
  }, [districts.data]);

  const ibf = useQuery({
    queryKey: ["ibf", selected, dekad],
    queryFn: () => api.ibf(selected!, dekad ?? undefined),
    enabled: !!selected && !!dekad,
  });
  const recs = useQuery({
    queryKey: ["recs", selected, dekad],
    queryFn: () => api.recommendations(selected!, dekad ?? undefined),
    enabled: !!selected && !!dekad,
  });

  const triggeredCount = districts.data?.filter((d) => d.triggered).length ?? 0;

  return (
    <div className="flex h-screen flex-col">
      <header className="flex items-center justify-between border-b border-stone-800/80 bg-gradient-to-r from-stone-900/40 to-transparent px-5 py-3">
        <div className="flex items-center gap-3">
          <TayariMark />
          <div>
            <h1 className="font-display text-xl font-bold tracking-tight">
              Tayari <span className="text-sm font-medium text-ochre-400">· Anticipatory Action Co-pilot</span>
            </h1>
            <p className="text-xs text-stone-400">ICPAC forecast → decision → last-mile action · real Combined Drought Indicator</p>
          </div>
        </div>
        <div className="text-right text-xs text-stone-400">
          <div className="font-display text-lg font-bold text-ochre-400">{triggeredCount}<span className="text-xs font-normal text-stone-400"> counties triggered</span></div>
          <div>dekad {dekad ?? "…"}</div>
        </div>
      </header>

      <div className="flex min-h-0 flex-1">
        <div className="relative w-1/2 border-r border-stone-800">
          {districts.data && (
            <MapView districts={districts.data} selected={selected} onSelect={setSelected} />
          )}
          <Legend />
        </div>

        <div className="w-1/2 space-y-3 overflow-y-auto p-4">
          <SituationBriefing briefing={briefing.data} loading={briefing.isLoading} />
          <DistrictStrip data={districts.data ?? []} selected={selected} onSelect={setSelected} />
          {ibf.data && <IbfCard ibf={ibf.data} />}
          {recs.data && recs.data.length > 0 && <Recommendations recs={recs.data} />}
          {selected && ibf.data?.trigger.triggered && (
            <MessagePanel adminId={selected} asOf={dekad ?? undefined} />
          )}
          {ibf.data && !ibf.data.trigger.triggered && (
            <div className="rounded-xl bg-stone-800/60 p-4 text-sm text-stone-400">
              Below anticipatory-action trigger — monitoring only. No last-mile alert dispatched.
            </div>
          )}
        </div>
      </div>

      <DekadTimeline dekads={dekads.data?.dekads ?? []} value={dekad} onChange={setDekad} />
    </div>
  );
}

function TayariMark() {
  // Savanna sun rising over cracked land — drought + early-warning motif.
  return (
    <svg width="38" height="38" viewBox="0 0 40 40" fill="none" aria-label="Tayari logo">
      <rect width="40" height="40" rx="10" fill="#211a13" />
      <circle cx="20" cy="17" r="7" fill="#e0b341" />
      <g stroke="#d9863c" strokeWidth="1.6" strokeLinecap="round">
        <line x1="20" y1="3" x2="20" y2="6.5" />
        <line x1="31" y1="6" x2="28.7" y2="8.3" />
        <line x1="9" y1="6" x2="11.3" y2="8.3" />
      </g>
      <path d="M4 28 Q12 24 20 28 T36 28" stroke="#6f9b6e" strokeWidth="1.8" fill="none" strokeLinecap="round" />
      <path d="M4 33 Q12 29 20 33 T36 33" stroke="#8a6f4e" strokeWidth="1.8" fill="none" strokeLinecap="round" />
    </svg>
  );
}

function DistrictStrip({ data, selected, onSelect }: {
  data: { id: string; name: string; severity: keyof typeof SEV_COLOR }[];
  selected: string | null; onSelect: (id: string) => void;
}) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {data.map((d) => (
        <button key={d.id} onClick={() => onSelect(d.id)}
          className={`rounded-lg px-2 py-1 text-xs ${selected === d.id ? "ring-2 ring-white" : ""}`}
          style={{ background: SEV_COLOR[d.severity], color: "#0f172a" }}>
          {d.name}
        </button>
      ))}
    </div>
  );
}

function Legend() {
  return (
    <div className="absolute bottom-3 left-3 rounded-lg bg-stone-900/90 p-2 text-xs">
      {(["alert", "warning", "watch", "none"] as const).map((s) => (
        <div key={s} className="flex items-center gap-2">
          <span className="inline-block h-3 w-3 rounded-full" style={{ background: SEV_COLOR[s] }} />
          {SEV_LABEL[s]}
        </div>
      ))}
    </div>
  );
}
