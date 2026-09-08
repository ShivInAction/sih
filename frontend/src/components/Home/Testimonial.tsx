"use client";

export function Testimonial() {
  return (
    <div className="bg-gradient-to-br from-white to-clinical-mint border border-gray-100 rounded-3xl p-8 shadow-sm flex flex-col md:flex-row gap-8 items-center md:items-start relative overflow-hidden">
      <div className="flex-1 relative z-10 pl-8 pt-4">
        <p className="text-lg font-medium text-[#0B2528] italic leading-relaxed mb-6">
          &quot;MahaArogya Setu has transformed how we guide families in our block. When a mother or child falls sick, we can instantly check emergency danger signs, understand which hospital has pediatric beds, and know exactly how to claim cashless MJPJAY benefits without confusion.&quot;
        </p>
        
        <div>
          <h4 className="font-bold text-[#0B2528]">Sunita Gavit</h4>
          <p className="text-xs text-gray-500">ASHA Healthcare Facilitator • Dhadgaon Tribal Block, Nandurbar</p>
          <div className="flex text-amber-400 mt-2 text-sm">
            ★★★★★
          </div>
        </div>
      </div>
      
      <div className="shrink-0 relative">
        <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-clinical-teal to-[#0B2528] flex items-center justify-center text-4xl shadow-lg relative z-10">
          👩‍⚕️
        </div>
        <div className="absolute inset-0 bg-clinical-teal blur-2xl opacity-40"></div>
      </div>
    </div>
  );
}
