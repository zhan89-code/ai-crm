import { ChevronLeft, ChevronRight } from "lucide-react"
interface Props { page: number; pageSize: number; total: number; onChange: (p: number) => void }
export function Pagination({ page, pageSize, total, onChange }: Props) {
  const totalPages = Math.ceil(total / pageSize)
  return (<div className="flex items-center justify-between"><span className="text-sm text-gray-500">Showing {(page-1)*pageSize+1}-{Math.min(page*pageSize, total)} of {total}</span><div className="flex gap-2"><button onClick={() => onChange(page-1)} disabled={page<=1} className="flex items-center gap-1 px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50 text-sm"><ChevronLeft className="w-4 h-4" />Prev</button><button onClick={() => onChange(page+1)} disabled={page>=totalPages} className="flex items-center gap-1 px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50 text-sm">Next<ChevronRight className="w-4 h-4" /></button></div></div>)
}
