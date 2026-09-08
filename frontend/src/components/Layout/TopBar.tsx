"use client";

export function TopBar({ onToggleSidebar }: { onToggleSidebar: () => void }) {
  return (
    <div className="w-full flex items-center justify-between px-6 py-4">
      {/* Left side tags */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 bg-white border border-gray-200 rounded-full px-3 py-1.5 shadow-sm">
          <div className="w-5 h-5 bg-clinical-teal rounded-full flex items-center justify-center">
            <svg className="w-3 h-3 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          </div>
          <span className="font-bold text-sm text-[#0B2528]">MahaArogya Setu</span>
        </div>
      </div>

      {/* Right side tags */}
      <div className="hidden lg:flex items-center gap-4 text-xs font-bold text-gray-500">
        <div className="flex items-center gap-1 text-[#137333]">
          <div className="w-2 h-2 rounded-full bg-[#137333]"></div>
          Rural Healthcare Portal
        </div>
        <span>MJPJAY • PM-JAY</span>
        <span>5 Tribal Districts</span>
        
        <a href="tel:108" className="bg-[#0B2528] text-white px-4 py-2 rounded-full flex items-center gap-2 font-bold ml-2 hover:bg-[#163c40] transition-colors">
          <svg className="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Call 108 Emergency
        </a>
      </div>
    </div>
  );
}
