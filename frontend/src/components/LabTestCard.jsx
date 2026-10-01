import React from 'react';
import { FlaskConical, Clock, AlertCircle, CheckCircle2 } from 'lucide-react';

const LabTestCard = ({ test }) => {
  if (!test) return null;

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 shadow-md backdrop-blur-sm transition-all hover:border-cyan-500/40 hover:bg-slate-900/80">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-teal-950/60 border border-teal-800/40 text-teal-400">
            <FlaskConical className="h-5 w-5" />
          </div>
          <div>
            <h4 className="font-semibold text-slate-100 text-sm">{test.name}</h4>
            <p className="text-xs text-slate-400">Sample: {test.sample_type}</p>
          </div>
        </div>
        <span className="inline-flex items-center rounded-full bg-slate-800 px-2.5 py-0.5 text-xs font-semibold text-teal-300">
          ₹{test.price_inr}
        </span>
      </div>

      {test.description && (
        <p className="mt-2.5 text-xs text-slate-300 line-clamp-2">
          {test.description}
        </p>
      )}

      <div className="mt-3 flex items-center justify-between border-t border-slate-800/70 pt-2.5 text-xs text-slate-400">
        <div className="flex items-center gap-1.5">
          <Clock className="h-3.5 w-3.5 text-slate-400" />
          <span>Results in {test.turnaround_hours}h</span>
        </div>
        <div className="flex items-center gap-1">
          {test.fasting_required ? (
            <span className="inline-flex items-center gap-1 text-amber-400 font-medium">
              <AlertCircle className="h-3.5 w-3.5" />
              Fasting Req (8-12h)
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 text-emerald-400 font-medium">
              <CheckCircle2 className="h-3.5 w-3.5" />
              Non-Fasting
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default LabTestCard;
