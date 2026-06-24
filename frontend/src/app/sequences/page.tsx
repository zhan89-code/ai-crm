"use client"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { AppShell } from "@/components/layout/app-shell"
import type { EmailSequence } from "@/types"
import { Plus, Play, Pause, Mail, Users } from "lucide-react"

export default function SequencesPage() {
  const { data, isLoading } = useQuery({ queryKey: ["sequences"], queryFn: () => api.sequences.list({ page: 1, page_size: 50 }) })
  const sequences: EmailSequence[] = (data as any)?.items || []
  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex items-center justify-between"><div><h1 className="text-2xl font-bold">Email Sequences</h1><p className="text-gray-500">{sequences.length} sequences</p></div>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"><Plus className="w-4 h-4" /> New Sequence</button>
        </div>
        {isLoading ? <div className="text-center text-gray-500 py-12">Loading...</div> : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {sequences.map((seq) => (
              <div key={seq.id} className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3"><div className={"w-10 h-10 rounded-lg flex items-center justify-center " + (seq.is_active ? "bg-green-100" : "bg-gray-100")}>{seq.is_active ? <Play className="w-5 h-5 text-green-600" /> : <Pause className="w-5 h-5 text-gray-400" />}</div><div><h3 className="font-semibold">{seq.name}</h3><p className="text-xs text-gray-500 capitalize">{seq.trigger_type.replace("_", " ")}</p></div></div>
                  <span className={"px-2 py-0.5 rounded text-xs font-medium " + (seq.is_active ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500")}>{seq.is_active ? "Active" : "Paused"}</span>
                </div>
                <div className="mt-4 flex items-center gap-4 text-sm text-gray-500"><div className="flex items-center gap-1"><Mail className="w-4 h-4" />{seq.step_count || 0} steps</div><div className="flex items-center gap-1"><Users className="w-4 h-4" />{seq.enrolled_count || 0} enrolled</div></div>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  )
}
