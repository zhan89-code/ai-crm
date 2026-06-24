"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"
import { AppShell } from "@/components/layout/app-shell"

export default function NewContactPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({ first_name: "", last_name: "", email: "", company: "" })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.contacts.create(formData)
      router.push("/contacts")
    } catch (err: any) {
      alert("Error saving contact: " + (err.message || err))
    }
  }

  return (
    <AppShell>
      <div className="max-w-xl mx-auto p-6 bg-white rounded-xl border border-gray-200">
        <h1 className="text-xl font-bold mb-4">Add New Contact</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input type="text" placeholder="First Name" className="w-full p-2 border rounded" onChange={e => setFormData({...formData, first_name: e.target.value})} />
          <input type="text" placeholder="Last Name" className="w-full p-2 border rounded" onChange={e => setFormData({...formData, last_name: e.target.value})} />
          <input type="email" placeholder="Email" className="w-full p-2 border rounded" onChange={e => setFormData({...formData, email: e.target.value})} />
          <input type="text" placeholder="Company" className="w-full p-2 border rounded" onChange={e => setFormData({...formData, company: e.target.value})} />
          <button type="submit" className="w-full py-2 bg-blue-600 text-white rounded">Save Contact</button>
        </form>
      </div>
    </AppShell>
  )
}
