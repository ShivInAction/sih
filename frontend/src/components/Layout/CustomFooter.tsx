"use client";

export function CustomFooter({ lang }: { lang: string }) {
  const translations = {
    en: {
      desc: "Bridging healthcare accessibility across Maharashtra's underserved tribal and rural blocks. Real-time AI clinical triage and scheme navigation in English, हिंदी, and मराठी.",
      h1: "24x7 HELPLINES",
      h2: "SCHEMES & PORTALS",
      h3: "KEY DISTRICTS",
      amb: "Ambulance",
      jan: "Janani Express",
      adv: "Health Advice",
      chd: "Childline",
      wom: "Women Helpline",
      disclaimer: "MahaArogya Setu © 2026 · General Healthcare Awareness & Access Navigation · In severe symptoms, immediately call 108 or visit nearest District Hospital."
    },
    hi: {
      desc: "महाराष्ट्र के वंचित आदिवासी और ग्रामीण ब्लॉकों में स्वास्थ्य सेवा की पहुंच को पाटना। अंग्रेजी, हिंदी और मराठी में रीयल-टाइम AI क्लिनिकल ट्राइएज और योजना नेविगेशन।",
      h1: "24x7 हेल्पलाइन",
      h2: "योजनाएं और पोर्टल",
      h3: "प्रमुख जिले",
      amb: "एम्बुलेंस",
      jan: "जननी एक्सप्रेस",
      adv: "स्वास्थ्य सलाह",
      chd: "चाइल्डलाइन",
      wom: "महिला हेल्पलाइन",
      disclaimer: "महाआरोग्य सेतु © 2026 · सामान्य स्वास्थ्य जागरूकता और पहुंच नेविगेशन · गंभीर लक्षणों में, तुरंत 108 पर कॉल करें या निकटतम जिला अस्पताल जाएं।"
    },
    mr: {
      desc: "महाराष्ट्रातील दुर्लक्षित आदिवासी आणि ग्रामीण भागातील आरोग्य सेवा सुलभ करणे. इंग्रजी, हिंदी आणि मराठीमध्ये रिअल-टाइम AI क्लिनिकल ट्रायज आणि योजना नेव्हिगेशन.",
      h1: "24x7 हेल्पलाइन",
      h2: "योजना आणि पोर्टल्स",
      h3: "प्रमुख जिल्हे",
      amb: "रुग्णवाहिका",
      jan: "जननी एक्सप्रेस",
      adv: "आरोग्य सल्ला",
      chd: "चाइल्डलाइन",
      wom: "महिला हेल्पलाइन",
      disclaimer: "महाआरोग्य सेतु © 2026 · सामान्य आरोग्य जागरूकता आणि प्रवेश नेव्हिगेशन · गंभीर लक्षणांमध्ये, त्वरित 108 वर कॉल करा किंवा जवळच्या जिल्हा रुग्णालयाला भेट द्या."
    }
  };

  const t = translations[lang as keyof typeof translations] || translations.en;

  return (
    <footer className="bg-[#0B2528] text-white rounded-3xl overflow-hidden shadow-xl">
      <div className="p-8 md:p-10 grid grid-cols-1 md:grid-cols-4 gap-8">
        
        <div className="md:col-span-1">
          <h4 className="text-white font-bold text-lg mb-3 flex items-center gap-2">
            <span className="text-gray-400">🩺</span> MahaArogya Setu
          </h4>
          <p className="text-xs text-gray-400 leading-relaxed mb-6">
            {t.desc}
          </p>
          <div className="inline-block border border-white/10 bg-white/5 px-3 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-widest text-gray-300">
            SMART INDIA HACKATHON • NHM
          </div>
        </div>
        
        <div>
          <h4 className="text-clinical-teal font-bold text-xs uppercase tracking-widest mb-4">{t.h1}</h4>
          <ul className="space-y-3 text-xs font-semibold">
            <li><a href="tel:108" className="hover:text-white hover:underline transition-colors"><span className="text-red-400 mr-2">🚑</span> {t.amb}: 108</a></li>
            <li><a href="tel:102" className="hover:text-white hover:underline transition-colors"><span className="text-pink-400 mr-2">🤱</span> {t.jan}: 102</a></li>
            <li><a href="tel:104" className="hover:text-white hover:underline transition-colors"><span className="text-teal-400 mr-2">🏥</span> {t.adv}: 104</a></li>
            <li><a href="tel:1098" className="hover:text-white hover:underline transition-colors"><span className="text-orange-400 mr-2">👶</span> {t.chd}: 1098</a></li>
            <li><a href="tel:181" className="hover:text-white hover:underline transition-colors"><span className="text-blue-400 mr-2">👩</span> {t.wom}: 181</a></li>
          </ul>
        </div>
        
        <div>
          <h4 className="text-clinical-teal font-bold text-xs uppercase tracking-widest mb-4">{t.h2}</h4>
          <ul className="space-y-3 text-xs font-semibold text-gray-300">
            <li>
              <a href="https://www.jeevandayee.gov.in/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:text-white transition-colors">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div> MJPJAY Portal (₹5L)
              </a>
            </li>
            <li>
              <a href="https://abdm.gov.in/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:text-white transition-colors">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div> Ayushman Bharat (PM-JAY)
              </a>
            </li>
            <li>
              <a href="https://esanjeevani.mohfw.gov.in/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:text-white transition-colors">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div> eSanjeevani Telemedicine
              </a>
            </li>
            <li>
              <a href="https://abha.abdm.gov.in/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:text-white transition-colors">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-400"></div> ABHA Digital Health ID
              </a>
            </li>
            <li>
              <a href="http://janaushadhi.gov.in/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:text-white transition-colors">
                <div className="w-1.5 h-1.5 rounded-full bg-amber-400"></div> PM Jan Aushadhi Kendra
              </a>
            </li>
          </ul>
        </div>
        
        <div>
          <h4 className="text-clinical-teal font-bold text-xs uppercase tracking-widest mb-4">{t.h3}</h4>
          <ul className="space-y-3 text-xs font-semibold text-gray-300">
            <li className="flex items-start gap-2">
              <span className="text-red-400 text-xs">📍</span> 
              <span>Nandurbar <span className="text-gray-500 font-normal">(Tribal Core)</span></span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 text-xs">📍</span> 
              <span>Gadchiroli <span className="text-gray-500 font-normal">(Aheri, Bhamragad)</span></span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 text-xs">📍</span> 
              <span>Amravati <span className="text-gray-500 font-normal">(Melghat Blocks)</span></span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 text-xs">📍</span> 
              <span>Palghar <span className="text-gray-500 font-normal">(Jawhar, Mokhada)</span></span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 text-xs">📍</span> 
              <span>Yavatmal <span className="text-gray-500 font-normal">(Pusad, City)</span></span>
            </li>
          </ul>
        </div>
        
      </div>
      
      <div className="bg-[#051415] p-4 text-center text-[10px] text-gray-500">
        {t.disclaimer}
      </div>
    </footer>
  );
}
