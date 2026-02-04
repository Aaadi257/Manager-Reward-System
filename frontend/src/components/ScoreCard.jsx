import React from 'react';

const ScoreCard = ({ data, onSave, onDismiss }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="card space-y-6 animate-fade-in-up">
      <div className="text-center border-b border-slate-700/50 pb-6">
        <h2 className="text-3xl font-bold text-white mb-2">{data.manager_name}</h2>
        <p className="text-slate-400 text-lg">{data.mall_name}</p>
        {data.month && (
  <p className="text-slate-500 text-sm mt-1">
    Month: {data.month}
  </p>
)}
        <div className="mt-6 flex flex-col items-center">
          <span className="text-slate-500 uppercase tracking-widest text-sm font-semibold">
            Total Score
          </span>
          <span className={`text-6xl font-extrabold ${getScoreColor(data.total_score)} mt-2`}>
            {data.total_score.toFixed(1)}
          </span>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-slate-300">Score Breakdown</h3>
        <div className="grid grid-cols-1 gap-4">
          {data.breakdown.map((item, idx) => (
            <div
              key={idx}
              className="bg-slate-900/50 rounded-lg p-4 flex justify-between items-center border border-slate-800 hover:border-slate-700 transition-colors"
            >
              <div>
                <p className="font-medium text-white">{item.metric_name}</p>
                <p className="text-xs text-slate-500">{item.details}</p>
              </div>
              <div className="text-right">
                <span className="text-xl font-bold text-indigo-400">{item.score}</span>
                <span className="text-slate-600 text-sm"> / {item.max_score}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="pt-6 flex gap-4">
        <button
          onClick={onSave}
          className="flex-1 py-3 rounded-lg bg-green-600 text-white font-semibold hover:bg-green-700 transition-colors"
        >
          Save to Leaderboard
        </button>

        <button
          onClick={onDismiss}
          className="flex-1 py-3 rounded-lg border border-slate-600 text-slate-300 hover:bg-slate-800 transition-colors"
        >
          Dismiss
        </button>
      </div>
    </div>
  );
};

export default ScoreCard;