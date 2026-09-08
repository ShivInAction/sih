"use client";
import { useEffect, useState } from "react";
import { Pill, Tag, TrendingDown } from "lucide-react";
import { fetchMedicines } from "@/lib/api";
import { Medicine } from "@/lib/types";

export function MedicineGrid({ lang }: { lang: string }) {
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  
  useEffect(() => {
    fetchMedicines().then(res => setMedicines(res.medicines)).catch(console.error);
  }, []);

  const titles = {
    en: "Generic Medicine Savings",
    hi: "जेनेरिक दवा बचत",
    mr: "जेनेरिक औषध बचत"
  };
  const title = titles[lang as keyof typeof titles] || titles.en;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between px-2 mb-4">
        <h3 className="text-xl font-bold text-clinical-slate flex items-center gap-2">
          <Pill className="text-clinical-teal" /> 
          {title}
        </h3>
        <span className="hidden sm:inline-block bg-amber-100 text-amber-800 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Jan Aushadhi
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {medicines.map((med, i) => (
          <div key={i} className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 relative overflow-hidden group hover:border-clinical-teal/30 transition-colors">
            
            {/* Saving Ribbon */}
            <div className="absolute top-0 right-0 bg-clinical-teal text-white text-[10px] font-bold px-3 py-1 rounded-bl-lg flex items-center gap-1 shadow-sm">
              <TrendingDown size={12} /> {med.saving_percent} Off
            </div>
            
            <h4 className="font-bold text-clinical-slate pr-16 mb-1">{med.name}</h4>
            <p className="text-xs text-gray-500 mb-4">{med.use}</p>
            
            <div className="flex items-end justify-between mt-auto">
              <div>
                <span className="block text-[10px] text-gray-400 font-medium uppercase mb-0.5">Jan Aushadhi</span>
                <span className="text-lg font-bold text-clinical-teal leading-none">{med.generic_price}</span>
              </div>
              <div className="text-right">
                <span className="block text-[10px] text-gray-400 font-medium uppercase mb-0.5">Branded</span>
                <span className="text-sm font-semibold text-gray-400 line-through leading-none">{med.branded_price}</span>
              </div>
            </div>
          </div>
        ))}
        
        {/* See More Box */}
        <a 
          href="http://janaushadhi.gov.in/" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="bg-amber-50/50 rounded-xl border-2 border-dashed border-amber-200 shadow-sm p-4 flex flex-col items-center justify-center text-center group hover:bg-amber-100/50 hover:border-amber-400 transition-all cursor-pointer min-h-[140px]"
        >
          <div className="w-10 h-10 bg-amber-100 rounded-full flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
            <svg className="w-5 h-5 text-amber-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </div>
          <h4 className="font-bold text-amber-900 mb-1">See More</h4>
          <p className="text-xs text-amber-700/80 font-medium">Explore all Jan Aushadhi medicines</p>
        </a>
      </div>
      
      <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-4 flex items-start gap-3 mt-4">
        <Tag className="text-blue-500 shrink-0 mt-0.5" size={18} />
        <p className="text-sm text-gray-600">
          Generic medicines have the exact same active ingredients and effectiveness as branded medicines. Always ask your doctor or pharmacist for the generic equivalent to save money.
        </p>
      </div>
    </div>
  );
}
