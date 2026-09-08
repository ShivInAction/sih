"use client";
import { useState } from "react";
import { ChatContainer } from "@/components/Chat/ChatContainer";
import { FacilityLocator } from "@/components/Facilities/FacilityLocator";
import { SchemeShowcase } from "@/components/Schemes/SchemeShowcase";
import { MaternalChildModule } from "@/components/MaternalChild/MaternalChildModule";

export function MainTabs({ lang, isLowBandwidth, isSidebarOpen }: { lang: string, isLowBandwidth: boolean, isSidebarOpen: boolean }) {
  const [activeTab, setActiveTab] = useState("consult");

  const translations = {
    en: {
      t1: "TRIBAL DISTRICTS",
      t2: "CONDITIONS TRIAGED",
      t3: "CASHLESS SCHEMES",
      t4: "FREE EMERGENCY LINKAGE",
      hint: "Voice input available — click the mic icon inside the text box to speak your symptoms in EN / HI / MR",
      tab1: "Consult AI",
      tab2: "Facility Locator",
      tab3: "Schemes",
      tab4: "Maternal & Child",
      tab5: "More Services"
    },
    hi: {
      t1: "आदिवासी जिले",
      t2: "स्थितियों का परीक्षण",
      t3: "कैशलेस योजनाएं",
      t4: "मुफ्त आपातकालीन जुड़ाव",
      hint: "वॉयस इनपुट उपलब्ध है - EN / HI / MR में अपने लक्षण बोलने के लिए टेक्स्ट बॉक्स के अंदर माइक आइकन पर क्लिक करें",
      tab1: "AI से परामर्श लें",
      tab2: "सुविधा लोकेटर",
      tab3: "योजनाएं",
      tab4: "मातृ एवं शिशु",
      tab5: "अधिक सेवाएँ"
    },
    mr: {
      t1: "आदिवासी जिल्हे",
      t2: "आजारांचे निदान",
      t3: "कॅशलेस योजना",
      t4: "मोफत आपत्कालीन मदत",
      hint: "व्हॉइस इनपुट उपलब्ध - EN / HI / MR मध्ये तुमची लक्षणे बोलण्यासाठी मजकूर बॉक्समधील माइक चिन्हावर क्लिक करा",
      tab1: "AI सल्ला घ्या",
      tab2: "रुग्णालय शोध",
      tab3: "योजना",
      tab4: "माता आणि बाळ",
      tab5: "अधिक सेवा"
    }
  };
  const t = translations[lang as keyof typeof translations] || translations.en;

  return (
    <div className="space-y-6" id="main-tabs-section">
      {/* Dark Stats Ribbon */}
      <div className="bg-[#0B2528] rounded-3xl p-6 text-white grid grid-cols-2 md:grid-cols-4 gap-6 divide-x divide-white/10 text-center">
        <div>
          <div className="text-3xl font-extrabold text-clinical-teal mb-1">5+</div>
          <div className="text-[10px] font-bold uppercase tracking-widest text-gray-400">{t.t1}</div>
        </div>
        <div>
          <div className="text-3xl font-extrabold text-clinical-teal mb-1">40+</div>
          <div className="text-[10px] font-bold uppercase tracking-widest text-gray-400">{t.t2}</div>
        </div>
        <div>
          <div className="text-3xl font-extrabold text-clinical-teal mb-1">6</div>
          <div className="text-[10px] font-bold uppercase tracking-widest text-gray-400">{t.t3}</div>
        </div>
        <div>
          <div className="text-3xl font-extrabold text-clinical-teal mb-1">24x7</div>
          <div className="text-[10px] font-bold uppercase tracking-widest text-gray-400">{t.t4}</div>
        </div>
      </div>

      <p className="text-center text-xs text-gray-500 flex items-center justify-center gap-2">
        <svg className="w-4 h-4 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
        {t.hint}
      </p>

      {/* Tabs */}
      <div className="flex justify-center border-b border-gray-100">
        <div className="flex gap-2 p-1 bg-white overflow-x-auto no-scrollbar max-w-full">
          <TabButton active={activeTab === "consult"} onClick={() => setActiveTab("consult")} icon={<div className="w-3 h-3 rounded-full bg-clinical-teal"></div>} label={t.tab1} />
          <TabButton active={activeTab === "facilities"} onClick={() => setActiveTab("facilities")} icon="🏥" label={t.tab2} />
          <TabButton active={activeTab === "schemes"} onClick={() => setActiveTab("schemes")} icon="📋" label={t.tab3} />
          <TabButton active={activeTab === "maternal"} onClick={() => setActiveTab("maternal")} icon="🤱" label={t.tab4} />
          <TabButton active={activeTab === "more"} onClick={() => setActiveTab("more")} icon="🔴" label={t.tab5} />
        </div>
      </div>

      {/* Content */}
      <div className="pt-4">
        {activeTab === "consult" && <ChatContainer lang={lang} isLowBandwidth={isLowBandwidth} isSidebarOpen={isSidebarOpen} />}
        {activeTab === "facilities" && <FacilityLocator />}
        {activeTab === "schemes" && <SchemeShowcase />}
        {activeTab === "maternal" && <MaternalChildModule />}
        {activeTab === "more" && <div className="text-center p-12 text-gray-500">More services coming soon.</div>}
      </div>
    </div>
  );
}

function TabButton({ active, onClick, icon, label }: { active: boolean, onClick: () => void, icon: React.ReactNode, label: string }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-bold transition-all ${
        active 
          ? "bg-clinical-teal/10 text-clinical-teal shadow-[inset_0_0_0_1px_rgba(0,210,180,0.2)]" 
          : "bg-white text-gray-500 hover:bg-gray-50"
      }`}
    >
      {icon}
      {label}
    </button>
  );
}

function QuickAction({ icon, label }: { icon: string, label: string }) {
  return (
    <button className="flex items-center gap-3 p-4 border border-gray-200 rounded-xl hover:border-clinical-teal hover:bg-clinical-mint transition-colors text-left font-bold text-[#0B2528]">
      <span className="text-xl">{icon}</span>
      {label}
    </button>
  );
}
