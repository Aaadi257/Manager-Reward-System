const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function calculateScore(payload) {
  const response = await fetch(`${API_BASE_URL}/api/calculate-score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Error calculating score");
  }

  return data;
}