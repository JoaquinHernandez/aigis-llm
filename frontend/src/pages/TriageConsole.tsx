import { useState } from 'react';

// Mock data to test the UI before the API is fully wired
const MOCK_ALERTS = [
  { id: 'AL-1042', source: 'Sentinel', severity: 'High', log: 'Suspicious PowerShell execution bypassing AMSI...' },
  { id: 'AL-1043', source: 'Splunk', severity: 'Critical', log: 'Multiple failed logins followed by successful RDP session from foreign IP.' }
];

export default function TriageConsole() {
  const [selectedAlert, setSelectedAlert] = useState(MOCK_ALERTS[0]);
  const [triageResult, setTriageResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleRunTriage = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8080/v1/triage/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          alert_id: selectedAlert.id,
          source: selectedAlert.source,
          raw_log: selectedAlert.log,
          severity: selectedAlert.severity
        })
      });
      const data = await response.json();
      setTriageResult(data);
    } catch (error) {
      console.error("Triage execution failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-300 font-sans">
      
      {/* Pane 1: Alert Queue */}
      <div className="w-1/4 border-r border-slate-800 p-4 overflow-y-auto">
        <h2 className="text-xl font-bold text-cyan-400 mb-6">AegisLLM Queue</h2>
        <div className="space-y-3">
          {MOCK_ALERTS.map(alert => (
            <div 
              key={alert.id}
              onClick={() => setSelectedAlert(alert)}
              className={`p-3 rounded border cursor-pointer transition-colors ${
                selectedAlert.id === alert.id ? 'bg-slate-800 border-cyan-500' : 'bg-slate-900 border-slate-700 hover:border-slate-500'
              }`}
            >
              <div className="flex justify-between items-center mb-1">
                <span className="font-mono text-sm">{alert.id}</span>
                <span className={`text-xs px-2 py-1 rounded ${alert.severity === 'Critical' ? 'bg-red-900/50 text-red-400' : 'bg-orange-900/50 text-orange-400'}`}>
                  {alert.severity}
                </span>
              </div>
              <p className="text-xs text-slate-400 truncate">{alert.log}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Pane 2: Raw Log & Action */}
      <div className="w-1/2 flex flex-col border-r border-slate-800">
        <div className="p-4 border-b border-slate-800 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-white">Alert Detail: {selectedAlert.id}</h3>
          <button 
            onClick={handleRunTriage}
            disabled={loading}
            className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded text-sm font-medium transition-colors disabled:opacity-50"
          >
            {loading ? 'Running Analysis...' : 'Run Aegis Triage'}
          </button>
        </div>
        <div className="p-4 flex-grow bg-slate-900/50">
          <h4 className="text-xs uppercase text-slate-500 mb-2 font-bold tracking-wider">Raw Telemetry</h4>
          <pre className="text-xs font-mono bg-slate-950 p-4 rounded border border-slate-800 text-green-400 overflow-x-auto">
            {selectedAlert.log}
          </pre>
        </div>
      </div>

      {/* Pane 3: LLM Analysis Output */}
      <div className="w-1/4 p-4 overflow-y-auto bg-slate-900">
        <h4 className="text-xs uppercase text-slate-500 mb-4 font-bold tracking-wider">AI Analysis</h4>
        
        {!triageResult && !loading && (
          <div className="text-sm text-slate-500 italic">Select an alert and run triage to view analysis.</div>
        )}

        {loading && (
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-slate-800 rounded w-3/4"></div>
            <div className="h-4 bg-slate-800 rounded w-1/2"></div>
            <div className="h-20 bg-slate-800 rounded w-full"></div>
          </div>
        )}

        {triageResult && !loading && (
          <div className="space-y-6 animate-in fade-in duration-300">
            {triageResult.blocked ? (
              <div className="p-3 bg-red-950 border border-red-900 rounded text-red-400 text-sm">
                {triageResult.summary}
              </div>
            ) : (
              <>
                <div>
                  <h5 className="text-xs text-slate-400 mb-1">Executive Summary</h5>
                  <p className="text-sm text-white">{triageResult.summary}</p>
                </div>
                
                <div>
                  <h5 className="text-xs text-slate-400 mb-2">MITRE ATT&CK Mapping</h5>
                  <div className="flex flex-wrap gap-2">
                    {triageResult.mitre_tactics?.map((tactic: str) => (
                      <span key={tactic} className="bg-slate-800 border border-slate-700 px-2 py-1 rounded text-xs text-cyan-300 font-mono">
                        {tactic}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h5 className="text-xs text-slate-400 mb-2">Recommended Actions</h5>
                  <ul className="list-disc list-inside text-sm space-y-1 text-slate-300">
                    {triageResult.recommended_actions?.map((action: str, idx: number) => (
                      <li key={idx}>{action}</li>
                    ))}
                  </ul>
                </div>
              </>
            )}
          </div>
        )}
      </div>

    </div>
  );
}
