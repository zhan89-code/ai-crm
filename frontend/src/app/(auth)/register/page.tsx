"use client"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { useAuthStore } from "@/stores/auth-store"

export default function RegisterPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [fullName, setFullName] = useState("")
  const { register, isLoading, error } = useAuthStore()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await register(fullName, email, password)
    router.push("/dashboard")
  }

  return (
    <div className="bg-white p-8 rounded-lg shadow-md w-96">
      <h1 className="text-xl font-bold mb-4">Create Account</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input type="text" placeholder="Full Name" className="w-full p-2 border rounded" onChange={e => setFullName(e.target.value)} required />
        <input type="email" placeholder="Email" className="w-full p-2 border rounded" onChange={e => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" className="w-full p-2 border rounded" onChange={e => setPassword(e.target.value)} required />
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <button type="submit" disabled={isLoading} className="w-full py-2 bg-blue-600 text-white rounded">
          {isLoading ? "Loading..." : "Sign Up"}
        </button>
      </form>
    </div>
  )
}
