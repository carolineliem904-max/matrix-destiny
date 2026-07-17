import type { LanguageCode } from "@/lib/types";

interface LanguageSwitcherProps {
  value: LanguageCode;
  onChange: (language: LanguageCode) => void;
}

export function LanguageSwitcher({ value, onChange }: LanguageSwitcherProps) {
  return (
    <div className="inline-flex rounded-lg border border-cream/20 bg-night/50 p-1" aria-label="Language">
      {(["en", "id"] as const).map((language) => (
        <button
          key={language}
          type="button"
          onClick={() => onChange(language)}
          className={`rounded-md px-4 py-2 text-sm font-semibold transition ${
            value === language
              ? "bg-gold text-night"
              : "text-cream/80 hover:bg-cream/10 hover:text-cream"
          }`}
          aria-pressed={value === language}
        >
          {language.toUpperCase()}
        </button>
      ))}
    </div>
  );
}
