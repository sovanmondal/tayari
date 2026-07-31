import { useEffect, useRef } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import type { District } from "../api/client";
import { SEV_COLOR } from "./severity";

const OSM_STYLE = {
  version: 8 as const,
  sources: {
    osm: {
      type: "raster" as const,
      tiles: ["https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"],
      tileSize: 256,
      attribution: "© OpenStreetMap contributors",
    },
  },
  layers: [{ id: "osm", type: "raster" as const, source: "osm" }],
};

export function MapView({
  districts,
  selected,
  onSelect,
}: {
  districts: District[];
  selected: string | null;
  onSelect: (id: string) => void;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const markers = useRef<maplibregl.Marker[]>([]);

  useEffect(() => {
    if (!ref.current || map.current) return;
    map.current = new maplibregl.Map({
      container: ref.current,
      style: OSM_STYLE,
      center: [38.5, 1.5],
      zoom: 5.2,
    });
  }, []);

  useEffect(() => {
    if (!map.current) return;
    markers.current.forEach((m) => m.remove());
    markers.current = [];
    districts.forEach((d) => {
      const el = document.createElement("div");
      const size = d.triggered ? 26 : 16;
      el.style.cssText = `width:${size}px;height:${size}px;border-radius:50%;cursor:pointer;
        background:${SEV_COLOR[d.severity]};border:2px solid ${
        selected === d.id ? "#fff" : "rgba(255,255,255,.5)"
      };box-shadow:0 0 ${d.triggered ? 12 : 4}px ${SEV_COLOR[d.severity]};`;
      el.title = `${d.name}: ${d.severity} (CDI ${d.cdi_class})`;
      el.onclick = () => onSelect(d.id);
      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([d.lon, d.lat])
        .addTo(map.current!);
      markers.current.push(marker);
    });
  }, [districts, selected, onSelect]);

  return <div ref={ref} className="h-full w-full" />;
}
