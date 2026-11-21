import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import { ChartDefinition } from '../types';

interface ChartRendererProps {
  chart: ChartDefinition;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#06b6d4', '#f97316', '#64748b'];

export const ChartRenderer: React.FC<ChartRendererProps> = ({ chart }) => {
  const { chart_type, data, x_axis, y_axis, title, description, insights, config } = chart;

  if (!data || data.length === 0) {
    return (
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 text-center text-slate-400">
        <p>No chart data available for this visualization.</p>
      </div>
    );
  }

  const renderChartContent = () => {
    switch (chart_type) {
      case 'bar': {
        const keys = Object.keys(data[0] || {}).filter((k) => k !== x_axis);
        return (
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis
                dataKey={x_axis || 'name'}
                stroke="#64748b"
                tick={{ fill: '#94a3b8', fontSize: 11 }}
                angle={-20}
                textAnchor="end"
              />
              <YAxis stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '0.5rem',
                  color: '#f8fafc',
                }}
              />
              <Legend wrapperStyle={{ paddingTop: 12 }} />
              {keys.map((k, idx) => (
                <Bar
                  key={k}
                  dataKey={k}
                  fill={COLORS[idx % COLORS.length]}
                  radius={[4, 4, 0, 0]}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        );
      }

      case 'line': {
        const keys = Object.keys(data[0] || {}).filter((k) => k !== x_axis);
        return (
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis
                dataKey={x_axis || 'period'}
                stroke="#64748b"
                tick={{ fill: '#94a3b8', fontSize: 11 }}
                angle={-20}
                textAnchor="end"
              />
              <YAxis stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '0.5rem',
                  color: '#f8fafc',
                }}
              />
              <Legend wrapperStyle={{ paddingTop: 12 }} />
              {keys.map((k, idx) => (
                <Line
                  key={k}
                  type="monotone"
                  dataKey={k}
                  stroke={COLORS[idx % COLORS.length]}
                  strokeWidth={2.5}
                  dot={{ r: 3, fill: COLORS[idx % COLORS.length] }}
                  activeDot={{ r: 6 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        );
      }

      case 'pie': {
        return (
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '0.5rem',
                  color: '#f8fafc',
                }}
              />
              <Legend wrapperStyle={{ paddingTop: 12 }} />
              <Pie
                data={data}
                dataKey={y_axis || 'value'}
                nameKey={x_axis || 'name'}
                cx="50%"
                cy="50%"
                innerRadius={65}
                outerRadius={105}
                paddingAngle={4}
                label={({ name, percent }: any) => `${name} (${(percent * 100).toFixed(0)}%)`}
              >
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        );
      }

      case 'histogram': {
        return (
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis
                dataKey={x_axis || 'bin'}
                stroke="#64748b"
                tick={{ fill: '#94a3b8', fontSize: 10 }}
                angle={-20}
                textAnchor="end"
              />
              <YAxis stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '0.5rem',
                  color: '#f8fafc',
                }}
              />
              <Bar dataKey={y_axis || 'frequency'} fill="#0ea5e9" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );
      }

      case 'scatter': {
        return (
          <ResponsiveContainer width="100%" height={320}>
            <ScatterChart margin={{ top: 10, right: 20, left: 0, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis
                dataKey={x_axis || 'x'}
                type="number"
                name={x_axis || 'X'}
                stroke="#64748b"
                tick={{ fill: '#94a3b8', fontSize: 11 }}
              />
              <YAxis
                dataKey={y_axis || 'y'}
                type="number"
                name={y_axis || 'Y'}
                stroke="#64748b"
                tick={{ fill: '#94a3b8', fontSize: 11 }}
              />
              <Tooltip
                cursor={{ strokeDasharray: '3 3' }}
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderColor: '#334155',
                  borderRadius: '0.5rem',
                  color: '#f8fafc',
                }}
              />
              <Scatter name="Points" data={data} fill="#f97316" />
            </ScatterChart>
          </ResponsiveContainer>
        );
      }

      case 'box': {
        return (
          <div className="space-y-4 py-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {data.map((item: any) => (
                <div
                  key={item.column}
                  className="bg-slate-950/70 border border-slate-800 rounded-lg p-3 text-xs space-y-2"
                >
                  <div className="flex justify-between items-center font-semibold text-slate-200">
                    <span>{item.column}</span>
                    <span className="text-blue-400">Median: {item.median}</span>
                  </div>
                  <div className="relative pt-4 pb-2">
                    <div className="h-2 bg-slate-800 rounded-full w-full relative">
                      <div
                        className="absolute top-0 h-2 bg-blue-600 rounded-full"
                        style={{
                          left: '25%',
                          width: '50%',
                        }}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-5 text-[10px] text-slate-400 text-center">
                    <div>Min<br /><span className="text-slate-300">{item.min}</span></div>
                    <div>Q1<br /><span className="text-slate-300">{item.q25}</span></div>
                    <div>Med<br /><span className="text-blue-400 font-semibold">{item.median}</span></div>
                    <div>Q3<br /><span className="text-slate-300">{item.q75}</span></div>
                    <div>Max<br /><span className="text-slate-300">{item.max}</span></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      }

      case 'heatmap': {
        const columns: string[] = config?.columns || [];
        if (columns.length === 0) return null;

        // Group cells into lookup map
        const lookup: Record<string, number> = {};
        data.forEach((c: any) => {
          lookup[`${c.x}__${c.y}`] = c.correlation;
        });

        const getColor = (val: number) => {
          if (val >= 0.7) return 'bg-emerald-600 text-white';
          if (val >= 0.4) return 'bg-emerald-800/80 text-emerald-200';
          if (val > 0.1) return 'bg-blue-900/40 text-blue-300';
          if (val >= -0.1) return 'bg-slate-800 text-slate-400';
          if (val >= -0.4) return 'bg-orange-950 text-orange-300';
          if (val >= -0.7) return 'bg-rose-900/80 text-rose-200';
          return 'bg-rose-600 text-white';
        };

        return (
          <div className="overflow-x-auto py-2">
            <table className="min-w-full text-xs">
              <thead>
                <tr>
                  <th className="p-2 text-left text-slate-500 font-medium"></th>
                  {columns.map((c) => (
                    <th key={c} className="p-2 text-center text-slate-400 font-semibold max-w-[90px] truncate" title={c}>
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {columns.map((rowCol) => (
                  <tr key={rowCol} className="border-t border-slate-800/60">
                    <td className="p-2 font-medium text-slate-300 max-w-[110px] truncate" title={rowCol}>
                      {rowCol}
                    </td>
                    {columns.map((colCol) => {
                      const val = lookup[`${colCol}__${rowCol}`] ?? 0;
                      return (
                        <td key={colCol} className="p-1 text-center">
                          <div
                            className={`rounded px-1.5 py-1 text-[11px] font-mono transition-transform hover:scale-105 cursor-pointer ${getColor(val)}`}
                            title={`${rowCol} vs ${colCol}: r = ${val}`}
                          >
                            {val.toFixed(2)}
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      }

      default:
        return <p className="text-slate-400">Unsupported chart type.</p>;
    }
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 hover:border-slate-700/80 rounded-xl p-5 transition-all shadow-lg flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between mb-1">
          <h3 className="font-semibold text-slate-100 text-base">{title}</h3>
          <span className="px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
            {chart_type}
          </span>
        </div>
        {description && (
          <p className="text-xs text-slate-400 mb-4">{description}</p>
        )}

        <div className="mt-2 min-h-[320px] flex items-center justify-center">
          {renderChartContent()}
        </div>
      </div>

      {insights && (
        <div className="mt-4 pt-3 border-t border-slate-800/80 text-xs text-slate-300 flex items-center gap-2">
          <span className="inline-block w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
          <span><b>Insight:</b> {insights}</span>
        </div>
      )}
    </div>
  );
};
