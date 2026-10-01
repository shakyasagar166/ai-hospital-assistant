import React, { useState, useEffect, useRef } from 'react';
import {
  Send,
  Sparkles,
  Bot,
  HeartPulse,
  Stethoscope,
  Building2,
  FlaskConical,
  Search,
  AlertTriangle,
  Clock,
  PhoneCall,
  ShieldCheck,
  RefreshCw,
  Info
} from 'lucide-react';
import ChatMessage from '../components/ChatMessage';
import DoctorCard from '../components/DoctorCard';
import DepartmentCard from '../components/DepartmentCard';
import LabTestCard from '../components/LabTestCard';
import TriageBadge from '../components/TriageBadge';
import {
  sendClinicalChat,
  getDoctors,
  getDepartments,
  getLabTests,
} from '../api/endpoints';

const QUICK_PROMPTS = [
  { label: 'Chest Pain Emergency', text: 'Sudden severe crushing chest pain radiating to left arm and shortness of breath.' },
  { label: 'Child High Fever', text: 'My 4-year-old child has high fever 102°F, dry barking cough, and lethargy since last night.' },
  { label: 'Severe Migraine', text: 'Severe throbbing headache on right temple with visual aura, nausea, and sensitivity to light.' },
  { label: 'Diabetes Lab Test', text: 'I need to check my blood sugar and HbA1c. What are the fasting rules and lab test cost?' },
  { label: 'ICU Visiting Hours', text: 'What are the visiting hours and guidelines for visitors in the Intensive Care Unit?' },
];

const DashboardPage = ({ activeTab, onBookDoctor, onOpenAuth }) => {
  // Chat state
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'bot',
      text: 'Hello, I am MediAssist, your Clinical AI Hospital Assistant. Describe your symptoms or medical concern, and our multi-agent triage network will evaluate your condition, recommend specialist doctors, schedule consultations, or guide emergency care.',
      clinical_payload: null,
      agent_steps: [],
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [activePayload, setActivePayload] = useState(null);
  const messagesEndRef = useRef(null);

  // Directory state
  const [doctorsList, setDoctorsList] = useState([]);
  const [departmentsList, setDepartmentsList] = useState([]);
  const [labTestsList, setLabTestsList] = useState([]);
  const [directoryLoading, setDirectoryLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDeptFilter, setSelectedDeptFilter] = useState('');

  // Auto-scroll chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Load directories data
  useEffect(() => {
    const loadDirectories = async () => {
      setDirectoryLoading(true);
      try {
        const [docs, depts, tests] = await Promise.all([
          getDoctors(),
          getDepartments(),
          getLabTests(),
        ]);
        setDoctorsList(docs);
        setDepartmentsList(depts);
        setLabTestsList(tests);
      } catch (err) {
        console.error('Error loading hospital directory:', err);
      } finally {
        setDirectoryLoading(false);
      }
    };
    loadDirectories();
  }, []);

  const handleSendMessage = async (customText = null) => {
    const query = (customText || inputText).trim();
    if (!query || isTyping) return;

    const userMsg = {
      id: Date.now().toString(),
      sender: 'user',
      text: query,
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!customText) setInputText('');
    setIsTyping(true);

    try {
      const response = await sendClinicalChat(query, conversationId);
      if (response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      const botMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'bot',
        text: response.response,
        clinical_payload: response.clinical_payload,
        agent_steps: response.agent_steps || [],
      };

      setMessages((prev) => [...prev, botMsg]);
      if (response.clinical_payload) {
        setActivePayload(response.clinical_payload);
      }
    } catch (err) {
      console.error(err);
      const errorMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'bot',
        text: 'I encountered an issue communicating with the clinical multi-agent system. Please check your backend connection or try again.',
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Filtered doctors
  const filteredDoctors = doctorsList.filter((doc) => {
    const matchesSearch =
      doc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.specialization.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (doc.department_name && doc.department_name.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesDept = selectedDeptFilter ? doc.department_id === Number(selectedDeptFilter) : true;
    return matchesSearch && matchesDept;
  });

  // Filtered lab tests
  const filteredLabTests = labTestsList.filter((t) =>
    t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    t.sample_type.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Filtered departments
  const filteredDepartments = departmentsList.filter((d) =>
    d.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
      {/* TAB 1: CLINICAL CHAT & MULTI-AGENT TRIAGE */}
      {activeTab === 'chat' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Main Chat Stream (8 cols) */}
          <div className="lg:col-span-8 flex flex-col h-[calc(100vh-140px)] rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur-xl shadow-xl overflow-hidden">
            {/* Chat header */}
            <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900/80 px-5 py-3">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-500/20 text-cyan-400">
                  <Bot className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                    MediAssist Multi-Agent Clinical Mesh
                    <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-semibold text-emerald-400 border border-emerald-500/30">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                      Active 7-Agents
                    </span>
                  </h2>
                  <p className="text-[11px] text-slate-400">
                    Groq Llama 3.3 70B • Triage • Doctors • Scheduling • RAG Protocol
                  </p>
                </div>
              </div>

              <button
                onClick={() => {
                  setMessages([messages[0]]);
                  setConversationId(null);
                  setActivePayload(null);
                }}
                className="text-xs text-slate-400 hover:text-cyan-400 transition-colors flex items-center gap-1 p-1 rounded-lg hover:bg-slate-800"
                title="Start New Clinical Session"
              >
                <RefreshCw className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">New Session</span>
              </button>
            </div>

            {/* Quick Prompts Bar */}
            <div className="border-b border-slate-800/80 bg-slate-950/40 px-4 py-2.5 overflow-x-auto flex gap-2 no-scrollbar">
              <span className="text-[11px] text-slate-400 flex items-center gap-1 shrink-0 font-medium">
                <Sparkles className="h-3 w-3 text-amber-400" />
                Quick Scenarios:
              </span>
              {QUICK_PROMPTS.map((prompt, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSendMessage(prompt.text)}
                  className="shrink-0 rounded-full border border-slate-800 bg-slate-900/90 px-3 py-1 text-xs text-slate-300 hover:border-cyan-500/50 hover:text-cyan-300 transition-all active:scale-95"
                >
                  {prompt.label}
                </button>
              ))}
            </div>

            {/* Messages Feed */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4">
              {messages.map((msg) => (
                <ChatMessage
                  key={msg.id}
                  message={msg}
                  onBookDoctor={(doc) => onBookDoctor(doc, activePayload?.triage?.symptoms_summary, activePayload?.triage?.urgency_level)}
                />
              ))}

              {isTyping && (
                <div className="flex items-center gap-3 text-xs text-slate-400">
                  <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-cyan-500/20 text-cyan-400">
                    <HeartPulse className="h-4 w-4 animate-spin text-cyan-400" />
                  </div>
                  <div className="flex items-center gap-2 rounded-2xl border border-slate-800 bg-slate-900 px-4 py-2.5">
                    <span className="h-2 w-2 rounded-full bg-cyan-400 animate-ping" />
                    <span>Clinical Multi-Agent Mesh is diagnosing and evaluating care paths...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Chat Input */}
            <div className="border-t border-slate-800 bg-slate-900/90 p-3 sm:p-4">
              <div className="relative flex items-center">
                <textarea
                  rows={2}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Describe patient symptoms, duration, urgency, or request appointment / test..."
                  className="w-full resize-none rounded-xl border border-slate-700 bg-slate-950/80 p-3 pr-14 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
                />
                <button
                  onClick={() => handleSendMessage()}
                  disabled={!inputText.trim() || isTyping}
                  className="absolute right-2.5 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 p-2.5 text-white shadow-md shadow-cyan-950/40 hover:from-cyan-500 hover:to-blue-500 disabled:opacity-40 transition-all"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
              <div className="mt-2 flex items-center justify-between text-[11px] text-slate-500">
                <span>Tip: Press Enter to send, Shift + Enter for new line</span>
                <span>Medical Triage Assistant is clinical support; always call 108 for life threats.</span>
              </div>
            </div>
          </div>

          {/* Right Clinical Sidebar (4 cols) */}
          <div className="lg:col-span-4 space-y-4">
            {/* Triage Decision Card */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-xl shadow-xl">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2 border-b border-slate-800 pb-3">
                <HeartPulse className="h-4 w-4 text-cyan-400" />
                Active Clinical Triage Assessment
              </h3>

              {activePayload?.triage ? (
                <div className="mt-3.5 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-400">Urgency Level:</span>
                    <TriageBadge level={activePayload.triage.urgency_level} size="md" />
                  </div>

                  {activePayload.triage.primary_department && (
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-slate-400">Target Ward:</span>
                      <span className="font-semibold text-cyan-300">
                        {activePayload.triage.primary_department}
                      </span>
                    </div>
                  )}

                  <div className="rounded-lg bg-slate-950/70 p-3 border border-slate-800 text-xs">
                    <span className="text-slate-400 font-medium block mb-1">Recommended Action:</span>
                    <p className="text-slate-200 leading-relaxed">
                      {activePayload.triage.recommended_action}
                    </p>
                  </div>

                  {activePayload.triage.red_flag_warnings?.length > 0 && (
                    <div className="rounded-lg bg-rose-950/20 border border-rose-500/30 p-2.5 text-xs text-rose-300">
                      <span className="font-bold flex items-center gap-1 mb-1">
                        <AlertTriangle className="h-3.5 w-3.5" />
                        Red Flag Warnings:
                      </span>
                      <ul className="list-disc list-inside space-y-0.5 text-rose-200/90 text-[11px]">
                        {activePayload.triage.red_flag_warnings.map((rf, idx) => (
                          <li key={idx}>{rf}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="py-8 text-center text-slate-500 text-xs">
                  <Info className="h-8 w-8 mx-auto mb-2 text-slate-600" />
                  <p>No active symptoms evaluated yet.</p>
                  <p className="mt-1 text-[11px]">
                    Enter your symptoms in the chat to see real-time AI triage status.
                  </p>
                </div>
              )}
            </div>

            {/* Quick Available Slots / Recommended Doctor */}
            {activePayload?.doctors?.length > 0 && (
              <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-xl shadow-xl">
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2 border-b border-slate-800 pb-3">
                  <Stethoscope className="h-4 w-4 text-cyan-400" />
                  Recommended Specialist
                </h3>
                <div className="mt-3">
                  <DoctorCard
                    doctor={activePayload.doctors[0]}
                    onBook={(doc) => onBookDoctor(doc, activePayload?.triage?.symptoms_summary, activePayload?.triage?.urgency_level)}
                  />
                </div>
              </div>
            )}

            {/* Quick Hospital Contacts & Info */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-xl shadow-xl text-xs space-y-3">
              <h4 className="font-bold text-slate-200 flex items-center gap-2 border-b border-slate-800 pb-2">
                <Building2 className="h-4 w-4 text-cyan-400" />
                Hospital Quick Desk Info
              </h4>
              <div className="space-y-2 text-slate-300">
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">🚨 Trauma & ER:</span>
                  <span className="font-bold text-rose-400">108 / Ext 911 (24/7)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">🏥 OPD Consultation:</span>
                  <span>08:00 AM – 08:00 PM</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">🕒 ICU Visiting:</span>
                  <span>11:00 AM - 12:00 PM & 05:00 - 06:00 PM</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">💊 Pharmacy:</span>
                  <span className="text-emerald-400 font-semibold">24/7 Ground Floor</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: SPECIALIST DOCTORS DIRECTORY */}
      {activeTab === 'doctors' && (
        <div className="space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                <Stethoscope className="h-6 w-6 text-cyan-400" />
                Specialist Doctors Directory
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Consult with top board-certified physicians, surgeons, and specialists
              </p>
            </div>

            {/* Filters */}
            <div className="flex flex-wrap items-center gap-3">
              <div className="relative">
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
                <input
                  type="text"
                  placeholder="Search doctor or specialization..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="rounded-xl border border-slate-700 bg-slate-900/90 py-2 pl-9 pr-3 text-xs text-slate-100 placeholder-slate-500 focus:border-cyan-500 focus:outline-none w-64"
                />
              </div>

              <select
                value={selectedDeptFilter}
                onChange={(e) => setSelectedDeptFilter(e.target.value)}
                className="rounded-xl border border-slate-700 bg-slate-900/90 py-2 px-3 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
              >
                <option value="">All Departments</option>
                {departmentsList.map((dept) => (
                  <option key={dept.id} value={dept.id}>
                    {dept.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {directoryLoading ? (
            <div className="py-20 text-center text-slate-400 text-sm">
              <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-2 text-cyan-400" />
              Loading specialists...
            </div>
          ) : filteredDoctors.length === 0 ? (
            <div className="py-20 text-center text-slate-500 text-sm">
              No specialist doctors found matching your criteria.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {filteredDoctors.map((doc) => (
                <DoctorCard key={doc.id} doctor={doc} onBook={onBookDoctor} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* TAB 3: DEPARTMENTS DIRECTORY */}
      {activeTab === 'departments' && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                <Building2 className="h-6 w-6 text-cyan-400" />
                Clinical Departments & Units
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Explore specialized inpatient wings, emergency facilities, and surgical theaters
              </p>
            </div>

            <div className="relative">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
              <input
                type="text"
                placeholder="Search departments..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="rounded-xl border border-slate-700 bg-slate-900/90 py-2 pl-9 pr-3 text-xs text-slate-100 placeholder-slate-500 focus:border-cyan-500 focus:outline-none w-64"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filteredDepartments.map((dept) => (
              <DepartmentCard
                key={dept.id}
                department={dept}
                onSelectDepartment={() => {
                  setSelectedDeptFilter(dept.id);
                  // switch to doctors
                }}
              />
            ))}
          </div>
        </div>
      )}

      {/* TAB 4: DIAGNOSTIC LAB TESTS */}
      {activeTab === 'lab' && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                <FlaskConical className="h-6 w-6 text-teal-400" />
                Diagnostic Pathology & Radiology Tests
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Accredited medical diagnostic lab tests with automated report delivery
              </p>
            </div>

            <div className="relative">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
              <input
                type="text"
                placeholder="Search blood test, MRI, ECG..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="rounded-xl border border-slate-700 bg-slate-900/90 py-2 pl-9 pr-3 text-xs text-slate-100 placeholder-slate-500 focus:border-cyan-500 focus:outline-none w-64"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredLabTests.map((test) => (
              <LabTestCard key={test.id} test={test} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
