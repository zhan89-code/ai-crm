# Data Models - AI-Powered CRM

## Overview
PostgreSQL 15+ schema with Row-Level Security (RLS), JSONB for flexible metadata, and full audit trail. All tables use UUIDv7 primary keys for distributed-system friendliness. Soft-delete via deleted_at timestamp. Multi-tenant via tenant_id partition key.

---


## 0. tenants - Multi-Tenant Root Entity

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK, gen_random_uuid() |
| name | VARCHAR(200) | NOT NULL |
| slug | VARCHAR(100) | UNIQUE NOT NULL |
| plan | VARCHAR(30) | DEFAULT free, CHECK: free/starter/pro/enterprise |
| status | VARCHAR(20) | DEFAULT active, CHECK: active/suspended/cancelled |
| settings | JSONB | DEFAULT {} |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() |
| deleted_at | TIMESTAMPTZ | soft delete |

Indexes: idx_tenants_slug on (slug) WHERE deleted_at IS NULL

## 1. users - Tenant Users (AuthN/AuthZ)

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK, gen_random_uuid() |
| email | CITEXT | UNIQUE NOT NULL |
| password_hash | TEXT | NOT NULL (argon2id) |
| full_name | VARCHAR(200) | NOT NULL |
| role | VARCHAR(30) | DEFAULT member, CHECK: admin/manager/member/readonly |
| tenant_id | UUID | NOT NULL, references tenants(id) |
| timezone | VARCHAR(50) | DEFAULT UTC |
| locale | VARCHAR(10) | DEFAULT en-US |
| mfa_enabled | BOOLEAN | DEFAULT FALSE |
| mfa_secret | TEXT | encrypted TOTP seed |
| last_login_at | TIMESTAMPTZ | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() |
| deleted_at | TIMESTAMPTZ | soft delete |

Indexes: idx_users_tenant on (tenant_id) WHERE deleted_at IS NULL

## 2. contacts - CRM Contacts

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| tenant_id | UUID | NOT NULL |
| external_id | VARCHAR(100) | SF/HubSpot/Pipedrive ID |
| source | VARCHAR(50) | DEFAULT manual |
| first_name | VARCHAR(100) | |
| last_name | VARCHAR(100) | |
| email | CITEXT | |
| phone | VARCHAR(30) | |
| title | VARCHAR(150) | |
| company | VARCHAR(200) | |
| industry | VARCHAR(100) | |
| website | VARCHAR(500) | |
| address_line1 | VARCHAR(200) | |
| address_line2 | VARCHAR(200) | |
| city | VARCHAR(100) | |
| state | VARCHAR(100) | |
| postal_code | VARCHAR(20) | |
| country | VARCHAR(2) | ISO-3166 |
| tags | JSONB | DEFAULT [] |
| custom_fields | JSONB | DEFAULT {} |
| consent_status | VARCHAR(20) | CHECK: none/given/withdrawn/expired |
| consent_at | TIMESTAMPTZ | |
| gdpr_basis | VARCHAR(30) | legitimate_interest/consent/contract/legal_obligation |
| data_retention_until | DATE | auto-purge schedule |
| owner_id | UUID | references users(id) |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |
| deleted_at | TIMESTAMPTZ | |

Indexes: tenant+email (partial), owner, company, GIN(tags)

## 3. leads - Qualified Leads (Scoring Target)

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| contact_id | UUID | NOT NULL, references contacts(id) |
| tenant_id | UUID | NOT NULL |
| status | VARCHAR(30) | CHECK: new/contacted/qualified/unqualified/converted/lost |
| source | VARCHAR(50) | |
| deal_value | NUMERIC(12,2) | |
| currency | VARCHAR(3) | DEFAULT USD |
| score | NUMERIC(5,4) | 0.0000-1.0000, Platt-calibrated |
| score_label | VARCHAR(10) | hot/warm/cold |
| score_factors | JSONB | SHAP explanations: [{feature, value, contribution}] |
| scored_at | TIMESTAMPTZ | |
| model_version | VARCHAR(50) | |
| assigned_to | UUID | references users(id) |
| notes | TEXT | |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |
| deleted_at | TIMESTAMPTZ | |

Indexes: tenant+score DESC (partial), contact_id, assigned_to

## 4. deals - Pipeline Deals

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| contact_id | UUID | references contacts(id) |
| lead_id | UUID | references leads(id) |
| tenant_id | UUID | NOT NULL |
| title | VARCHAR(300) | NOT NULL |
| stage | VARCHAR(30) | CHECK: prospecting/qualification/proposal/negotiation/closed_won/closed_lost |
| amount | NUMERIC(14,2) | |
| currency | VARCHAR(3) | DEFAULT USD |
| probability | NUMERIC(5,2) | AI-suggested win probability |
| expected_close | DATE | |
| actual_close | DATE | |
| assigned_to | UUID | references users(id) |
| pipeline_id | UUID | DEFAULT single pipeline |
| custom_fields | JSONB | |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |
| deleted_at | TIMESTAMPTZ | |

Indexes: tenant+stage (partial), assigned_to, tenant+pipeline+stage

## 5. email_templates - Reusable Email Templates

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| tenant_id | UUID | NOT NULL |
| name | VARCHAR(200) | NOT NULL |
| subject | VARCHAR(500) | NOT NULL |
| body_html | TEXT | NOT NULL |
| body_text | TEXT | NOT NULL |
| tokens | JSONB | [{name, description, default_value}] |
| category | VARCHAR(50) | follow-up/nurture/onboarding/re-engagement |
| created_by | UUID | references users(id) |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |
| deleted_at | TIMESTAMPTZ | |

## 6. email_sequences - Drip Sequences / Automation

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| tenant_id | UUID | NOT NULL |
| name | VARCHAR(200) | NOT NULL |
| description | TEXT | |
| trigger_type | VARCHAR(50) | CHECK: lead_score_threshold/deal_stage_change/form_submission/inactivity/date_based |
| trigger_config | JSONB | e.g. {score_above: 0.7, stage: proposal} |
| status | VARCHAR(20) | CHECK: draft/active/paused/archived |
| entry_count | INT | DEFAULT 0 |
| ab_test_enabled | BOOLEAN | DEFAULT FALSE |
| ab_variant_id | UUID | self-reference to variant sequence |
| created_by | UUID | references users(id) |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |
| deleted_at | TIMESTAMPTZ | |

## 7. email_sequence_steps - Steps within a Sequence

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| sequence_id | UUID | NOT NULL, references email_sequences(id), CASCADE |
| step_order | INT | NOT NULL |
| template_id | UUID | references email_templates(id) |
| delay_days | INT | DEFAULT 0 |
| delay_hours | INT | DEFAULT 0 |
| condition | JSONB | {type: opened_previous, or_clicked: true} |
| subject_override | VARCHAR(500) | |
| body_override | TEXT | |
| ab_variant | CHAR(1) | CHECK: A/B |
| | | UNIQUE(sequence_id, step_order) |

## 8. email_logs - Outbound Email Audit Trail

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| tenant_id | UUID | NOT NULL |
| contact_id | UUID | references contacts(id) |
| sequence_id | UUID | references email_sequences(id) |
| step_id | UUID | references email_sequence_steps(id) |
| template_id | UUID | references email_templates(id) |
| status | VARCHAR(20) | CHECK: queued/sent/delivered/opened/clicked/bounced/failed/unsubscribed |
| trigger_type | VARCHAR(50) | |
| subject | VARCHAR(500) | |
| sent_at | TIMESTAMPTZ | |
| delivered_at | TIMESTAMPTZ | |
| opened_at | TIMESTAMPTZ | |
| clicked_at | TIMESTAMPTZ | |
| bounce_reason | TEXT | |
| ip_address | INET | |
| user_agent | TEXT | |
| ab_variant | CHAR(1) | |
| created_at | TIMESTAMPTZ | |

Indexes: tenant+created_at DESC, contact_id, sequence_id, tenant+status

## 9. audit_log - Immutable Audit Trail (SOC2 / GDPR Art.30)

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | BIGSERIAL | PK |
| tenant_id | UUID | NOT NULL |
| user_id | UUID | |
| action | VARCHAR(50) | NOT NULL: CREATE/READ/UPDATE/DELETE/EXPORT/LOGIN/CONSENT_CHANGE |
| resource_type | VARCHAR(50) | NOT NULL |
| resource_id | UUID | |
| details | JSONB | |
| ip_address | INET | |
| user_agent | TEXT | |
| created_at | TIMESTAMPTZ | |

Indexes: tenant+created_at DESC, resource_type+resource_id. Partition by month for performance.

## 10. dsar_requests - GDPR Data Subject Access Requests

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| tenant_id | UUID | NOT NULL |
| contact_id | UUID | references contacts(id) |
| request_email | CITEXT | NOT NULL |
| type | VARCHAR(30) | CHECK: access/rectification/erasure/portability/restriction |
| status | VARCHAR(20) | CHECK: pending/processing/completed/denied |
| due_by | DATE | NOT NULL (30 days from request) |
| completed_at | TIMESTAMPTZ | |
| response_data | JSONB | exported data for access/portability |
| notes | TEXT | |
| created_at | TIMESTAMPTZ | |

Indexes: tenant+status, due_by (partial: pending/processing)

## 11. sync_records - CRM Integration Sync State

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| tenant_id | UUID | NOT NULL |
| integration | VARCHAR(30) | salesforce/hubspot/pipedrive |
| entity_type | VARCHAR(30) | contact/lead/deal |
| external_id | VARCHAR(100) | NOT NULL |
| internal_id | UUID | NOT NULL |
| last_synced_at | TIMESTAMPTZ | |
| conflict_data | JSONB | conflicting fields snapshot |
| sync_direction | VARCHAR(10) | inbound/outbound/bidirectional |
| status | VARCHAR(20) | CHECK: synced/conflict/error/pending |
| | | UNIQUE(integration, entity_type, external_id) |

## 12. model_registry - AI Model Version Tracking

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| tenant_id | UUID | NULL = global model |
| model_type | VARCHAR(50) | lead_scoring_ensemble |
| version | VARCHAR(50) | NOT NULL |
| artifact_path | TEXT | S3/MinIO path |
| metrics | JSONB | {auc, precision, recall, f1, psi} |
| training_date | TIMESTAMPTZ | NOT NULL |
| is_active | BOOLEAN | DEFAULT FALSE |
| feature_list | JSONB | NOT NULL |
| shap_baseline | JSONB | mean absolute SHAP per feature for drift |
| created_at | TIMESTAMPTZ | |

---


## 13. crm_integrations - CRM Connection Configurations

| Column | Type | Constraints / Default |
|--------|------|-----------------------|
| id | UUID | PK |
| tenant_id | UUID | NOT NULL, references tenants(id) |
| crm_type | VARCHAR(30) | NOT NULL, CHECK: salesforce/hubspot/pipedrive |
| status | VARCHAR(20) | DEFAULT connected, CHECK: connected/paused/error/pending_auth |
| access_token | TEXT | NOT NULL, encrypted (Fernet) |
| refresh_token | TEXT | encrypted (Fernet) |
| instance_url | VARCHAR(500) | SFDC-specific |
| domain | VARCHAR(255) | HubSpot hub domain |
| api_key | TEXT | Pipedrive-specific, encrypted |
| sync_config | JSONB | {frequency, field_mappings, sync_direction} |
| last_sync_at | TIMESTAMPTZ | |
| last_error | TEXT | |
| token_expires_at | TIMESTAMPTZ | |
| created_by | UUID | references users(id) |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() |
| deleted_at | TIMESTAMPTZ | |

Indexes: idx_crm_int_tenant on (tenant_id, crm_type) WHERE deleted_at IS NULL

---

## Row-Level Security (RLS)

All tenant-scoped tables enable RLS with policy:
CREATE POLICY tenant_isolation ON contacts
    USING (tenant_id = current_setting(app.current_tenant)::UUID);

## Migrations

- Tool: Alembic + SQLAlchemy async
- Location: alembic/versions/
- Apply: On container startup via entrypoint script
- Convention: Revision ID = timestamp prefix, descriptive slug
