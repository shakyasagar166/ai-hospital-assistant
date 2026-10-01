import React from 'react';
import { AlertCircle, AlertTriangle, Clock, CheckCircle } from 'lucide-react';

const TriageBadge = ({ level = 'Low', size = 'md' }) => {
  const normalized = (level || 'Low').toLowerCase();

  const configs = {
    emergency: {
      label: 'Emergency',
      bg: 'bg-rose-500/15 text-rose-400 border-rose-500/40 shadow-rose-950/40',
      dot: 'bg-rose-500 animate-ping',
      icon: AlertCircle,
    },
    urgent: {
      label: 'Urgent',
      bg: 'bg-amber-500/15 text-amber-400 border-amber-500/40 shadow-amber-950/40',
      dot: 'bg-amber-400',
      icon: AlertTriangle,
    },
    medium: {
      label: 'Moderate',
      bg: 'bg-sky-500/15 text-sky-400 border-sky-500/40 shadow-sky-950/40',
      dot: 'bg-sky-400',
      icon: Clock,
    },
    low: {
      label: 'Routine / Low',
      bg: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/40 shadow-emerald-950/40',
      dot: 'bg-emerald-400',
      icon: CheckCircle,
    },
  };

  const config = configs[normalized] || configs.low;
  const Icon = config.icon;

  const sizeClasses = size === 'sm' 
    ? 'text-xs px-2 py-0.5 space-x-1.5' 
    : size === 'lg' 
      ? 'text-sm px-3.5 py-1.5 space-x-2.5 font-semibold' 
      : 'text-xs px-2.5 py-1 space-x-2 font-medium';

  return (
    <span
      className={`inline-flex items-center rounded-full border shadow-sm backdrop-blur-sm transition-all ${config.bg} ${sizeClasses}`}
    >
      <span className="relative flex h-2 w-2">
        {normalized === 'emergency' && (
          <span className={`absolute inline-flex h-full w-full rounded-full opacity-75 ${config.dot}`} />
        )}
        <span className={`relative inline-flex rounded-full h-2 w-2 ${normalized === 'emergency' ? 'bg-rose-500' : config.dot}`} />
      </span>
      <Icon className={size === 'lg' ? 'w-4 h-4' : 'w-3.5 h-3.5'} />
      <span>{config.label}</span>
    </span>
  );
};

export default TriageBadge;
