import React, { useState, useEffect } from 'react';
import { X, CalendarCheck, Clock, User, AlertCircle, RefreshCw, Trash2, CheckCircle2 } from 'lucide-react';
import { getMyAppointments, cancelAppointment } from '../api/endpoints';
import TriageBadge from './TriageBadge';

const MyAppointmentsModal = ({ isOpen, onClose }) => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAppointments = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getMyAppointments();
      setAppointments(data);
    } catch (err) {
      console.error(err);
      setError('Failed to load appointments.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchAppointments();
    }
  }, [isOpen]);

  const handleCancel = async (id) => {
    if (!window.confirm('Are you sure you want to cancel this appointment?')) return;
    try {
      await cancelAppointment(id);
      fetchAppointments();
    } catch (err) {
      console.error(err);
      alert('Could not cancel appointment.');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in">
      <div className="relative w-full max-w-2xl max-h-[85vh] flex flex-col rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/20 text-cyan-400">
              <CalendarCheck className="h-5 w-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-100">My Consultation Bookings</h3>
              <p className="text-xs text-slate-400">Your scheduled outpatient appointments and tokens</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={fetchAppointments}
              disabled={loading}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors"
              title="Refresh"
            >
              <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Content list */}
        <div className="flex-1 overflow-y-auto pr-1 space-y-3">
          {loading && appointments.length === 0 ? (
            <div className="py-12 text-center text-slate-400 text-sm">
              <RefreshCw className="h-6 w-6 animate-spin mx-auto mb-2 text-cyan-400" />
              Loading your clinical bookings...
            </div>
          ) : error ? (
            <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center gap-2">
              <AlertCircle className="h-4 w-4" />
              <span>{error}</span>
            </div>
          ) : appointments.length === 0 ? (
            <div className="py-12 text-center text-slate-400 text-sm">
              <CalendarCheck className="h-10 w-10 mx-auto mb-2 text-slate-600" />
              <p className="font-medium text-slate-300">No appointments scheduled</p>
              <p className="text-xs text-slate-500 mt-1">
                You can chat with our AI triage assistant or choose a specialist from the doctors directory.
              </p>
            </div>
          ) : (
            appointments.map((appt) => (
              <div
                key={appt.id}
                className="rounded-xl border border-slate-800 bg-slate-950/70 p-4 transition-all hover:border-slate-700"
              >
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="font-bold text-slate-100 text-sm">
                        {appt.doctor ? appt.doctor.name : `Doctor #${appt.doctor_id}`}
                      </h4>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase ${
                          appt.status === 'confirmed'
                            ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                            : 'bg-rose-500/20 text-rose-400 border-rose-500/40'
                        }`}
                      >
                        {appt.status}
                      </span>
                    </div>
                    <p className="text-xs text-cyan-400 mt-0.5">
                      {appt.doctor ? appt.doctor.specialization : 'Specialist Consultant'}
                    </p>
                  </div>

                  <div className="text-right">
                    <span className="font-mono text-xs font-bold text-slate-300 bg-slate-800/80 px-2 py-1 rounded border border-slate-700">
                      {appt.confirmation_code}
                    </span>
                  </div>
                </div>

                <div className="mt-3 grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs border-t border-slate-800/70 pt-2.5 text-slate-300">
                  <div>
                    <span className="text-slate-500 block text-[10px]">Date:</span>
                    <span>{appt.appointment_date}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Time Slot:</span>
                    <span>{appt.time_slot}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Triage Priority:</span>
                    <TriageBadge level={appt.triage_level} size="sm" />
                  </div>
                </div>

                {appt.symptoms_summary && (
                  <p className="mt-2 text-xs text-slate-400 bg-slate-900/60 p-2 rounded border border-slate-800/80">
                    <span className="text-slate-500 font-medium">Notes: </span>
                    {appt.symptoms_summary}
                  </p>
                )}

                {appt.status === 'confirmed' && (
                  <div className="mt-3 flex justify-end">
                    <button
                      onClick={() => handleCancel(appt.id)}
                      className="flex items-center gap-1 text-xs text-rose-400 hover:text-rose-300 transition-colors"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                      <span>Cancel Booking</span>
                    </button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default MyAppointmentsModal;
