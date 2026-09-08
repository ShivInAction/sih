"use client";
import { useEffect, useState } from "react";
import { Baby, Syringe } from "lucide-react";
import { fetchSchedules } from "@/lib/api";
import { ANCVB, Immunization } from "@/lib/types";

export function MaternalChildModule() {
  const [anc, setAnc] = useState<ANCVB[]>([]);
  const [imm, setImm] = useState<Immunization[]>([]);
  
  useEffect(() => {
    fetchSchedules().then(res => {
      setAnc(res.anc_schedule);
      setImm(res.immunization_schedule);
    }).catch(console.error);
  }, []);

  return (
    <div className="space-y-8">
      {/* ANC Section */}
      <div>
        <h3 className="text-xl font-bold text-clinical-slate flex items-center gap-2 px-2 mb-4">
          <Baby className="text-pink-500" /> 
          Pregnancy Care (ANC) Schedule
        </h3>
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-1 sm:p-4">
          <div className="relative border-l-2 border-pink-100 ml-4 sm:ml-6 space-y-6 py-4">
            {anc.map((visit, i) => (
              <div key={i} className="relative pl-6 sm:pl-8">
                <div className="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-pink-500 border-4 border-white shadow-sm"></div>
                <div className="bg-pink-50/50 rounded-xl p-4 border border-pink-100/50">
                  <h4 className="font-bold text-clinical-slate">{visit.visit}</h4>
                  <div className="text-sm font-semibold text-pink-600 mb-2">{visit.timing}</div>
                  <p className="text-sm text-gray-600 leading-relaxed">{visit.importance}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Immunization Section */}
      <div>
        <h3 className="text-xl font-bold text-clinical-slate flex items-center gap-2 px-2 mb-4">
          <Syringe className="text-blue-500" /> 
          Child Immunization (UIP)
        </h3>
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="bg-gray-50/80 text-gray-600 text-xs uppercase font-bold tracking-wider">
                <tr>
                  <th className="px-4 py-3 sm:px-6 sm:py-4">Age</th>
                  <th className="px-4 py-3 sm:px-6 sm:py-4">Vaccines Given</th>
                  <th className="px-4 py-3 sm:px-6 sm:py-4">Protects Against</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {imm.map((item, i) => (
                  <tr key={i} className="hover:bg-blue-50/30 transition-colors">
                    <td className="px-4 py-3 sm:px-6 sm:py-4 font-semibold text-clinical-slate whitespace-nowrap">{item.age}</td>
                    <td className="px-4 py-3 sm:px-6 sm:py-4 text-gray-700">{item.vaccines}</td>
                    <td className="px-4 py-3 sm:px-6 sm:py-4 text-gray-500 text-xs sm:text-sm">{item.protects}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
