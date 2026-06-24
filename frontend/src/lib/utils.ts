import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatCurrency(value: number, currency = "USD") {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(value)
}

export function formatDate(date: string | Date) {
  return new Date(date).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
}

export function formatRelative(date: string | Date) {
  const now = new Date()
  const d = new Date(date)
  const diff = Math.floor((now.getTime() - d.getTime()) / 1000)
  if (diff < 60) return "just now"
  if (diff < 3600) return Math.floor(diff / 60) + "m ago"
  if (diff < 86400) return Math.floor(diff / 3600) + "h ago"
  if (diff < 604800) return Math.floor(diff / 86400) + "d ago"
  return formatDate(date)
}

export function scoreToTier(score: number): string {
  if (score >= 0.8) return "A"
  if (score >= 0.6) return "B"
  if (score >= 0.4) return "C"
  return "D"
}

export function tierColor(tier: string): string {
  const colors: Record<string, string> = {
    A: "bg-green-100 text-green-800 border-green-200",
    B: "bg-yellow-100 text-yellow-800 border-yellow-200",
    C: "bg-orange-100 text-orange-800 border-orange-200",
    D: "bg-red-100 text-red-800 border-red-200",
  }
  return colors[tier] || "bg-gray-100 text-gray-800 border-gray-200"
}
