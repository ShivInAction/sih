"use client";

export function ComprehensiveCapabilities({ lang }: { lang: string }) {
  const translations = {
    en: {
      badge: "WHY CHOOSE MAHAAROGYA",
      title: "Explore Comprehensive Rural Health Capabilities",
      c1_title: "Instant AI Triage",
      c1_desc: "Evaluates symptoms with AI embeddings and alerts immediate red-flags for critical medical emergencies.",
      c2_title: "Cashless Guarantee",
      c2_desc: "Direct guidelines on documents and Arogyamitra desks to claim full cashless treatment under MJPJAY/PM-JAY.",
      c3_title: "Maternal & Child Health",
      c3_desc: "Complete 4-visit ANC schedule, danger sign detection, infant vaccination timeline, and ₹700 JSY cash aid.",
      c4_title: "2G Low-Bandwidth Mode",
      c4_desc: "Instant keyword matching designed to work seamlessly in deep forest and remote tribal areas with poor connectivity."
    },
    hi: {
      badge: "महाआरोग्य क्यों चुनें",
      title: "व्यापक ग्रामीण स्वास्थ्य क्षमताओं का अन्वेषण करें",
      c1_title: "त्वरित AI ट्राइएज",
      c1_desc: "AI एम्बेडिंग के साथ लक्षणों का मूल्यांकन करता है और गंभीर चिकित्सा आपात स्थितियों के लिए तत्काल चेतावनी देता है।",
      c2_title: "कैशलेस गारंटी",
      c2_desc: "MJPJAY/PM-JAY के तहत पूर्ण कैशलेस उपचार का दावा करने के लिए दस्तावेजों और आरोग्यमित्र डेस्क पर सीधा मार्गदर्शन।",
      c3_title: "मातृ एवं शिशु स्वास्थ्य",
      c3_desc: "पूर्ण 4-यात्रा ANC शेड्यूल, खतरे के संकेतों का पता लगाना, शिशु टीकाकरण समयरेखा, और ₹700 JSY नकद सहायता।",
      c4_title: "2G लो-बैंडविड्थ मोड",
      c4_desc: "कम कनेक्टिविटी वाले घने जंगलों और दूरदराज के आदिवासी क्षेत्रों में निर्बाध रूप से काम करने के लिए कीवर्ड मिलान।"
    },
    mr: {
      badge: "महाआरोग्य का निवडावे",
      title: "सर्वसमावेशक ग्रामीण आरोग्य क्षमता एक्सप्लोर करा",
      c1_title: "झटपट AI ट्रायज",
      c1_desc: "AI एम्बेडिंगसह लक्षणांचे मूल्यांकन करते आणि गंभीर वैद्यकीय आणीबाणीसाठी त्वरित सूचना देते.",
      c2_title: "कॅशलेस हमी",
      c2_desc: "MJPJAY/PM-JAY अंतर्गत संपूर्ण कॅशलेस उपचारांचा लाभ घेण्यासाठी कागदपत्रे आणि आरोग्यमित्र डेस्कवर थेट मार्गदर्शन.",
      c3_title: "माता आणि बाल आरोग्य",
      c3_desc: "संपूर्ण 4-भेट ANC वेळापत्रक, धोक्याची लक्षणे ओळखणे, बाल लसीकरण वेळापत्रक आणि ₹700 JSY रोख मदत.",
      c4_title: "2G कमी बँडविड्थ मोड",
      c4_desc: "कमी कनेक्टिव्हिटी असलेल्या घनदाट जंगलात आणि दुर्गम आदिवासी भागात अखंडपणे काम करण्यासाठी कीवर्ड मॅचिंग."
    }
  };

  const t = translations[lang as keyof typeof translations] || translations.en;

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="inline-block bg-clinical-teal/10 text-clinical-teal text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full mb-4">
          {t.badge}
        </div>
        <h2 className="text-3xl font-extrabold text-[#0B2528]">{t.title}</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white border border-gray-100 rounded-3xl p-6 shadow-sm hover:shadow-md transition-shadow">
          <div className="w-8 h-8 rounded bg-amber-50 text-amber-500 flex items-center justify-center mb-4 text-xl">⚡</div>
          <h3 className="text-lg font-bold text-[#0B2528] mb-3">{t.c1_title}</h3>
          <p className="text-sm text-gray-500 leading-relaxed">
            {t.c1_desc}
          </p>
        </div>

        <div className="bg-white border border-gray-100 rounded-3xl p-6 shadow-sm hover:shadow-md transition-shadow">
          <div className="w-8 h-8 rounded bg-red-50 text-red-500 flex items-center justify-center mb-4 text-xl">🛡️</div>
          <h3 className="text-lg font-bold text-[#0B2528] mb-3">{t.c2_title}</h3>
          <p className="text-sm text-gray-500 leading-relaxed">
            {t.c2_desc}
          </p>
        </div>

        <div className="bg-white border border-gray-100 rounded-3xl p-6 shadow-sm hover:shadow-md transition-shadow">
          <div className="w-8 h-8 rounded bg-purple-50 text-purple-500 flex items-center justify-center mb-4 text-xl">🤱</div>
          <h3 className="text-lg font-bold text-[#0B2528] mb-3">{t.c3_title}</h3>
          <p className="text-sm text-gray-500 leading-relaxed">
            {t.c3_desc}
          </p>
        </div>

        <div className="bg-white border border-gray-100 rounded-3xl p-6 shadow-sm hover:shadow-md transition-shadow">
          <div className="w-8 h-8 rounded bg-blue-50 text-blue-500 flex items-center justify-center mb-4 text-xl">📱</div>
          <h3 className="text-lg font-bold text-[#0B2528] mb-3">{t.c4_title}</h3>
          <p className="text-sm text-gray-500 leading-relaxed">
            {t.c4_desc}
          </p>
        </div>
      </div>
    </div>
  );
}
