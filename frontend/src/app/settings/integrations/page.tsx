"use client"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { AppShell } from "@/components/layout/app-shell"
import type { CRMIntegration } from "@/types"
import { Link2, CheckCircle, XCircle } from "lucide-react"

const AVAILABLE = [
  { id: "hubspot", name: "HubSpot", desc: "Sync contacts, deals, and companies", color: "bg-orange-100 text-orange-600" },
  { id: "salesforce", name: "Salesforce", desc: "Bi-directional sync with Sales Cloud", color: "bg-blue-100 text-blue-600" },
  { id: "pipedrive", name: "Pipedrive", desc: "Import deals and contacts", color: "bg-green-100 text-green-600" },
]

export default function IntegrationsPage() {
  const { data } = useQuery({ queryKey: ["integrations"], queryFn: () => api.integrations.list() })
  const active: CRMIntegration[] = (data as any) || []
  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex items-center gap-3"><Link2 className="w-6 h-6 text-blue-600" /><div><h1 className="text-2xl font-bold">Integrations</h1><p className="text-gray-500">Connect your favorite CRM tools</p></div></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {AVAILABLE.map((intg) => {
            const isActive = active.some((a) => a.provider === intg.id && a.is_active)
            return (<div key={intg.id} className="bg-white rounded-xl border border-gray-200 p-6">
              <div className="flex items-start justify-between"><div className={"w-12 h-12 rounded-lg " + intg.color + " flex items-center justify-center font-bold text-lg"}>{intg.name[0]}</div>{isActive ? <CheckCircle className="w-5 h-5 text-green-500" /> : <XCircle className="w-5 h-5 text-gray-300" />}</div>
              <h3 className="font-semibold mt-4">{intg.name}</h3><p className="text-sm text-gray-500 mt-1">{intg.desc}</p>
              <button className={"mt-4 w-full py-2 rounded-lg text-sm font-medium " + (isActive ? "bg-gray-100 text-gray-600 hover:bg-gray-200" : "bg-blue-600 text-white hover:bg-blue-700")}>{isActive ? "Manage" : "Connect"}</button>
            </div>)
          })}
        </div>
      </div>
    </AppShell>
  )
}
