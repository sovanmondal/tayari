import { useState } from "react";
import type { Recommendation } from "../api/client";

export function Recommendations({ recs }: { recs: Recommendation[] }) {
  return (
    <div className="rounded-xl bg-stone-800/80 p-4">
      <h3 className="mb-2 font-bold">Anticipatory actions <span className="text-xs font-normal text-stone-400">(ranked)</span></h3>
      <ol className="space-y-2">
        {recs.map((r) => (
          <RecItem key={r.rank} r={r} />
        ))}
      </ol>
    </div>
  );
}

function RecItem({ r }: { r: Recommendation }) {
  const [open, setOpen] = useState(r.rank === 1);
  return (
    <li className="rounded-lg bg-stone-900/60 p-3">
      <div className="flex items-start gap-2">
        <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-amber-600 text-xs font-bold">
          {r.rank}
        </span>
        <div className="flex-1">
          <div className="font-medium">{r.action}</div>
          <div className="mt-1 flex flex-wrap gap-2 text-xs text-stone-400">
            <span className="rounded bg-stone-700 px-1.5 py-0.5">lead {r.lead_time_days}d</span>
            <span className="rounded bg-stone-700 px-1.5 py-0.5">cost: {r.cost_band}</span>
            <span className="rounded bg-stone-700 px-1.5 py-0.5">{r.window}</span>
          </div>
          <div className="mt-1 text-xs text-stone-500">Actor: {r.actor}</div>
          {r.evidence.length > 0 && (
            <button onClick={() => setOpen(!open)} className="mt-2 text-xs text-amber-400 hover:underline">
              {open ? "▼ Hide" : "▶ Show"} evidence chain
            </button>
          )}
          {open && r.evidence.length > 0 && (
            <ol className="mt-2 space-y-1 border-l-2 border-stone-700 pl-3">
              {r.evidence.map((e, i) => (
                <li key={i} className="text-xs">
                  <span className="font-semibold text-stone-300">{e.step}: </span>
                  <span className="text-stone-400">{e.detail}</span>
                  {e.source && <span className="block text-[10px] text-stone-600">source: {e.source}</span>}
                </li>
              ))}
            </ol>
          )}
        </div>
      </div>
    </li>
  );
}
