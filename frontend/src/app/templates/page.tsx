"use client"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { AppShell } from "@/components/layout/app-shell"
import type { EmailTemplate } from "@/types"
import { Plus, Copy, Edit } from "lucide-react"

export default function TemplatesPage() {
  const { data, isLoading } = useQuery({ queryKey: ["templates"], queryFn: () => api.templates.list({ page: 1, page_size: 50 }) })
  const templates: EmailTemplate[] = (data as any)?.items || []
  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex items-center justify-between"><div><h1 className="text-2xl font-bold">Email Templates</h1><p className="text-gray-500">{templates.length} templates</p></div>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"><Plus className="w-4 h-4" /> New Template</button>
        </div>
        {isLoading ? <div className="text-center text-gray-500 py-12">Loading...</div> : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {templates.map((t) => (
              <div key={t.id} className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between"><h3 className="font-semibold">{t.name}</h3><div className="flex gap-1"><button className="p-1 hover:bg-gray-100 rounded"><Copy className="w-4 h-4 text-gray-400" /></button><button className="p-1 hover:bg-gray-100 rounded"><Edit className="w-4 h-4 text-gray-400" /></button></div></div>
                <p className="text-sm text-gray-500 mt-2">{t.subject}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  )
}
