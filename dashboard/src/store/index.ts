import { create } from 'zustand';
import i18n from '../i18n';

interface User { id: string; email: string; full_name: string; role: string; preferred_language: string; }

interface Store {
  user:            User | null;
  isAuthenticated: boolean;
  lang:            string;
  sidebarOpen:     boolean;
  setAuth:    (user: User, access: string, refresh: string) => void;
  clearAuth:  () => void;
  setLang:    (lang: string) => void;
  toggleSidebar: () => void;
  loadFromStorage: () => Promise<void>;
}

export const useStore = create<Store>((set) => ({
  user:            null,
  isAuthenticated: false,
  lang:            localStorage.getItem('dashboard_lang') ?? 'ar',
  sidebarOpen:     true,

  setAuth: (user, access, refresh) => {
    localStorage.setItem('access_token',  access);
    localStorage.setItem('refresh_token', refresh);
    localStorage.setItem('dashboard_user', JSON.stringify(user));
    set({ user, isAuthenticated: true });
  },

  clearAuth: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('dashboard_user');
    set({ user: null, isAuthenticated: false });
  },

  setLang: (lang) => {
    localStorage.setItem('dashboard_lang', lang);
    i18n.changeLanguage(lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('lang', lang);
    set({ lang });
  },

  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),

  loadFromStorage: async () => {
    const token = localStorage.getItem('access_token');
    const raw   = localStorage.getItem('dashboard_user');
    const lang  = localStorage.getItem('dashboard_lang') ?? 'ar';
    i18n.changeLanguage(lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    if (token && raw) {
      set({ user: JSON.parse(raw), isAuthenticated: true, lang });
    }
  },
}));
