import React, { useState, useEffect } from 'react';
import { Sidebar, NavTab } from './components/Sidebar';
import { Navbar } from './components/Navbar';
import { DashboardPage } from './pages/DashboardPage';
import { UploadPage } from './pages/UploadPage';
import { AgentPage } from './pages/AgentPage';
import { VisualizationsPage } from './pages/VisualizationsPage';
import { DataQualityPage } from './pages/DataQualityPage';
import { ChatPage } from './pages/ChatPage';
import { ReportsPage } from './pages/ReportsPage';
import { HistoryPage } from './pages/HistoryPage';
import { SettingsPage } from './pages/SettingsPage';
import { Dataset, AnalysisResults } from './types';
import { api } from './services/api';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<NavTab>('dashboard');
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<Dataset | null>(null);

  // Analysis session state
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [sessionStatus, setSessionStatus] = useState<any | null>(null);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);

  // Load datasets on startup
  useEffect(() => {
    loadInitialDatasets();
  }, []);

  const loadInitialDatasets = async () => {
    try {
      const data = await api.getDatasets();
      setDatasets(data);
      if (data.length > 0) {
        // Fetch detailed profile for first dataset
        const detailed = await api.getDataset(data[0].id);
        setSelectedDataset(detailed);
        // Try fetching past results for this dataset
        loadLatestAnalysisForDataset(detailed.id);
      }
    } catch (err) {
      console.error('Error fetching datasets:', err);
    }
  };

  const handleSelectDataset = async (dataset: Dataset) => {
    try {
      const detailed = await api.getDataset(dataset.id);
      setSelectedDataset(detailed);
      loadLatestAnalysisForDataset(detailed.id);
    } catch (err) {
      setSelectedDataset(dataset);
    }
  };

  const loadLatestAnalysisForDataset = async (datasetId: string) => {
    try {
      const res = await api.getVisualizations(datasetId);
      if (res && (res as any).session_id) {
        const fullResults = await api.getAnalysisResults((res as any).session_id);
        setAnalysisResults(fullResults);
        setActiveSessionId(fullResults.session_id);
      } else {
        setAnalysisResults(null);
      }
    } catch (err) {
      setAnalysisResults(null);
    }
  };

  const handleDatasetUploaded = (newDataset: Dataset) => {
    setDatasets((prev) => [newDataset, ...prev.filter((d) => d.id !== newDataset.id)]);
    setSelectedDataset(newDataset);
    setAnalysisResults(null);
    setActiveSessionId(null);
    setCurrentTab('upload');
  };

  const handleDeleteDataset = async (id: string) => {
    try {
      await api.deleteDataset(id);
      const remaining = datasets.filter((d) => d.id !== id);
      setDatasets(remaining);
      if (selectedDataset?.id === id) {
        if (remaining.length > 0) {
          handleSelectDataset(remaining[0]);
        } else {
          setSelectedDataset(null);
          setAnalysisResults(null);
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Launch Autonomous Analysis
  const handleStartAnalysis = async () => {
    if (!selectedDataset || isAnalyzing) return;

    try {
      setIsAnalyzing(true);
      setCurrentTab('analyst');
      setAnalysisResults(null);

      const res = await api.startAnalysis(selectedDataset.id);
      setActiveSessionId(res.session_id);
      setSessionStatus({
        session_id: res.session_id,
        status: 'running',
        current_step: 'understanding',
        progress_percent: 10,
        logs: [],
      });
    } catch (err) {
      console.error(err);
      setIsAnalyzing(false);
    }
  };

  // Polling for active analysis session
  useEffect(() => {
    if (!activeSessionId || !isAnalyzing) return;

    const interval = setInterval(async () => {
      try {
        const status = await api.getAnalysisStatus(activeSessionId);
        setSessionStatus(status);

        if (status.status === 'completed') {
          clearInterval(interval);
          setIsAnalyzing(false);
          const results = await api.getAnalysisResults(activeSessionId);
          setAnalysisResults(results);
        } else if (status.status === 'failed') {
          clearInterval(interval);
          setIsAnalyzing(false);
        }
      } catch (err) {
        console.error('Polling error:', err);
      }
    }, 1200);

    return () => clearInterval(interval);
  }, [activeSessionId, isAnalyzing]);

  // Load a specific historical session
  const handleLoadSession = async (sessionId: string) => {
    try {
      const results = await api.getAnalysisResults(sessionId);
      setAnalysisResults(results);
      setActiveSessionId(sessionId);
      const ds = datasets.find((d) => d.id === results.dataset_id);
      if (ds) {
        handleSelectDataset(ds);
      }
      setCurrentTab('analyst');
    } catch (err) {
      console.error('Failed to load session:', err);
    }
  };

  return (
    <div className="flex h-screen bg-[#0b1120] text-slate-100 overflow-hidden font-sans">
      {/* Sidebar */}
      <Sidebar
        currentTab={currentTab}
        onSelectTab={setCurrentTab}
        datasets={datasets}
        selectedDataset={selectedDataset}
        onSelectDataset={handleSelectDataset}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <Navbar
          currentTab={currentTab}
          selectedDataset={selectedDataset}
          onStartAnalysis={handleStartAnalysis}
          isAnalyzing={isAnalyzing}
        />

        <main className="flex-1 overflow-y-auto bg-gradient-to-b from-slate-950 via-[#0b1120] to-[#090d16]">
          {currentTab === 'dashboard' && (
            <DashboardPage
              onNavigate={setCurrentTab}
              selectedDataset={selectedDataset}
              onSelectDataset={handleSelectDataset}
              onStartAnalysis={handleStartAnalysis}
              isAnalyzing={isAnalyzing}
            />
          )}

          {currentTab === 'upload' && (
            <UploadPage
              onDatasetUploaded={handleDatasetUploaded}
              selectedDataset={selectedDataset}
              onSelectDataset={handleSelectDataset}
              onStartAnalysis={handleStartAnalysis}
              isAnalyzing={isAnalyzing}
              onDeleteDataset={handleDeleteDataset}
            />
          )}

          {currentTab === 'analyst' && (
            <AgentPage
              selectedDataset={selectedDataset}
              onStartAnalysis={handleStartAnalysis}
              isAnalyzing={isAnalyzing}
              activeSessionId={activeSessionId}
              sessionStatus={sessionStatus}
              analysisResults={analysisResults}
              onNavigate={setCurrentTab}
            />
          )}

          {currentTab === 'visualizations' && (
            <VisualizationsPage
              selectedDataset={selectedDataset}
              visualizations={analysisResults?.visualizations || []}
              onStartAnalysis={handleStartAnalysis}
              isAnalyzing={isAnalyzing}
            />
          )}

          {currentTab === 'quality' && (
            <DataQualityPage
              selectedDataset={selectedDataset}
              onDatasetUpdated={handleDatasetUploaded}
            />
          )}

          {currentTab === 'chat' && (
            <ChatPage
              selectedDataset={selectedDataset}
              activeSessionId={activeSessionId}
            />
          )}

          {currentTab === 'reports' && (
            <ReportsPage
              selectedDataset={selectedDataset}
              activeSessionId={activeSessionId}
              analysisResults={analysisResults}
            />
          )}

          {currentTab === 'history' && (
            <HistoryPage
              datasets={datasets}
              selectedDataset={selectedDataset}
              onSelectDataset={handleSelectDataset}
              onNavigate={setCurrentTab}
              onLoadSession={handleLoadSession}
            />
          )}

          {currentTab === 'settings' && <SettingsPage />}
        </main>
      </div>
    </div>
  );
};

export default App;
