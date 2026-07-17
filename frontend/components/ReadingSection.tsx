import type { ReadingResponse } from "@/lib/types";
import { Disclaimer } from "./Disclaimer";
import { MatrixChart } from "./MatrixChart";
import { MatrixPosition } from "./MatrixPosition";

interface ReadingSectionProps {
  reading: ReadingResponse;
}

export function ReadingSection({ reading }: ReadingSectionProps) {
  return (
    <section className="space-y-5" aria-live="polite">
      <div className="rounded-lg border border-gold/30 bg-night/55 p-5">
        <p className="text-sm font-semibold uppercase tracking-[0.16em] text-gold">
          {reading.methodology_version}
        </p>
        <h2 className="mt-2 text-2xl font-bold">
          {reading.name ? `${reading.name}'s Matrix` : "Matrix Reading"}
        </h2>
        <p className="mt-3 leading-7 text-cream/78">{reading.summary}</p>
      </div>

      <MatrixChart positions={reading.positions} />

      {reading.warnings.map((warning) => (
        <p key={warning} className="rounded-lg border border-gold/30 bg-gold/10 p-4 text-sm text-cream">
          {warning}
        </p>
      ))}

      <div className="grid gap-4">
        {reading.positions.map((item) => (
          <MatrixPosition key={item.position.id} item={item} />
        ))}
      </div>

      <Disclaimer text={reading.disclaimer} />
    </section>
  );
}
