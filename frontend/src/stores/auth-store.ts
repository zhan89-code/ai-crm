import { create } from "zustand"
import { api } from "@/lib/api"
import type { User } from "@/types"

interface AuthState {
  user: User | null
  access_token: string | null
  refresh_token: string | null
  isLoading: boolean
  error: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  fetchMe: () => Promise<void>
  clearError: () => void
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  access_token: typeof window !== "undefined" ? localStorage.getItem("access_token") : null,
  refresh_token: typeof window !== "undefined" ? localStorage.getItem("refresh_token") : null,
  isLoading: false,
  error: null,

  login: async (email, password) => {
    set({ isLoading: true, error: null })
    try {
      const res = await api.auth.login({ email, password })
      localStorage.setItem("access_token", res.access_token)
      localStorage.setItem("refresh_token", res.refresh_token)
      const user = await api.auth.me()
      set({ user, access_token: res.access_token, refresh_token: res.refresh_token, isLoading: false })
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Login failed"
      set({ error: message, isLoading: false })
    }
  },

  logout: () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    set({ user: null, access_token: null, refresh_token: null })
  },

  fetchMe: async () => {
    try {
      const user = await api.auth.me()
      set({ user })
    } catch {
      get().logout()
    }
  },

  clearError: () => set({ error: null }),
}))
