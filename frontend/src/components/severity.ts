import type { Severity } from "../api/client";

export const SEV_COLOR: Record<Severity, string> = {
  none: "#6f9b6e",
  watch: "#e0b341",
  warning: "#d9863c",
  alert: "#c0442e",
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
