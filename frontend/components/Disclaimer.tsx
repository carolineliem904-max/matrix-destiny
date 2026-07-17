interface DisclaimerProps {
  text: string;
}

export function Disclaimer({ text }: DisclaimerProps) {
  return (
    <aside className="rounded-lg border border-gold/30 bg-cream/10 p-4 text-sm leading-6 text-cream/88">
      {text}
    </aside>
  );
}
