from fastapi import APIRouter
from app.api.v1 import auth_routes, contacts_routes, leads_routes, deals_routes
from app.api.v1 import sequences_routes, dashboard_routes, integrations_routes
from app.api.v1 import webhooks, ai_routes, compliance_routes, templates_routes

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_routes.router)
api_router.include_router(contacts_routes.router)
api_router.include_router(leads_routes.router)
api_router.include_router(deals_routes.router)
api_router.include_router(sequences_routes.router)
api_router.include_router(dashboard_routes.router)
api_router.include_router(integrations_routes.router)
api_router.include_router(webhooks.router)
api_router.include_router(ai_routes.router)
api_router.include_router(compliance_routes.router)
api_router.include_router(templates_routes.router)
