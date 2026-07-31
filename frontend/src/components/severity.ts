import type { Severity } from "../api/client";

export const SEV_COLOR: Record<Severity, string> = {
  none: "#4ade80",
  watch: "#facc15",
  warning: "#fb923c",
  alert: "#ef4444",
};

export const SEV_LABEL: Record<Severity, string> = {
  none: "Normal",
  watch: "Watch",
  warning: "Warning",
  alert: "Alert",
};

export function num(n: number): string {
  return n.toLocaleString("en-US");
}
