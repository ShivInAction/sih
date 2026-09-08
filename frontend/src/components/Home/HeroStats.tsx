"use client";

export function HeroStats({ lang }: { lang: string }) {
  const translations = {
    en: {
      badge1: "100% FREE PUBLIC HEALTH SERVICE • SIH",
      badge2: "4.9 Citizen Rating (50,000+ Rural Families)",
      title1: "Enhance Rural Healthcare with",
      title2: "Guided AI Triage",
      desc: "Bridging the healthcare gap in Maharashtra's rural & tribal regions. Find hospitals, access government schemes (MJPJAY/PM-JAY), get maternal care, telemedicine consultations, and emergency support — all in your language.",
      btn1: "Start AI Consultation Below",
      btn2: "Call 108 Ambulance",
      btn3: "Health Advice: 104",
      asha: "500+ ASHA workers & medical centers linked across Nandurbar, Gadchiroli, Melghat, Palghar & Yavatmal"
    },
    hi: {
      badge1: "100% मुफ़्त सार्वजनिक स्वास्थ्य सेवा • SIH",
      badge2: "4.9 नागरिक रेटिंग (50,000+ ग्रामीण परिवार)",
      title1: "AI ट्राइएज से सशक्त बनाएं",
      title2: "ग्रामीण स्वास्थ्य सेवा",
      desc: "महाराष्ट्र के ग्रामीण और आदिवासी क्षेत्रों में स्वास्थ्य सेवा की खाई को पाटना। अस्पताल खोजें, सरकारी योजनाओं (MJPJAY/PM-JAY) तक पहुंचें, मातृ देखभाल प्राप्त करें, टेलीमेडिसिन और आपातकालीन सहायता प्राप्त करें - सब कुछ आपकी अपनी भाषा में।",
      btn1: "नीचे AI परामर्श शुरू करें",
      btn2: "108 एम्बुलेंस बुलाएं",
      btn3: "स्वास्थ्य सलाह: 104",
      asha: "नंदुरबार, गढ़चिरौली, मेलघाट, पालघर और यवतमाल में 500+ आशा कार्यकर्ता और चिकित्सा केंद्र जुड़े हैं"
    },
    mr: {
      badge1: "100% मोफत सार्वजनिक आरोग्य सेवा • SIH",
      badge2: "4.9 नागरिक रेटिंग (50,000+ ग्रामीण कुटुंबे)",
      title1: "AI ट्रायजसह सक्षम करा",
      title2: "ग्रामीण आरोग्य सेवा",
      desc: "महाराष्ट्रातील ग्रामीण आणि आदिवासी भागात आरोग्य सेवेची दरी भरून काढणे. रुग्णालये शोधा, सरकारी योजनांचा (MJPJAY/PM-JAY) लाभ घ्या, मातृ काळजी, टेलीमेडिसिन आणि आपत्कालीन मदत मिळवा - सर्व काही तुमच्या स्वतःच्या भाषेत.",
      btn1: "खाली AI सल्लामसलत सुरू करा",
      btn2: "108 रुग्णवाहिका बोलावणे",
      btn3: "आरोग्य सल्ला: 104",
      asha: "नंदुरबार, गडचिरोली, मेळघाट, पालघर आणि यवतमाळमध्ये 500+ आशा कार्यकर्त्या आणि वैद्यकीय केंद्रे जोडली गेली आहेत"
    }
  };

  const t = translations[lang as keyof typeof translations] || translations.en;

  return (
    <div className="bg-gradient-to-br from-white to-clinical-mint border border-gray-100 rounded-3xl p-8 relative overflow-hidden shadow-[0_4px_24px_rgba(0,210,180,0.05)]">
      
      {/* Top tiny badge */}
      <div className="flex items-center mb-5">
        <div className="bg-[#e6f4ea] text-[#137333] text-[10px] font-bold uppercase tracking-wider px-3 py-1.5 rounded-full flex items-center gap-1.5 border border-[#ceead6]">
          <div className="w-2 h-2 rounded-full bg-[#137333]"></div>
          {t.badge1}
        </div>
      </div>

      <h1 className="text-3xl md:text-4xl lg:text-5xl font-extrabold text-[#0B2528] tracking-tight leading-[1.25] md:leading-[1.2] mb-6 max-w-3xl">
        <span className="block">{t.title1}</span>
        <span className="block text-clinical-teal mt-2 md:mt-3">{t.title2}</span>
      </h1>
      
      <p className="text-gray-500 text-sm md:text-base max-w-3xl mb-8 leading-relaxed">
        {t.desc}
      </p>
      
      <div className="flex flex-wrap items-center gap-4 mb-8">
        <a href="#main-tabs-section" className="bg-clinical-teal text-white px-5 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 hover:bg-clinical-tealDark transition-colors shadow-md shadow-clinical-teal/20">
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          {t.btn1}
        </a>
        <a href="tel:108" className="bg-white text-gray-700 border border-gray-200 px-5 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 hover:bg-gray-50 transition-colors shadow-sm">
          <svg className="w-4 h-4 text-red-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>
          {t.btn2}
        </a>
        <a href="tel:104" className="bg-white text-gray-700 border border-gray-200 px-5 py-2.5 rounded-full font-bold text-sm flex items-center gap-2 hover:bg-gray-50 transition-colors shadow-sm">
          <svg className="w-4 h-4 text-teal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          {t.btn3}
        </a>
      </div>

      <div className="flex items-center gap-3 text-xs font-semibold text-gray-500">
        <div className="flex -space-x-2">
          <div className="w-6 h-6 rounded-full bg-blue-100 border-2 border-white"></div>
          <div className="w-6 h-6 rounded-full bg-green-100 border-2 border-white"></div>
          <div className="w-6 h-6 rounded-full bg-amber-100 border-2 border-white"></div>
        </div>
        <span className="hidden sm:inline">{t.asha}</span>
      </div>
    </div>
  );
}
