// API client to interact with the FastAPI backend running on port 8000
const API_BASE = "http://localhost:8000/api";

export async function fetchSchemes() {
  const res = await fetch(`${API_BASE}/schemes`);
  if (!res.ok) throw new Error("Failed to fetch schemes");
  return res.json();
}

export async function fetchDistricts() {
  const res = await fetch(`${API_BASE}/districts`);
  if (!res.ok) throw new Error("Failed to fetch districts");
  return res.json();
}

export async function fetchFacilities(district?: string, service?: string) {
  const params = new URLSearchParams();
  if (district) params.append("district", district);
  if (service) params.append("service", service);
  
  const res = await fetch(`${API_BASE}/facilities?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch facilities");
  return res.json();
}

export async function fetchSchedules() {
  const res = await fetch(`${API_BASE}/schedules`);
  if (!res.ok) throw new Error("Failed to fetch schedules");
  return res.json();
}

export async function fetchMedicines() {
  const res = await fetch(`${API_BASE}/medicines`);
  if (!res.ok) throw new Error("Failed to fetch medicines");
  return res.json();
}

export async function fetchTriage(query: string, language: string = "en", low_bandwidth: boolean = false) {
  const res = await fetch(`${API_BASE}/triage`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, language, low_bandwidth }),
  });
  
  if (!res.ok) throw new Error("Failed to process triage query");
  return res.json();
}
