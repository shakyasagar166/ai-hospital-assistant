import React, { useState } from 'react';
import { X, Calendar, Clock, Stethoscope, CheckCircle, AlertCircle, FileText } from 'lucide-react';
import { bookAppointment } from '../api/endpoints';
import { useAuth } from '../context/AuthContext';

const AppointmentModal = ({ isOpen, onClose, doctor, initialSymptoms = '', initialTriage = 'Low', onSuccess }) => {
  const { user } = useAuth();
  const [appointmentDate, setAppointmentDate] = useState(() => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().split('T')[0];
  });
  const [timeSlot, setTimeSlot] = useState('10:00 AM');
  const [symptoms, setSymptoms] = useState(initialSymptoms);
  const [triageLevel, setTriageLevel] = useState(initialTriage);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [confirmedAppointment, setConfirmedAppointment] = useState(null);

  if (!isOpen || !doctor) return null;

  const defaultSlots = ['09:00 AM', '10:00 AM', '11:30 AM', '02:00 PM', '03:30 PM', '05:00 PM'];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      setError('Please sign in or use Demo Patient login to confirm an appointment booking.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const payload = {
        doctor_id: doctor.id,
        appointment_date: appointmentDate,
        time_slot: timeSlot,
        symptoms_summary: symptoms || 'Routine medical consultation',
        triage_level: triageLevel || 'Low',
      };

      const result = await bookAppointment(payload);
      setConfirmedAppointment(result);
      if (onSuccess) onSuccess(result);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to book appointment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResetAndClose = () => {
    setConfirmedAppointment(null);
    setError(null);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in">
      <div className="relative w-full max-w-lg rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
        <button
          onClick={handleResetAndClose}
          className="absolute right-4 top-4 rounded-lg p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-100 transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        {confirmedAppointment ? (
          <div className="text-center py-6">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 mb-4 animate-bounce">
              <CheckCircle className="h-10 w-10" />
            </div>
            <h3 className="text-xl font-bold text-slate-100">Appointment Confirmed!</h3>
            <p className="text-sm text-slate-400 mt-1">Your clinical token has been scheduled.</p>

            <div className="my-5 rounded-xl border border-dashed border-emerald-500/40 bg-emerald-950/20 p-4 text-left space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">Confirmation Code:</span>
                <span className="font-mono text-emerald-400 font-bold text-sm tracking-wider">
                  {confirmedAppointment.confirmation_code}
                </span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">Specialist:</span>
                <span className="text-slate-200 font-semibold">{doctor.name}</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">Date & Slot:</span>
                <span className="text-slate-200 font-medium">
                  {confirmedAppointment.appointment_date} at {confirmedAppointment.time_slot}
                </span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">OPD Room:</span>
                <span className="text-cyan-400 font-medium">{doctor.room_no || 'OPD-102'}</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">Consultation Fee:</span>
                <span className="text-slate-200">₹{doctor.consultation_fee_inr} (Pay at desk)</span>
              </div>
            </div>

            <button
              onClick={handleResetAndClose}
              className="w-full rounded-xl bg-cyan-600 py-2.5 font-semibold text-white hover:bg-cyan-500 transition-colors shadow-lg shadow-cyan-950/50"
            >
              Done & Return to Assistant
            </button>
          </div>
        ) : (
          <div>
            <div className="flex items-center gap-3 border-b border-slate-800 pb-4 mb-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-500/20 text-cyan-400">
                <Stethoscope className="h-5 w-5" />
              </div>
              <div>
                <h3 className="font-bold text-slate-100">Schedule Consultation</h3>
                <p className="text-xs text-slate-400">
                  {doctor.name} • {doctor.specialization}
                </p>
              </div>
            </div>

            {error && (
              <div className="mb-4 flex items-center gap-2 rounded-lg bg-rose-500/10 border border-rose-500/30 p-3 text-xs text-rose-400">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1 flex items-center gap-1.5">
                  <Calendar className="h-3.5 w-3.5 text-cyan-400" />
                  Appointment Date
                </label>
                <input
                  type="date"
                  value={appointmentDate}
                  min={new Date().toISOString().split('T')[0]}
                  onChange={(e) => setAppointmentDate(e.target.value)}
                  className="w-full rounded-lg border border-slate-700 bg-slate-800/80 px-3 py-2 text-sm text-slate-100 focus:border-cyan-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5 flex items-center gap-1.5">
                  <Clock className="h-3.5 w-3.5 text-cyan-400" />
                  Available OPD Time Slot
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {defaultSlots.map((slot) => (
                    <button
                      key={slot}
                      type="button"
                      onClick={() => setTimeSlot(slot)}
                      className={`rounded-lg py-2 px-2 text-xs font-medium border transition-all text-center ${
                        timeSlot === slot
                          ? 'border-cyan-500 bg-cyan-500/20 text-cyan-300'
                          : 'border-slate-800 bg-slate-800/50 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                      }`}
                    >
                      {slot}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1 flex items-center gap-1.5">
                  <FileText className="h-3.5 w-3.5 text-cyan-400" />
                  Primary Symptoms / Medical Notes
                </label>
                <textarea
                  rows={3}
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  placeholder="Describe your symptoms, duration, fever, or pain intensity..."
                  className="w-full rounded-lg border border-slate-700 bg-slate-800/80 px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:border-cyan-500 focus:outline-none resize-none"
                />
              </div>

              <div className="rounded-lg bg-slate-800/50 p-3 text-xs flex justify-between items-center text-slate-300">
                <span>Estimated Consultation Fee:</span>
                <span className="text-sm font-bold text-cyan-400">₹{doctor.consultation_fee_inr}</span>
              </div>

              <div className="pt-2 flex gap-3">
                <button
                  type="button"
                  onClick={handleResetAndClose}
                  className="w-1/3 rounded-xl border border-slate-700 py-2.5 text-xs font-medium text-slate-300 hover:bg-slate-800 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="w-2/3 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 py-2.5 text-xs font-bold text-white shadow-lg shadow-cyan-950/40 hover:from-cyan-500 hover:to-blue-500 disabled:opacity-50 transition-all"
                >
                  {loading ? 'Confirming...' : 'Confirm Consultation Booking'}
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default AppointmentModal;
