const authHeader = `Basic ${btoa("analyst:threatpulse-demo")}`;
const headers = {
  Authorization: authHeader,
  "Content-Type": "application/json",
};

const sampleAssets = [
  {
    hostname: "pay-api-prod-01",
    owner: "payments-platform",
    business_unit: "digital-banking",
    environment: "production",
    criticality: 5,
    technologies: ["Apache Struts", "Java 17", "PostgreSQL"],
    internet_exposed: true,
    data_classification: "restricted",
    tags: ["crown-jewel", "pci"],
  },
  {
    hostname: "vpn-edge-01",
    owner: "network-security",
    business_unit: "infrastructure",
    environment: "production",
    criticality: 5,
    technologies: ["Ivanti Connect Secure", "Linux"],
    internet_exposed: true,
    data_classification: "internal",
    tags: ["remote-access", "edge"],
  },
];

const sampleIntel = [
  {
    source: "CISA KEV",
    title: "Active exploitation reported for Ivanti Connect Secure gateway vulnerability",
    summary:
      "Multiple organizations reported exploitation attempts against exposed Ivanti Connect Secure appliances.",
    affected_products: ["Ivanti Connect Secure"],
    industries: ["financial-services", "technology"],
    cves: ["CVE-2025-0282"],
    iocs: ["198.51.100.77", "vpn-check.jsp"],
    mitre_techniques: ["T1190", "T1133"],
    references: ["https://www.cisa.gov/known-exploited-vulnerabilities-catalog"],
    observed_exploitation: true,
    severity: "critical",
    confidence: "high",
    source_reliability: "A",
    published_at: "2026-07-01T09:30:00+00:00",
  },
  {
    source: "Security Research Blog",
    title: "Apache Struts exploit attempts observed against internet-facing Java applications",
    summary:
      "Researchers observed scanning and exploit attempts against vulnerable Apache Struts applications.",
    affected_products: ["Apache Struts"],
    industries: ["financial-services", "retail"],
    cves: ["CVE-2026-23010"],
    iocs: ["struts2-showcase.action", "192.0.2.91"],
    mitre_techniques: ["T1190", "T1059"],
    references: ["https://example.com/research/struts-exploitation"],
    observed_exploitation: true,
    severity: "critical",
    confidence: "high",
    source_reliability: "B",
    published_at: "2026-07-03T06:45:00+00:00",
  },
];

async function api(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    ...options,
    headers: { ...headers, ...(options.headers || {}) },
  });
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

async function refresh() {
  const [health, assets, intel, briefings, audit] = await Promise.all([
    fetch("/api/health").then((res) => res.json()),
    api("/assets"),
    api("/intel"),
    api("/briefings"),
    api("/audit"),
  ]);
  document.querySelector("#health").textContent = `${health.service}: ${health.status}`;
  renderMetrics(assets, intel, briefings);
  renderAssets(assets);
  renderIntel(intel);
  renderBriefing(briefings[0]);
  renderAudit(audit);
}

function renderMetrics(assets, intel, briefings) {
  document.querySelector("#assetCount").textContent = assets.length;
  document.querySelector("#intelCount").textContent = intel.length;
  document.querySelector("#priorityCount").textContent = intel.filter((item) =>
    ["critical", "high"].includes(item.priority),
  ).length;
  document.querySelector("#briefingCount").textContent = briefings.filter(
    (briefing) => briefing.status === "draft",
  ).length;
}

function renderIntel(items) {
  const node = document.querySelector("#intelList");
  node.innerHTML = items.length
    ? items
        .map(
          (item) => `
          <article class="item">
            <h3>${escapeHtml(item.title)}</h3>
            <p>${escapeHtml(item.source)} · relevance ${item.relevance_score} · ${item.affected_asset_count} affected asset(s)</p>
            <div class="chips">
              <span class="chip ${item.priority}">${item.priority}</span>
              <span class="chip">${item.severity}</span>
              ${item.observed_exploitation ? '<span class="chip critical">active exploitation</span>' : ""}
            </div>
          </article>`,
        )
        .join("")
    : '<article class="item"><p>No intelligence items yet.</p></article>';
}

function renderAssets(assets) {
  const node = document.querySelector("#assetList");
  node.innerHTML = assets.length
    ? assets
        .map(
          (asset) => `
          <article class="item">
            <h3>${escapeHtml(asset.hostname)}</h3>
            <p>${escapeHtml(asset.owner)} · criticality ${asset.criticality}/5 · ${asset.environment}</p>
            <div class="chips">
              ${asset.internet_exposed ? '<span class="chip high">internet exposed</span>' : ""}
              <span class="chip">${escapeHtml(asset.data_classification)}</span>
              ${asset.technologies.map((tech) => `<span class="chip">${escapeHtml(tech)}</span>`).join("")}
            </div>
          </article>`,
        )
        .join("")
    : '<article class="item"><p>No assets registered.</p></article>';
}

function renderBriefing(briefing) {
  const node = document.querySelector("#briefingView");
  if (!briefing) {
    node.className = "briefing-empty";
    node.textContent = "No briefing generated yet.";
    return;
  }
  node.className = "briefing";
  node.innerHTML = `
    <h3>${escapeHtml(briefing.title)}</h3>
    <p>Status: ${briefing.status} · audience: ${briefing.audience} · sections: ${briefing.sections.length}</p>
    ${
      briefing.status === "draft"
        ? `<button type="button" onclick="approveBriefing('${briefing.id}')">Approve Briefing</button>`
        : ""
    }
    ${briefing.sections
      .map(
        (section) => `
          <section>
            <h3>${escapeHtml(section.title)}</h3>
            <p>${escapeHtml(section.summary)}</p>
            <div class="chips">
              <span class="chip ${section.priority}">${section.priority}</span>
              ${section.affected_assets.map((asset) => `<span class="chip">${escapeHtml(asset)}</span>`).join("")}
            </div>
            <ul>${section.recommended_actions.map((action) => `<li>${escapeHtml(action)}</li>`).join("")}</ul>
          </section>`,
      )
      .join("")}
  `;
}

function renderAudit(events) {
  const node = document.querySelector("#auditList");
  node.innerHTML = events.length
    ? events
        .slice(0, 20)
        .map(
          (event) => `
          <article class="item">
            <h3>${escapeHtml(event.action)}</h3>
            <p>${escapeHtml(event.detail)}</p>
            <div class="meta"><span class="chip">${escapeHtml(event.actor)}</span><span class="chip">${new Date(event.created_at).toLocaleString()}</span></div>
          </article>`,
        )
        .join("")
    : '<article class="item"><p>No audit events yet.</p></article>';
}

async function seedSample() {
  await api("/assets/bulk", { method: "POST", body: JSON.stringify(sampleAssets) });
  for (const item of sampleIntel) {
    await api("/intel", { method: "POST", body: JSON.stringify(item) });
  }
  await refresh();
}

async function generateBriefing() {
  await api("/briefings/generate", {
    method: "POST",
    body: JSON.stringify({ audience: "soc", lookback_days: 30, max_items: 5 }),
  });
  await refresh();
}

async function approveBriefing(id) {
  await api(`/briefings/${id}/approve`, {
    method: "POST",
    body: JSON.stringify({ approver: "soc-manager", note: "Reviewed for demo workflow" }),
  });
  await refresh();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

document.querySelector("#seedBtn").addEventListener("click", seedSample);
document.querySelector("#briefBtn").addEventListener("click", generateBriefing);
refresh().catch((error) => {
  document.querySelector("#health").textContent = error.message;
});
