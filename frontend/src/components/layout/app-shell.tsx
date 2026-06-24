"use client";

import { ReactNode } from "react";
import { useAuthStore } from "@/stores/auth-store";

export function AppShell({ children }: { children: ReactNode }) {
  const user = useAuthStore((s) => s.user);
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold">AI CRM</h1>
        {user && <span className="text-sm text-gray-600">{user.name}</span>}
      </header>
      <main className="p-6">{children}</main>
    </div>
  );
}
