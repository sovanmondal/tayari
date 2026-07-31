import { useEffect, useRef, useState } from "react";
import type { Briefing } from "../api/client";
import { num } from "./severity";

/** Typewriter effect so the AI briefing "flows" onto the screen. */
function useTypewriter(text: string, speed = 18) {
  const [out, setOut] = useState("");
  const idx = useRef(0);
  useEffect(() => {
    setOut("");
    idx.current = 0;
    if (!text) return;
    const t = setInterval(() => {
      idx.current += 1;
      setOut(text.slice(0, idx.current));
      if (idx.current >= text.length) clearInterval(t);
    }, speed);
    return () => clearInterval(t);
  }, [text, speed]);
  return out;
}

export function SituationBriefing({ briefing, loading }: { briefing?: Briefing; loading: boolean }) {
  const typed = useTypewriter(briefing?.text ?? "");
  const s = briefing?.stats;
  return (
    <div className="rounded-xl border border-amber-900/60 bg-gradient-to-br from-stone-800/90 to-stone-900/90 p-4">
      <div className="mb-2 flex items-center gap-2">
        <span className="flex h-6 items-center gap-1 rounded-full bg-amber-600/20 px-2 text-[11px] font-semibold text-amber-300">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-amber-400 opacity-75" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-amber-400" />
          </span>
          AI SITUATION BRIEFING
        </span>
        {briefing && (
          <span className="text-[10px] uppercase tracking-wide text-stone-500">
            {briefing.llm === "template" ? "rule-based" : `LLM: ${briefing.llm}`}
          </span>
        )}
      </div>

      {s && (
        <div className="mb-2 flex flex-wrap gap-2 text-xs">
          <Stat label="counties triggered" value={`${s.counties_triggered}/${s.counties_total}`} />
          <Stat label="people exposed" value={num(s.total_exposed)} />
          {s.worst_county && <Stat label="worst-hit" value={s.worst_county} />}
        </div>
      )}

      <p className="min-h-[3rem] text-sm leading-relaxed text-stone-200">
        {loading ? "Analysing latest drought conditions…" : typed}
        {typed && typed.length < (briefing?.text.length ?? 0) && <span className="animate-pulse">▋</span>}
      </p>

      {s && s.counties_triggered === 0 && !loading && (
        <p className="mt-1 text-xs text-amber-300/80">
          ↓ No active triggers at this dekad. Drag the timeline to a past event (e.g. May 2021) to see anticipatory action in motion.
        </p>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <span className="rounded-lg bg-stone-900/70 px-2 py-1">
      <b className="text-stone-100">{value}</b> <span className="text-stone-400">{label}</span>
    </span>
  );
}
