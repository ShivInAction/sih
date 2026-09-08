export interface Facility {
  name: string;
  type: string;
  location: string;
  phone: string;
  beds: string;
  facilities: string;
  services_list: string[];
  district?: string;
  is_hq?: boolean;
  match_reasons?: string[];
}

export interface Scheme {
  name: string;
  benefits: string;
  eligibility: string;
  apply_how: string;
  what_to_carry: string;
  verify_at: string;
  source: string;
  status: string;
}

export interface Medicine {
  name: string;
  branded_price: string;
  generic_price: string;
  saving_percent: string;
  use: string;
}

export interface ANCVB {
  visit: string;
  timing: string;
  importance: string;
}

export interface Immunization {
  age: string;
  vaccines: string;
  protects: string;
}

export interface HealthCamp {
  date: string;
  name: string;
  location: string;
  services: string;
  target: string;
  action: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}
