"use client";
import { useState, useEffect } from "react";
import { Sidebar } from "@/components/Layout/Sidebar";
import { TopBar } from "@/components/Layout/TopBar";
import { HeroStats } from "@/components/Home/HeroStats";
import { FeatureGrid } from "@/components/Home/FeatureGrid";
import { MainTabs } from "@/components/Home/MainTabs";
import { MedicineGrid } from "@/components/Medicines/MedicineGrid";
import { ComprehensiveCapabilities } from "@/components/Home/ComprehensiveCapabilities";
import { CustomFooter } from "@/components/Layout/CustomFooter";

export default function Home() {
  const [lang, setLang] = useState("en");
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isLowBandwidth, setIsLowBandwidth] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined") {
      window.scrollTo(0, 0);
      if ("serviceWorker" in navigator) {
        navigator.serviceWorker.register("/sw.js").catch(console.error);
      }
    }
  }, []);

  return (
    <div className="flex w-full min-h-screen">
      {/* Fixed Hamburger Toggle */}
      <button 
        onClick={() => setIsSidebarOpen(!isSidebarOpen)} 
        className={`fixed top-3 left-4 z-50 p-2 text-gray-500 hover:text-[#0B2528] hover:bg-gray-200/50 rounded transition-colors ${isSidebarOpen ? 'bg-transparent' : 'bg-white shadow-sm border border-gray-100'}`}
      >
        <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>

      <Sidebar lang={lang} setLang={setLang} isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} isLowBandwidth={isLowBandwidth} setIsLowBandwidth={setIsLowBandwidth} />
      
      <main className={`flex-1 bg-white flex flex-col relative pb-32 transition-all duration-300 ${isSidebarOpen ? 'md:ml-64' : 'ml-0'}`}>
        <div className={`transition-all duration-300 ${!isSidebarOpen ? 'ml-12' : ''}`}>
          <TopBar onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
        </div>
        
        <div className="px-4 sm:px-8 max-w-5xl mx-auto w-full pt-6 space-y-10">
          <HeroStats lang={lang} />
          <FeatureGrid lang={lang} />
          
          <MainTabs lang={lang} isLowBandwidth={isLowBandwidth} isSidebarOpen={isSidebarOpen} />

          <MedicineGrid lang={lang} />

          <ComprehensiveCapabilities lang={lang} />

          <div className="pb-10">
            <CustomFooter lang={lang} />
          </div>
        </div>
      </main>
    </div>
  );
}
