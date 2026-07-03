from app.schemas import SchemaField, SchemaResponse

FIELDS = [
    SchemaField(name="timestamp", type="datetime", description="Event time in UTC."),
    SchemaField(
        name="source",
        type="keyword",
        description="Log source such as vpn, edr, firewall.",
    ),
    SchemaField(name="host", type="keyword", description="Endpoint, server, or network device."),
    SchemaField(name="user", type="keyword", description="User or service account."),
    SchemaField(name="action", type="keyword", description="Normalized activity name."),
    SchemaField(name="src_ip", type="ip", description="Source IP address."),
    SchemaField(name="dst_ip", type="ip", description="Destination IP address."),
    SchemaField(name="country", type="keyword", description="Destination or source country."),
    SchemaField(name="department", type="keyword", description="Business unit context."),
    SchemaField(name="severity", type="keyword", description="Normalized event severity."),
    SchemaField(name="message", type="text", description="Original security event message."),
]


def get_schema() -> SchemaResponse:
    return SchemaResponse(fields=FIELDS, supported_dialects=["splunk", "sentinel", "elastic"])
