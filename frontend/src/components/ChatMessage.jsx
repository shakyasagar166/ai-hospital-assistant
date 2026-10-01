import React, { useState } from 'react';
import { User, HeartPulse, ChevronDown, ChevronUp, Bot, AlertOctagon, Stethoscope, FlaskConical, Calendar, ArrowRight } from 'lucide-react';
import TriageBadge from './TriageBadge';

const ChatMessage = ({ message, onBookDoctor }) => {
  const isUser = message.sender === 'user';
  const [showSteps, setShowSteps] = useState(false);

  const payload = message.clinical_payload;
  const triage = payload?.triage;
  const doctors = payload?.doctors || [];
  const labTests = payload?.lab_tests || [];
  const steps = message.agent_steps || [];

  return (
    <div className={`flex w-full gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {/* Bot Avatar */}
      {!isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 text-white shadow-md shadow-cyan-950/40 mt-1">
          <HeartPulse className="h-5 w-5" />
        </div>
      )}

      {/* Message Bubble */}
      <div
        className={`relative max-w-2xl rounded-2xl p-4 shadow-lg ${
          isUser
            ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-tr-none'
            : 'border border-slate-800 bg-slate-900/90 text-slate-100 rounded-tl-none backdrop-blur-md'
        }`}
      >
        {/* User Message */}
        {isUser ? (
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
        ) : (
          <div className="space-y-3.5">
            {/* Multi-Agent Execution Steps (collapsible) */}
            {steps.length > 0 && (
              <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-2 text-xs">
                <button
                  onClick={() => setShowSteps(!showSteps)}
                  className="flex w-full items-center justify-between font-medium text-slate-400 hover:text-cyan-400 transition-colors"
                >
                  <span className="flex items-center gap-1.5">
                    <Bot className="h-3.5 w-3.5 text-cyan-400" />
                    <span>Multi-Agent Routing ({steps.length} Agents Orchestrated)</span>
                  </span>
                  {showSteps ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                </button>

                {showSteps && (
                  <div className="mt-2.5 space-y-1.5 border-t border-slate-800/80 pt-2">
                    {steps.map((st, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-[11px] text-slate-300">
                        <span className="mt-0.5 inline-block h-1.5 w-1.5 rounded-full bg-cyan-400" />
                        <div>
                          <span className="font-semibold text-cyan-300">{st.agent}:</span>{' '}
                          <span className="text-slate-400">{st.output}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Triage Urgency Header */}
            {triage && (
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-2.5">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">Clinical Triage:</span>
                  <TriageBadge level={triage.urgency_level} size="md" />
                </div>
                {triage.primary_department && (
                  <span className="rounded-md bg-slate-800 px-2 py-0.5 text-xs text-cyan-300 font-medium">
                    {triage.primary_department} Department
                  </span>
                )}
              </div>
            )}

            {/* Emergency Alert Banner */}
            {triage?.is_emergency && (
              <div className="rounded-xl border border-rose-500/50 bg-rose-950/40 p-3.5 text-rose-200">
                <div className="flex items-start gap-2.5">
                  <AlertOctagon className="h-5 w-5 text-rose-400 shrink-0 mt-0.5 animate-pulse" />
                  <div>
                    <h5 className="font-bold text-rose-300 text-xs sm:text-sm">EMERGENCY PROTOCOL ACTIVATED</h5>
                    <p className="text-xs text-rose-200/90 mt-1 leading-relaxed">
                      {payload?.emergency_instructions || 'Life-threatening indicators detected. Please proceed directly to the Emergency Department or dial 108.'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Main Clinical Response Text */}
            <div className="text-xs sm:text-sm leading-relaxed text-slate-200 whitespace-pre-wrap">
              {message.text}
            </div>

            {/* Red Flag Warnings */}
            {triage?.red_flag_warnings && triage.red_flag_warnings.length > 0 && (
              <div className="rounded-lg bg-amber-950/20 border border-amber-500/30 p-2.5 text-xs text-amber-300">
                <p className="font-semibold mb-1">Key Clinical Red Flags:</p>
                <ul className="list-disc list-inside space-y-0.5 text-amber-200/90">
                  {triage.red_flag_warnings.map((rf, i) => (
                    <li key={i}>{rf}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recommended Specialists Inline in Chat */}
            {doctors.length > 0 && (
              <div className="mt-3 space-y-2">
                <p className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <Stethoscope className="h-3.5 w-3.5 text-cyan-400" />
                  Recommended Specialist Doctors:
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {doctors.slice(0, 2).map((doc, i) => (
                    <div
                      key={i}
                      className="rounded-lg border border-slate-800 bg-slate-950/70 p-2.5 flex flex-col justify-between"
                    >
                      <div>
                        <p className="font-medium text-xs text-slate-100">{doc.name}</p>
                        <p className="text-[11px] text-cyan-400">{doc.specialization}</p>
                        <p className="text-[10px] text-slate-400 mt-1">
                          Exp: {doc.experience_years} yrs • Fee: ₹{doc.consultation_fee_inr}
                        </p>
                      </div>
                      <button
                        onClick={() => onBookDoctor && onBookDoctor(doc)}
                        className="mt-2 flex items-center justify-center gap-1 rounded bg-cyan-600/30 hover:bg-cyan-600/50 border border-cyan-500/40 py-1 text-[11px] font-semibold text-cyan-200 transition-colors"
                      >
                        <Calendar className="h-3 w-3" />
                        <span>Book Slot</span>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommended Lab Tests Inline in Chat */}
            {labTests.length > 0 && (
              <div className="mt-2 space-y-1.5">
                <p className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <FlaskConical className="h-3.5 w-3.5 text-teal-400" />
                  Recommended Diagnostic Lab Tests:
                </p>
                <div className="flex flex-wrap gap-1.5">
                  {labTests.map((t, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1 rounded-md bg-teal-950/40 border border-teal-800/40 px-2 py-1 text-[11px] text-teal-300"
                    >
                      <span className="font-medium">{t.name}</span>
                      <span className="text-slate-400">(₹{t.price_inr})</span>
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-800 text-slate-200 border border-slate-700 mt-1">
          <User className="h-5 w-5" />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
