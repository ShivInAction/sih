"use client";
import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";
import { ChatBubble } from "./ChatBubble";
import { ClinicalLoader } from "./ClinicalLoader";
import { ChatMessage } from "@/lib/types";
import { fetchTriage } from "@/lib/api";

export function ChatContainer({ lang, isLowBandwidth, isSidebarOpen = true }: { lang: string, isLowBandwidth: boolean, isSidebarOpen?: boolean }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [interimTranscript, setInterimTranscript] = useState("");
  const endRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);

  // Auto-scroll to bottom only when conversation starts
  useEffect(() => {
    if (messages.length > 0 || isLoading) {
      endRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isLoading]);

  // Clean up recognition on unmount
  useEffect(() => {
    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch (e) {}
      }
    };
  }, []);

  const t = {
    en: { placeholder: "Type your symptoms or ask about hospitals, schemes, ABHA..." },
    hi: { placeholder: "अपने लक्षण या स्वास्थ्य प्रश्न बताएं..." },
    mr: { placeholder: "तुमची लक्षणे किंवा आरोग्य प्रश्न सांगा..." }
  }[lang as "en"|"hi"|"mr"] || { placeholder: "Type your symptoms..." };

  const stopListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (e) {}
      recognitionRef.current = null;
    }
    setIsListening(false);
    setInterimTranscript("");
  };

  const toggleListening = () => {
    // @ts-ignore
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Voice recognition is not supported in this browser.");
      return;
    }

    if (isListening) {
      stopListening();
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = lang === 'hi' ? 'hi-IN' : lang === 'mr' ? 'mr-IN' : 'en-US';
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onstart = () => {
        setIsListening(true);
        setInterimTranscript("");
      };
      
      recognition.onresult = (event: any) => {
        let finalTrans = "";
        let interim = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTrans += event.results[i][0].transcript;
          } else {
            interim += event.results[i][0].transcript;
          }
        }
        if (finalTrans) {
          setInput((prev) => prev + (prev ? " " : "") + finalTrans);
        }
        setInterimTranscript(interim);
      };

      recognition.onerror = () => {
        stopListening();
      };
      recognition.onend = () => {
        setIsListening(false);
        setInterimTranscript("");
        recognitionRef.current = null;
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (e) {
      console.error("Speech recognition start failed:", e);
      stopListening();
    }
  };

  const handleSend = async (e?: React.FormEvent, overrideInput?: string) => {
    e?.preventDefault();
    
    // Automatically stop voice recording when sending
    stopListening();

    const finalInput = overrideInput || input;
    if (!finalInput.trim() || isLoading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: finalInput,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const data = await fetchTriage(userMsg.content, lang, isLowBandwidth);
      const aiMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.html,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `<div class="th-alert caution"><h4>System Error</h4><p>Unable to process your request at this time.</p></div>`,
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const emptyStateT = {
    en: {
      title: "How can we help you today?",
      desc: "Describe your symptoms in EN/HI/MR or ask about hospitals, schemes, or services.",
      quick: "💡 POPULAR QUICK ACTIONS",
      q1: "I have symptoms",
      q2: "Find Government Hospital",
      q3: "Emergency",
      q4: "Pregnancy / Child Care",
      q5: "Government Schemes",
      q6: "Generic Medicines"
    },
    hi: {
      title: "आज हम आपकी कैसे मदद कर सकते हैं?",
      desc: "EN/HI/MR में अपने लक्षणों का वर्णन करें या अस्पतालों, योजनाओं या सेवाओं के बारे में पूछें।",
      quick: "💡 लोकप्रिय त्वरित कार्रवाइयां",
      q1: "मुझे लक्षण हैं",
      q2: "सरकारी अस्पताल खोजें",
      q3: "आपातकाल",
      q4: "गर्भावस्था / शिशु देखभाल",
      q5: "सरकारी योजनाएं",
      q6: "जेनेरिक दवाएं"
    },
    mr: {
      title: "आज आम्ही तुमची कशी मदत करू शकतो?",
      desc: "EN/HI/MR मध्ये तुमची लक्षणे सांगा किंवा रुग्णालये, योजना किंवा सेवांबद्दल विचारा.",
      quick: "💡 लोकप्रिय त्वरित कृती",
      q1: "मला लक्षणे आहेत",
      q2: "सरकारी रुग्णालय शोधा",
      q3: "आणीबाणी",
      q4: "गर्भधारणा / बालसंगोपन",
      q5: "सरकारी योजना",
      q6: "जेनेरिक औषधे"
    }
  };
  const et = emptyStateT[lang as keyof typeof emptyStateT] || emptyStateT.en;

  return (
    <div className="flex flex-col relative w-full mb-12">
      {/* Messages Area */}
      <div className="flex-1 w-full pb-24">
        {messages.length === 0 && (
          <div className="bg-white border border-gray-100 rounded-3xl p-8 text-center">
            <div className="w-12 h-12 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-6 h-6 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z"/></svg>
            </div>
            <h2 className="text-2xl font-bold text-[#0B2528] mb-3">{et.title}</h2>
            <p className="text-gray-500 mb-10">{et.desc}</p>
            
            <div className="text-left max-w-3xl mx-auto">
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                {et.quick}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <QuickAction icon="🩺" label={et.q1} onClick={() => handleSend(undefined, et.q1)} />
                <QuickAction icon="🏥" label={et.q2} onClick={() => handleSend(undefined, et.q2)} />
                <QuickAction icon="🚨" label={et.q3} onClick={() => handleSend(undefined, et.q3)} />
                <QuickAction icon="🤱" label={et.q4} onClick={() => handleSend(undefined, et.q4)} />
                <QuickAction icon="🏛️" label={et.q5} onClick={() => handleSend(undefined, et.q5)} />
                <QuickAction icon="💊" label={et.q6} onClick={() => handleSend(undefined, et.q6)} />
              </div>
            </div>
          </div>
        )}
        
        <div className="space-y-4 px-2">
          {messages.map(msg => <ChatBubble key={msg.id} message={msg} />)}
          {isLoading && <ClinicalLoader lang={lang} />}
          <div ref={endRef} />
        </div>
      </div>

      {/* Floating Input Area */}
      <div className={`fixed bottom-0 right-0 p-4 bg-white/90 backdrop-blur-sm border-t border-gray-100 z-50 transition-all duration-300 ${isSidebarOpen ? 'left-0 md:left-64' : 'left-0'}`}>
        <form onSubmit={handleSend} className="max-w-4xl mx-auto relative flex items-center">
          <input 
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t.placeholder}
            className="w-full pl-6 pr-24 py-4 rounded-full border border-gray-200 shadow-lg text-sm text-gray-900 font-medium focus:outline-none focus:ring-2 focus:ring-clinical-teal bg-white"
          />
          <div className="absolute right-2 flex items-center gap-1">
            <div className="relative">
              {isListening && interimTranscript && (
                <div className="absolute bottom-full mb-3 right-0 bg-white shadow-xl border border-gray-100 rounded-2xl px-4 py-2 text-sm text-gray-700 whitespace-nowrap z-50 animate-in fade-in slide-in-from-bottom-2">
                  <span className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
                    {interimTranscript}
                  </span>
                  {/* Speech bubble tail */}
                  <div className="absolute -bottom-2 right-4 w-4 h-4 bg-white border-b border-r border-gray-100 transform rotate-45"></div>
                </div>
              )}
              <button 
                type="button"
                onClick={toggleListening}
                className={`p-2.5 rounded-full transition-all flex items-center justify-center ${isListening ? 'bg-red-500 hover:bg-red-600 shadow-lg shadow-red-500/30' : 'bg-transparent text-gray-400 hover:text-gray-600 hover:bg-gray-100'}`}
              >
                {isListening ? (
                  <div className="w-4 h-4 bg-white rounded-sm"></div>
                ) : (
                  <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
                )}
              </button>
            </div>
            <button 
              type="submit"
              disabled={!input.trim() || isLoading}
              className="p-2 bg-clinical-teal text-white hover:bg-clinical-tealDark rounded-full disabled:opacity-50 ml-1"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function QuickAction({ icon, label, onClick }: { icon: string, label: string, onClick: () => void }) {
  return (
    <button onClick={onClick} className="flex items-center gap-3 p-4 border border-gray-200 rounded-xl hover:border-clinical-teal hover:bg-clinical-mint transition-colors text-left font-bold text-[#0B2528] w-full">
      <span className="text-xl">{icon}</span>
      {label}
    </button>
  );
}
