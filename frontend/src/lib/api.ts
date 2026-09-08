// API client to interact with the FastAPI backend running on port 8000
const getApiBase = () => {
  if (typeof window !== "undefined") {
    return `http://${window.location.hostname}:8000/api`;
  }
  return "http://localhost:8000/api";
};

export async function fetchSchemes() {
  const res = await fetch(`${getApiBase()}/schemes`);
  if (!res.ok) throw new Error("Failed to fetch schemes");
  return res.json();
}

export async function fetchDistricts() {
  const res = await fetch(`${getApiBase()}/districts`);
  if (!res.ok) throw new Error("Failed to fetch districts");
  return res.json();
}

export async function fetchFacilities(district?: string, service?: string) {
  const params = new URLSearchParams();
  if (district) params.append("district", district);
  if (service) params.append("service", service);
  
  const res = await fetch(`${getApiBase()}/facilities?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch facilities");
  return res.json();
}

export async function fetchSchedules() {
  const res = await fetch(`${getApiBase()}/schedules`);
  if (!res.ok) throw new Error("Failed to fetch schedules");
  return res.json();
}

export async function fetchMedicines() {
  const res = await fetch(`${getApiBase()}/medicines`);
  if (!res.ok) throw new Error("Failed to fetch medicines");
  return res.json();
}

export async function fetchTriage(query: string, language: string = "en", low_bandwidth: boolean = false) {
  const res = await fetch(`${getApiBase()}/triage`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, language, low_bandwidth }),
  });
  
  if (!res.ok) throw new Error("Failed to process triage query");
  return res.json();
}

export async function getGeminiConfig() {
  const res = await fetch(`${getApiBase()}/config/gemini`);
  if (!res.ok) throw new Error("Failed to fetch Gemini status");
  return res.json();
}

export async function saveGeminiApiKey(apiKey: string) {
  const res = await fetch(`${getApiBase()}/config/gemini`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ api_key: apiKey }),
  });
  if (!res.ok) throw new Error("Failed to save API key");
  return res.json();
}
