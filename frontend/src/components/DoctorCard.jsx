import React from 'react';
import { UserCheck, Award, Calendar, DollarSign, Stethoscope, Clock, ShieldCheck } from 'lucide-react';

const DoctorCard = ({ doctor, onBook }) => {
  if (!doctor) return null;

  return (
    <div className="group relative rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg backdrop-blur-md transition-all duration-300 hover:border-cyan-500/40 hover:bg-slate-900/90 hover:shadow-cyan-950/20">
      {/* Header with avatar & name */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/30 text-cyan-400 group-hover:scale-105 transition-transform">
            <Stethoscope className="h-6 w-6" />
          </div>
          <div>
            <h4 className="font-semibold text-slate-100 flex items-center gap-1.5 group-hover:text-cyan-300 transition-colors">
              {doctor.name}
              <ShieldCheck className="h-4 w-4 text-emerald-400 inline" title="Verified Specialist" />
            </h4>
            <p className="text-xs font-medium text-cyan-400/90">{doctor.specialization}</p>
            <p className="text-xs text-slate-400">{doctor.department_name || (doctor.department && doctor.department.name)}</p>
          </div>
        </div>
        <div className="text-right">
          <span className="inline-flex items-center rounded-full bg-cyan-950/60 px-2.5 py-0.5 text-xs font-semibold text-cyan-300 border border-cyan-800/40">
            ₹{doctor.consultation_fee_inr || 800}
          </span>
          <p className="text-[10px] text-slate-400 mt-0.5">Consultation</p>
        </div>
      </div>

      {/* Qualifications & Experience */}
      <div className="mt-4 grid grid-cols-2 gap-2 text-xs border-y border-slate-800/80 py-2.5 my-3">
        <div className="flex items-center gap-1.5 text-slate-300">
          <Award className="h-3.5 w-3.5 text-amber-400" />
          <span>{doctor.experience_years || 10}+ Years Exp</span>
        </div>
        <div className="flex items-center gap-1.5 text-slate-300">
          <UserCheck className="h-3.5 w-3.5 text-blue-400" />
          <span className="truncate">{doctor.qualification || 'MBBS, MD'}</span>
        </div>
      </div>

      {/* OPD Schedule & Room */}
      <div className="space-y-1.5 text-xs text-slate-400 mb-4">
        <div className="flex items-center gap-1.5">
          <Calendar className="h-3.5 w-3.5 text-slate-400" />
          <span className="text-slate-300 font-medium">Days:</span>
          <span className="text-slate-400">{doctor.schedule_days || 'Mon - Fri'}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Clock className="h-3.5 w-3.5 text-slate-400" />
          <span className="text-slate-300 font-medium">Room:</span>
          <span>{doctor.room_no || 'OPD-102'}</span>
        </div>
      </div>

      {/* Booking Action */}
      <button
        onClick={() => onBook && onBook(doctor)}
        className="w-full flex items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 px-4 py-2 text-xs font-semibold text-white shadow-md shadow-cyan-950/40 transition-all hover:from-cyan-500 hover:to-blue-500 active:scale-[0.98]"
      >
        <Calendar className="h-3.5 w-3.5" />
        Book Consultation
      </button>
    </div>
  );
};

export default DoctorCard;
