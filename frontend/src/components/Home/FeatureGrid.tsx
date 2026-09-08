"use client";

export function FeatureGrid({ lang }: { lang: string }) {
  const translations = {
    en: {
      f1_title: "Audio & Voice Triage",
      f1_desc: "In-browser speech recognition in Marathi, Hindi, and English for rural citizens who prefer speaking symptoms.",
      f2_title: "Smart Hospital Locator",
      f2_desc: "Locates PHCs, CHCs, SDHs, and District Hospitals across tribal Maharashtra with verified services and contact details.",
      f3_title: "Cashless Health Schemes",
      f3_desc: "Comprehensive navigation for MJPJAY (up to ₹5L cover), PM-JAY, Aapla Dawakhana, and Janani Suraksha Yojana."
    },
    hi: {
      f1_title: "ऑडियो और वॉयस ट्राइएज",
      f1_desc: "मराठी, हिंदी और अंग्रेजी में इन-ब्राउज़र भाषण पहचान उन ग्रामीण नागरिकों के लिए जो लक्षण बोलना पसंद करते हैं।",
      f2_title: "स्मार्ट अस्पताल लोकेटर",
      f2_desc: "सत्यापित सेवाओं और संपर्क विवरण के साथ आदिवासी महाराष्ट्र भर में PHC, CHC, SDH और जिला अस्पतालों का पता लगाता है।",
      f3_title: "कैशलेस स्वास्थ्य योजनाएं",
      f3_desc: "MJPJAY (₹5L तक कवर), PM-JAY, आपला दवाखाना और जननी सुरक्षा योजना के लिए व्यापक मार्गदर्शन।"
    },
    mr: {
      f1_title: "ऑडिओ आणि व्हॉइस ट्रायज",
      f1_desc: "मराठी, हिंदी आणि इंग्रजीमध्ये इन-ब्राउझर भाषण ओळख त्या ग्रामीण नागरिकांसाठी ज्यांना लक्षणे सांगायला आवडते.",
      f2_title: "स्मार्ट रुग्णालय शोधक",
      f2_desc: "प्रमाणित सेवा आणि संपर्क तपशीलांसह आदिवासी महाराष्ट्रभर PHC, CHC, SDH आणि जिल्हा रुग्णालये शोधते.",
      f3_title: "कॅशलेस आरोग्य योजना",
      f3_desc: "MJPJAY (₹5L पर्यंत कव्हर), PM-JAY, आपला दवाखाना आणि जननी सुरक्षा योजनेसाठी सविस्तर मार्गदर्शन."
    }
  };
  const t = translations[lang as keyof typeof translations] || translations.en;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
        <div className="w-10 h-10 rounded-xl bg-gray-50 flex items-center justify-center mb-4">
          <svg className="w-5 h-5 text-gray-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
        </div>
        <h3 className="text-lg font-bold text-[#0B2528] mb-2">{t.f1_title}</h3>
        <p className="text-sm text-gray-500 leading-relaxed">
          {t.f1_desc}
        </p>
      </div>
      
      <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
        <div className="w-10 h-10 rounded-xl bg-gray-50 flex items-center justify-center mb-4">
          <svg className="w-5 h-5 text-teal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/><circle cx="12" cy="10" r="3"/></svg>
        </div>
        <h3 className="text-lg font-bold text-[#0B2528] mb-2">{t.f2_title}</h3>
        <p className="text-sm text-gray-500 leading-relaxed">
          {t.f2_desc}
        </p>
      </div>

      <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
        <div className="w-10 h-10 rounded-xl bg-gray-50 flex items-center justify-center mb-4">
          <svg className="w-5 h-5 text-amber-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="3" x2="21" y1="9" y2="9"/><path d="M9 21V9"/></svg>
        </div>
        <h3 className="text-lg font-bold text-[#0B2528] mb-2">{t.f3_title}</h3>
        <p className="text-sm text-gray-500 leading-relaxed">
          {t.f3_desc}
        </p>
      </div>
    </div>
  );
}
