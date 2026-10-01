import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import DashboardPage from './pages/DashboardPage';
import AuthModal from './components/AuthModal';
import AppointmentModal from './components/AppointmentModal';
import MyAppointmentsModal from './components/MyAppointmentsModal';
import { ShieldCheck, HeartHandshake, PhoneCall } from 'lucide-react';

const MainApp = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('chat');
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isAppointmentOpen, setIsAppointmentOpen] = useState(false);
  const [isMyAppointmentsOpen, setIsMyAppointmentsOpen] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [bookingSymptoms, setBookingSymptoms] = useState('');
  const [bookingTriage, setBookingTriage] = useState('Low');

  const handleBookDoctor = (doctor, symptoms = '', triageLevel = 'Low') => {
    setSelectedDoctor(doctor);
    setBookingSymptoms(symptoms || '');
    setBookingTriage(triageLevel || 'Low');
    if (!user) {
      setIsAuthOpen(true);
    } else {
      setIsAppointmentOpen(true);
    }
  };

  return (
    <div className="min-h-screen bg-[#070B13] text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenAuth={() => setIsAuthOpen(true)}
        onOpenMyAppointments={() => {
          if (!user) {
            setIsAuthOpen(true);
          } else {
            setIsMyAppointmentsOpen(true);
          }
        }}
      />

      {/* Main Body */}
      <main className="flex-1">
        <DashboardPage
          activeTab={activeTab}
          onBookDoctor={handleBookDoctor}
          onOpenAuth={() => setIsAuthOpen(true)}
        />
      </main>

      {/* Modals */}
      <AuthModal isOpen={isAuthOpen} onClose={() => setIsAuthOpen(false)} />
      <AppointmentModal
        isOpen={isAppointmentOpen}
        onClose={() => setIsAppointmentOpen(false)}
        doctor={selectedDoctor}
        initialSymptoms={bookingSymptoms}
        initialTriage={bookingTriage}
        onSuccess={() => {
          // Keep open to show confirmation
        }}
      />
      <MyAppointmentsModal
        isOpen={isMyAppointmentsOpen}
        onClose={() => setIsMyAppointmentsOpen(false)}
      />

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950/70 py-6 text-center text-xs text-slate-500">
        <div className="mx-auto max-w-7xl px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2 text-slate-400">
            <HeartHandshake className="h-4 w-4 text-cyan-400" />
            <span>MediAssist AI Hospital Assistant • Groq Llama 3.3 70B Clinical Mesh</span>
          </div>

          <p className="text-[11px] text-slate-500 max-w-lg">
            Clinical Decision Support System. In case of acute medical emergencies (chest pain, stroke, heavy bleeding), immediately dial 108 or reach the nearest trauma center.
          </p>

          <div className="flex items-center gap-1.5 text-slate-400">
            <PhoneCall className="h-3.5 w-3.5 text-emerald-400" />
            <span>Helpline: 1800-MED-CARE</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
}

export default App;
