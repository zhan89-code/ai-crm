# RESTful API Specification

## Authentication
Bearer token auth via JWT. Token refresh via /auth/refresh.
All endpoints return JSON. Errors use RFC 7807 Problem Details.

### POST /api/v1/auth/login
Request: { email: string, password: string }
Response 200: { access_token, refresh_token, token_type: "Bearer", expires_in: 3600, user: {id, email, role} }
Response 401: { error: "invalid_credentials" }

### POST /api/v1/auth/refresh
Request: { refresh_token: string }
Response 200: { access_token, token_type: "Bearer", expires_in: 3600 }

### POST /api/v1/auth/logout
Response 204: No Content

## Contacts

### GET /api/v1/contacts
Query: page(default 1), limit(default 20, max 100), search, lifecycle_stage, owner_id, company, sort, order
Response 200: { data: Contact[], pagination: {page, limit, total, total_pages} }

### GET /api/v1/contacts/:id
Response 200: ContactDetail (includes deals, email_logs, score_history, activities)

### POST /api/v1/contacts
Request: ContactCreate (email required)
Response 201: Contact

### PUT /api/v1/contacts/:id
Request: ContactUpdate (partial)
Response 200: Contact

### DELETE /api/v1/contacts/:id
Response 200: { archived: true, deleted_at: timestamp }

### POST /api/v1/contacts/:id/merge
Request: { target_contact_id: UUID, strategy: "newest"|"oldest"|"manual" }
Response 200: Contact (merged)

### POST /api/v1/contacts/:id/gdpr-export
Response 202: { job_id, status: "processing", download_url (presigned, expires 24h) }

## Leads

### GET /api/v1/leads
Query: page, limit, score_min, score_max, score_tier, source, status, owner_id, sort, order
Response 200: { data: Lead[], pagination }

### POST /api/v1/leads
Request: LeadCreate (email + source required)
Response 201: Lead (with initial score from AI engine)

### POST /api/v1/leads/:id/score
Response 200: { score: number(0-100), tier: string, factors: [{feature, value, contribution}] }

### POST /api/v1/leads/:id/convert
Request: { create_deal: boolean, deal_value?: number, pipeline_id?: UUID }
Response 200: ContactDetail (converted contact with optional deal)

### POST /api/v1/leads/bulk-import
Request: multipart/form-data with CSV file
Response 202: { job_id, status: "processing", total_rows, imported: 0, errors: [] }

## Deals

### GET /api/v1/deals
Query: page, limit, stage, pipeline_id, owner_id, value_min, value_max
Response 200: { data: Deal[], pagination, summary: {total_value, avg_value, count_by_stage} }

### GET /api/v1/deals/pipeline
Response 200: { stages: [{name, deal_count, total_value, deals: Deal[]}], total_pipeline_value }

### POST /api/v1/deals
Request: DealCreate (contact_id, title required, value, currency, stage, pipeline_id)
Response 201: Deal

### PUT /api/v1/deals/:id
Request: DealUpdate (partial)
Response 200: Deal

### POST /api/v1/deals/:id/stage
Request: { stage: string, probability?: integer }
Response 200: Deal

## Email Sequences

### GET /api/v1/sequences
Response 200: { data: EmailSequence[], pagination }

### POST /api/v1/sequences
Request: EmailSequenceCreate (name, category, steps[])
Response 201: EmailSequence

### PUT /api/v1/sequences/:id
Request: EmailSequenceUpdate (partial)
Response 200: EmailSequence

### POST /api/v1/sequences/:id/enroll
Request: { contact_ids: UUID[] }
Response 200: { enrolled: number, errors: [{contact_id, reason}] }

### GET /api/v1/sequences/:id/stats
Response: { sent, delivered, opened, clicked, bounced, unsubscribed, open_rate, click_rate }

### GET /api/v1/email-stats
Query: date_from, date_to, group_by(day|week|month)
Response: { metrics: [{date, sent, delivered, opened, clicked, bounced}], breakdown: [] }

## AI/ML Endpoints

### GET /api/v1/models/status
Response: { current_model: {version, trained_at, metrics: {auc, precision, psi}}, last_training: timestamp, is_retraining: boolean }

### POST /api/v1/models/retrain
Response 202: { job_id, status: "queued", estimated_duration: "15 minutes" }

### GET /api/v1/models/retrain/:job_id
Response: { job_id, status: "queued"|"running"|"completed"|"failed", progress: number(0-100), error?: string }


## Dashboard

### GET /api/v1/dashboard/summary
Response 200: {
  pipeline_value: number,
  pipeline_count: number,
  leads_today: number,
  leads_this_week: number,
  avg_score: number,
  score_distribution: {A: number, B: number, C: number, D: number},
  email_metrics: {sent: number, open_rate: number, click_rate: number},
  model_health: {status: "healthy"|"degraded"|"retraining", auc: number, psi: number, last_retrain: timestamp},
  recent_activity: [{action, entity_type, entity_name, user, timestamp}]
}

### GET /api/v1/dashboard/pipeline
Query: pipeline_id, date_from, date_to
Response 200: { stages: [{name, count, total_value, avg_probability}], total_value: number }

### GET /api/v1/dashboard/leaderboard
Query: period(today|week|month)
Response 200: { top_performers: [{user_id, name, deals_won, revenue, conversion_rate}] }

## CRM Integrations

### GET /api/v1/integrations
Response: { data: CRMIntegration[] }

### POST /api/v1/integrations
Request: { crm_type: "salesforce"|"hubspot"|"pipedrive", access_token, refresh_token?, instance_url? }
Response 201: CRMIntegration

### POST /api/v1/integrations/:id/sync
Response 202: { job_id, status: "syncing" }

### GET /api/v1/integrations/:id/sync-status
Response: { last_sync_at, synced_records, errors: [{entity, external_id, message}] }

## Webhooks

### POST /webhooks/:crm_type
Auth: HMAC-SHA256 signature in X-Signature header
Body: { event: string, data: object, timestamp: string }
Response 200: { received: true, job_id }

## Error Format (RFC 7807)
All errors return:
{ type: "https://api.ai-crm.example.com/errors/validation", title: "Validation Error", status: 422, detail: "...", instance: "/api/v1/contacts", errors: [{field, message}] }


## WebSocket (Real-Time)

### WS /ws/v1/events
Auth: Bearer token on connect (query param or header)
Events sent to client:
- lead.scored: { lead_id, score, tier, factors, scored_at }
- deal.stage_changed: { deal_id, old_stage, new_stage, probability }
- email.sent: { email_log_id, contact_id, subject, status }
- model.retrained: { version, metrics, completed_at }
- integration.sync_completed: { integration_id, records_synced, errors }
- dsar.status_changed: { request_id, old_status, new_status }

### Client -> Server
- subscribe: { channels: ["lead.*", "deal.*"] }
- ping/pong: heartbeat (server sends pong every 30s)

## Rate Limits
- 1000 requests/hour per user
- 100 requests/minute per user
- 429 status with Retry-After header