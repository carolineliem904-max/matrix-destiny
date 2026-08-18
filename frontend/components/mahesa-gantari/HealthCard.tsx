"use client";

import type { HealthCard as HealthCardData, HealthCardCell } from "@/lib/mahesa-gantari";

const COPY = {
  en: {
    title: "Experimental Health Card",
    intro: "A provisional numerology table reconstructed from a reference diagram.",
    chakra: "Chakra", physics: "Physics", energy: "Energy", emotions: "Emotions", result: "Result",
    formula: "Formula", trace: "Calculation trace", evidence: "Evidence", reference: "Reference status",
    disclaimer: "This experimental numerology table is provided for reflection and entertainment. It is not a medical assessment, diagnosis, or treatment recommendation.",
    open: "Show calculation details for"
  },
  id: {
    title: "Kartu Kesehatan Eksperimental",
    intro: "Tabel numerologi sementara yang direkonstruksi dari diagram referensi.",
    chakra: "Cakra", physics: "Fisik", energy: "Energi", emotions: "Emosi", result: "Hasil",
    formula: "Rumus", trace: "Jejak perhitungan", evidence: "Bukti", reference: "Status referensi",
    disclaimer: "Tabel numerologi eksperimental ini disediakan untuk refleksi dan hiburan. Ini bukan pemeriksaan medis, diagnosis, atau rekomendasi pengobatan.",
    open: "Tampilkan detail perhitungan untuk"
  }
} as const;

const CHAKRA_ID: Record<string, string> = {
  sahasrara: "Sahasrara", ajna: "Ajna", vishuddha: "Vishuddha", anahata: "Anahata",
  manipura: "Manipura", svadhisthana: "Svadhisthana", muladhara: "Muladhara"
};

function Cell({cell, row, language}:{cell:HealthCardCell;row:string;language:"en"|"id"}) {
  const copy = COPY[language];
  return <details className="group min-w-0">
    <summary aria-label={`${copy.open} ${row} ${copy[cell.column_id]}`} className="cursor-pointer list-none rounded border border-gold/25 bg-gold/10 px-3 py-2 text-center font-bold text-gold outline-none focus:ring-2 focus:ring-gold">
      <span className="block text-lg">{cell.value}</span>
      <span className="block text-[11px] font-normal text-cream/60">{cell.arcana_name}</span>
    </summary>
    <div className="mt-2 space-y-2 border-l-2 border-gold/50 pl-3 text-xs text-cream/75">
      <p><strong>{copy.formula}:</strong> <span className="break-words font-mono">{cell.formula}</span></p>
      <div><strong>{copy.trace}:</strong><ol className="mt-1 space-y-1 font-mono">{cell.calculation_trace.map((line,index)=><li key={`${index}-${line}`} className="break-words">{line}</li>)}</ol></div>
      <p><strong>{copy.evidence}:</strong> {cell.evidence.evidence_status.replaceAll("_"," ")}</p>
      <p><strong>{copy.reference}:</strong> {cell.evidence.source_document}</p>
      <p className="font-mono font-bold text-red-200">verified: false</p>
    </div>
  </details>;
}

export function HealthCard({data,language}:{data:HealthCardData;language:"en"|"id"}) {
  const copy = COPY[language];
  const rows = [...data.rows, {row_id:"result",label:copy.result,...data.result}];
  return <section className="mt-8" aria-labelledby="health-card-title">
    <div className="flex flex-wrap items-end justify-between gap-3">
      <div><p className="text-xs font-bold uppercase text-gold">Experimental · verified: false</p><h2 id="health-card-title" className="mt-1 text-2xl font-bold">{copy.title}</h2><p className="mt-2 text-sm text-cream/65">{copy.intro}</p></div>
    </div>
    <div className="mt-4 hidden overflow-hidden border border-cream/15 bg-night/65 md:block">
      <table className="w-full table-fixed border-collapse text-left">
        <thead className="border-b border-gold/25 text-xs uppercase text-cream/60"><tr><th className="w-[22%] p-3">{copy.chakra}</th><th className="p-3">{copy.physics}</th><th className="p-3">{copy.energy}</th><th className="p-3">{copy.emotions}</th></tr></thead>
        <tbody>{rows.map(row=><tr key={row.row_id} className={`border-b border-cream/10 align-top last:border-0 ${row.row_id==="result"?"bg-gold/10":""}`}><th scope="row" className="break-words p-2 text-xs font-bold text-cream sm:p-3 sm:text-sm">{row.row_id==="result"?copy.result:CHAKRA_ID[row.row_id]}</th>{(["physics","energy","emotions"] as const).map(column=><td key={column} className="p-1 sm:p-2"><Cell cell={row[column]} row={row.label} language={language}/></td>)}</tr>)}</tbody>
      </table>
    </div>
    <div className="mt-4 space-y-4 md:hidden">
      {rows.map(row=><article key={row.row_id} className={`border border-cream/15 p-4 ${row.row_id==="result"?"bg-gold/10":"bg-night/65"}`}>
        <h3 className="font-bold text-gold">{row.row_id==="result"?copy.result:CHAKRA_ID[row.row_id]}</h3>
        <div className="mt-3 space-y-3">{(["physics","energy","emotions"] as const).map(column=><div key={column}><p className="mb-1 text-xs font-bold uppercase text-cream/55">{copy[column]}</p><Cell cell={row[column]} row={row.label} language={language}/></div>)}</div>
      </article>)}
    </div>
    <p className="mt-4 border border-red-300/25 bg-red-950/25 p-4 text-sm leading-6 text-red-100">{copy.disclaimer}</p>
  </section>;
}
