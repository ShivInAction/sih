export function ClinicalLoader({ lang }: { lang: string }) {
  const t = {
    en: "Analyzing symptoms securely...",
    hi: "लक्षणों का सुरक्षित विश्लेषण कर रहे हैं...",
    mr: "लक्षणे सुरक्षितपणे तपासत आहे..."
  }[lang as "en"|"hi"|"mr"] || "Analyzing symptoms...";

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 my-4 max-w-sm ml-2">
      <div className="flex items-center gap-3 mb-3">
        <div className="relative w-8 h-8 rounded-full bg-clinical-mint flex items-center justify-center">
          <div className="absolute inset-0 border-2 border-clinical-teal border-t-transparent rounded-full animate-spin"></div>
        </div>
        <p className="text-sm font-semibold text-clinical-slate">{t}</p>
      </div>
      
      {/* ECG Line visual */}
      <div className="h-12 bg-gray-50 rounded-lg overflow-hidden flex items-center px-2 relative">
        <div className="absolute inset-y-0 left-0 w-1/3 bg-gradient-to-r from-gray-50 to-transparent z-10"></div>
        <div className="absolute inset-y-0 right-0 w-1/3 bg-gradient-to-l from-gray-50 to-transparent z-10"></div>
        <div className="w-[200%] h-full flex items-center justify-center animate-[translateX_2s_linear_infinite]" style={{ animation: "slideLeft 2s linear infinite" }}>
          <svg className="h-6 w-full text-clinical-teal" preserveAspectRatio="none" viewBox="0 0 100 24" fill="none" stroke="currentColor" strokeWidth="1.5">
             <path d="M0,12 L20,12 L25,4 L35,20 L40,12 L100,12" vectorEffect="non-scaling-stroke" />
             <path d="M100,12 L120,12 L125,4 L135,20 L140,12 L200,12" vectorEffect="non-scaling-stroke" />
          </svg>
        </div>
      </div>
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes slideLeft {
          from { transform: translateX(0); }
          to { transform: translateX(-50%); }
        }
      `}} />
    </div>
  );
}
