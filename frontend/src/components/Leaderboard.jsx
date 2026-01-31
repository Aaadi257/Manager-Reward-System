import React, { useEffect, useState } from 'react';

const Leaderboard = () => {
    const [scores, setScores] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/leaderboard')
            .then(res => res.json())
            .then(data => {
                setScores(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className="text-center text-slate-400 py-10">Loading Leaderboard...</div>;

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
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {scores.length === 0 ? (
                            <tr><td colSpan="4" className="p-4 text-center text-slate-500">No scores yet.</td></tr>
                        ) : (
                            scores.map((s, idx) => (
                                <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                                    <td className="p-4 text-slate-500 font-mono">#{idx + 1}</td>
                                    <td className="p-4 font-medium text-white">{s.manager_name}</td>
                                    <td className="p-4 text-slate-300">{s.mall_name}</td>
                                    <td className="p-4 text-right font-bold text-indigo-400">{s.total_score.toFixed(1)}</td>
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
