const API = "http://localhost:8000/api/v1";

async function submitQuery() {
  const query = document.getElementById("query").value;
  const userId = document.getElementById("userId").value;
  const role = document.getElementById("role").value;
  const tools = document.getElementById("tools").value
    .split(",")
    .map(v => v.trim())
    .filter(Boolean);

  const payload = { query, requested_tools: tools };

  const res = await fetch(`${API}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-User-Id": userId,
      "X-User-Role": role
    },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  document.getElementById("responseBox").textContent = JSON.stringify(data, null, 2);
  loadReviews();
  loadTraces();
}

async function loadReviews() {
  const res = await fetch(`${API}/reviews`);
  const items = await res.json();
  const list = document.getElementById("reviewsList");
  list.innerHTML = "";
  items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = `${item.review_id} | ${item.status} | ${item.reason}`;
    list.appendChild(li);
  });
}

async function loadTraces() {
  const res = await fetch(`${API}/traces`);
  const items = await res.json();
  const list = document.getElementById("tracesList");
  list.innerHTML = "";
  items.slice(0, 8).forEach(item => {
    const li = document.createElement("li");
    li.textContent = `${item.trace_id} | ${item.final_status} | ${item.query}`;
    list.appendChild(li);
  });
}

loadReviews();
loadTraces();
