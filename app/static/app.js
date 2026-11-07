const $ = (id) => document.getElementById(id);
const COLORS = { "0.3": "#4c9be8", "0.5": "#2ca58d", "1.0": "#e0a526", "1.5": "#e8742c", "2.0": "#c43b3b" };

let meta, cfg;
let lineChart, rankChart;

async function getJSON(url) {
  const res = await fetch(url);
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.detail || `${url}: ${res.status}`);
  return body;
}

function showError(msg) {
  const el = $("error");
  el.textContent = msg;
  el.hidden = false;
}

function fillSelect(sel, options, value) {
  sel.innerHTML = options.map(([v, label]) => `<option value="${v}">${label}</option>`).join("");
  sel.value = value;
}

function scenarioLabel(key) {
  return `${meta.scenarios[key]} (${key} m by 2100)`;
}

async function init() {
  cfg = await getJSON("/api/config");
  try {
    meta = await getJSON("/api/meta");
  } catch (e) {
    showError(e.message);
    return;
  }

  const stations = [...meta.stations].sort((a, b) =>
    a.name === "GMSL" ? -1 : b.name === "GMSL" ? 1 : a.name.localeCompare(b.name));
  fillSelect($("site"), stations.map((s) => [s.name, s.name === "GMSL" ? "Global mean (GMSL)" : `${s.name} (${s.region})`]), "GMSL");
  fillSelect($("scenario"), Object.keys(meta.scenarios).map((k) => [k, scenarioLabel(k)]), "1.0");
  fillSelect($("rank-year"), meta.years.slice(1).map((y) => [y, y]), 2100);

  $("scenario-list").innerHTML = Object.keys(meta.scenarios)
    .map((k) => `<dt style="color:${COLORS[k]}">${meta.scenarios[k]}</dt><dd>About ${k} m of global sea level rise by 2100.</dd>`)
    .join("");

  ["site", "scenario"].forEach((id) => $(id).addEventListener("change", () => { renderSite(); renderRanking(); }));
  $("rank-year").addEventListener("change", renderRanking);

  await Promise.all([renderSite(), renderRanking()]);
}

async function renderSite() {
  const site = $("site").value;
  const scen = $("scenario").value;
  const proj = await getJSON(`/api/projections/${encodeURIComponent(site)}`);
  const years = meta.years;
  const sel = proj[scen];

  // Stat cards for the selected scenario.
  $("stats").innerHTML = [2050, 2100, 2150].map((y) => {
    const i = years.indexOf(y);
    return `<div class="stat"><div class="k">By ${y}</div>
      <div class="v">${sel.MED[i]} <small>cm</small></div>
      <div class="r">likely range ${sel.LOW[i]}&ndash;${sel.HIGH[i]} cm</div></div>`;
  }).join("");

  $("chart-title").textContent = `${site === "GMSL" ? "Global mean" : site}: projected rise since 2005`;
  $("chart-sub").textContent =
    `Lines are median projections for each scenario. The shaded band is the likely range for ${meta.scenarios[scen]}.`;

  const datasets = [];
  // Band first so it draws beneath the lines: low fills up to high.
  datasets.push({ label: "Low", data: sel.LOW, borderWidth: 0, pointRadius: 0, backgroundColor: COLORS[scen] + "33", fill: "+1" });
  datasets.push({ label: "High", data: sel.HIGH, borderWidth: 0, pointRadius: 0, fill: false });
  for (const k of Object.keys(meta.scenarios)) {
    datasets.push({
      label: scenarioLabel(k),
      data: proj[k].MED,
      borderColor: COLORS[k],
      backgroundColor: COLORS[k],
      borderWidth: k === scen ? 3.5 : 1.5,
      pointRadius: 0,
      pointHoverRadius: 4,
      tension: 0.25,
    });
  }

  lineChart?.destroy();
  lineChart = new Chart($("chart"), {
    type: "line",
    data: { labels: years, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { labels: { filter: (item) => item.text !== "Low" && item.text !== "High" } },
        tooltip: { filter: (item) => item.dataset.label !== "Low" && item.dataset.label !== "High" },
      },
      scales: {
        x: { title: { display: true, text: "Year" } },
        y: { title: { display: true, text: "Rise since 2005 (cm)" }, beginAtZero: true },
      },
    },
  });
}

async function renderRanking() {
  const scen = $("scenario").value;
  const year = +$("rank-year").value;
  const rows = await getJSON(`/api/ranking?year=${year}&scenario=${scen}&level=MED`);
  const site = $("site").value;

  rankChart?.destroy();
  rankChart = new Chart($("rank-chart"), {
    type: "bar",
    data: {
      labels: rows.map((r) => r.name),
      datasets: [{
        label: `Median rise by ${year} (cm)`,
        data: rows.map((r) => r.value),
        backgroundColor: rows.map((r) => (r.name === site ? "#0b6bcb" : COLORS[scen] + "aa")),
      }],
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { title: { display: true, text: `Rise since 2005 by ${year} (cm), ${meta.scenarios[scen]} scenario` } },
        y: { ticks: { autoSkip: false, font: { size: 10 } } },
      },
    },
  });
}

// Simple hash router between the dashboard and the embedded notebook.
function route() {
  const nb = location.hash === "#notebook";
  $("view-dashboard").hidden = nb;
  $("view-notebook").hidden = !nb;
  $("nav-dashboard").classList.toggle("active", !nb);
  $("nav-notebook").classList.toggle("active", nb);
  if (nb && !$("jupyter").src) {
    // Jupyter runs on its own port on the same host the dashboard was loaded from.
    const base = `${location.protocol}//${location.hostname}:${cfg.jupyter_port}/lab/tree/analysis.ipynb`;
    const url = cfg.jupyter_token ? `${base}?token=${encodeURIComponent(cfg.jupyter_token)}` : base;
    $("jupyter").src = url;
    $("nb-external").href = url;
  }
}
window.addEventListener("hashchange", route);

init().then(route);
