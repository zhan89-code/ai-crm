"use client"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { AppShell } from "@/components/layout/app-shell"
import { formatCurrency } from "@/lib/utils"
import type { Deal } from "@/types"
import { Plus, DollarSign } from "lucide-react"

const STAGES = ["prospecting", "qualification", "proposal", "negotiation", "closed_won", "closed_lost"]
const COLORS = { prospecting: "border-t-gray-400", qualification: "border-t-blue-400", proposal: "border-t-yellow-400", negotiation: "border-t-orange-400", closed_won: "border-t-green-500", closed_lost: "border-t-red-500" }

export default function PipelinePage() {
  const { data, isLoading } = useQuery({ queryKey: ["deals"], queryFn: () => api.deals.list({ page: 1, page_size: 200 }) })
  const deals: Deal[] = (data as any)?.items || []
  const byStage = STAGES.reduce((acc, s) => { acc[s] = deals.filter((d) => d.stage === s); return acc }, {} as Record<string, Deal[]>)
  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex items-center justify-between"><div><h1 className="text-2xl font-bold">Pipeline</h1><p className="text-gray-500">{deals.length} total deals</p></div>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"><Plus className="w-4 h-4" /> New Deal</button>
        </div>
        {isLoading ? <div className="text-center text-gray-500 py-12">Loading...</div> : (
          <div className="flex gap-4 overflow-x-auto pb-4">
            {STAGES.map((stage) => (
              <div key={stage} className={"min-w-[280px] flex-1 bg-gray-50 rounded-xl border-t-4 " + COLORS[stage]}>
                <div className="p-4 border-b border-gray-200"><div className="flex items-center justify-between"><h3 className="font-semibold text-sm capitalize">{stage.replace("_", " ")}</h3><span className="text-xs text-gray-500 bg-gray-200 px-2 py-0.5 rounded-full">{byStage[stage]?.length || 0}</span></div></div>
                <div className="p-2 space-y-2">{(byStage[stage] || []).map((deal) => (<div key={deal.id} className="bg-white rounded-lg p-3 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer"><p className="font-medium text-sm">{deal.title}</p><p className="text-xs text-gray-500 mt-1">{deal.contact?.company || "No company"}</p><div className="flex items-center justify-between mt-3"><div className="flex items-center gap-1 text-sm font-semibold text-green-600"><DollarSign className="w-3 h-3" />{formatCurrency(deal.value)}</div></div></div>))}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  )
}
