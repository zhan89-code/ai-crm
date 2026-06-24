"use client"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { AppShell } from "@/components/layout/app-shell"
import type { DSARRequest } from "@/types"
import { Shield, Clock, CheckCircle, XCircle } from "lucide-react"

export default function CompliancePage() {
  const { data, isLoading } = useQuery({ queryKey: ["dsar"], queryFn: () => api.compliance.dsarList({ page: 1, page_size: 50 }) })
  const requests: DSARRequest[] = (data as any)?.items || []
  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex items-center gap-3"><Shield className="w-6 h-6 text-blue-600" /><div><h1 className="text-2xl font-bold">Compliance & DSAR</h1><p className="text-gray-500">Manage data subject access requests</p></div></div>
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white rounded-xl border p-6"><div className="flex items-center gap-2"><Clock className="w-5 h-5 text-yellow-500" /><span className="text-sm text-gray-500">Pending</span></div><p className="text-2xl font-bold mt-2">{requests.filter((r) => r.status === "pending").length}</p></div>
          <div className="bg-white rounded-xl border p-6"><div className="flex items-center gap-2"><CheckCircle className="w-5 h-5 text-green-500" /><span className="text-sm text-gray-500">Completed</span></div><p className="text-2xl font-bold mt-2">{requests.filter((r) => r.status === "completed").length}</p></div>
          <div className="bg-white rounded-xl border p-6"><div className="flex items-center gap-2"><XCircle className="w-5 h-5 text-red-500" /><span className="text-sm text-gray-500">Rejected</span></div><p className="text-2xl font-bold mt-2">{requests.filter((r) => r.status === "rejected").length}</p></div>
        </div>
        <div className="bg-white rounded-xl border border-gray-200">
          {isLoading ? <div className="p-8 text-center text-gray-500">Loading...</div> : (
            <table className="w-full"><thead><tr className="text-left text-sm text-gray-500 border-b"><th className="px-4 py-3">Requester</th><th className="px-4 py-3">Type</th><th className="px-4 py-3">Status</th><th className="px-4 py-3">Date</th></tr></thead>
            <tbody>{requests.map((r) => (<tr key={r.id} className="border-b hover:bg-gray-50"><td className="px-4 py-3">{r.requester_email}</td><td className="px-4 py-3 capitalize">{r.request_type}</td><td className="px-4 py-3"><span className={"px-2 py-0.5 rounded text-xs " + (r.status === "completed" ? "bg-green-100 text-green-700" : r.status === "pending" ? "bg-yellow-100 text-yellow-700" : "bg-red-100 text-red-700")}>{r.status}</span></td><td className="px-4 py-3 text-sm text-gray-500">{new Date(r.created_at).toLocaleDateString()}</td></tr>))}</tbody></table>
          )}
        </div>
      </div>
    </AppShell>
  )
}
