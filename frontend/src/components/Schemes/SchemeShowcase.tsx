"use client";
import { useEffect, useState } from "react";
import { ShieldCheck, Info, FileText } from "lucide-react";
import { fetchSchemes } from "@/lib/api";
import { Scheme } from "@/lib/types";

export function SchemeShowcase() {
  const [schemes, setSchemes] = useState<Scheme[]>([]);
  
  useEffect(() => {
    fetchSchemes().then(res => setSchemes(res.schemes)).catch(console.error);
  }, []);

  const schemeLinks: Record<string, string> = {
    "Mahatma Jyotirao Phule Jan Arogya Yojana (MJPJAY)": "https://www.jeevandayee.gov.in/",
    "Ayushman Bharat – PMJAY (Integrated with MJPJAY)": "https://abdm.gov.in/",
    "Balasaheb Thackeray Aapla Dawakhana": "https://arogya.maharashtra.gov.in/",
    "Navsanjivan Yojana (Tribal Focus)": "https://tribal.maharashtra.gov.in/",
    "Janani Suraksha Yojana (JSY)": "https://nhm.gov.in/",
    "Rashtriya Bal Swasthya Karyakram (RBSK)": "https://rbsk.gov.in/"
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between px-1">
        <div>
          <h3 className="text-xl font-bold text-clinical-slate flex items-center gap-2">
            <ShieldCheck className="text-clinical-teal" /> 
            Government Health Schemes & Coverage
          </h3>
          <p className="text-xs text-gray-500 mt-1">100% Cashless & subsidized healthcare entitlements across Maharashtra</p>
        </div>
        <span className="hidden sm:inline-block bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Verified Active
        </span>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        {schemes.map((scheme, i) => {
          const portalUrl = schemeLinks[scheme.name] || "https://arogya.maharashtra.gov.in/";
          return (
            <div key={i} className="bg-white rounded-2xl border border-gray-200/80 shadow-sm hover:shadow-md hover:border-clinical-teal/40 transition-all overflow-hidden flex flex-col group">
              
              {/* Card Header */}
              <div className="p-5 bg-gradient-to-r from-[#0B2528] to-[#163C40] text-white flex flex-col justify-between min-h-[105px]">
                <div className="flex items-start justify-between gap-3">
                  <h4 className="font-bold text-base leading-snug tracking-tight text-white group-hover:text-clinical-mint transition-colors">
                    {scheme.name}
                  </h4>
                  <span className="shrink-0 bg-emerald-400/20 text-emerald-300 border border-emerald-400/30 px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider">
                    {scheme.status || "LIVE"}
                  </span>
                </div>
              </div>
              
              {/* Card Body */}
              <div className="p-5 flex-1 flex flex-col gap-4">
                
                {/* Benefits Pill Box */}
                <div className="bg-[#E6FBF7] border border-[#00D2B4]/30 rounded-xl p-3.5">
                  <span className="text-[10px] font-extrabold text-[#0B2528] uppercase tracking-wider flex items-center gap-1.5 mb-1">
                    <ShieldCheck size={14} className="text-clinical-teal" /> Benefits & Coverage
                  </span>
                  <p className="text-xs font-semibold text-[#0B2528] leading-relaxed">
                    {scheme.benefits}
                  </p>
                </div>
                
                {/* Eligibility */}
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider flex items-center gap-1.5">
                    <Info size={13} className="text-amber-500" /> Eligibility Criteria
                  </span>
                  <p className="text-xs text-gray-600 leading-relaxed pl-1">
                    {scheme.eligibility}
                  </p>
                </div>
                
                {/* Documents & How to apply */}
                <div className="mt-auto pt-3 border-t border-gray-100 space-y-2.5">
                  <div className="flex items-start gap-2 text-xs text-gray-500">
                    <FileText size={14} className="shrink-0 mt-0.5 text-gray-400" />
                    <span><strong className="text-gray-700">Carry:</strong> {scheme.what_to_carry}</span>
                  </div>
                  
                  <div className="bg-gray-50 border border-gray-100 rounded-lg p-2.5 text-xs text-gray-600">
                    <strong className="text-gray-800">Apply: </strong> 
                    {scheme.apply_how}
                  </div>

                  <a 
                    href={portalUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full mt-2 py-2 px-3 bg-gray-50 hover:bg-clinical-teal hover:text-white border border-gray-200 rounded-xl text-xs font-bold text-center text-gray-700 transition-all flex items-center justify-center gap-1.5 shadow-sm"
                  >
                    <span>Official Scheme Portal</span>
                    <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
