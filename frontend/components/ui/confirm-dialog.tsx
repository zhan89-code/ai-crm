"use client"
import { AlertTriangle } from "lucide-react"
interface Props { open: boolean; onClose: () => void; onConfirm: () => void; title: string; description: string; confirmLabel?: string; destructive?: boolean }
export function ConfirmDialog({ open, onClose, onConfirm, title, description, confirmLabel = "Confirm", destructive }: Props) {
  if (!open) return null
  return (<div className="fixed inset-0 z-50 flex items-center justify-center"><div className="absolute inset-0 bg-black/50" onClick={onClose} /><div className="relative bg-white rounded-2xl shadow-xl w-full max-w-md mx-4 p-6"><div className="flex items-center gap-3 mb-4"><div className={"w-10 h-10 rounded-full flex items-center justify-center " + (destructive ? "bg-red-100" : "bg-yellow-100")}><AlertTriangle className={"w-5 h-5 " + (destructive ? "text-red-600" : "text-yellow-600")} /></div><h2 className="text-lg font-semibold">{title}</h2></div><p className="text-gray-600 mb-6">{description}</p><div className="flex gap-3 justify-end"><button onClick={onClose} className="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancel</button><button onClick={() => { onConfirm(); onClose() }} className={"px-4 py-2 rounded-lg text-white " + (destructive ? "bg-red-600 hover:bg-red-700" : "bg-blue-600 hover:bg-blue-700")}>{confirmLabel}</button></div></div></div>)
}
