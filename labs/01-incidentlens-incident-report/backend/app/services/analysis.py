from app.schemas import Incident
from app.services.mitre import map_to_mitre
from app.services.parser import parse_logs
from app.services.report import generate_reports
from app.services.timeline import build_timeline


def analyze_incident(incident: Incident) -> Incident:
    incident.events = parse_logs(incident.raw_logs)
    incident.timeline = build_timeline(incident.events)
    incident.mitre = map_to_mitre(incident.events)
    incident.reports = generate_reports(incident)
    return incident
