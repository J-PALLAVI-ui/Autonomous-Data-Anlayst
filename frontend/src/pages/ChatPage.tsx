import React, { useState, useEffect, useRef } from 'react';
import {
  MessageSquareCode,
  Send,
  Sparkles,
  Bot,
  User,
  Zap,
  TrendingUp,
  BarChart2,
  AlertTriangle,
  Lightbulb
} from 'lucide-react';
import { ChatMessage, Dataset } from '../types';
import { api } from '../services/api';
import { ChartRenderer } from '../components/ChartRenderer';

interface ChatPageProps {
  selectedDataset: Dataset | null;
  activeSessionId: string | null;
}

export const ChatPage: React.FC<ChatPageProps> = ({
  selectedDataset,
  activeSessionId,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const suggestedQuestions = [
    'What are the most important findings in this dataset?',
    'Which category has the highest sales or volume?',
    'Show me the chronological monthly trend.',
    'Are there any unusual outliers or anomalies?',
    'What are the strongest correlations between variables?',
    'What strategic recommendations can you provide?'
  ];

  useEffect(() => {
    if (selectedDataset) {
      loadHistory();
    }
  }, [selectedDataset]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const loadHistory = async () => {
    if (!selectedDataset) return;
    try {
      const history = await api.getChatHistory(selectedDataset.id);
      if (history.length > 0) {
        setMessages(history);
      } else {
        // Initial welcome message
        setMessages([
          {
            id: 'welcome',
            role: 'assistant',
            content: `Hello! I am your Autonomous AI Data Analyst. I have fully indexed **${selectedDataset.filename}** (${selectedDataset.row_count.toLocaleString()} rows, ${selectedDataset.column_count} columns). You can ask me any analytical, statistical, or business question about this data, and I will compute the answer directly from your dataset.`,
            created_at: new Date().toISOString(),
          },
        ]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSend = async (textToSend?: string) => {
    const q = (textToSend || input).trim();
    if (!q || !selectedDataset || isLoading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: q,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await api.sendChatMessage(selectedDataset.id, q, activeSessionId || undefined);
      setMessages((prev) => [...prev, res]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          role: 'assistant',
          content: `I encountered an issue processing your query: ${err.message}. Please try rephrasing or asking for specific metrics.`,
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!selectedDataset) {
    return (
      <div className="p-8 max-w-7xl mx-auto">
        <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-12 text-center text-slate-400 text-xs">
          Please select or upload a dataset to begin conversational AI analysis.
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-5xl mx-auto h-[calc(100vh-4rem)] flex flex-col space-y-4">
      {/* Chat Messages Container */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.map((m) => {
          const isUser = m.role === 'user';
          return (
            <div
              key={m.id}
              className={`flex items-start gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}
            >
              {!isUser && (
                <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white shrink-0 mt-1 shadow-md shadow-blue-500/20">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-2xl rounded-2xl p-4 text-xs leading-relaxed shadow-lg ${
                  isUser
                    ? 'bg-blue-600 text-white rounded-tr-none'
                    : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-none space-y-3'
                }`}
              >
                {/* Tools Badge */}
                {!isUser && m.tools_used && m.tools_used.length > 0 && (
                  <div className="flex items-center gap-1.5 flex-wrap pb-2 border-b border-slate-800 text-[10px] text-blue-400">
                    <Zap className="w-3 h-3 text-amber-400" />
                    <span className="font-semibold text-slate-400">Tools:</span>
                    {m.tools_used.map((t) => (
                      <span key={t} className="px-1.5 py-0.5 rounded bg-blue-950/60 border border-blue-500/30 font-mono">
                        {t}
                      </span>
                    ))}
                  </div>
                )}

                {/* Text Content */}
                <div className="whitespace-pre-wrap">{m.content}</div>

                {/* Optional Dynamic Inline Chart */}
                {m.chart && (
                  <div className="pt-2">
                    <ChartRenderer chart={m.chart} />
                  </div>
                )}
              </div>

              {isUser && (
                <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 shrink-0 mt-1">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          );
        })}

        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 text-xs text-slate-400 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-blue-400 animate-spin" />
              <span>Analyzing dataset, executing analytical tools, and synthesizing response...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions Pills */}
      <div className="pt-2 border-t border-slate-800/80">
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          <span className="text-[10px] uppercase font-bold text-slate-500 shrink-0">Prompts:</span>
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(q)}
              className="px-3 py-1 rounded-full text-[11px] bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 hover:text-white shrink-0 transition-all cursor-pointer whitespace-nowrap"
            >
              {q}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="flex items-center gap-2 pt-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSend();
            }}
            placeholder={`Ask a question about ${selectedDataset.filename}...`}
            className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 shadow-inner"
          />
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isLoading}
            className={`p-3 rounded-xl transition-all cursor-pointer shadow-lg ${
              input.trim() && !isLoading
                ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-blue-600/20'
                : 'bg-slate-900 text-slate-600 border border-slate-800 cursor-not-allowed'
            }`}
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
