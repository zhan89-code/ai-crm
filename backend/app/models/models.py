
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Numeric, Date, DateTime,
    ForeignKey, UniqueConstraint, Index, JSON, BigInteger
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET, CITEXT
from sqlalchemy.orm import relationship
from app.db.database import Base


class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    plan = Column(String(30), default="free")
    status = Column(String(20), default="active")
    settings = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    users = relationship("User", back_populates="tenant")


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(CITEXT, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(30), default="member")
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    timezone = Column(String(50), default="UTC")
    locale = Column(String(10), default="en-US")
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(Text, nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    tenant = relationship("Tenant", back_populates="users")
    __table_args__ = (
        Index("idx_users_tenant", "tenant_id", postgresql_where=deleted_at.is_(None)),
    )


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    external_id = Column(String(100), nullable=True)
    source = Column(String(50), default="manual")
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(CITEXT, nullable=True)
    phone = Column(String(30), nullable=True)
    title = Column(String(150), nullable=True)
    company = Column(String(200), nullable=True)
    industry = Column(String(100), nullable=True)
    website = Column(String(500), nullable=True)
    address_line1 = Column(String(200), nullable=True)
    address_line2 = Column(String(200), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(2), nullable=True)
    tags = Column(JSONB, default=[])
    custom_fields = Column(JSONB, default={})
    consent_status = Column(String(20), default="none")
    consent_at = Column(DateTime(timezone=True), nullable=True)
    gdpr_basis = Column(String(30), nullable=True)
    data_retention_until = Column(Date, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deals = relationship("Deal", back_populates="contact")
    leads = relationship("Lead", back_populates="contact")
    __table_args__ = (
        Index("idx_contacts_tenant_email", "tenant_id", "email", postgresql_where=deleted_at.is_(None)),
        Index("idx_contacts_owner", "owner_id", postgresql_where=deleted_at.is_(None)),
        Index("idx_contacts_tags", "tenant_id", postgresql_using="gin", postgresql_ops={"tags": "jsonb_path_ops"}),
    )


class Lead(Base):
    __tablename__ = "leads"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    status = Column(String(30), default="new")
    source = Column(String(50), nullable=True)
    deal_value = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(3), default="USD")
    score = Column(Numeric(5, 4), nullable=True)
    score_label = Column(String(10), nullable=True)
    score_factors = Column(JSONB, nullable=True)
    scored_at = Column(DateTime(timezone=True), nullable=True)
    model_version = Column(String(50), nullable=True)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    contact = relationship("Contact", back_populates="leads")
    __table_args__ = (
        Index("idx_leads_tenant_score", "tenant_id", "score", postgresql_where=deleted_at.is_(None)),
        Index("idx_leads_contact", "contact_id"),
        Index("idx_leads_assigned", "assigned_to", postgresql_where=deleted_at.is_(None)),
    )


class Deal(Base):
    __tablename__ = "deals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), nullable=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    title = Column(String(300), nullable=False)
    stage = Column(String(30), default="prospecting")
    amount = Column(Numeric(14, 2), nullable=True)
    currency = Column(String(3), default="USD")
    probability = Column(Numeric(5, 2), nullable=True)
    expected_close = Column(Date, nullable=True)
    actual_close = Column(Date, nullable=True)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    pipeline_id = Column(UUID(as_uuid=True), nullable=True)
    custom_fields = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    contact = relationship("Contact", back_populates="deals")
    __table_args__ = (
        Index("idx_deals_tenant_stage", "tenant_id", "stage", postgresql_where=deleted_at.is_(None)),
        Index("idx_deals_assigned", "assigned_to", postgresql_where=deleted_at.is_(None)),
    )


class EmailTemplate(Base):
    __tablename__ = "email_templates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    name = Column(String(200), nullable=False)
    subject = Column(String(500), nullable=False)
    body_html = Column(Text, nullable=False)
    body_text = Column(Text, nullable=False)
    tokens = Column(JSONB, default=[])
    category = Column(String(50), default="follow-up")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class EmailSequence(Base):
    __tablename__ = "email_sequences"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    trigger_type = Column(String(50), nullable=True)
    trigger_config = Column(JSONB, default={})
    status = Column(String(20), default="draft")
    entry_count = Column(Integer, default=0)
    ab_test_enabled = Column(Boolean, default=False)
    ab_variant_id = Column(UUID(as_uuid=True), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    steps = relationship("EmailSequenceStep", back_populates="sequence", cascade="all, delete-orphan")


class EmailSequenceStep(Base):
    __tablename__ = "email_sequence_steps"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sequence_id = Column(UUID(as_uuid=True), ForeignKey("email_sequences.id", ondelete="CASCADE"), nullable=False)
    step_order = Column(Integer, nullable=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey("email_templates.id"), nullable=True)
    delay_days = Column(Integer, default=0)
    delay_hours = Column(Integer, default=0)
    condition = Column(JSONB, nullable=True)
    subject_override = Column(String(500), nullable=True)
    body_override = Column(Text, nullable=True)
    ab_variant = Column(String(1), nullable=True)
    sequence = relationship("EmailSequence", back_populates="steps")
    __table_args__ = (
        UniqueConstraint("sequence_id", "step_order", name="uq_sequence_step_order"),
    )


class EmailLog(Base):
    __tablename__ = "email_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=True)
    sequence_id = Column(UUID(as_uuid=True), ForeignKey("email_sequences.id"), nullable=True)
    step_id = Column(UUID(as_uuid=True), ForeignKey("email_sequence_steps.id"), nullable=True)
    template_id = Column(UUID(as_uuid=True), ForeignKey("email_templates.id"), nullable=True)
    status = Column(String(20), default="queued")
    trigger_type = Column(String(50), nullable=True)
    subject = Column(String(500), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    opened_at = Column(DateTime(timezone=True), nullable=True)
    clicked_at = Column(DateTime(timezone=True), nullable=True)
    bounce_reason = Column(Text, nullable=True)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    ab_variant = Column(String(1), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    __table_args__ = (
        Index("idx_email_logs_tenant_date", "tenant_id", "created_at"),
        Index("idx_email_logs_contact", "contact_id"),
        Index("idx_email_logs_sequence", "sequence_id"),
    )


class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String(50), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    details = Column(JSONB, default={})
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    __table_args__ = (
        Index("idx_audit_tenant_date", "tenant_id", "created_at"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
    )


class DSARRequest(Base):
    __tablename__ = "dsar_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=True)
    request_email = Column(CITEXT, nullable=False)
    type = Column(String(30), nullable=False)
    status = Column(String(20), default="pending")
    due_by = Column(Date, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    response_data = Column(JSONB, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    __table_args__ = (
        Index("idx_dsar_tenant_status", "tenant_id", "status"),
        Index("idx_dsar_due", "due_by", postgresql_where=status.in_(["pending", "processing"])),
    )


class SyncRecord(Base):
    __tablename__ = "sync_records"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    integration = Column(String(30), nullable=False)
    entity_type = Column(String(30), nullable=False)
    external_id = Column(String(100), nullable=False)
    internal_id = Column(UUID(as_uuid=True), nullable=False)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    conflict_data = Column(JSONB, nullable=True)
    sync_direction = Column(String(10), default="bidirectional")
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        UniqueConstraint("integration", "entity_type", "external_id", name="uq_sync_record"),
    )


class ModelRegistry(Base):
    __tablename__ = "model_registry"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=True)
    model_type = Column(String(50), default="lead_scoring_ensemble")
    version = Column(String(50), nullable=False)
    artifact_path = Column(Text, nullable=False)
    metrics = Column(JSONB, default={})
    training_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=False)
    feature_list = Column(JSONB, default=[])
    shap_baseline = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class CRMIntegration(Base):
    __tablename__ = "crm_integrations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    crm_type = Column(String(30), nullable=False)
    status = Column(String(20), default="connected")
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    instance_url = Column(String(500), nullable=True)
    domain = Column(String(255), nullable=True)
    api_key = Column(Text, nullable=True)
    sync_config = Column(JSONB, default={})
    last_sync_at = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    token_expires_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    __table_args__ = (
        Index("idx_crm_int_tenant", "tenant_id", "crm_type", postgresql_where=deleted_at.is_(None)),
    )
