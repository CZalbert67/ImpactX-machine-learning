const presets = {
  normal: { g_force_peak: 1.2, heart_rate_bpm: 78, impact_duration_ms: 35, speed_delta_kmh: 1, post_impact_inactivity_seconds: 0 },
  mild: { g_force_peak: 4.5, heart_rate_bpm: 96, impact_duration_ms: 120, speed_delta_kmh: 9, post_impact_inactivity_seconds: 3 },
  moderate: { g_force_peak: 8, heart_rate_bpm: 128, impact_duration_ms: 280, speed_delta_kmh: 31, post_impact_inactivity_seconds: 18 },
  severe: { g_force_peak: 14, heart_rate_bpm: 165, impact_duration_ms: 560, speed_delta_kmh: 62, post_impact_inactivity_seconds: 75 },
  critical: { g_force_peak: 22, heart_rate_bpm: 210, impact_duration_ms: 900, speed_delta_kmh: 100, post_impact_inactivity_seconds: 160 },
};

const severityLabels = {
  sin_choque: "Sin choque",
  leve: "Leve",
  moderado: "Moderado",
  grave: "Grave",
  critico: "Crítico",
};

const actionLabels = {
  sin_alerta: "Sin alerta",
  validacion_10_segundos: "Validación 10 s",
  validacion_5_segundos: "Validación 5 s",
  alerta_inmediata: "Alerta inmediata",
};

const inputIds = {
  g_force_peak: "g-force",
  heart_rate_bpm: "heart-rate",
  impact_duration_ms: "duration",
  speed_delta_kmh: "speed-delta",
  post_impact_inactivity_seconds: "inactivity",
};

const form = document.querySelector("#prediction-form");
const preset = document.querySelector("#preset");
const analyzeButton = document.querySelector("#analyze-button");
const emptyResult = document.querySelector("#empty-result");
const resultContainer = document.querySelector("#result");
const simulationControls = document.querySelector("#simulation-controls");
const simulationMessage = document.querySelector("#simulation-message");

function applyPreset(name) {
  const values = presets[name];
  Object.entries(values).forEach(([key, value]) => {
    document.querySelector(`#${inputIds[key]}`).value = value;
  });
}

function readPayload() {
  return {
    g_force_peak: Number(document.querySelector("#g-force").value),
    heart_rate_bpm: Number(document.querySelector("#heart-rate").value),
    impact_duration_ms: Number(document.querySelector("#duration").value),
    speed_delta_kmh: Number(document.querySelector("#speed-delta").value),
    post_impact_inactivity_seconds: Number(document.querySelector("#inactivity").value),
  };
}

function setDecisionStyle(action) {
  const message = document.querySelector("#decision-message");
  message.className = "decision-message";
  if (action === "alerta_inmediata") message.classList.add("decision-danger");
  else if (action === "sin_alerta") message.classList.add("decision-safe");
  else message.classList.add("decision-warning");
}

function renderProbabilities(probabilities) {
  const container = document.querySelector("#probabilities");
  container.replaceChildren();
  Object.entries(probabilities).forEach(([severity, probability]) => {
    const percentage = probability * 100;
    const row = document.createElement("div");
    row.className = "probability-row";
    row.innerHTML = `
      <span>${severityLabels[severity]}</span>
      <div class="track"><div class="fill" style="width: ${percentage.toFixed(2)}%"></div></div>
      <span class="probability-value">${percentage.toFixed(1)}%</span>
    `;
    container.appendChild(row);
  });
}

function renderResult(data) {
  emptyResult.classList.add("hidden");
  resultContainer.classList.remove("hidden");
  simulationMessage.classList.add("hidden");

  const { decision } = data;
  document.querySelector("#severity-value").textContent = severityLabels[data.severity];
  document.querySelector("#confidence-value").textContent = `${(data.confidence * 100).toFixed(1)}%`;
  document.querySelector("#action-value").textContent = actionLabels[decision.action];
  document.querySelector("#severity-badge").textContent = severityLabels[data.severity];
  document.querySelector("#decision-reason").textContent = decision.reason;
  document.querySelector("#raw-json").textContent = JSON.stringify(data, null, 2);

  const decisionMessage = document.querySelector("#decision-message");
  setDecisionStyle(decision.action);
  if (decision.action === "alerta_inmediata") {
    decisionMessage.textContent = "ALERTA INSTANTÁNEA: se activaría inmediatamente el protocolo ImpactX.";
    simulationControls.classList.add("hidden");
  } else if (decision.action === "sin_alerta") {
    decisionMessage.textContent = "SIN ALERTA: el evento no activa el protocolo de emergencia.";
    simulationControls.classList.add("hidden");
  } else {
    decisionMessage.textContent = `VALIDACIÓN: el wearable mostraría una cuenta regresiva de ${decision.countdown_seconds} segundos.`;
    simulationControls.classList.remove("hidden");
  }

  document.querySelector("#override-note").classList.toggle("hidden", !decision.safety_override);
  renderProbabilities(data.probabilities);
}

function renderError(message) {
  emptyResult.classList.remove("hidden");
  resultContainer.classList.add("hidden");
  emptyResult.querySelector("h2").textContent = "No se pudo analizar";
  emptyResult.querySelector("p").textContent = message;
}

preset.addEventListener("change", (event) => applyPreset(event.target.value));

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  analyzeButton.disabled = true;
  analyzeButton.textContent = "Analizando...";
  try {
    const response = await fetch("/api/v1/predictions/collision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(readPayload()),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail ? JSON.stringify(error.detail) : "Solicitud inválida");
    }
    renderResult(await response.json());
  } catch (error) {
    renderError(error.message || "Error inesperado al conectar con el modelo local.");
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.textContent = "Analizar evento";
  }
});

document.querySelector("#cancel-button").addEventListener("click", () => {
  simulationMessage.textContent = "El usuario confirmó que está bien; la alerta simulada fue cancelada.";
  simulationMessage.classList.remove("hidden");
});

document.querySelector("#timeout-button").addEventListener("click", () => {
  simulationMessage.textContent = "El tiempo terminó; la alerta simulada fue enviada a los monitores autorizados.";
  simulationMessage.classList.remove("hidden");
});

applyPreset(preset.value);
