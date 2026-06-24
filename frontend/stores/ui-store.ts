import { create } from "zustand"

interface UIState {
  sidebarCollapsed: boolean
  globalSearchOpen: boolean
  toggleSidebar: () => void
  setGlobalSearchOpen: (open: boolean) => void
}

export const useUIStore = create<UIState>((set) => ({
  sidebarCollapsed: false,
  globalSearchOpen: false,
  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
  setGlobalSearchOpen: (open) => set({ globalSearchOpen: open }),
}))
