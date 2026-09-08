"use client";
import { useState, useEffect } from "react";
import { Zap, Phone, Key, Sparkles, Check, AlertCircle } from "lucide-react";
import { getGeminiConfig, saveGeminiApiKey } from "@/lib/api";

export function Sidebar({ lang, setLang, isOpen, setIsOpen, isLowBandwidth, setIsLowBandwidth }: { lang: string, setLang: (l: string) => void, isOpen: boolean, setIsOpen: (o: boolean) => void, isLowBandwidth: boolean, setIsLowBandwidth: (b: boolean) => void }) {
  const [geminiStatus, setGeminiStatus] = useState<{ has_key: boolean; masked_key: string; model: string } | null>(null);
  const [apiKeyInput, setApiKeyInput] = useState("");
  const [isEditingKey, setIsEditingKey] = useState(false);
  const [isSavingKey, setIsSavingKey] = useState(false);
  const [saveMessage, setSaveMessage] = useState<{ text: string; type: "success" | "error" } | null>(null);

  useEffect(() => {
    getGeminiConfig()
      .then((data) => {
        setGeminiStatus(data);
        if (!data.has_key) {
          setIsEditingKey(true);
        }
      })
      .catch(() => {
        setGeminiStatus({ has_key: false, masked_key: "", model: "Gemini 2.5 Flash" });
        setIsEditingKey(true);
      });
  }, []);

  const handleSaveKey = async () => {
    if (!apiKeyInput.trim()) return;
    setIsSavingKey(true);
    setSaveMessage(null);
    try {
      const res = await saveGeminiApiKey(apiKeyInput.trim());
      if (res.status === "success") {
        setGeminiStatus({ has_key: true, masked_key: res.masked_key, model: "Gemini 2.5 Flash" });
        setIsEditingKey(false);
        setApiKeyInput("");
        setSaveMessage({ text: "API Key Connected Successfully!", type: "success" });
        setTimeout(() => setSaveMessage(null), 3500);
      } else {
        setSaveMessage({ text: res.message || "Failed to save API key", type: "error" });
        setTimeout(() => setSaveMessage(null), 3500);
      }
    } catch (e) {
      setSaveMessage({ text: "Failed to connect to backend", type: "error" });
      setTimeout(() => setSaveMessage(null), 3500);
    } finally {
      setIsSavingKey(false);
    }
  };

  return (
    <div className={`w-64 bg-[#f8f9fa] h-screen fixed left-0 top-0 border-r border-gray-200 overflow-y-auto hidden md:flex flex-col flex-shrink-0 z-40 transition-transform duration-300 pt-14 ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
      
      {/* Connectivity Mode */}
      <div className="p-4 border-b border-gray-200 relative">
        <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
          <svg className="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          CONNECTIVITY MODE
        </h3>
        <div className="flex items-center gap-2 mb-3 cursor-pointer" onClick={() => setIsLowBandwidth(!isLowBandwidth)}>
          <div className={`w-8 h-4 rounded-full relative transition-colors ${isLowBandwidth ? 'bg-amber-400' : 'bg-gray-300'}`}>
            <div className={`absolute top-0.5 w-3 h-3 bg-white rounded-full transition-all ${isLowBandwidth ? 'left-4.5' : 'left-0.5'}`} style={isLowBandwidth ? { left: '18px' } : {}}></div>
          </div>
          <span className="text-sm text-gray-800 font-semibold flex items-center gap-1">
            <Zap size={14} className="text-amber-400" />
            Low-Bandwidth Mode
          </span>
        </div>
        {isLowBandwidth ? (
          <div className="bg-[#FEF3C7] border border-[#F59E0B] rounded-lg p-3">
            <div className="text-xs text-[#92400E] font-medium flex items-start gap-1.5">
              <div className="w-2 h-2 rounded-full bg-[#92400E] mt-0.5 shrink-0"></div>
              ⚡ Low-Bandwidth Mode ON ✓ — Keyword matching active. Internet still required.
            </div>
          </div>
        ) : (
          <div className="bg-[#e6f4ea] border border-[#ceead6] rounded-lg p-3">
            <div className="text-xs text-[#137333] font-medium flex items-start gap-1.5">
              <div className="w-2 h-2 rounded-full bg-[#137333] mt-0.5 shrink-0"></div>
              Full Mode — AI semantic matching + translation active.
            </div>
          </div>
        )}
      </div>

      {/* Language */}
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
          <GlobeIcon /> LANGUAGE / भाषा
        </h3>
        <div className="space-y-2">
          {["en", "hi", "mr", "auto"].map((l) => (
            <label key={l} onClick={() => setLang(l)} className="flex items-center gap-2 cursor-pointer p-2 rounded-lg hover:bg-gray-100 transition-colors">
              <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${lang === l ? 'border-clinical-teal' : 'border-gray-300'}`}>
                {lang === l && <div className="w-2 h-2 bg-clinical-teal rounded-full"></div>}
              </div>
              <span className={`text-sm text-gray-800 ${lang === l ? 'font-bold' : 'font-medium'}`}>
                {l === "en" ? "English" : l === "hi" ? "हिंदी (Hindi)" : l === "mr" ? "मराठी (Marathi)" : "🌐 Auto-detect"}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* AI Engine */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles size={13} className="text-clinical-teal" /> AI ENGINE
          </h3>
          {geminiStatus?.has_key && (
            <button
              onClick={() => setIsEditingKey(!isEditingKey)}
              className="text-[11px] font-semibold text-clinical-teal hover:underline"
            >
              {isEditingKey ? "Hide" : "+ Add API"}
            </button>
          )}
        </div>

        {saveMessage && (
          <div className={`mb-2.5 p-2 rounded text-xs font-semibold flex items-center gap-1.5 ${saveMessage.type === "success" ? "bg-emerald-50 text-emerald-800 border border-emerald-200" : "bg-red-50 text-red-800 border border-red-200"}`}>
            {saveMessage.type === "success" ? <Check size={13} className="shrink-0" /> : <AlertCircle size={13} className="shrink-0" />}
            <span>{saveMessage.text}</span>
          </div>
        )}

        {geminiStatus?.has_key ? (
          <div className="bg-[#e6f4ea] border border-[#ceead6] rounded-lg p-2.5 flex items-center gap-2 text-xs font-bold text-[#137333]">
            <span>✨</span>
            <span>Gemini 2.5 Flash Active</span>
          </div>
        ) : (
          <div className="bg-gray-100 border border-gray-200 rounded-lg p-2.5 flex items-center gap-2 text-xs font-semibold text-gray-600">
            <span>⚪</span>
            <span>Gemini Inactive (Add Key below)</span>
          </div>
        )}
      </div>

      {/* ADD API Box — automatically hides once saved */}
      {(!geminiStatus?.has_key || isEditingKey) && (
        <div className="p-4 border-b border-gray-200 bg-white">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
              <Key size={13} className="text-clinical-teal" /> ADD API
            </h3>
            {geminiStatus?.has_key && (
              <button
                onClick={() => setIsEditingKey(false)}
                className="text-[10px] text-gray-400 hover:text-gray-700"
              >
                Close ✕
              </button>
            )}
          </div>

          <div className="border border-gray-200 rounded-lg p-3 shadow-xs space-y-2.5 bg-[#fcfdfd]">
            <input
              type="password"
              value={apiKeyInput}
              onChange={(e) => setApiKeyInput(e.target.value)}
              placeholder="Enter Gemini API Key..."
              className="w-full text-xs px-2.5 py-1.5 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-clinical-teal bg-white text-gray-800 placeholder-gray-400 font-mono"
            />

            <button
              onClick={handleSaveKey}
              disabled={isSavingKey || !apiKeyInput.trim()}
              className="w-full text-xs font-bold py-1.5 px-3 bg-clinical-teal text-white rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1.5 shadow-xs"
            >
              {isSavingKey ? "Saving..." : "Save API Key ✓"}
            </button>

            <a
              href="https://aistudio.google.com/app/apikey"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[10px] text-teal-700 hover:underline flex items-center justify-center gap-1 pt-0.5 font-medium"
            >
              Get Free Key (Google AI Studio) ↗
            </a>
          </div>
        </div>
      )}

      {/* Helplines */}
      <div className="p-4">
        <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-1.5">
          <Phone size={12} /> 24x7 EMERGENCY HELPLINES
        </h3>
        <div className="space-y-2">
          <Helpline label="🚑 Ambulance (MEMS)" number="108" color="bg-red-50 text-red-700 border-red-100" />
          <Helpline label="🤱 Janani Express" number="102" color="bg-pink-50 text-pink-700 border-pink-100" />
          <Helpline label="🏥 MH Health Line" number="104" color="bg-teal-50 text-teal-700 border-teal-100" />
          <Helpline label="👶 Child Helpline" number="1098" color="bg-orange-50 text-orange-700 border-orange-100" />
          <Helpline label="👩 Women Helpline" number="181" color="bg-blue-50 text-blue-700 border-blue-100" />
        </div>
      </div>
      
      <div className="mt-auto p-4 text-[10px] text-gray-400 italic">
        † General awareness only — not a diagnosis.
      </div>
    </div>
  );
}

function GlobeIcon() {
  return <svg className="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>;
}

function Helpline({ label, number, color }: { label: string, number: string, color: string }) {
  return (
    <a href={`tel:${number}`} className={`flex justify-between items-center p-2.5 rounded-lg border ${color} hover:opacity-80 transition-opacity cursor-pointer block`}>
      <span className="text-xs font-bold">{label}</span>
      <span className="text-xs font-bold px-1.5 py-0.5 bg-white/50 rounded">{number}</span>
    </a>
  );
}
