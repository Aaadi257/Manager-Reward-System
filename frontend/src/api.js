const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function saveScore(scoreData) {
  const res = await fetch(`${API_BASE_URL}/api/save-score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(scoreData),
  });
  if (!res.ok) throw new Error("Failed to save score");
}

export async function deleteScore(scoreId) {
  const res = await fetch(`${API_BASE_URL}/api/score/${scoreId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete score");
}

  return data;
