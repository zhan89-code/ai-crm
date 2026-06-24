"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { useUIStore } from "@/stores/ui-store"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard, Users, UserCheck, GitFork, Mail,
  FileText, Settings, ChevronLeft, ChevronRight, BrainCircuit
} from "lucide-react"

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/contacts", label: "Contacts", icon: Users },
  { href: "/leads", label: "Leads", icon: UserCheck },
  { href: "/pipeline", label: "Pipeline", icon: GitFork },
  { href: "/sequences", label: "Sequences", icon: Mail },
  { href: "/templates", label: "Templates", icon: FileText },
  { href: "/settings", label: "Settings", icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()
  const { sidebarCollapsed, toggleSidebar } = useUIStore()

  return (
    <aside
      className={cn(
        "fixed left-0 top-0 z-40 h-screen bg-gray-900 text-white transition-all duration-300 flex flex-col",
        sidebarCollapsed ? "w-16" : "w-64"
      )}
    >
      <div className="flex items-center justify-between p-4 border-b border-gray-700">
        {!sidebarCollapsed && (
          <div className="flex items-center gap-2">
            <BrainCircuit className="w-6 h-6 text-blue-400" />
            <span className="font-bold text-lg">AI CRM</span>
          </div>
        )}
        <button onClick={toggleSidebar} className="p-1 rounded hover:bg-gray-700">
          {sidebarCollapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
        </button>
      </div>
      <nav className="flex-1 p-2 space-y-1">
        {navItems.map((item) => {
          const active = pathname.startsWith(item.href)
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
                active ? "bg-blue-600 text-white" : "text-gray-300 hover:bg-gray-700"
              )}
            >
              <item.icon className="w-5 h-5 shrink-0" />
              {!sidebarCollapsed && <span className="text-sm font-medium">{item.label}</span>}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
