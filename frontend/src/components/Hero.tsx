import { Activity } from "lucide-react";

export function Hero({ lang }: { lang: string }) {
  const t = {
    en: { title: "AI Rural Health Assistant", sub: "Instant clinical triage, scheme info & hospital locator" },
    hi: { title: "AI ग्रामीण स्वास्थ्य सहायक", sub: "तत्काल नैदानिक सलाह, योजना की जानकारी और अस्पताल" },
    mr: { title: "AI ग्रामीण आरोग्य सहाय्यक", sub: "त्वरित क्लिनिकल सल्ला, योजना माहिती आणि रुग्णालय" }
  }[lang as "en"|"hi"|"mr"] || { title: "AI Rural Health Assistant", sub: "Instant clinical triage & scheme info" };

  return (
    <div className="bg-clinical-slate text-white py-6 px-4">
      <div className="max-w-4xl mx-auto flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-1.5 bg-white/10 px-3 py-1 rounded-full text-xs font-medium text-clinical-teal mb-4 backdrop-blur-sm border border-white/10">
          <Activity size={14} />
          <span>Smart India Hackathon 2024</span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-bold mb-2 tracking-tight">
          {t.title}
        </h2>
        <p className="text-gray-300 text-sm sm:text-base max-w-lg">
          {t.sub}
        </p>
      </div>
    </div>
  );
}
