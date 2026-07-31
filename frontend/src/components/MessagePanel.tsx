import { useState } from "react";
import { api, type Message } from "../api/client";

const AUDIENCES = ["pastoralist", "farmer", "drm_officer"];
const LANGUAGES = [{ v: "en", l: "English" }, { v: "sw", l: "Swahili" }];
const CHANNELS = ["sms", "voice"];

export function MessagePanel({ adminId, asOf }: { adminId: string; asOf?: string }) {
  const [audience, setAudience] = useState("pastoralist");
  const [language, setLanguage] = useState("en");
  const [channel, setChannel] = useState("sms");
  const [msg, setMsg] = useState<Message | null>(null);
  const [dispatch, setDispatch] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function preview() {
    setLoading(true);
    setDispatch(null);
    try {
      setMsg(await api.message({ admin_id: adminId, audience, language, channel, as_of: asOf }));
    } finally {
      setLoading(false);
    }
  }
  async function send() {
    setLoading(true);
    try {
      const r = await api.dispatch({ admin_id: adminId, audience, language, channel, as_of: asOf });
      setMsg(r.message);
      const d = r.dispatch;
      setDispatch(
        `${d.status.toUpperCase()} · ${d.gateway ?? "gateway"}` +
          (d.reference ? ` · ref ${d.reference}` : "") +
          (d.provider_id ? ` · ${d.provider_id}` : "")
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-xl bg-stone-800/80 p-4">
      <h3 className="mb-2 font-bold">Last-mile message <span className="text-xs font-normal text-stone-400">(feeds HUSIKA)</span></h3>
      <div className="flex flex-wrap gap-2 text-xs">
        <Select value={audience} set={setAudience} opts={AUDIENCES} />
        <Select value={language} set={setLanguage} opts={LANGUAGES.map((l) => l.v)} labels={LANGUAGES} />
        <Select value={channel} set={setChannel} opts={CHANNELS} />
      </div>
      <div className="mt-3 flex gap-2">
        <button onClick={preview} disabled={loading}
          className="rounded-lg bg-amber-600 px-3 py-1.5 text-sm font-medium hover:bg-amber-500 disabled:opacity-50">
          {loading ? "Generating…" : "Preview"}
        </button>
        <button onClick={send} disabled={loading}
          className="rounded-lg bg-emerald-600 px-3 py-1.5 text-sm font-medium hover:bg-emerald-500 disabled:opacity-50">
          Approve &amp; dispatch
        </button>
      </div>

      {loading && (
        <div className="mt-3 flex items-center gap-2 text-xs text-stone-400">
          <span className="h-3 w-3 animate-spin rounded-full border-2 border-amber-500 border-t-transparent" />
          Generating {language === "sw" ? "Swahili" : "English"} message with AI…
        </div>
      )}

      {msg && (
        <div className="mt-3 space-y-2">
          <div className="rounded-lg bg-stone-900/70 p-3 text-sm">{msg.text}</div>
          {channel === "sms" && (
            <div className="text-xs text-stone-400">
              {msg.sms_segments.length} SMS segment(s): {msg.sms_segments.map((s, i) => (
                <span key={i} className="mr-1 rounded bg-stone-700 px-1">{s.length} chars</span>
              ))}
            </div>
          )}
          {channel === "voice" && (
            <div className="rounded-lg bg-stone-900/70 p-3 text-xs text-stone-400">
              <span className="font-semibold text-stone-300">Voice/IVR script: </span>{msg.voice_script}
            </div>
          )}
        </div>
      )}
      {dispatch && (
        <div className="mt-2 rounded-lg bg-emerald-900/40 p-2 text-xs text-emerald-300">
          ✓ Delivered to gateway — <b>{dispatch}</b>
        </div>
      )}
    </div>
  );
}

function Select({ value, set, opts, labels }: {
  value: string; set: (v: string) => void; opts: string[]; labels?: { v: string; l: string }[];
}) {
  return (
    <select value={value} onChange={(e) => set(e.target.value)}
      className="rounded-lg border border-stone-600 bg-stone-900 px-2 py-1 capitalize">
      {opts.map((o) => (
        <option key={o} value={o}>{labels ? labels.find((l) => l.v === o)?.l : o.replace("_", " ")}</option>
      ))}
    </select>
  );
}
