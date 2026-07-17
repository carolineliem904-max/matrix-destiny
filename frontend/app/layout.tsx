import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Matrix Destiny",
  description: "Bilingual deterministic Destiny Matrix MVP for reflection and education."
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
