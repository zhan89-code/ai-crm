"use client"
import { AppShell } from "@/components/layout/app-shell"
import { Shield, Link2, Users, Bell, CreditCard } from "lucide-react"
import Link from "next/link"

const sections = [
  { href: "/settings/compliance", label: "Compliance & DSAR", desc: "GDPR/CCPA requests, data retention", icon: Shield },
  { href: "/settings/integrations", label: "Integrations", desc: "Connect HubSpot, Salesforce, Pipedrive", icon: Link2 },
  { href: "/settings/team", label: "Team Management", desc: "Invite members, manage roles", icon: Users },
  { href: "/settings/notifications", label: "Notifications", desc: "Email, webhook, and in-app alerts", icon: Bell },
  { href: "/settings/billing", label: "Billing", desc: "Subscription, usage, invoices", icon: CreditCard },
]

export default function SettingsPage() {
  return (
    <AppShell>
      <div className="space-y-6">
        <div><h1 className="text-2xl font-bold">Settings</h1><p className="text-gray-500">Manage your CRM configuration</p></div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sections.map((s) => (
            <Link key={s.href} href={s.href} className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow flex items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center"><s.icon className="w-5 h-5 text-blue-600" /></div>
              <div><h3 className="font-semibold">{s.label}</h3><p className="text-sm text-gray-500 mt-1">{s.desc}</p></div>
            </Link>
          ))}
        </div>
      </div>
    </AppShell>
  )
}
