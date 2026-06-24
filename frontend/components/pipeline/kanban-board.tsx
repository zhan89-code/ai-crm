"use client"
import type { Deal } from "@/types"
import { formatCurrency } from "@/lib/utils"
const STAGES = ["prospecting", "qualification", "proposal", "negotiation", "closed_won", "closed_lost"]
const COLORS: Record<string, string> = { prospecting: "border-t-gray-400", qualification: "border-t-blue-400", proposal: "border-t-yellow-400", negotiation: "border-t-orange-400", closed_won: "border-t-green-500", closed_lost: "border-t-red-500" }
export function KanbanBoard({ deals, onDealClick }: { deals: Deal[]; onDealClick?: (d: Deal) => void }) {
  const byStage = STAGES.reduce((acc, s) => { acc[s] = deals.filter((d) => d.stage === s); return acc }, {} as Record<string, Deal[]>)
  return (<div className="flex gap-4 overflow-x-auto pb-4">{STAGES.map((stage) => (<div key={stage} className={"min-w-[280px] flex-1 bg-gray-50 rounded-xl border-t-4 " + COLORS[stage]}><div className="p-4 border-b border-gray-200"><div className="flex items-center justify-between"><h3 className="font-semibold text-sm capitalize">{stage.replace("_", " ")}</h3><span className="text-xs text-gray-500 bg-gray-200 px-2 py-0.5 rounded-full">{byStage[stage]?.length || 0}</span></div></div><div className="p-2 space-y-2">{(byStage[stage] || []).map((deal) => (<div key={deal.id} onClick={() => onDealClick?.(deal)} className="bg-white rounded-lg p-3 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer"><p className="font-medium text-sm">{deal.title}</p><p className="text-xs text-gray-500 mt-1">{deal.contact?.company || "No company"}</p><p className="text-sm font-semibold text-green-600 mt-2">{formatCurrency(deal.value)}</p></div>))}</div></div>))}</div>)
}
