import React, { useState } from 'react';
import ScoreForm from './components/ScoreForm';
import ScoreCard from './components/ScoreCard';
import Leaderboard from './components/Leaderboard';
import { calculateScore as calculateScoreAPI } from "./api";

function App() {
  const [view, setView] = useState('form'); // form, result, leaderboard
  const [scoreData, setScoreData] = useState(null);
  const [loading, setLoading] = useState(false);

const calculateScore = async (payload) => {
  setLoading(true);
  try {
    const data = await calculateScoreAPI(payload);
    setScoreData(data);
    setView('result');
  } catch (e) {
    console.error(e);
    alert(e.message || 'Failed to connect to backend');
  } finally {
    setLoading(false);
  }
};
const openScorecardFromLeaderboard = (score) => {
    setScoreData(score);
    setView('result');
};

  return (
    <div className="min-h-screen pb-20">
      {/* Navbar */}
      <nav className="bg-slate-900/80 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setView('form')}>
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white">M</div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">Manager Rewards</span>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => setView('form')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${view === 'form' ? 'bg-white/10 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                Calculator
              </button>
              <button
                onClick={() => setView('leaderboard')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${view === 'leaderboard' ? 'bg-white/10 text-white' : 'text-slate-400 hover:text-white'}`}
              >
                Leaderboard
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pt-10">
        {view === 'form' && (
          <div className="animate-fade-in">
            <div className="mb-8 text-center">
              <h1 className="text-4xl font-extrabold text-white mb-2">Manager Performance Calculator</h1>
              <p className="text-slate-400">Enter metrics for Amritsari Express & Cafe Chennai to generate the score.</p>
            </div>
            <ScoreForm onCalculate={calculateScore} loading={loading} />
          </div>
        )}

        {view === 'result' && scoreData && (
          <div className="max-w-2xl mx-auto">
            <div className="mb-6">
              <button onClick={() => setView('form')} className="text-slate-400 hover:text-white flex items-center space-x-2 transition-colors">
                <span>← Back to Calculator</span>
              </button>
            </div>
            <ScoreCard data={scoreData} onReset={() => setView('form')} />
          </div>
        )}

       {view === 'leaderboard' && (
  <div className="animate-fade-in">
    <Leaderboard onViewScorecard={openScorecardFromLeaderboard} />
  </div>
)}
      </main>
    </div>
  );
}

export default App;
