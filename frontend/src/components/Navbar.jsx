import React from 'react';
import { HeartPulse, PhoneCall, User, LogOut, CalendarCheck, ShieldAlert, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navbar = ({ activeTab, setActiveTab, onOpenAuth, onOpenMyAppointments }) => {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-40 border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 shadow-md shadow-cyan-950/50">
            <HeartPulse className="h-6 w-6 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-base font-bold tracking-tight text-white">MediAssist</span>
              <span className="rounded-md bg-cyan-950 px-1.5 py-0.5 text-[10px] font-bold text-cyan-400 border border-cyan-800/40">
                AI CLINICAL
              </span>
            </div>
            <p className="text-[11px] text-slate-400">Autonomous Hospital Triage & Multi-Agent Network</p>
          </div>
        </div>

        {/* Emergency Hotline Banner */}
        <div className="hidden lg:flex items-center gap-2 rounded-full border border-rose-500/30 bg-rose-500/10 px-3 py-1 text-xs text-rose-400 shadow-sm shadow-rose-950/20">
          <ShieldAlert className="h-3.5 w-3.5 text-rose-400 animate-bounce" />
          <span className="font-semibold">Emergency Trauma: 108 / 102</span>
          <span className="text-slate-500">|</span>
          <span className="text-slate-300">ER Desk: Ext 911</span>
        </div>

        {/* Navigation Tabs */}
        <div className="hidden md:flex items-center space-x-1 rounded-xl bg-slate-900/80 p-1 border border-slate-800">
          {[
            { id: 'chat', label: 'Triage Assistant' },
            { id: 'doctors', label: 'Specialists' },
            { id: 'departments', label: 'Departments' },
            { id: 'lab', label: 'Diagnostic Tests' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* User Account / Auth Actions */}
        <div className="flex items-center gap-2">
          {user ? (
            <div className="flex items-center gap-2">
              <button
                onClick={onOpenMyAppointments}
                className="flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-900/90 px-3 py-1.5 text-xs font-medium text-slate-200 hover:border-cyan-500/40 hover:text-cyan-300 transition-all"
              >
                <CalendarCheck className="h-3.5 w-3.5 text-cyan-400" />
                <span className="hidden sm:inline">My Bookings</span>
              </button>

              <div className="flex items-center gap-2 rounded-lg bg-slate-900 border border-slate-800 px-2.5 py-1 text-xs">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-cyan-600/30 text-cyan-400 font-bold text-[10px]">
                  {user.full_name ? user.full_name[0].toUpperCase() : 'P'}
                </div>
                <div className="hidden sm:block text-left">
                  <p className="font-medium text-slate-200 leading-none">{user.full_name}</p>
                  <p className="text-[10px] text-slate-500 leading-none mt-0.5 truncate max-w-[100px]">{user.email}</p>
                </div>
                <button
                  onClick={logout}
                  title="Sign Out"
                  className="ml-1 p-1 text-slate-400 hover:text-rose-400 transition-colors"
                >
                  <LogOut className="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          ) : (
            <button
              onClick={onOpenAuth}
              className="flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 px-3.5 py-1.5 text-xs font-semibold text-white shadow-md shadow-cyan-950/40 hover:from-cyan-500 hover:to-blue-500 transition-all"
            >
              <User className="h-3.5 w-3.5" />
              <span>Sign In / Demo</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
