"use client"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { AppShell } from "@/components/layout/app-shell"
import { useState } from "react"
import type { Contact, PaginatedResponse } from "@/types"
import { Plus, Search, MoreHorizontal } from "lucide-react"

export default function ContactsPage() {
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState("")
  const { data, isLoading } = useQuery({
    queryKey: ["contacts", page, search],
    queryFn: () => api.contacts.list({ page, page_size: 20, search: search || undefined }) as Promise<PaginatedResponse<Contact>>,
  })
  const contacts = (data as PaginatedResponse<Contact> | undefined)?.items || []
  const total = (data as PaginatedResponse<Contact> | undefined)?.total || 0
  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div><h1 className="text-2xl font-bold">Contacts</h1><p className="text-gray-500">{total} total contacts</p></div>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"><Plus className="w-4 h-4" /> Add Contact</button>
        </div>
        <div className="bg-white rounded-xl border border-gray-200">
          <div className="p-4 border-b border-gray-200">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input type="text" placeholder="Search contacts..." value={search} onChange={(e) => setSearch(e.target.value)} className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>
          {isLoading ? <div className="p-8 text-center text-gray-500">Loading...</div> : (
            <table className="w-full">
              <thead><tr className="text-left text-sm text-gray-500 border-b border-gray-100">
                <th className="px-4 py-3 font-medium">Name</th><th className="px-4 py-3 font-medium">Email</th>
                <th className="px-4 py-3 font-medium">Company</th><th className="px-4 py-3 font-medium">Source</th>
                <th className="px-4 py-3 font-medium">Tags</th><th className="px-4 py-3 font-medium"></th>
              </tr></thead>
              <tbody>
                {contacts.map((c) => (
                  <tr key={c.id} className="border-b border-gray-50 hover:bg-gray-50">
                    <td className="px-4 py-3"><div className="flex items-center gap-3"><div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-sm font-medium">{c.first_name?.[0]}{c.last_name?.[0]}</div><span className="font-medium">{c.first_name} {c.last_name}</span></div></td>
                    <td className="px-4 py-3 text-gray-600">{c.email}</td>
                    <td className="px-4 py-3 text-gray-600">{c.company || "-"}</td>
                    <td className="px-4 py-3">{c.source && <span className="px-2 py-0.5 bg-gray-100 rounded text-xs">{c.source}</span>}</td>
                    <td className="px-4 py-3"><div className="flex gap-1">{c.tags?.slice(0, 2).map((t) => (<span key={t} className="px-2 py-0.5 bg-blue-50 text-blue-600 rounded text-xs">{t}</span>))}</div></td>
                    <td className="px-4 py-3"><button className="p-1 hover:bg-gray-100 rounded"><MoreHorizontal className="w-4 h-4" /></button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          <div className="p-4 border-t border-gray-200 flex items-center justify-between">
            <span className="text-sm text-gray-500">Showing {contacts.length} of {total}</span>
            <div className="flex gap-2">
              <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page <= 1} className="px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50">Previous</button>
              <button onClick={() => setPage((p) => p + 1)} disabled={contacts.length < 20} className="px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50">Next</button>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  )
}
