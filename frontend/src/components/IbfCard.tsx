import type { Ibf } from "../api/client";
import { SEV_COLOR, SEV_LABEL, num } from "./severity";
import { ProvenanceBadge } from "./ProvenanceBadge";

export function IbfCard({ ibf }: { ibf: Ibf }) {
  return (
    <div className="rounded-xl bg-stone-800/80 p-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold">{ibf.admin.name}, {ibf.admin.country}</h2>
        <span
          className="rounded-full px-3 py-1 text-sm font-semibold text-stone-900"
          style={{ background: SEV_COLOR[ibf.severity] }}
        >
          {SEV_LABEL[ibf.severity]}
        </span>
      </div>
      <div className="mt-1 text-xs text-stone-400">
        CDI class {ibf.cdi_class} · {ibf.cdi_label} · dekad {ibf.as_of}
      </div>

      <div className="mt-3 grid grid-cols-2 gap-3">
        <div className="rounded-lg bg-stone-900/60 p-3">
          <div className="text-2xl font-bold">{num(ibf.impact.total_population_exposed)}</div>
          <div className="text-xs text-stone-400">people exposed</div>
        </div>
        <div className="rounded-lg bg-stone-900/60 p-3">
          <div className="text-sm">
            {ibf.impact.by_livelihood.length
              ? ibf.impact.by_livelihood.map((b) => (
                  <div key={b.livelihood} className="flex justify-between">
                    <span className="text-stone-400">{b.livelihood}</span>
                    <span>{num(b.population)}</span>
                  </div>
                ))
              : <span className="text-stone-500">Not triggered</span>}
          </div>
        </div>
      </div>

      <p className="mt-3 text-sm leading-relaxed text-stone-200">{ibf.narrative}</p>
      <ProvenanceBadge provenance={ibf.provenance} />
    </div>
  );
}
