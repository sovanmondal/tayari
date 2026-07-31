import type { Ibf } from "../api/client";

export function ProvenanceBadge({ provenance }: { provenance: Ibf["provenance"] }) {
  return (
    <div className="mt-3 rounded-lg bg-slate-800/60 p-3 text-xs">
      <div className="mb-1 font-semibold text-slate-300">Data provenance (real sources)</div>
      <ul className="space-y-1">
        {provenance.map((p, i) => (
          <li key={i} className="flex gap-2">
            <span className="shrink-0 rounded bg-slate-700 px-1.5 py-0.5 text-[10px] uppercase tracking-wide text-slate-300">
              {p.role}
            </span>
            {p.url ? (
              <a href={p.url} target="_blank" rel="noreferrer" className="text-sky-400 hover:underline">
                {p.source}
              </a>
            ) : (
              <span className="text-slate-400">{p.source}</span>
            )}
            {p.stale && <span className="text-amber-400">(cached)</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}
