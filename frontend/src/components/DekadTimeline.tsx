import { useEffect, useMemo, useState } from "react";

/** Real-data timeline: pick any available CDI dekad. Defaults to latest (real-time).
 *  The dekad is committed only when the user releases the slider — dragging across
 *  dozens of dekads must NOT fire a request (and a raster download) per step. */
export function DekadTimeline({
  dekads,
  value,
  onChange,
}: {
  dekads: string[];
  value: string | null;
  onChange: (dekad: string) => void;
}) {
  // dekads come newest-first; slider goes oldest(left) -> newest(right)
  const ordered = useMemo(() => [...dekads].reverse(), [dekads]);
  const committedIdx = value ? ordered.indexOf(value) : ordered.length - 1;
  const [pos, setPos] = useState(committedIdx);

  useEffect(() => {
    setPos(committedIdx < 0 ? ordered.length - 1 : committedIdx);
  }, [committedIdx, ordered.length]);

  if (!ordered.length) return null;
  const commit = () => {
    const d = ordered[pos];
    if (d && d !== value) onChange(d);
  };
  const shown = ordered[pos] ?? value ?? ordered[ordered.length - 1];

  return (
    <div className="flex items-center gap-3 border-t border-stone-800 px-4 py-2">
      <span className="text-xs text-stone-400">Dekad</span>
      <input
        type="range"
        min={0}
        max={ordered.length - 1}
        value={pos < 0 ? ordered.length - 1 : pos}
        onChange={(e) => setPos(Number(e.target.value))}
        onMouseUp={commit}
        onTouchEnd={commit}
        onKeyUp={commit}
        className="flex-1 accent-amber-500"
      />
      <span className="w-24 text-right font-mono text-xs text-stone-200">{shown}</span>
      <button
        onClick={() => onChange(ordered[ordered.length - 1])}
        className="rounded-md bg-stone-700 px-2 py-1 text-[11px] text-stone-200 hover:bg-stone-600"
        title="Jump to latest available dekad"
      >
        Latest
      </button>
    </div>
  );
}
