"use client";

import type { KeyboardEvent } from "react";
import type { CoursePoint } from "@/lib/mahesa-gantari";

const POSITIONS: Record<string, [number, number]> = {
  A:[70,350], B:[350,70], C:[630,350], D:[350,630], E:[350,350],
  F:[152,152], G:[548,152], H:[548,548], I:[152,548],
  J:[190,350], K:[350,190], L:[510,350], M:[350,510], N:[430,430],
  O:[270,270], P:[220,220], Q:[480,220], R:[480,480], S:[220,480],
  A_plus_J:[130,350], B_plus_K:[350,130], C_plus_L:[570,350], D_plus_M:[350,570],
  F_plus_P:[185,185], G_plus_Q:[515,185], H_plus_R:[515,515], I_plus_S:[185,515],
  E_plus_K:[350,265], E_plus_O:[310,310], L_plus_N:[470,390], M_plus_N:[390,470]
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
    <svg viewBox="0 0 700 700" className="aspect-square w-full" role="img" aria-labelledby="mg-title mg-desc">
      <title id="mg-title">{language === "en" ? "Mahesa Gantari calculation map" : "Peta perhitungan Mahesa Gantari"}</title>
      <desc id="mg-desc">{language === "en" ? "Interactive map of all primary and additional calculated nodes." : "Peta interaktif semua node utama dan tambahan yang dihitung."}</desc>
      <path d="M70 350 L152 152 L350 70 L548 152 L630 350 L548 548 L350 630 L152 548 Z" fill="rgba(217,181,109,.035)" stroke="#d9b56d" strokeWidth="2"/>
      <path d="M70 350H630 M350 70V630 M152 152L548 548 M548 152L152 548" stroke="#d9b56d" strokeOpacity=".28" strokeWidth="2"/>
      <path d="M190 350L350 190L510 350L350 510Z M220 220L480 220L480 480L220 480Z" fill="none" stroke="#fff7e8" strokeOpacity=".16" strokeDasharray="7 8"/>
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
