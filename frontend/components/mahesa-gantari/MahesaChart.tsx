"use client";

import type { KeyboardEvent } from "react";
import type { CoursePoint } from "@/lib/mahesa-gantari";

const POSITIONS: Record<string, [number, number]> = {
  A:[70,350], B:[400,70], C:[730,350], D:[400,630], E:[400,350],
  F:[170,152], G:[630,152], H:[630,548], I:[170,548],
  J:[220,350], K:[400,190], L:[600,350], M:[400,510], N:[490,430],
  O:[460,350], P:[240,220], Q:[560,220], R:[560,480], S:[240,480],
  A_plus_J:[145,350], E_plus_J:[320,350], B_plus_K:[400,130], C_plus_L:[665,350], D_plus_M:[400,570],
  F_plus_P:[205,185], G_plus_Q:[595,185], H_plus_R:[595,515], I_plus_S:[205,515],
  E_plus_K:[400,265], E_plus_O:[510,350], L_plus_N:[555,350], M_plus_N:[445,470]
};
const primary = new Set(["A","B","C","D","E"]);
const corners = new Set(["F","G","H","I"]);
const inner = new Set(["J","K","L","M","N"]);
const shadow = new Set(["O","P","Q","R","S"]);

export function MahesaChart({points, selected, onSelect, language}:{points:CoursePoint[];selected:string;onSelect:(id:string)=>void;language:"en"|"id"}) {
  const key = (event: KeyboardEvent<SVGGElement>, id:string) => {
    if (event.key === "Enter" || event.key === " ") { event.preventDefault(); onSelect(id); }
  };
  return <figure className="overflow-hidden border border-gold/25 bg-night/75 p-2 sm:p-4">
    <svg viewBox="0 0 800 700" className="w-full" role="img" aria-labelledby="mg-title mg-desc">
      <title id="mg-title">{language === "en" ? "Mahesa Gantari calculation map" : "Peta perhitungan Mahesa Gantari"}</title>
      <desc id="mg-desc">{language === "en" ? "Interactive map of all primary and additional calculated nodes." : "Peta interaktif semua node utama dan tambahan yang dihitung."}</desc>
      <path d="M70 350 L170 152 L400 70 L630 152 L730 350 L630 548 L400 630 L170 548 Z" fill="rgba(217,181,109,.035)" stroke="#d9b56d" strokeWidth="2"/>
      <path d="M70 350H730 M400 70V630 M170 152L630 548 M630 152L170 548" stroke="#d9b56d" strokeOpacity=".28" strokeWidth="2"/>
      <path d="M220 350L400 190L600 350L400 510Z M240 220L560 220L560 480L240 480Z" fill="none" stroke="#fff7e8" strokeOpacity=".16" strokeDasharray="7 8"/>
      {points.map(point => {
        const [x,y] = POSITIONS[point.position_id] ?? [350,350];
        const additional = !primary.has(point.position_id)&&!corners.has(point.position_id)&&!inner.has(point.position_id)&&!shadow.has(point.position_id);
        const radius = primary.has(point.position_id) ? 34 : corners.has(point.position_id) ? 27 : additional ? 19 : 22;
        const fill = primary.has(point.position_id) ? "#d9b56d" : corners.has(point.position_id) ? "#79b8b5" : inner.has(point.position_id) ? "#8f79b8" : shadow.has(point.position_id) ? "#b66583" : "#f4dfb3";
        const active = selected === point.position_id;
        return <g key={point.position_id} role="button" tabIndex={0} aria-pressed={active} aria-label={`${point.position_id}, ${point.label}, ${point.value}, ${point.arcana_name}`} onClick={()=>onSelect(point.position_id)} onKeyDown={e=>key(e,point.position_id)} className="teacher-node cursor-pointer outline-none">
          <circle className="teacher-node-focus" cx={x} cy={y} r={radius} fill={fill} stroke={active?"#fff":"#1b1728"} strokeWidth={active?5:2}/>
          <text x={x} y={y-(additional?4:7)} textAnchor="middle" className={`pointer-events-none fill-night font-bold ${additional?"text-[9px]":"text-[13px]"}`}>{point.position_id.replace("_plus_","+")}</text>
          <text x={x} y={y+(additional?12:15)} textAnchor="middle" className={`pointer-events-none fill-night font-bold ${additional?"text-[14px]":"text-[18px]"}`}>{point.value}</text>
        </g>;
      })}
    </svg>
    <figcaption className="grid grid-cols-2 gap-2 border-t border-cream/10 pt-3 text-xs text-cream/65 sm:grid-cols-5">
      {[["#d9b56d","A–E"],["#79b8b5","F–I"],["#8f79b8","J–N"],["#b66583","O–S"],["#f4dfb3",language==="en"?"Additional":"Tambahan"]].map(([color,label])=><span key={label} className="flex items-center gap-2"><i className="h-3 w-3 rounded-full" style={{background:color}}/>{label}</span>)}
    </figcaption>
  </figure>;
}
