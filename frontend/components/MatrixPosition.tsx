import type { InterpretedPosition } from "@/lib/types";

interface MatrixPositionProps {
  item: InterpretedPosition;
}

export function MatrixPosition({ item }: MatrixPositionProps) {
  const { position, role, energy } = item;

  return (
    <article className="rounded-lg border border-cream/15 bg-cream/95 p-4 text-night">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-bold">{role?.label ?? position.label}</h3>
          <p className="mt-1 text-sm text-night/70">{role?.description}</p>
        </div>
        <span className="rounded-md bg-plum px-3 py-1 text-sm font-bold text-cream">
          {position.value}
        </span>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-night/50">
            Positive
          </p>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-night/75">
            {(energy?.positive_expression ?? ["Awaiting verified formula and matching energy."]).map((text) => (
              <li key={text}>{text}</li>
            ))}
          </ul>
        </div>
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-night/50">
            Shadow
          </p>
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-night/75">
            {(energy?.shadow_expression ?? ["No final interpretation is attached to placeholder value 0."]).map((text) => (
              <li key={text}>{text}</li>
            ))}
          </ul>
        </div>
      </div>

      <details className="mt-4 rounded-md bg-night/5 p-3">
        <summary className="cursor-pointer text-sm font-bold">Calculation trace</summary>
        <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-night/70">
          {position.calculation_trace.map((trace) => (
            <li key={trace}>{trace}</li>
          ))}
        </ul>
      </details>
    </article>
  );
}
