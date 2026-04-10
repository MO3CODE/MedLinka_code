import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useStore } from '../../store';
import { authAPI } from '../../services/api';
import clsx from 'clsx';

/* ── Nav items per role ─────────────────────────────── */
const ADMIN_NAV = [
  { to: '/',             icon: '▦',  key: 'dashboard'     },
  { to: '/doctors',      icon: '👨‍⚕️', key: 'doctors'       },
  { to: '/appointments', icon: '📅', key: 'appointments'   },
  { to: '/pharmacy',     icon: '💊', key: 'pharmacy'       },
  { to: '/orders',       icon: '📦', key: 'orders'         },
  { to: '/analytics',    icon: '📊', key: 'analytics'      },
];
const DOCTOR_NAV = [
  { to: '/',             icon: '▦',  key: 'dashboard'     },
  { to: '/schedule',     icon: '📅', key: 'my_schedule'    },
];
const PHARMACY_NAV = [
  { to: '/',             icon: '▦',  key: 'dashboard'     },
  { to: '/medicines',    icon: '💊', key: 'medicines'      },
  { to: '/orders',       icon: '📦', key: 'orders'         },
];

/* ── Sidebar ─────────────────────────────────────────── */
export const Sidebar: React.FC = () => {
  const { t } = useTranslation();
  const { user, sidebarOpen } = useStore();

  const navItems = user?.role === 'doctor'
    ? DOCTOR_NAV
    : user?.role === 'pharmacy'
    ? PHARMACY_NAV
    : ADMIN_NAV;

  return (
    <aside style={{
      width: sidebarOpen ? 'var(--sidebar-w)' : 64,
      background: 'var(--sidebar-bg)',
      borderInlineEnd: '1px solid var(--sidebar-border)',
      height: '100vh', position: 'fixed', insetInlineStart: 0, top: 0,
      display: 'flex', flexDirection: 'column',
      transition: 'width .25s var(--ease)',
      zIndex: 100, overflowX: 'hidden',
    }}>

      {/* Logo */}
      <div style={{ padding: '20px 16px', borderBottom: '1px solid var(--sidebar-border)', display: 'flex', alignItems: 'center', gap: 12, minHeight: 64 }}>
        <div style={{ width: 36, height: 36, borderRadius: 10, background: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 18, fontWeight: 700, color: '#fff', flexShrink: 0 }}>M</div>
        {sidebarOpen && (
          <div>
            <div style={{ color: '#fff', fontWeight: 700, fontSize: 15, lineHeight: 1.2 }}>MedLinka</div>
            <div style={{ color: 'var(--sidebar-text)', fontSize: 11 }}>Dashboard</div>
          </div>
        )}
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: '12px 8px', display: 'flex', flexDirection: 'column', gap: 2, overflowY: 'auto' }}>
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            style={({ isActive }) => ({
              display: 'flex', alignItems: 'center', gap: 12,
              padding: '10px 12px', borderRadius: 8,
              color: isActive ? '#fff' : 'var(--sidebar-text)',
              background: isActive ? 'var(--primary)' : 'transparent',
              textDecoration: 'none', fontWeight: isActive ? 500 : 400,
              fontSize: 14, transition: 'all .15s',
              whiteSpace: 'nowrap',
            })}
            onMouseEnter={(e) => {
              if (!(e.currentTarget.style.background.includes('var(--primary)'))) {
                e.currentTarget.style.background = 'rgba(255,255,255,.06)';
                e.currentTarget.style.color = '#fff';
              }
            }}
            onMouseLeave={(e) => {
              if (!(e.currentTarget.style.background.includes('var(--primary)'))) {
                e.currentTarget.style.background = 'transparent';
                e.currentTarget.style.color = 'var(--sidebar-text)';
              }
            }}
          >
            <span style={{ fontSize: 18, flexShrink: 0, width: 22, textAlign: 'center' }}>{item.icon}</span>
            {sidebarOpen && <span>{t(item.key)}</span>}
          </NavLink>
        ))}
      </nav>

      {/* User at bottom */}
      {sidebarOpen && user && (
        <div style={{ padding: 12, borderTop: '1px solid var(--sidebar-border)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: 8, borderRadius: 8 }}>
            <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontWeight: 600, flexShrink: 0 }}>
              {user.full_name[0].toUpperCase()}
            </div>
            <div style={{ overflow: 'hidden' }}>
              <div style={{ color: '#e2e8f0', fontSize: 13, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{user.full_name}</div>
              <div style={{ color: 'var(--sidebar-text)', fontSize: 11 }}>{user.role}</div>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
};

/* ── Topbar ─────────────────────────────────────────── */
const LANG_OPTIONS = [{ value: 'ar', label: 'ع' }, { value: 'tr', label: 'TR' }, { value: 'en', label: 'EN' }];

export const Topbar: React.FC = () => {
  const { t } = useTranslation();
  const { lang, setLang, toggleSidebar, clearAuth } = useStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try { await authAPI.logout(); } catch {}
    clearAuth();
    navigate('/login');
  };

  return (
    <header style={{
      height: 'var(--topbar-h)', background: 'var(--surface)',
      borderBottom: '1px solid var(--border)',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 24px', position: 'sticky', top: 0, zIndex: 50,
      backdropFilter: 'blur(8px)', gap: 16,
    }}>
      {/* Left */}
      <button onClick={toggleSidebar} style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: 18, color: 'var(--text-2)', padding: 6, borderRadius: 6, display: 'flex', alignItems: 'center' }}>
        ☰
      </button>

      {/* Right */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>

        {/* Language switcher */}
        <div style={{ display: 'flex', gap: 2, background: 'var(--bg)', borderRadius: 8, padding: 3 }}>
          {LANG_OPTIONS.map((l) => (
            <button
              key={l.value}
              onClick={() => setLang(l.value)}
              style={{
                padding: '4px 10px', borderRadius: 6, border: 'none', cursor: 'pointer',
                fontSize: 12, fontWeight: 600, transition: 'all .15s',
                background: lang === l.value ? 'var(--surface)' : 'transparent',
                color: lang === l.value ? 'var(--primary)' : 'var(--text-3)',
                boxShadow: lang === l.value ? 'var(--shadow-sm)' : 'none',
              }}
            >
              {l.label}
            </button>
          ))}
        </div>

        {/* Logout */}
        <button
          onClick={handleLogout}
          title={t('logout')}
          style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: 8, padding: '6px 12px', cursor: 'pointer', fontSize: 13, color: 'var(--text-2)', display: 'flex', alignItems: 'center', gap: 6, transition: 'all .15s' }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLButtonElement).style.borderColor = 'var(--danger)'; (e.currentTarget as HTMLButtonElement).style.color = 'var(--danger)'; }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLButtonElement).style.borderColor = 'var(--border)'; (e.currentTarget as HTMLButtonElement).style.color = 'var(--text-2)'; }}
        >
          ⏻ {t('logout')}
        </button>
      </div>
    </header>
  );
};

/* ── App Shell ─────────────────────────────────────────── */
export const Shell: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { sidebarOpen } = useStore();
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <div style={{
        marginInlineStart: sidebarOpen ? 'var(--sidebar-w)' : '64px',
        flex: 1, display: 'flex', flexDirection: 'column',
        transition: 'margin-inline-start .25s var(--ease)', minWidth: 0,
      }}>
        <Topbar />
        <main style={{ flex: 1, padding: 28, maxWidth: 1400, width: '100%', margin: '0 auto' }}>
          {children}
        </main>
      </div>
    </div>
  );
};
