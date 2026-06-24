# CRM Integration Architecture

## Supported CRMs
- Salesforce (REST API v57.0, OAuth 2.0)
- HubSpot (v3 API, OAuth 2.0)
- Pipedrive (v1 API, API key auth)

## Architecture

[AI-CRM Backend] <--> [Integration Service] <--> [Salesforce API]
                              |
                              +--> [HubSpot API]
                              |
                              +--> [Pipedrive API]

## Data Sync Model

### Bidirectional Sync Strategy
1. Real-time: Webhook from source CRM on record change
2. Batch fallback: Hourly full sync (cursor-based pagination)
3. Conflict resolution: Last-write-wins with timestamp comparison + audit trail

### Entities Synced
- Contacts/Leads (bidirectional)
- Deals/Opportunities (bidirectional)
- Tasks/Activities (outbound to external CRM)
- Notes/Comments (outbound to external CRM)
- Custom fields (configurable mapping)

### Field Mapping
Admin can define per-integration:
- Source field -> Target field mapping
- Field type validation (string, number, date, enum)
- Sync direction (inbound, outbound, bidirectional)
- Default values for unmapped fields

## Salesforce Integration

### OAuth 2.0 Flow
1. User clicks "Connect Salesforce" in Settings > Integrations
2. Redirect to Salesforce OAuth login page
3. User grants access, returns with authorization code
4. Backend exchanges code for access_token + refresh_token
5. Tokens stored encrypted (Fernet) in crm_integrations table
6. Token refresh: automatic before expiry (cron every 5 min)

### Webhook Configuration
- Salesforce Platform Events: EventBusSubscriber object
- Or: Apex Trigger + Outbound Message to webhook URL
- Webhook endpoint: POST /webhooks/salesforce
- Auth: HMAC-SHA256 signature via Salesforce consumer secret

### Sync Logic
- Push: On contact/deal update in AI-CRM, call Salesforce REST API (PATCH/POST)
- Pull: Webhook triggers immediate sync, batch runs hourly
- Conflict: Compare LastModifiedDate, newest wins, log in sync_records.conflict_data

### API Endpoints Used
- GET /services/data/v57.0/sobjects/Contact/{id}
- PATCH /services/data/v57.0/sobjects/Contact/{id}
- POST /services/data/v57.0/sobjects/Contact
- GET /services/data/v57.0/query/?q={SOQL}

## HubSpot Integration

### OAuth 2.0 Flow
1. Redirect to HubSpot OAuth URL with scopes: crm.objects.contacts.write, crm.objects.deals.write
2. User logs in, grants app permissions
3. Return with auth code
4. Exchange for tokens, store in DB
5. Token refresh: automatic via refresh_token grant

### Webhook
- HubSpot Webhooks API: subscribe to contact.creation, contact.propertyChange, deal.creation
- Endpoint: POST /webhooks/hubspot
- Auth: HMAC-SHA256 using client secret in X-HubSpot-Signature header

### API Endpoints Used
- GET /crm/v3/objects/contacts/{id}?properties=...
- POST /crm/v3/objects/contacts
- PATCH /crm/v3/objects/contacts/{id}
- POST /crm/v3/objects/contacts/search

## Pipedrive Integration

### API Key Auth
- User provides API key from Pipedrive Settings > Personal Settings > API
- All requests include ?api_token={key}

### Webhook
- Pipedrive webhooks configured via Settings > Workflow automation
- Endpoint: POST /webhooks/pipedrive
- Auth: token query parameter verification

### API Endpoints Used
- GET /v1/persons/{id}
- POST /v1/persons
- PUT /v1/persons/{id}
- GET /v1/deals/{id}
- POST /v1/deals

## Conflict Resolution

### Strategy: Last-Write-Wins with Audit Trail
1. Compare updated_at timestamps from both systems
2. Apply the newer change
3. Log conflict in sync_records.conflict_data (JSON: {field, local_value, remote_value, resolved_value})
4. Provide manual override UI for edge cases

### Merge UI
- Side-by-side diff of conflicting fields
- User selects which version to keep per field
- Merged record written to both systems
- Audit log entry created

## Rate Limiting (per CRM)
- Salesforce: 100 API calls/15 min per user
- HubSpot: 100 requests/10 seconds per API key
- Pipedrive: 3600 requests/hour (free tier)

### Queuing
- Use Celery with Redis broker
- Respect queue rate limits via token bucket algorithm
- Failed requests retried with exponential backoff (3x max, 1s -> 8s -> 64s)
- Dead Letter Queue after 5 failures

## Error Handling
- Auth errors -> Re-auth flow (trigger notification to user)
- Rate limit -> 429 received, wait for Retry-After header, then retry
- Network errors -> Exponential backoff + DLQ after 5 failures
- All errors logged in integration_errors table
- User notification: in-app toast + email for critical errors

## Sync Health Dashboard
- Per-integration status card: last sync time, records synced, error count
- Sync history table: timestamp, direction, records_count, duration_ms, status
- Error details modal: entity, external_id, error message, retry button