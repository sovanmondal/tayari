import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import { MapView } from "../components/MapView";
import { IbfCard } from "../components/IbfCard";
import { Recommendations } from "../components/Recommendations";
import { MessagePanel } from "../components/MessagePanel";
import { SEV_COLOR, SEV_LABEL } from "../components/severity";

export function Dashboard() {
  const districts = useQuery({ queryKey: ["districts"], queryFn: api.districts });
  const [selected, setSelected] = useState<string | null>(null);

  useEffect(() => {
    if (!selected && districts.data?.length) {
      const firstTriggered = districts.data.find((d) => d.triggered) ?? districts.data[0];
      setSelected(firstTriggered.id);
    }
  }, [districts.data, selected]);

  const ibf = useQuery({
    queryKey: ["ibf", selected],
    queryFn: () => api.ibf(selected!),
    enabled: !!selected,
  });
  const recs = useQuery({
    queryKey: ["recs", selected],
    queryFn: () => api.recommendations(selected!),
    enabled: !!selected,
  });

  const triggeredCount = districts.data?.filter((d) => d.triggered).length ?? 0;

  return (
    <div className="flex h-screen flex-col">
      <header className="flex items-center justify-between border-b border-slate-800 px-5 py-3">
        <div>
          <h1 className="text-xl font-bold">Tayari <span className="text-sm font-normal text-slate-400">· Anticipatory Action Co-pilot</span></h1>
          <p className="text-xs text-slate-500">From ICPAC forecast → decision → last-mile action. Real CDI data.</p>
        </div>
        <div className="text-right text-xs text-slate-400">
          <div><b className="text-amber-400">{triggeredCount}</b> counties triggered</div>
          {districts.data?.[0] && <div>dekad {districts.data[0].as_of}</div>}
        </div>
      </header>

      <div className="flex min-h-0 flex-1">
        <div className="relative w-1/2 border-r border-slate-800">
          {districts.data && (
            <MapView districts={districts.data} selected={selected} onSelect={setSelected} />
          )}
          <Legend />
        </div>

        <div className="w-1/2 space-y-3 overflow-y-auto p-4">
          <DistrictStrip
            data={districts.data ?? []}
            selected={selected}
            onSelect={setSelected}
          />
          {ibf.data && <IbfCard ibf={ibf.data} />}
          {recs.data && recs.data.length > 0 && <Recommendations recs={recs.data} />}
          {selected && ibf.data?.trigger.triggered && <MessagePanel adminId={selected} />}
          {ibf.data && !ibf.data.trigger.triggered && (
            <div className="rounded-xl bg-slate-800/60 p-4 text-sm text-slate-400">
              Below anticipatory-action trigger — monitoring only. No last-mile alert dispatched.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function DistrictStrip({ data, selected, onSelect }: {
  data: { id: string; name: string; severity: keyof typeof SEV_COLOR; population_exposed: number }[];
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
    <div className="absolute bottom-3 left-3 rounded-lg bg-slate-900/90 p-2 text-xs">
      {(["alert", "warning", "watch", "none"] as const).map((s) => (
        <div key={s} className="flex items-center gap-2">
          <span className="inline-block h-3 w-3 rounded-full" style={{ background: SEV_COLOR[s] }} />
          {SEV_LABEL[s]}
        </div>
      ))}
    </div>
  );
}
