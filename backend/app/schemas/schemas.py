
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Any, Dict
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID
import enum


class TenantCreate(BaseModel):
    name: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=100)
    plan: str = "free"

class TenantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    slug: str
    plan: str
    status: str
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., max_length=200)
    role: str = "member"
    timezone: str = "UTC"

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: str
    full_name: str
    role: str
    tenant_id: UUID
    timezone: str
    mfa_enabled: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class ContactCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = Field(None, max_length=2)
    tags: List[str] = []
    custom_fields: Dict[str, Any] = {}
    consent_status: str = "none"
    gdpr_basis: Optional[str] = None
    owner_id: Optional[UUID] = None

class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    tags: List[str] = []
    custom_fields: Dict[str, Any] = {}
    consent_status: str
    owner_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

class ContactGDPRExport(BaseModel):
    contact: Dict[str, Any]
    leads: List[Dict[str, Any]]
    deals: List[Dict[str, Any]]
    email_logs: List[Dict[str, Any]]
    audit_trail: List[Dict[str, Any]]
    exported_at: datetime


class LeadCreate(BaseModel):
    contact_id: UUID
    source: Optional[str] = None
    deal_value: Optional[Decimal] = None
    currency: str = "USD"
    notes: Optional[str] = None
    assigned_to: Optional[UUID] = None

class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    contact_id: UUID
    status: str
    source: Optional[str] = None
    deal_value: Optional[Decimal] = None
    score: Optional[Decimal] = None
    score_label: Optional[str] = None
    score_factors: Optional[Dict[str, Any]] = None
    scored_at: Optional[datetime] = None
    model_version: Optional[str] = None
    assigned_to: Optional[UUID] = None
    created_at: datetime

class LeadScoreResponse(BaseModel):
    lead_id: UUID
    score: float
    tier: str
    factors: List[Dict[str, Any]]
    model_version: str
    scored_at: datetime


class DealCreate(BaseModel):
    contact_id: UUID
    lead_id: Optional[UUID] = None
    title: str = Field(..., max_length=300)
    stage: str = "prospecting"
    amount: Optional[Decimal] = None
    currency: str = "USD"
    probability: Optional[Decimal] = None
    expected_close: Optional[date] = None
    assigned_to: Optional[UUID] = None
    custom_fields: Dict[str, Any] = {}

class DealRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    contact_id: UUID
    lead_id: Optional[UUID] = None
    title: str
    stage: str
    amount: Optional[Decimal] = None
    probability: Optional[Decimal] = None
    expected_close: Optional[date] = None
    actual_close: Optional[date] = None
    assigned_to: Optional[UUID] = None
    created_at: datetime

class DealStageUpdate(BaseModel):
    stage: str
    probability: Optional[Decimal] = None
    actual_close: Optional[date] = None


class EmailTemplateCreate(BaseModel):
    name: str = Field(..., max_length=200)
    subject: str = Field(..., max_length=500)
    body_html: str
    body_text: str
    tokens: List[str] = []
    category: str = "follow-up"

class EmailTemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    subject: str
    body_html: str
    body_text: str
    tokens: List[str]
    category: str
    created_at: datetime


class EmailSequenceCreate(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    trigger_type: Optional[str] = None
    trigger_config: Dict[str, Any] = {}
    steps: List[Dict[str, Any]] = []

class EmailSequenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: Optional[str] = None
    trigger_type: Optional[str] = None
    trigger_config: Dict[str, Any]
    status: str
    entry_count: int
    ab_test_enabled: bool
    created_at: datetime


class DSARCreateRequest(BaseModel):
    contact_id: Optional[UUID] = None
    request_email: EmailStr
    type: str
    notes: Optional[str] = None

class DSARProcessRequest(BaseModel):
    status: str
    response_data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class CRMIntegrationCreate(BaseModel):
    crm_type: str
    access_token: str
    refresh_token: Optional[str] = None
    instance_url: Optional[str] = None
    domain: Optional[str] = None
    api_key: Optional[str] = None
    sync_config: Dict[str, Any] = {}

class CRMIntegrationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    crm_type: str
    status: str
    instance_url: Optional[str] = None
    last_sync_at: Optional[datetime] = None
    created_at: datetime


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


class DashboardSummary(BaseModel):
    pipeline_value: float
    pipeline_count: int
    leads_today: int
    leads_this_week: int
    avg_score: Optional[float] = None
    score_distribution: Dict[str, int] = {}
    email_metrics: Dict[str, Any] = {}
    model_health: Dict[str, Any] = {}
    recent_activity: List[Dict[str, Any]] = []


class DSARRequestCreate(BaseModel):
    request_type: str
    requester_email: str
    requester_name: Optional[str] = None
    details: Optional[str] = None

class DSARRequestResponse(BaseModel):
    id: str
    tenant_id: str
    request_type: str
    requester_email: str
    status: str
    created_at: str

