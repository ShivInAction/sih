"use client";
import { useState, useEffect } from "react";
import { Search, MapPin, Phone, Hospital } from "lucide-react";
import { fetchDistricts, fetchFacilities } from "@/lib/api";
import { Facility } from "@/lib/types";

export function FacilityLocator() {
  const [districts, setDistricts] = useState<{name: string, count: number}[]>([]);
  const [selectedDistrict, setSelectedDistrict] = useState("");
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchDistricts().then(res => {
      setDistricts(res.districts.map((d: {name: string, facility_count: number}) => ({ name: d.name, count: d.facility_count })));
    }).catch(console.error);
  }, []);

  useEffect(() => {
    if (!selectedDistrict) {
      setFacilities([]);
      return;
    }
    setIsLoading(true);
    fetchFacilities(selectedDistrict)
      .then(res => setFacilities(res.facilities))
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, [selectedDistrict]);

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="p-4 sm:p-6 border-b border-gray-100 bg-gray-50/50">
        <h3 className="text-lg font-bold text-clinical-slate flex items-center gap-2 mb-4">
          <MapPin className="text-clinical-teal" />
          Locate Health Facilities
        </h3>
        
        <div className="relative">
          <select 
            value={selectedDistrict}
            onChange={e => setSelectedDistrict(e.target.value)}
            className="w-full pl-10 pr-10 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-clinical-teal bg-white text-gray-900 font-semibold cursor-pointer shadow-sm hover:border-clinical-teal/50 transition-colors"
          >
            <option value="" className="text-gray-500 font-normal">Select your district...</option>
            {districts.map(d => (
              <option key={d.name} value={d.name} className="text-gray-900 font-medium py-1.5 bg-white">
                {d.name} ({d.count})
              </option>
            ))}
          </select>
          <Search className="absolute left-3.5 top-3.5 text-gray-500" size={18} />
          <div className="absolute right-3.5 top-4 pointer-events-none text-gray-400">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m6 9 6 6 6-6"/></svg>
          </div>
        </div>
      </div>

      <div className="p-4 sm:p-6 min-h-[300px]">
        {isLoading ? (
          <div className="flex justify-center items-center h-40">
             <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-clinical-teal"></div>
          </div>
        ) : facilities.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {facilities.map((fac, i) => (
              <div key={i} className="border border-gray-100 rounded-xl p-4 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-bold text-clinical-slate flex items-start gap-2">
                    <Hospital className="text-clinical-teal shrink-0 mt-0.5" size={18} />
                    {fac.name}
                  </h4>
                  {fac.is_hq && <span className="text-[10px] bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">HQ</span>}
                </div>
                
                <p className="text-xs text-gray-500 mb-3">{fac.type} • {fac.location}</p>
                
                <div className="flex flex-wrap gap-1 mb-4">
                  {fac.services_list.slice(0,3).map((s, idx) => (
                    <span key={idx} className="bg-clinical-mint text-clinical-tealDark text-[10px] px-2 py-1 rounded-full font-medium">
                      {s}
                    </span>
                  ))}
                  {fac.services_list.length > 3 && <span className="text-[10px] text-gray-400 self-center">+{fac.services_list.length - 3}</span>}
                </div>
                
                <div className="flex items-center justify-between mt-auto pt-3 border-t border-gray-50">
                    <div className="text-xs text-gray-500">
                      <span className="font-semibold text-gray-700">{fac.beds}</span> Beds
                    </div>
                    <div className="flex items-center gap-2">
                      <a 
                        href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(fac.name + ' ' + fac.location + ' ' + selectedDistrict)}`} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="flex items-center gap-1 text-xs font-bold text-gray-700 bg-gray-100 px-3 py-1.5 rounded-lg hover:bg-gray-200 transition-colors"
                      >
                        <MapPin size={13} /> Maps
                      </a>
                      <a href={`tel:${fac.phone}`} className="flex items-center gap-1 text-xs font-bold text-clinical-teal bg-clinical-mint px-3 py-1.5 rounded-lg hover:bg-clinical-teal hover:text-white transition-colors">
                        <Phone size={14} /> Call
                      </a>
                    </div>
                 </div>
              </div>
            ))}
          </div>
        ) : selectedDistrict ? (
          <p className="text-center text-gray-500 mt-10">No facilities found for this district.</p>
        ) : (
          <div className="flex flex-col items-center justify-center h-48 text-gray-400 space-y-3">
             <MapPin size={48} className="opacity-20" />
             <p>Select a district to view hospitals</p>
          </div>
        )}
      </div>
    </div>
  );
}
