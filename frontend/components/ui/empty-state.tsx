interface Props { title: string; description: string; action?: React.ReactNode; icon?: React.ElementType }
export function EmptyState({ title, description, action, icon: Icon }: Props) {
  return (<div className="text-center py-12">{Icon && <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4"><Icon className="w-8 h-8 text-gray-400" /></div>}<h3 className="font-semibold text-gray-700">{title}</h3><p className="text-sm text-gray-500 mt-1">{description}</p>{action && <div className="mt-4">{action}</div>}</div>)
}
