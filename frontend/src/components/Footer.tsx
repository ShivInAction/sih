import { Phone } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-clinical-slate text-gray-300 py-10 px-4 mt-8">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        
        <div>
          <h4 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
            <span className="text-clinical-teal text-2xl font-bold">+</span> MahaArogya Setu
          </h4>
          <p className="text-sm text-gray-400 max-w-xs">
            Connecting rural Maharashtra to accessible, affordable, and quality healthcare through AI-driven triage and government schemes.
          </p>
        </div>
        
        <div>
          <h4 className="text-white font-bold mb-4 uppercase tracking-wider text-sm">24×7 Emergency Helplines</h4>
          <ul className="space-y-3">
            <li>
              <a href="tel:108" className="flex items-center gap-3 hover:text-white transition-colors group">
                <div className="bg-clinical-slateLight p-2 rounded-lg group-hover:bg-clinical-teal/20 transition-colors">
                  <Phone size={16} className="text-clinical-danger" />
                </div>
                <div>
                  <span className="block font-bold text-white leading-tight">108</span>
                  <span className="text-xs text-gray-400">Medical Emergency & Ambulance</span>
                </div>
              </a>
            </li>
            <li>
              <a href="tel:104" className="flex items-center gap-3 hover:text-white transition-colors group">
                <div className="bg-clinical-slateLight p-2 rounded-lg group-hover:bg-clinical-teal/20 transition-colors">
                  <Phone size={16} className="text-clinical-teal" />
                </div>
                <div>
                  <span className="block font-bold text-white leading-tight">104</span>
                  <span className="text-xs text-gray-400">Health Advice Helpline</span>
                </div>
              </a>
            </li>
          </ul>
        </div>
        
        <div>
          <h4 className="text-white font-bold mb-4 uppercase tracking-wider text-sm">Important Portals</h4>
          <ul className="space-y-2 text-sm">
            <li><a href="https://abdm.gov.in" target="_blank" rel="noopener noreferrer" className="hover:text-clinical-teal transition-colors flex items-center gap-2">→ Ayushman Bharat Digital Mission (ABHA)</a></li>
            <li><a href="https://esanjeevani.mohfw.gov.in/#/" target="_blank" rel="noopener noreferrer" className="hover:text-clinical-teal transition-colors flex items-center gap-2">→ eSanjeevani National Telemedicine</a></li>
          </ul>
        </div>
        
      </div>
      
      <div className="max-w-7xl mx-auto mt-10 pt-6 border-t border-gray-700/50 text-xs text-center text-gray-500">
        <p>Built for Smart India Hackathon 2024. Not a substitute for professional medical advice.</p>
      </div>
    </footer>
  );
}
