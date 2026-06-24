import type { EmailSequence } from "@/types"
export function SequenceStats({ sequence }: { sequence: EmailSequence }) {
  const cards = [{ label: "Enrolled", value: sequence.enrolled_count || 0 }, { label: "Steps", value: sequence.step_count || 0 }, { label: "Completion", value: sequence.completion_rate ? Math.round(sequence.completion_rate * 100) + "%" : "-" }, { label: "Conversion", value: sequence.conversion_rate ? Math.round(sequence.conversion_rate * 100) + "%" : "-" }]
  return (<div className="grid grid-cols-2 md:grid-cols-4 gap-4">{cards.map((c) => (<div key={c.label} className="bg-white rounded-lg border p-4 text-center"><p className="text-2xl font-bold">{c.value}</p><p className="text-xs text-gray-500">{c.label}</p></div>))}</div>)
}
