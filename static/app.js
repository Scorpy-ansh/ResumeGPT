const form = document.querySelector("#analyze-form");
const input = document.querySelector("#resume-input");
const dropZone = document.querySelector("#drop-zone");
const fileName = document.querySelector("#file-name");
const analyzeButton = document.querySelector("#analyze-button");
const errorMessage = document.querySelector("#error-message");
const resultsSection = document.querySelector("#results-section");
const tabs = document.querySelector("#result-tabs");
const content = document.querySelector("#result-content");
const labels = {
  resume_analysis: "Resume review",
  ats_check: "ATS checker",
  interview_questions: "Interview prep",
  career_assistant: "Career roadmap",
  cover_letter: "Cover letter",
};
let report = {};
let activeKey = "resume_analysis";

function chooseFile(file) {
  if (!file) return;
  if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
    errorMessage.textContent = "Please choose a PDF file.";
    return;
  }
  input.files = new DataTransfer().files;
  const transfer = new DataTransfer();
  transfer.items.add(file);
  input.files = transfer.files;
  fileName.textContent = file.name;
  analyzeButton.disabled = false;
  errorMessage.textContent = "";
}

input.addEventListener("change", () => chooseFile(input.files[0]));
["dragenter", "dragover"].forEach((event) => dropZone.addEventListener(event, (e) => {
  e.preventDefault(); dropZone.classList.add("dragging");
}));
["dragleave", "drop"].forEach((event) => dropZone.addEventListener(event, (e) => {
  e.preventDefault(); dropZone.classList.remove("dragging");
}));
dropZone.addEventListener("drop", (e) => chooseFile(e.dataTransfer.files[0]));

function renderText(text) {
  const escaped = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return escaped.replace(/^### (.*)$/gm, "<h3>$1</h3>")
    .replace(/^## (.*)$/gm, "<h3>$1</h3>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/^\s*[-*] (.*)$/gm, "• $1")
    .replace(/\n/g, "<br>");
}

function showTab(key) {
  activeKey = key;
  document.querySelectorAll(".result-tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.key === key));
  content.innerHTML = renderText(report[key] || "No result was returned for this section.");
}

function showResults() {
  tabs.innerHTML = Object.keys(labels).map((key) =>
    `<button class="result-tab ${key === activeKey ? "active" : ""}" data-key="${key}" type="button">${labels[key]}</button>`
  ).join("");
  tabs.querySelectorAll(".result-tab").forEach((tab) => tab.addEventListener("click", () => showTab(tab.dataset.key)));
  resultsSection.classList.remove("hidden");
  showTab(activeKey);
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!input.files[0]) return;
  analyzeButton.disabled = true;
  analyzeButton.innerHTML = '<span class="loading"><i class="spinner"></i>Analyzing...</span>';
  errorMessage.textContent = "";
  try {
    const response = await fetch("/api/analyze", { method: "POST", body: new FormData(form) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analysis failed.");
    report = data.results;
    document.querySelector("#report-title").textContent = `Insights for ${data.filename}`;
    showResults();
  } catch (error) {
    errorMessage.textContent = error.message;
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.innerHTML = 'Analyze my resume <span>→</span>';
  }
});

document.querySelector("#new-analysis").addEventListener("click", () => {
  resultsSection.classList.add("hidden");
  form.reset();
  fileName.textContent = "Maximum 8,000 characters are analyzed";
  analyzeButton.disabled = true;
});
document.querySelector("#theme-toggle").addEventListener("click", (event) => {
  document.body.classList.toggle("dark");
  event.currentTarget.textContent = document.body.classList.contains("dark") ? "☀" : "☾";
});
