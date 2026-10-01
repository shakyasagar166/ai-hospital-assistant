import React from 'react';
import { Building2, PhoneCall, MapPin, User, ChevronRight, Activity } from 'lucide-react';

const DepartmentCard = ({ department, onSelectDepartment }) => {
  if (!department) return null;

  return (
    <div className="group relative rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg backdrop-blur-md transition-all duration-300 hover:border-cyan-500/40 hover:bg-slate-900/90">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-cyan-950/70 border border-cyan-800/40 text-cyan-400 group-hover:scale-105 transition-transform">
            <Building2 className="h-5 w-5" />
          </div>
          <div>
            <h4 className="font-semibold text-slate-100 group-hover:text-cyan-300 transition-colors">
              {department.name}
            </h4>
            <div className="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
              <span className="flex items-center gap-1">
                <MapPin className="h-3 w-3 text-cyan-400" />
                {department.floor || 'Ground Floor'}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <PhoneCall className="h-3 w-3 text-emerald-400" />
                Ext: {department.phone_extension || '101'}
              </span>
            </div>
          </div>
        </div>
      </div>

      <p className="mt-3 text-xs leading-relaxed text-slate-300 line-clamp-2">
        {department.description || 'Comprehensive clinical care and inpatient diagnosis services.'}
      </p>

      <div className="mt-3 pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
        <div className="flex items-center gap-1.5 text-slate-400">
          <User className="h-3.5 w-3.5 text-slate-400" />
          <span className="text-slate-300">HOD:</span>
          <span className="text-slate-400 truncate max-w-[120px]">{department.hod || 'Chief Physician'}</span>
        </div>

        {onSelectDepartment && (
          <button
            onClick={() => onSelectDepartment(department)}
            className="flex items-center gap-1 font-medium text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            <span>Doctors</span>
            <ChevronRight className="h-3.5 w-3.5" />
          </button>
        )}
      </div>
    </div>
  );
};

export default DepartmentCard;
