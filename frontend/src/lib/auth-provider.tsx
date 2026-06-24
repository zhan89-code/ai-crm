"use client"
import { useEffect } from "react"
import { useAuthStore } from "@/stores/auth-store"

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const fetchMe = useAuthStore((s) => s.fetchMe)
  const token = useAuthStore((s) => s.access_token)
  useEffect(() => {
    if (token) fetchMe()
  }, [token, fetchMe])
  return <>{children}</>
}
