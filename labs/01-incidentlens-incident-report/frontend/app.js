const sampleLogs = [
  '{"timestamp":"2026-06-28T08:11:04Z","source":"vpn","host":"vpn-gw-01","user":"j.nguyen","action":"failed_login","src_ip":"203.0.113.44","message":"Failed login for j.nguyen from 203.0.113.44"}',
  '{"timestamp":"2026-06-28T08:15:42Z","source":"vpn","host":"vpn-gw-01","user":"j.nguyen","action":"successful_login","src_ip":"203.0.113.44","message":"Successful VPN login from new device"}',
  '{"timestamp":"2026-06-28T08:24:11Z","source":"edr","host":"FIN-WS-044","user":"j.nguyen","action":"suspicious_powershell","message":"powershell.exe -EncodedCommand detected outbound download cradle"}',
  '{"timestamp":"2026-06-28T08:41:29Z","source":"windows","host":"FIN-FS-01","user":"j.nguyen","action":"lateral_movement","src_ip":"10.20.5.44","dst_ip":"10.20.8.10","message":"SMB admin$ access from FIN-WS-044 to FIN-FS-01"}',
  '{"timestamp":"2026-06-28T08:52:03Z","source":"zeek","host":"FIN-WS-044","action":"command_and_control","src_ip":"10.20.5.44","dst_ip":"198.51.100.77","message":"Periodic C2 beacon over HTTPS every 60 seconds"}',
  '{"timestamp":"2026-06-28T09:03:37Z","source":"edr","host":"FIN-FS-01","user":"j.nguyen","action":"impact","message":"Multiple files encrypted with ransom note observed"}',
].join("\n");

const state = {
  incident: null,
};

const $ = (id) => document.getElementById(id);

function authHeader() {
  const token = btoa(`${$("username").value}:${$("password").value}`);
  return { Authorization: `Basic ${token}` };
}

async function api(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeader(),
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }
  const contentType = response.headers.get("content-type") || "";
  return contentType.includes("application/json") ? response.json() : response.text();
}

function setStatus(message, isError = false) {
  $("status").textContent = message;
  $("status").classList.toggle("error", isError);
}

function renderIncident(incident) {
  state.incident = incident;
  $("event-count").textContent = incident.events.length;
  $("mitre-count").textContent = incident.mitre.length;
  $("severity-label").textContent = incident.severity.toUpperCase();
  renderTimeline(incident.timeline);
  renderMitre(incident.mitre);
  $("technical").textContent = incident.reports?.technical || "";
  $("executive").textContent = incident.reports?.executive || "";
}

function renderTimeline(timeline) {
  $("timeline").innerHTML = timeline.length
    ? timeline
        .map(
          (step) => `
          <article class="card">
            <span class="pill">${step.phase}</span>
            <h3>${escapeHtml(step.title)}</h3>
            <p><strong>Time:</strong> ${step.timestamp || "unknown"}</p>
            <p><strong>Inference:</strong> ${escapeHtml(step.inference)}</p>
            <p><strong>Confidence:</strong> ${step.confidence.toFixed(2)}</p>
            <ul>${step.evidence.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
          </article>
        `,
        )
        .join("")
    : "<p>No timeline available.</p>";
}

function renderMitre(items) {
  $("mitre").innerHTML = items.length
    ? items
        .map(
          (item) => `
          <article class="card">
            <span class="pill">${item.tactic}</span>
            <h3>${item.technique_id} · ${escapeHtml(item.technique)}</h3>
            <p><strong>Confidence:</strong> ${item.confidence.toFixed(2)}</p>
            <ul>${item.evidence.map((evidence) => `<li>${escapeHtml(evidence)}</li>`).join("")}</ul>
          </article>
        `,
        )
        .join("")
    : "<p>No MITRE mapping available.</p>";
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => {
    const entities = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
    return entities[char];
  });
}

async function refreshIncidents() {
  try {
    const incidents = await api("/incidents");
    $("incident-picker").innerHTML =
      '<option value="">Recent incidents</option>' +
      incidents
        .map((incident) => `<option value="${incident.id}">${escapeHtml(incident.title)}</option>`)
        .join("");
  } catch (error) {
    setStatus("Could not load incidents. Check credentials.", true);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  $("raw_logs").value = sampleLogs;

  $("load-sample").addEventListener("click", () => {
    $("raw_logs").value = sampleLogs;
    setStatus("Sample incident loaded.");
  });

  $("incident-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    setStatus("Analyzing incident...");
    try {
      const incident = await api("/incidents", {
        method: "POST",
        body: JSON.stringify({
          title: $("title").value,
          severity: $("severity").value,
          summary: $("summary").value,
          raw_logs: $("raw_logs").value,
        }),
      });
      renderIncident(incident);
      await refreshIncidents();
      setStatus("Incident analyzed successfully.");
    } catch (error) {
      setStatus(error.message, true);
    }
  });

  $("incident-picker").addEventListener("change", async (event) => {
    if (!event.target.value) return;
    try {
      renderIncident(await api(`/incidents/${event.target.value}`));
      setStatus("Incident loaded.");
    } catch (error) {
      setStatus(error.message, true);
    }
  });

  document.querySelectorAll(".tabs button").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".tabs button").forEach((item) => item.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      $(button.dataset.tab).classList.add("active");
    });
  });

  refreshIncidents();
});
