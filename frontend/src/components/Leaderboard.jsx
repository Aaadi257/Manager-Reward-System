import React, { useEffect, useState } from "react";

const Leaderboard = ({ onViewScorecard }) => {
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  const [month, setMonth] = useState("");
  const [managerOfMonth, setManagerOfMonth] = useState(null);

  useEffect(() => {
  setLoading(true);
  if (month) {
  fetch(`${API_BASE_URL}/api/manager-of-the-month?month=${month}`)
    .then(res => res.json())
    .then(data => setManagerOfMonth(data));
} else {
  setManagerOfMonth(null);
}

  const query = month ? `?month=${month}` : "";

  fetch(`${API_BASE_URL}/api/leaderboard${query}`)
    .then((res) => res.json())
    .then((data) => {
      setScores(data);
      setLoading(false);
    })
    .catch((err) => {
      console.error(err);
      setLoading(false);
    });
}, [month]);

  // Remove score from leaderboard
  <select
  value={month}
  onChange={e => setMonth(e.target.value)}
  className="input mb-4"
>
  <option value="">All / Testing</option>
  <option value="2026-01">January 2026</option>
  <option value="2026-02">February 2026</option>
  <option value="2026-03">March 2026</option>
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
          {managerOfMonth && (
  <div className="mb-6 p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/30">
    <h3 className="text-lg font-bold text-yellow-400">
      🏆 Manager of the Month
    </h3>
    <p className="text-slate-300">
      {managerOfMonth.manager_name} — {managerOfMonth.mall_name}
    </p>
    <p className="text-yellow-400 font-semibold">
      Score: {managerOfMonth.total_score.toFixed(1)}
    </p>
  </div>
)}

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

                  <td className="p-4 font-medium text-white flex items-center gap-2">
  {s.manager_name}

  {managerOfMonth && s.id === managerOfMonth.id && (
    <span className="px-2 py-0.5 text-xs rounded-full bg-yellow-500 text-black font-semibold">
      🏆 Manager of the Month
    </span>
  )}
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