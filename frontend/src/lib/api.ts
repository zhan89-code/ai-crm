
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export class ApiError extends Error {
  status: number
  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null
  const headers: Record<string, string> = { "Content-Type": "application/json" }
  if (token) headers["Authorization"] = "Bearer " + token
  const res = await fetch(API_BASE + path, { ...options, headers: { ...headers, ...options.headers } })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new ApiError(body.detail || res.statusText, res.status)
  }
  if (res.status === 204) return {} as T
  return res.json()
}

function qs(params?: Record<string, unknown>): string {
  if (!params) return ""
  const sp = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null) sp.set(k, String(v))
  }
  const s = sp.toString()
  return s ? "?" + s : ""
}

export const api = {
  auth: {
    login: (data: { email: string; password: string }) =>
      request<{ access_token: string; refresh_token: string; expires_in: number }>("/api/v1/auth/login", { method: "POST", body: JSON.stringify(data) }),
    register: (data: { name: string; slug: string; plan?: string }) =>
      request("/api/v1/auth/register", { method: "POST", body: JSON.stringify(data) }),
    me: () => request("/api/v1/auth/me"),
    refresh: (token: string) =>
      request("/api/v1/auth/refresh", { method: "POST", body: JSON.stringify({ refresh_token: token }) }),
  },
  contacts: {
    list: (params?: { page?: number; page_size?: number; search?: string; tag?: string }) =>
      request("/api/v1/contacts" + qs(params)),
    get: (id: string) => request("/api/v1/contacts/" + id),
    create: (data: Record<string, unknown>) =>
      request("/api/v1/contacts", { method: "POST", body: JSON.stringify(data) }),
    update: (id: string, data: Record<string, unknown>) =>
      request("/api/v1/contacts/" + id, { method: "PUT", body: JSON.stringify(data) }),
    delete: (id: string) => request("/api/v1/contacts/" + id, { method: "DELETE" }),
  },
  leads: {
    list: (params?: { page?: number; page_size?: number; status?: string; min_score?: number }) =>
      request("/api/v1/leads" + qs(params)),
    get: (id: string) => request("/api/v1/leads/" + id),
    create: (data: Record<string, unknown>) =>
      request("/api/v1/leads", { method: "POST", body: JSON.stringify(data) }),
    score: (id: string) => request("/api/v1/leads/" + id + "/score", { method: "POST" }),
    convert: (id: string) => request("/api/v1/leads/" + id + "/convert", { method: "POST" }),
  },
  deals: {
    list: (params?: { page?: number; page_size?: number; stage?: string }) =>
      request("/api/v1/deals" + qs(params)),
    get: (id: string) => request("/api/v1/deals/" + id),
    create: (data: Record<string, unknown>) =>
      request("/api/v1/deals", { method: "POST", body: JSON.stringify(data) }),
    update: (id: string, data: Record<string, unknown>) =>
      request("/api/v1/deals/" + id, { method: "PUT", body: JSON.stringify(data) }),
    updateStage: (id: string, data: { stage: string; probability?: number }) =>
      request("/api/v1/deals/" + id + "/stage", { method: "PATCH", body: JSON.stringify(data) }),
    delete: (id: string) => request("/api/v1/deals/" + id, { method: "DELETE" }),
  },
  sequences: {
    list: (params?: { page?: number; page_size?: number; status?: string }) =>
      request("/api/v1/sequences" + qs(params)),
    get: (id: string) => request("/api/v1/sequences/" + id),
    create: (data: Record<string, unknown>) =>
      request("/api/v1/sequences", { method: "POST", body: JSON.stringify(data) }),
    templates: (params?: { page?: number; page_size?: number }) =>
      request("/api/v1/sequences/templates" + qs(params)),
    createTemplate: (data: Record<string, unknown>) =>
      request("/api/v1/sequences/templates", { method: "POST", body: JSON.stringify(data) }),
    enroll: (id: string, contactId: string) =>
      request("/api/v1/sequences/" + id + "/enroll", { method: "POST", body: JSON.stringify({ contact_id: contactId }) }),
  },
  dashboard: {
    summary: () => request("/api/v1/dashboard/summary"),
  },
  integrations: {
    list: () => request("/api/v1/integrations"),
    create: (data: Record<string, unknown>) =>
      request("/api/v1/integrations", { method: "POST", body: JSON.stringify(data) }),
    sync: (id: string) => request("/api/v1/integrations/" + id + "/sync", { method: "POST" }),
  },
  ai: {
    modelStatus: () => request("/api/v1/model/status"),
    retrain: () => request("/api/v1/model/retrain", { method: "POST" }),
  },
  compliance: {
    dsarList: (params?: { page?: number; page_size?: number; status?: string }) =>
      request("/api/v1/compliance/dsar" + qs(params)),
    dsarCreate: (data: Record<string, unknown>) =>
      request("/api/v1/compliance/dsar", { method: "POST", body: JSON.stringify(data) }),
    dsarUpdate: (id: string, data: Record<string, unknown>) =>
      request("/api/v1/compliance/dsar/" + id, { method: "PUT", body: JSON.stringify(data) }),
  },
  templates: {
    list: (params?: { page?: number; page_size?: number; category?: string }) =>
      request("/api/v1/templates" + qs(params)),
    get: (id: string) => request("/api/v1/templates/" + id),
    create: (data: Record<string, unknown>) =>
      request("/api/v1/templates", { method: "POST", body: JSON.stringify(data) }),
    update: (id: string, data: Record<string, unknown>) =>
      request("/api/v1/templates/" + id, { method: "PUT", body: JSON.stringify(data) }),
    delete: (id: string) => request("/api/v1/templates/" + id, { method: "DELETE" }),
  },
}
