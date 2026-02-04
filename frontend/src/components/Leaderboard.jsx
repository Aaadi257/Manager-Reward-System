import React, { useEffect, useState } from "react";

const Leaderboard = ({ onViewScorecard }) => {
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const [month, setMonth] = useState("");

useEffect(() => {
  const query = month ? `?month=${month}` : "";
  fetch(`${API_BASE_URL}/api/leaderboard${query}`)
    .then(res => res.json())
    .then(setScores);
}, [month]);

  // Fetch leaderboard on load
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/leaderboard`)
      .then((res) => res.json())
      .then((data) => {
        setScores(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  // Remove score from leaderboard
  <select
  value={month}
  onChange={e => setMonth(e.target.value)}
  className="input mb-4"
>
  <option value="">All / Testing</option>
  <option value="2026-02">Feb 2026</option>
  <option value="2026-03">Mar 2026</option>
</select>
  const handleDelete = async (id) => {
    const confirmDelete = window.confirm(
      "Remove this score from the leaderboard?"
    );
    if (!confirmDelete) return;

    try {
      await fetch(`${API_BASE_URL}/api/score/${id}`, {
        method: "DELETE",
      });

      // Update UI immediately
      setScores((prev) => prev.filter((s) => s.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to remove score");
    }
  };

  if (loading) {
    return (
      <div className="text-center text-slate-400 py-10">
        Loading Leaderboard...
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-white mb-6">Leaderboard</h2>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-700 text-slate-400 text-sm uppercase tracking-wider">
              <th className="p-4">Rank</th>
              <th className="p-4">Manager</th>
              <th className="p-4">Mall</th>
              <th className="p-4 text-right">Score</th>
              <th className="p-4 text-right">Actions</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-800">
            {scores.length === 0 ? (
              <tr>
                <td
                  colSpan="5"
                  className="p-4 text-center text-slate-500"
                >
                  No scores yet.
                </td>
              </tr>
            ) : (
              scores.map((s, idx) => (
                <tr
                  key={s.id}
                  className="hover:bg-slate-800/30 transition-colors"
                >
                  <td className="p-4 text-slate-500 font-mono">
                    #{idx + 1}
                  </td>

                  <td className="p-4 font-medium text-white">
                    {s.manager_name}
                  </td>

                  <td className="p-4 text-slate-300">
                    {s.mall_name}
                  </td>

                  <td className="p-4 text-right font-bold text-indigo-400">
                    {s.total_score.toFixed(1)}
                  </td>

                  <td className="p-4 text-right">
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => onViewScorecard(s)}
                        className="px-3 py-1.5 text-sm rounded-md 
                                   bg-indigo-600 hover:bg-indigo-500 
                                   text-white transition"
                      >
                        View
                      </button>

                      <button
                        onClick={() => handleDelete(s.id)}
                        className="px-3 py-1.5 text-sm rounded-md 
                                   bg-red-600 hover:bg-red-500 
                                   text-white transition"
                      >
                        Remove
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Leaderboard;