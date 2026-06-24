const COLORS: Record<string, string> = { A: "bg-green-500", B: "bg-yellow-500", C: "bg-orange-500", D: "bg-red-500" }
const LABELS: Record<string, string> = { A: "Hot (80-100)", B: "Warm (60-79)", C: "Cool (40-59)", D: "Cold (0-39)" }
export function ScoreDistribution({ distribution }: { distribution: Record<string, number> }) {
  const total = Object.values(distribution).reduce((a, b) => a + b, 0) || 1
  return (<div className="space-y-3">{(["A","B","C","D"]).map((tier) => { const n = distribution[tier] || 0; const pct = Math.round((n / total) * 100); return (<div key={tier} className="flex items-center gap-3"><span className="w-28 text-sm text-gray-500">{LABELS[tier]}</span><div className="flex-1 h-6 bg-gray-100 rounded-full overflow-hidden"><div className={"h-full " + COLORS[tier] + " rounded-full transition-all"} style={{ width: pct + "%" }} /></div><span className="w-12 text-sm font-medium text-right">{n} ({pct}%)</span></div>) })}</div>)
}
