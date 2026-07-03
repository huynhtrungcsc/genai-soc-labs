const sampleQuestion =
  "Trong 24h qua, có máy nào trong phòng kế toán kết nối ra IP lạ ở nước ngoài không?";

const state = {
  job: null,
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
  return response.json();
}

function setStatus(message, isError = false) {
  $("status").textContent = message;
  $("status").classList.toggle("error", isError);
}

function renderJob(job) {
  state.job = job;
  $("dialect-label").textContent = job.dialect;
  $("range-label").textContent = job.time_range;
  $("row-count").textContent = job.execution?.row_count ?? 0;
  $("query").textContent = job.generated.query;
  $("execute").disabled = false;
  renderExplanation(job);
  renderResults(job.execution);
  renderFollowups(job.generated.next_questions);
}

function renderExplanation(job) {
  const warnings = job.generated.validations
    .map(
      (item) =>
        `<li class="${item.severity === "warning" ? "warning" : ""}">${escapeHtml(
          item.severity.toUpperCase(),
        )}: ${escapeHtml(item.message)}</li>`,
    )
    .join("");

  $("explanation").innerHTML = `
    <article class="card">
      <span class="pill">Explanation</span>
      <ul>${job.generated.explanation.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    </article>
    <article class="card">
      <span class="pill">Assumptions</span>
      <ul>${job.generated.assumptions.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
    </article>
    <article class="card">
      <span class="pill">Validation</span>
      <ul>${warnings}</ul>
    </article>
  `;
}

function renderResults(execution) {
  if (!execution) {
    $("results").innerHTML = "<p>No execution results yet. Generate a query, then run it.</p>";
    return;
  }
  const headers = [
    "count",
    "host",
    "user",
    "src_ip",
    "dst_ip",
    "country",
    "action",
    "severity",
    "first_seen",
    "last_seen",
  ];
  $("results").innerHTML = `
    <article class="card">
      <span class="pill">Sample Execution</span>
      <p>${escapeHtml(execution.summary)}</p>
    </article>
    <table>
      <thead><tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr></thead>
      <tbody>
        ${execution.rows
          .map(
            (row) =>
              `<tr>${headers.map((header) => `<td>${escapeHtml(row[header] || "")}</td>`).join("")}</tr>`,
          )
          .join("")}
      </tbody>
    </table>
  `;
}

function renderFollowups(questions) {
  $("followups").innerHTML = `
    <article class="card">
      <span class="pill">Suggested Next Hunts</span>
      <ul>${questions.map((question) => `<li>${escapeHtml(question)}</li>`).join("")}</ul>
    </article>
  `;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => {
    const entities = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
    return entities[char];
  });
}

async function refreshQueries() {
  try {
    const queries = await api("/queries");
    $("query-picker").innerHTML =
      '<option value="">Recent queries</option>' +
      queries
        .map((query) => `<option value="${query.id}">${escapeHtml(query.question)}</option>`)
        .join("");
  } catch (error) {
    setStatus("Could not load query history. Check credentials.", true);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  $("load-sample").addEventListener("click", () => {
    $("question").value = sampleQuestion;
    $("dialect").value = "splunk";
    $("time_range").value = "24h";
    $("data_source").value = "security_events";
    setStatus("Sample hunt loaded.");
  });

  $("query-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    setStatus("Generating query...");
    try {
      const job = await api("/queries", {
        method: "POST",
        body: JSON.stringify({
          question: $("question").value,
          dialect: $("dialect").value,
          time_range: $("time_range").value,
          data_source: $("data_source").value,
        }),
      });
      renderJob(job);
      await refreshQueries();
      setStatus("Query generated. Review it before execution.");
    } catch (error) {
      setStatus(error.message, true);
    }
  });

  $("execute").addEventListener("click", async () => {
    if (!state.job) return;
    setStatus("Executing against sample data...");
    try {
      const job = await api(`/queries/${state.job.id}/execute`, { method: "POST" });
      renderJob(job);
      await refreshQueries();
      setStatus("Execution completed.");
    } catch (error) {
      setStatus(error.message, true);
    }
  });

  $("query-picker").addEventListener("change", async (event) => {
    if (!event.target.value) return;
    try {
      renderJob(await api(`/queries/${event.target.value}`));
      setStatus("Query loaded.");
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

  refreshQueries();
});
