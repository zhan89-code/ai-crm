"use client"
import { useAuthStore } from "@/stores/auth-store"
import { useUIStore } from "@/stores/ui-store"
import { Sidebar } from "./sidebar"
import { Header } from "./header"
import { cn } from "@/lib/utils"
import { redirect } from "next/navigation"
import { useEffect } from "react"

export function AppShell({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((s) => s.access_token)
  const { sidebarCollapsed } = useUIStore()

  useEffect(() => {
    if (!token) redirect("/login")
  }, [token])

  if (!token) return null

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className={cn("transition-all duration-300", sidebarCollapsed ? "ml-16" : "ml-64")}>
        <Header />
        <main className="p-6">{children}</main>
      </div>
    </div>
  )
}
