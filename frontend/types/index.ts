export interface Tenant {
  id: string
  name: string
  slug: string
  plan: string
  created_at: string
}

export interface User {
  id: string
  email: string
  full_name: string
  role: string
  tenant_id: string
  avatar_url?: string
  last_login_at?: string
  created_at: string
}

export interface Contact {
  id: string
  tenant_id: string
  first_name: string
  last_name: string
  email: string
  phone?: string
  company?: string
  title?: string
  industry?: string
  website?: string
  source?: string
  tags: string[]
  custom_fields: Record<string, unknown>
  created_at: string
  updated_at: string
  deleted_at?: string
}

export interface Lead {
  id: string
  tenant_id: string
  contact_id: string
  status: string
  source?: string
  score?: number
  score_label?: string
  score_factors?: Record<string, unknown>
  scored_at?: string
  model_version?: string
  owner_id?: string
  lifecycle_stage?: string
  created_at: string
  updated_at: string
  deleted_at?: string
  contact?: Contact
}

export interface Deal {
  id: string
  tenant_id: string
  contact_id?: string
  lead_id?: string
  title: string
  stage: string
  amount: number
  probability?: number
  expected_close?: string
  actual_close?: string
  owner_id?: string
  pipeline_id?: string
  custom_fields: Record<string, unknown>
  created_at: string
  updated_at: string
  deleted_at?: string
}

export interface EmailTemplate {
  id: string
  tenant_id: string
  name: string
  subject: string
  body_html: string
  body_text?: string
  category?: string
  created_by: string
  created_at: string
  updated_at: string
  deleted_at?: string
}

export interface EmailSequence {
  id: string
  tenant_id: string
  name: string
  description?: string
  status: string
  trigger_type: string
  entry_count: number
  created_by: string
  steps?: EmailSequenceStep[]
  created_at: string
  updated_at: string
  deleted_at?: string
}

export interface EmailSequenceStep {
  id: string
  sequence_id: string
  step_order: number
  template_id?: string
  delay_days: number
  condition?: string
  ab_variant?: boolean
  created_at: string
}

export interface DashboardSummary {
  pipeline_value: number
  pipeline_count: number
  leads_today: number
  leads_this_week: number
  avg_score: number
  score_distribution: Record<string, number>
  email_metrics: Record<string, number>
  model_health: {
    status: string
    auc: number
    psi: number
    last_retrain?: string
  }
  recent_activity: Array<{ id: string; type: string; description: string; created_at: string }>
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface CRMIntegration {
  id: string
  tenant_id: string
  crm_type: string
  status: string
  config: Record<string, unknown>
  last_sync_at?: string
  created_at: string
  updated_at: string
  deleted_at?: string
}
