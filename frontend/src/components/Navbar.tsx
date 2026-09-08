"use client";
import { useState } from "react";
import { Globe, Shield, PhoneCall } from "lucide-react";

export function Navbar({ currentLang, setLang }: { currentLang: string, setLang: (l: string) => void }) {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          
          <div className="flex items-center gap-2">
            <Shield className="h-8 w-8 text-clinical-teal" />
            <div>
              <h1 className="font-bold text-xl text-clinical-slate leading-tight tracking-tight">
                MahaArogya <span className="text-clinical-teal">Setu</span>
              </h1>
              <p className="text-[0.65rem] text-gray-500 font-semibold uppercase tracking-wider">
                Govt. of Maharashtra
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <a href="tel:108" className="hidden sm:flex items-center gap-1.5 bg-clinical-dangerBg text-clinical-danger px-3 py-1.5 rounded-full font-bold text-sm border border-red-200">
              <PhoneCall size={16} />
              108 Emergency
            </a>
            
            <div className="relative">
              <button 
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-50 border border-gray-200 rounded-lg text-sm font-medium hover:bg-gray-100 transition-colors"
              >
                <Globe size={16} className="text-gray-500" />
                {currentLang === "en" ? "English" : currentLang === "hi" ? "हिंदी" : "मराठी"}
              </button>
              
              {isOpen && (
                <div className="absolute right-0 mt-2 w-36 bg-white border border-gray-100 rounded-lg shadow-lg py-1 z-50">
                  <button onClick={() => { setLang("en"); setIsOpen(false); }} className={`w-full text-left px-4 py-2 text-sm ${currentLang === 'en' ? 'bg-clinical-mint text-clinical-teal font-semibold' : 'hover:bg-gray-50'}`}>English</button>
                  <button onClick={() => { setLang("hi"); setIsOpen(false); }} className={`w-full text-left px-4 py-2 text-sm ${currentLang === 'hi' ? 'bg-clinical-mint text-clinical-teal font-semibold' : 'hover:bg-gray-50'}`}>हिंदी (Hindi)</button>
                  <button onClick={() => { setLang("mr"); setIsOpen(false); }} className={`w-full text-left px-4 py-2 text-sm ${currentLang === 'mr' ? 'bg-clinical-mint text-clinical-teal font-semibold' : 'hover:bg-gray-50'}`}>मराठी (Marathi)</button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
