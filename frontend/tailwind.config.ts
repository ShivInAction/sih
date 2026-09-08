import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        clinical: {
          teal: "#00D2B4",       // Primary interactive elements
          tealDark: "#00B096",   // Hover states
          slate: "#0B2528",      // Typography and high-contrast footers
          slateLight: "#163c40", // Secondary text / backgrounds
          mint: "#F2FBF9",       // App background / card backgrounds
          danger: "#DC2626",     // 108 Emergency actions
          dangerBg: "#FEF2F2",
          warning: "#F59E0B",    // Alerts
          warningBg: "#FFFBEB",
        }
      },
      animation: {
        'ecg-pulse': 'ecgPulse 1.5s ease-in-out infinite',
        'fade-in-up': 'fadeInUp 0.3s ease-out forwards',
      },
      keyframes: {
        ecgPulse: {
          '0%, 100%': { transform: 'scaleY(1)' },
          '15%': { transform: 'scaleY(2)' },
          '30%': { transform: 'scaleY(-1.5)' },
          '45%': { transform: 'scaleY(1.2)' },
          '60%': { transform: 'scaleY(1)' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
};
export default config;
