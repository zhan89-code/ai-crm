"use client"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { AppShell } from "@/components/layout/app-shell"
import { useState } from "react"
import type { Lead, PaginatedResponse } from "@/types"
import { tierColor } from "@/lib/utils"
import { Zap, Filter, MoreHorizontal } from "lucide-react"

export default function LeadsPage() {
  const [page, setPage] = useState(1)
  const [statusFilter, setStatusFilter] = useState("")
  const [scoreFilter, setScoreFilter] = useState("")
  const qc = useQueryClient()
  const { data, isLoading } = useQuery({
    queryKey: ["leads", page, statusFilter, scoreFilter],
    queryFn: () => api.leads.list({ page, page_size: 20, status: statusFilter || undefined, min_score: scoreFilter ? parseFloat(scoreFilter) : undefined }) as Promise<PaginatedResponse<Lead>>,
  })
  const scoreMutation = useMutation({ mutationFn: (id: string) => api.leads.score(id), onSuccess: () => qc.invalidateQueries({ queryKey: ["leads"] }) })
  const leads = (data as PaginatedResponse<Lead> | undefined)?.items || []
  const total = (data as PaginatedResponse<Lead> | undefined)?.total || 0
  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex items-center justify-between"><div><h1 className="text-2xl font-bold">Leads</h1><p className="text-gray-500">{total} total leads</p></div></div>
        <div className="flex gap-3">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-gray-400" />
            <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="border border-gray-200 rounded-lg px-3 py-2 text-sm"><option value="">All Status</option><option value="new">New</option><option value="contacted">Contacted</option><option value="qualified">Qualified</option><option value="converted">Converted</option><option value="lost">Lost</option></select>
            <select value={scoreFilter} onChange={(e) => setScoreFilter(e.target.value)} className="border border-gray-200 rounded-lg px-3 py-2 text-sm"><option value="">All Scores</option><option value="0.8">A (80%+)</option><option value="0.6">B (60%+)</option><option value="0.4">C (40%+)</option></select>
          </div>
        </div>
        <div className="bg-white rounded-xl border border-gray-200">
          {isLoading ? <div className="p-8 text-center text-gray-500">Loading...</div> : (
            <table className="w-full">
              <thead><tr className="text-left text-sm text-gray-500 border-b border-gray-100">
                <th className="px-4 py-3 font-medium">Lead</th><th className="px-4 py-3 font-medium">Company</th>
                <th className="px-4 py-3 font-medium">Score</th><th className="px-4 py-3 font-medium">Tier</th>
                <th className="px-4 py-3 font-medium">Status</th><th className="px-4 py-3 font-medium">Source</th>
                <th className="px-4 py-3 font-medium"></th>
              </tr></thead>
              <tbody>
                {leads.map((l) => (
                  <tr key={l.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="px-4 py-3"><div className="flex items-center gap-3"><div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 text-sm font-medium">{l.contact?.first_name?.[0] || "?"}{l.contact?.last_name?.[0] || "?"}</div><div><span className="font-medium">{l.contact?.first_name} {l.contact?.last_name}</span><p className="text-xs text-gray-400">{l.contact?.email}</p></div></div></td>
                    <td className="px-4 py-3 text-gray-600">{l.contact?.company || "-"}</td>
                    <td className="px-4 py-3">{l.score !== undefined ? (<div className="flex items-center gap-2"><div className="w-16 h-2 bg-gray-100 rounded-full overflow-hidden"><div className="h-full bg-blue-500 rounded-full" style={{ width: Math.round(l.score * 100) + "%" }} /></div><span className="text-sm font-medium">{Math.round(l.score * 100)}</span></div>) : (<button onClick={() => scoreMutation.mutate(l.id)} className="flex items-center gap-1 text-xs text-blue-600 hover:text-blue-700"><Zap className="w-3 h-3" /> Score</button>)}</td>
                    <td className="px-4 py-3">{l.score_label && (<span className={"px-2 py-0.5 rounded text-xs font-medium border " + tierColor(l.score_label)}>{l.score_label}</span>)}</td>
                    <td className="px-4 py-3"><span className="px-2 py-0.5 bg-gray-100 rounded text-xs capitalize">{l.status}</span></td>
                    <td className="px-4 py-3 text-gray-500 text-sm">{l.source || "-"}</td>
                    <td className="px-4 py-3"><button className="p-1 hover:bg-gray-100 rounded"><MoreHorizontal className="w-4 h-4" /></button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </AppShell>
  )
}
