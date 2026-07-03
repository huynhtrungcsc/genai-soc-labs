from app.schemas import Incident
from app.services.mitre import map_to_mitre
from app.services.parser import parse_logs
from app.services.quality import assess_data_quality
from app.services.report import generate_reports
from app.services.response import build_response_plan
from app.services.risk import assess_risk
from app.services.timeline import build_timeline


def analyze_incident(incident: Incident) -> Incident:
    incident.events = parse_logs(incident.raw_logs)
    incident.timeline = build_timeline(incident.events)
    incident.mitre = map_to_mitre(incident.events)
    incident.data_quality = assess_data_quality(incident.events)
    incident.risk = assess_risk(incident)
    incident.response_tasks = build_response_plan(incident)
    incident.reports = generate_reports(incident)
    return incident
