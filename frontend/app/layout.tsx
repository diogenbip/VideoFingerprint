import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Header } from "../src/shared/ui/Header/Header";
import { ToastNotificationProvider } from "../src/shared/hooks/useToast";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Video Similarity Finder",
  description: "Video Similarity Finder by debug_dream_team",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ToastNotificationProvider>
          <Header />
          {children}
        </ToastNotificationProvider>
      </body>
    </html>
  );
}
