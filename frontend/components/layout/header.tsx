"use client"
import { useAuthStore } from "@/stores/auth-store"
import { useUIStore } from "@/stores/ui-store"
import { Search, Bell, LogOut } from "lucide-react"

export function Header() {
  const { user, logout } = useAuthStore()
  const { setGlobalSearchOpen } = useUIStore()

  return (
    <header className="h-16 border-b border-gray-200 bg-white flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <button
          onClick={() => setGlobalSearchOpen(true)}
          className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 rounded-lg text-sm text-gray-500 hover:bg-gray-200"
        >
          <Search className="w-4 h-4" />
          <span>Search...</span>
          <kbd className="ml-4 px-1.5 py-0.5 bg-white rounded text-xs border">Cmd+K</kbd>
        </button>
      </div>
      <div className="flex items-center gap-4">
        <button className="relative p-2 rounded-lg hover:bg-gray-100">
          <Bell className="w-5 h-5 text-gray-600" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-medium">
            {user?.full_name?.charAt(0) || "U"}
          </div>
          <span className="text-sm font-medium text-gray-700">{user?.full_name || "User"}</span>
        </div>
        <button onClick={logout} className="p-2 rounded-lg hover:bg-gray-100 text-gray-500">
          <LogOut className="w-5 h-5" />
        </button>
      </div>
    </header>
  )
}
