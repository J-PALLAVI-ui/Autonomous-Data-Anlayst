import {
  Dataset,
  DashboardStats,
  AnalysisResults,
  ChatMessage,
  CleaningPreview
} from '../types';

const API_BASE = '/api';

export const api = {
  // Dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    if (!res.ok) throw new Error('Failed to fetch dashboard metrics');
    return res.json();
  },

  // Datasets
  async getDatasets(): Promise<Dataset[]> {
    const res = await fetch(`${API_BASE}/datasets`);
    if (!res.ok) throw new Error('Failed to fetch datasets list');
    return res.json();
  },

  async getDataset(id: string): Promise<Dataset> {
    const res = await fetch(`${API_BASE}/datasets/${id}`);
    if (!res.ok) throw new Error('Failed to fetch dataset details');
    return res.json();
  },

  async uploadDataset(file: File): Promise<Dataset> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/datasets/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(err.detail || 'Upload failed');
    }
    return res.json();
  },

  async deleteDataset(id: string): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/datasets/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete dataset');
    return res.json();
  },

  // Autonomous Analysis
  async startAnalysis(datasetId: string): Promise<{ session_id: string; status: string }> {
    const res = await fetch(`${API_BASE}/analysis/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dataset_id: datasetId }),
    });
    if (!res.ok) throw new Error('Failed to start analysis');
    return res.json();
  },

  async getAnalysisStatus(sessionId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/analysis/${sessionId}/status`);
    if (!res.ok) throw new Error('Failed to fetch analysis status');
    return res.json();
  },

  async getAnalysisResults(sessionId: string): Promise<AnalysisResults> {
    const res = await fetch(`${API_BASE}/analysis/${sessionId}/results`);
    if (!res.ok) throw new Error('Failed to fetch analysis results');
    return res.json();
  },

  // Visualizations
  async getVisualizations(id: string): Promise<{ visualizations: any[] }> {
    const res = await fetch(`${API_BASE}/visualizations/${id}`);
    if (!res.ok) throw new Error('Failed to fetch visualizations');
    return res.json();
  },

  // AI Chat
  async sendChatMessage(datasetId: string, message: string, sessionId?: string): Promise<ChatMessage> {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dataset_id: datasetId,
        session_id: sessionId,
        message,
      }),
    });
    if (!res.ok) throw new Error('Failed to process message');
    return res.json();
  },

  async getChatHistory(datasetId: string): Promise<ChatMessage[]> {
    const res = await fetch(`${API_BASE}/chat/${datasetId}/history`);
    if (!res.ok) throw new Error('Failed to fetch chat history');
    return res.json();
  },

  // Data Quality & Cleaning
  async previewCleaning(datasetId: string, operation: string, params: any = {}): Promise<CleaningPreview> {
    const res = await fetch(`${API_BASE}/quality/preview-cleaning`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dataset_id: datasetId,
        operation,
        params,
      }),
    });
    if (!res.ok) throw new Error('Failed to preview cleaning operation');
    return res.json();
  },

  async applyCleaning(datasetId: string, operation: string, params: any = {}): Promise<any> {
    const res = await fetch(`${API_BASE}/quality/apply-cleaning`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dataset_id: datasetId,
        operation,
        params,
      }),
    });
    if (!res.ok) throw new Error('Failed to apply cleaning operation');
    return res.json();
  },

  // Reports
  async getReportMeta(id: string): Promise<any> {
    const res = await fetch(`${API_BASE}/reports/${id}`);
    if (!res.ok) throw new Error('Failed to fetch report');
    return res.json();
  },

  getReportPdfUrl(id: string): string {
    return `${API_BASE}/reports/${id}/pdf`;
  },

  getAnalysisCsvUrl(id: string): string {
    return `${API_BASE}/reports/${id}/csv`;
  },

  // Settings
  async getSettings(): Promise<any> {
    const res = await fetch(`${API_BASE}/settings`);
    if (!res.ok) throw new Error('Failed to fetch settings');
    return res.json();
  },

  async updateSettings(payload: { gemini_api_key?: string }): Promise<any> {
    const res = await fetch(`${API_BASE}/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to update settings');
    return res.json();
  },
};
