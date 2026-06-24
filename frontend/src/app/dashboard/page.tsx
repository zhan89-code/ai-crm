"use client"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { AppShell } from "@/components/layout/app-shell"
import { formatCurrency } from "@/lib/utils"
import type { DashboardSummary } from "@/types"
import { DollarSign, Users, TrendingUp, Mail, BrainCircuit, Activity } from "lucide-react"

function StatCard({ title, value, icon: Icon, sub }: { title: string; value: string | number; icon: any; sub?: string }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <Icon className="w-6 h-6 text-blue-600" />
      </div>
    </div>
  )
}

export default function DashboardPage() {
  const { data } = useQuery({ queryKey: ["dashboard"], queryFn: () => api.dashboard.summary() })
  const d = data as DashboardSummary | undefined
  return (
    <AppShell>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div className="grid grid-cols-4 gap-4">
          <StatCard title="Pipeline Value" value={formatCurrency(d?.pipeline_value || 0)} icon={DollarSign} />
          <StatCard title="Leads Today" value={String(d?.leads_today || 0)} icon={Users} />
          <StatCard title="Avg Score" value={String(Math.round((d?.avg_score || 0) * 100))} icon={TrendingUp} />
          <StatCard title="Open Rate" value={Math.round((d?.email_metrics?.open_rate || 0) * 100) + "%"} icon={Mail} />
        </div>
      </div>
    </AppShell>
  )
}
