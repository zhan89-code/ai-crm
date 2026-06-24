# UI Component Architecture

## Tech Stack
- Framework: Next.js 14 (App Router, React Server Components)
- Styling: Tailwind CSS + shadcn/ui
- State: Zustand (client) + TanStack Query v5 (server)
- Charts: Recharts
- Forms: React Hook Form + Zod validation
- Tables: TanStack Table v8
- DnD: @dnd-kit/core + @dnd-kit/sortable
- Rich Text: TipTap (for email template editor)
- Date: date-fns + react-day-picker

## Layout Structure

### RootLayout
- Sidebar (navigation, collapsible)
- Header (global search Cmd+K, notifications, user menu)
- Main content area (responsive)
- Toast provider (sonner)
- Global modal provider
- QueryClientProvider

### AuthLayout
- Centered card with gradient background
- Login form (email + password + MFA)
- Password reset flow
- OAuth buttons (Google, Microsoft)

## Page Components

### Dashboard (/dashboard)
Widgets:
- PipelineFunnel (funnel chart, stage counts + values)
- LeadScoreDistribution (histogram, 0-100 distribution)
- EmailPerformance (line chart, opens/clicks over time)
- UpcomingTasks (list, next 5 pending)
- RecentActivity (feed, last 20 events)
- AIHealthCard (model status, last retrain, AUC, drift indicator)
- ConversionFunnel (lead -> contact -> deal -> won)

Data: /api/v1/dashboard/summary
Refresh: 5-min polling + WebSocket for real-time score updates

### Leads (/leads)
Components:
- LeadsDataGrid (TanStack Table)
  - Columns: checkbox, name, company, email, score(badge), tier(colored dot), source, owner, lifecycle_stage, last_activity, actions
  - Filters: score range slider, tier multi-select, source, owner, lifecycle stage, date range
  - Bulk actions: assign owner, export CSV, enroll sequence, add tags
- LeadDetailSheet (ResizablePanel)
  - Tab 1: Overview (contact info, deal history, AI score explanation)
  - Tab 2: Email timeline (sent/opened/clicked timeline)
  - Tab 3: Activity log (calls, notes, tasks)
  - Tab 4: GDPR/compliance (consent status, data export)
- ScoreFactorsPanel (SHAP waterfall chart)
- LeadScoreBadge (A=green, B=yellow, C=orange, D=red)

### Pipeline (/pipeline/kanban)
Components:
- DealBoard (KanbanBoard via @dnd-kit)
  - Columns = pipeline stages
  - Deal cards: title, value(format currency), contact name, probability bar, expected close date
  - Drag-and-drop updates stage + probability
- DealDetailModal (full deal edit)
- StageProbabilityEditor
- PipelineSelector (if multiple pipelines)

### Email Sequences (/sequences)
Components:
- SequenceList (table with stats: enrollment count, open rate, click rate)
- SequenceBuilder (visual flow editor using React Flow)
  - Node types: Start, Email Step, Wait/Delay, Condition (opened|clicked|replied|score_above), A/B Split, End
  - Each email node: template selector dropdown, delay settings, A/B variant toggle
  - Condition nodes: configure threshold/event
- SequenceStats (funnel: sent -> delivered -> opened -> clicked -> replied)
- ABTestResults (bar chart comparing variant performance)

### Templates (/templates)
Components:
- TemplateList (table with category filter)
- TemplateEditor
  - Subject line with token insertion buttons
  - Rich text editor (TipTap) for HTML body
  - Plain text fallback textarea
  - Token panel: first_name, company, industry, last_activity, score_tier, etc.
  - Preview panel with sample contact data
  - A/B test subject line manager

### Settings > Compliance (/settings/compliance)
Components:
- GDPRPanel
  - Consent management dashboard (stats: granted/pending/withdrawn counts)
  - DSAR request queue (table with status: pending/processing/completed)
  - Data export request processing (generates presigned URL)
  - Retention policy settings (auto-delete after N days of inactivity)
- AuditLogViewer (filterable table: user, action, entity_type, date range)
- DataRetentionConfig form

### Settings > Integrations (/settings/integrations)
Components:
- IntegrationCard per CRM
  - Status: connected(paused(gray), error(red) with icon
  - Connect button (OAuth flow modal)
  - Sync configuration: frequency(dropdown), field mapping editor
  - Sync history log (table: timestamp, records_synced, errors)
  - Pause/Resume/Delete buttons

## Shared Components
- GlobalSearch (Cmd+K, fuzzy search across contacts/leads/deals)
- DateRangePicker (preset ranges + custom)
- UserAvatar (initials fallback)
- StatusBadge (variant: success/warning/error/info)
- EmptyState (icon + message + optional CTA)
- LoadingStates (skeleton screens per page)
- Pagination (page info + page size selector)
- ConfirmDialog (destructive actions)
- TokenBadge (inline pill for template tokens)

## Data Fetching Pattern
Use TanStack Query v5 for server state:
- queryKey arrays for cache invalidation
- staleTime: 30s for most queries
- Optimistic updates for mutations (score, stage change)
- Infinite scroll for large lists (contacts, leads)

## Component Hierarchy
RootLayout
  Dashboard (PipelineFunnel, LeadScoreDistribution, EmailPerformance, UpcomingTasks, RecentActivity, AIHealthCard)
  Leads (LeadsDataGrid, LeadDetailSheet, ScoreFactorsPanel, LeadScoreBadge)
  Pipeline (DealBoard, DealDetailModal)
  Sequences (SequenceBuilder, ABTestResults)
  Templates (TemplateEditor)
  Settings
    Compliance (GDPRPanel, AuditLogViewer)
    Integrations (IntegrationCard[])