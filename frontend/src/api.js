const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// ✅ frontend utility function (used by App.jsx)
export function calculateScore(data) {
  // adjust logic if needed — this is a safe default
  let score = 0;

  if (data.sales) score += data.sales * 10;
  if (data.bonus) score += data.bonus;
  if (data.rating) score += data.rating * 5;

  return score;
}

export async function saveScore(scoreData) {
  const res = await fetch(`${API_BASE_URL}/api/save-score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(scoreData),
  });

  if (!res.ok) throw new Error("Failed to save score");

  return await res.json();
}

export async function deleteScore(scoreId) {
  const res = await fetch(`${API_BASE_URL}/api/score/${scoreId}`, {
    method: "DELETE",
  });

  if (!res.ok) throw new Error("Failed to delete score");

  return await res.json();
}