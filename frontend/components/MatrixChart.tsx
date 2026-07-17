import type { InterpretedPosition } from "@/lib/types";

interface MatrixChartProps {
  positions: InterpretedPosition[];
}

export function MatrixChart({ positions }: MatrixChartProps) {
  const chartPositions = positions.filter((item) => item.position.coordinates);

  return (
    <figure className="rounded-lg border border-cream/15 bg-night/55 p-4 shadow-glow">
      <svg viewBox="0 0 100 100" role="img" aria-label="Destiny Matrix chart" className="aspect-square w-full">
        <defs>
          <linearGradient id="matrixLine" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0%" stopColor="#d9b56d" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#fff7e8" stopOpacity="0.45" />
          </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="35" fill="none" stroke="rgba(255, 247, 232, 0.22)" strokeWidth="0.8" />
        <path d="M50 16 L78 32 L78 68 L50 84 L22 68 L22 32 Z" fill="rgba(255, 247, 232, 0.04)" stroke="url(#matrixLine)" strokeWidth="0.8" />
        <path d="M50 16 L50 84 M22 32 L78 68 M78 32 L22 68" stroke="rgba(217, 181, 109, 0.42)" strokeWidth="0.6" />
        {chartPositions.map(({ position }) => (
          <g key={position.id}>
            <circle
              cx={position.coordinates?.x}
              cy={position.coordinates?.y}
              r={position.id === "center" ? 8 : 6}
              fill={position.verified ? "#d9b56d" : "#fff7e8"}
              stroke="#d9b56d"
              strokeWidth="1"
            />
            <text
              x={position.coordinates?.x}
              y={(position.coordinates?.y ?? 0) + 1.4}
              textAnchor="middle"
              className="fill-night text-[5px] font-bold"
            >
              {position.value}
            </text>
          </g>
        ))}
      </svg>
      <figcaption className="mt-3 text-sm text-cream/70">
        Placeholder chart positions are visible, but formulas are not verified yet.
      </figcaption>
    </figure>
  );
}
