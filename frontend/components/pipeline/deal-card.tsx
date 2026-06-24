import type { Deal } from "@/types"
import { formatCurrency } from "@/lib/utils"
export function DealCard({ deal, onClick }: { deal: Deal; onClick?: () => void }) {
  return (<div onClick={onClick} className="bg-white rounded-lg p-3 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer"><p className="font-medium text-sm">{deal.title}</p><p className="text-xs text-gray-500 mt-1">{deal.contact?.company || "No company"}</p><div className="flex items-center justify-between mt-3"><span className="text-sm font-semibold text-green-600">{formatCurrency(deal.value)}</span><div className="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-xs font-medium">{deal.contact?.first_name?.[0] || "?"}</div></div></div>)
}
