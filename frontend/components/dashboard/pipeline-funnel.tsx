import type { Deal } from "@/types"
import { formatCurrency } from "@/lib/utils"
const STAGES = ["prospecting", "qualification", "proposal", "negotiation", "closed_won"]
export function PipelineFunnel({ deals }: { deals: Deal[] }) {
  const byStage = STAGES.map((s) => ({ stage: s, items: deals.filter((d) => d.stage === s), value: deals.filter((d) => d.stage === s).reduce((a, d) => a + (d.value || 0), 0) }))
  const max = Math.max(...byStage.map((s) => s.items.length), 1)
  return (<div className="space-y-3">{byStage.map((s) => (<div key={s.stage} className="flex items-center gap-3"><span className="w-24 text-sm text-gray-500 capitalize truncate">{s.stage.replace("_", " ")}</span><div className="flex-1 h-8 bg-gray-100 rounded overflow-hidden"><div className="h-full bg-blue-500 rounded flex items-center px-2" style={{ width: (s.items.length / max) * 100 + "%" }}><span className="text-xs text-white font-medium">{s.items.length}</span></div></div><span className="w-20 text-sm text-gray-500 text-right">{formatCurrency(s.value)}</span></div>))}</div>)
}
