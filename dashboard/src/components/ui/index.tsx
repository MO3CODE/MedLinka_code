import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import clsx from 'clsx';

/* ── Button ─────────────────────────────────────────── */
interface BtnProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?:    'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?:    React.ReactNode;
}
export const Button: React.FC<BtnProps> = ({
  children, variant = 'primary', size = 'md', loading, icon, className, disabled, ...rest
}) => {
  const base = 'inline-flex items-center gap-2 font-medium rounded-lg transition-all duration-150 whitespace-nowrap';
  const variants: Record<string, string> = {
    primary:   'bg-[var(--primary)] text-white hover:bg-[var(--primary-dark)] shadow-sm hover:shadow-[var(--shadow-blue)]',
    secondary: 'bg-[var(--secondary)] text-white hover:opacity-90',
    outline:   'border border-[var(--border)] text-[var(--text-2)] hover:border-[var(--primary)] hover:text-[var(--primary)] bg-white',
    ghost:     'text-[var(--text-2)] hover:bg-[var(--bg)] hover:text-[var(--text-1)]',
    danger:    'bg-[var(--danger)] text-white hover:opacity-90',
  };
  const sizes: Record<string, string> = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-2.5 text-base',
  };
  return (
    <button
      {...rest}
      disabled={disabled || loading}
      className={clsx(base, variants[variant], sizes[size], (disabled || loading) && 'opacity-50 cursor-not-allowed', className)}
      style={{ fontFamily: 'var(--font)' }}
    >
      {loading ? <Spinner size="sm" /> : icon}
      {children}
    </button>
  );
};

/* ── Input ─────────────────────────────────────────── */
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?:  string;
}
export const Input: React.FC<InputProps> = ({ label, error, hint, className, ...rest }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginBottom: 12 }}>
    {label && <label style={{ fontSize: 13, fontWeight: 500, color: 'var(--text-2)' }}>{label}</label>}
    <input
      {...rest}
      style={{
        padding: '8px 12px', borderRadius: 8, border: `1.5px solid ${error ? 'var(--danger)' : 'var(--border)'}`,
        fontSize: 14, color: 'var(--text-1)', background: 'var(--surface)',
        outline: 'none', fontFamily: 'var(--font)', transition: 'border-color .15s',
        ...rest.style,
      }}
      onFocus={(e) => { e.target.style.borderColor = error ? 'var(--danger)' : 'var(--primary)'; }}
      onBlur={(e)  => { e.target.style.borderColor = error ? 'var(--danger)' : 'var(--border)'; }}
    />
    {error && <span style={{ fontSize: 12, color: 'var(--danger)' }}>{error}</span>}
    {hint  && <span style={{ fontSize: 12, color: 'var(--text-3)' }}>{hint}</span>}
  </div>
);

/* ── Select ─────────────────────────────────────────── */
interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
}
export const Select: React.FC<SelectProps> = ({ label, options, ...rest }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: 4, marginBottom: 12 }}>
    {label && <label style={{ fontSize: 13, fontWeight: 500, color: 'var(--text-2)' }}>{label}</label>}
    <select
      {...rest}
      style={{
        padding: '8px 12px', borderRadius: 8, border: '1.5px solid var(--border)',
        fontSize: 14, color: 'var(--text-1)', background: 'var(--surface)',
        outline: 'none', fontFamily: 'var(--font)', cursor: 'pointer',
      }}
    >
      {options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
    </select>
  </div>
);

/* ── Card ─────────────────────────────────────────── */
export const Card: React.FC<{ children: React.ReactNode; style?: React.CSSProperties; className?: string }> = ({ children, style, className }) => (
  <div style={{ background: 'var(--surface)', borderRadius: 'var(--radius-lg)', boxShadow: 'var(--shadow-sm)', border: '1px solid var(--border)', ...style }} className={className}>
    {children}
  </div>
);

/* ── Badge ─────────────────────────────────────────── */
const STATUS_MAP: Record<string, { bg: string; color: string }> = {
  pending:   { bg: 'var(--warning-light)', color: 'var(--warning)' },
  confirmed: { bg: 'var(--success-light)', color: 'var(--success)' },
  cancelled: { bg: 'var(--danger-light)',  color: 'var(--danger)'  },
  completed: { bg: 'var(--info-light)',    color: 'var(--info)'    },
  shipped:   { bg: 'var(--primary-light)', color: 'var(--primary)' },
  delivered: { bg: 'var(--success-light)', color: 'var(--success)' },
};
export const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
  const { t } = useTranslation();
  const { bg, color } = STATUS_MAP[status] ?? { bg: 'var(--bg)', color: 'var(--text-2)' };
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 4,
      background: bg, color, padding: '3px 10px',
      borderRadius: 999, fontSize: 12, fontWeight: 500,
    }}>
      <span style={{ width: 6, height: 6, borderRadius: '50%', background: color, display: 'inline-block' }} />
      {t(status)}
    </span>
  );
};

/* ── Spinner ─────────────────────────────────────────── */
export const Spinner: React.FC<{ size?: 'sm' | 'md' | 'lg' }> = ({ size = 'md' }) => {
  const s = size === 'sm' ? 14 : size === 'lg' ? 32 : 20;
  return (
    <svg width={s} height={s} viewBox="0 0 24 24" style={{ animation: 'spin 0.8s linear infinite' }}>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" strokeWidth="3" strokeDasharray="50 30" strokeLinecap="round" />
    </svg>
  );
};

/* ── Table ─────────────────────────────────────────── */
interface Column<T> { key: string; label: string; render?: (row: T) => React.ReactNode; }
interface TableProps<T> { columns: Column<T>[]; data: T[]; loading?: boolean; emptyMessage?: string; }
export function Table<T extends { id?: string }>({ columns, data, loading, emptyMessage }: TableProps<T>) {
  const { t } = useTranslation();
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
        <thead>
          <tr style={{ borderBottom: '1px solid var(--border)', background: 'var(--surface-2)' }}>
            {columns.map((c) => (
              <th key={c.key} style={{ padding: '10px 16px', textAlign: 'start', fontSize: 12, fontWeight: 600, color: 'var(--text-3)', textTransform: 'uppercase', letterSpacing: '.04em', whiteSpace: 'nowrap' }}>
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr><td colSpan={columns.length} style={{ padding: 40, textAlign: 'center', color: 'var(--text-3)' }}><Spinner /> </td></tr>
          ) : data.length === 0 ? (
            <tr><td colSpan={columns.length} style={{ padding: 40, textAlign: 'center', color: 'var(--text-3)' }}>{emptyMessage ?? t('no_data')}</td></tr>
          ) : (
            data.map((row, i) => (
              <tr key={row.id ?? i} style={{ borderBottom: '1px solid var(--border)', transition: 'background .1s' }}
                onMouseEnter={(e) => (e.currentTarget.style.background = 'var(--surface-2)')}
                onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
              >
                {columns.map((c) => (
                  <td key={c.key} style={{ padding: '12px 16px', color: 'var(--text-1)', whiteSpace: 'nowrap' }}>
                    {c.render ? c.render(row) : String((row as any)[c.key] ?? '—')}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

/* ── Modal ─────────────────────────────────────────── */
export const Modal: React.FC<{
  open: boolean; onClose: () => void;
  title: string; children: React.ReactNode; width?: number;
}> = ({ open, onClose, title, children, width = 480 }) => {
  if (!open) return null;
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 999, display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'rgba(0,0,0,.45)', backdropFilter: 'blur(2px)' }}
      onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div style={{ background: 'var(--surface)', borderRadius: 'var(--radius-xl)', width, maxWidth: '95vw', maxHeight: '90vh', overflowY: 'auto', boxShadow: 'var(--shadow-lg)', animation: 'fadeSlideIn .2s ease both' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px 24px', borderBottom: '1px solid var(--border)' }}>
          <h3 style={{ margin: 0 }}>{title}</h3>
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: 20, cursor: 'pointer', color: 'var(--text-3)', lineHeight: 1, padding: 4, borderRadius: 6 }}>✕</button>
        </div>
        <div style={{ padding: 24 }}>{children}</div>
      </div>
    </div>
  );
};

/* ── Stat Card ─────────────────────────────────────────── */
export const StatCard: React.FC<{
  icon: string; label: string; value: string | number;
  trend?: number; color?: string; delay?: number;
}> = ({ icon, label, value, trend, color = 'var(--primary)', delay = 0 }) => (
  <Card style={{ padding: 20, animation: `fadeSlideIn .3s ease ${delay}ms both` }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
      <div style={{ width: 44, height: 44, borderRadius: 12, background: color + '1A', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22 }}>
        {icon}
      </div>
      {trend !== undefined && (
        <span style={{ fontSize: 12, fontWeight: 600, color: trend >= 0 ? 'var(--success)' : 'var(--danger)', background: trend >= 0 ? 'var(--success-light)' : 'var(--danger-light)', padding: '2px 8px', borderRadius: 999 }}>
          {trend >= 0 ? '↑' : '↓'} {Math.abs(trend)}%
        </span>
      )}
    </div>
    <div style={{ marginTop: 16 }}>
      <div style={{ fontSize: 28, fontWeight: 700, color: 'var(--text-1)', letterSpacing: '-.02em' }}>{value}</div>
      <div style={{ fontSize: 13, color: 'var(--text-3)', marginTop: 2 }}>{label}</div>
    </div>
  </Card>
);

/* ── Page Header ─────────────────────────────────────────── */
export const PageHeader: React.FC<{ title: string; subtitle?: string; action?: React.ReactNode }> = ({ title, subtitle, action }) => (
  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
    <div>
      <h2 style={{ margin: 0, color: 'var(--text-1)' }}>{title}</h2>
      {subtitle && <p style={{ margin: '4px 0 0', fontSize: 14, color: 'var(--text-3)' }}>{subtitle}</p>}
    </div>
    {action}
  </div>
);

/* ── Search Bar ─────────────────────────────────────────── */
export const SearchBar: React.FC<{ value: string; onChange: (v: string) => void; placeholder?: string }> = ({ value, onChange, placeholder }) => (
  <div style={{ position: 'relative', display: 'inline-flex', alignItems: 'center' }}>
    <span style={{ position: 'absolute', insetInlineStart: 12, fontSize: 16, color: 'var(--text-3)', pointerEvents: 'none' }}>🔍</span>
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      style={{
        paddingInlineStart: 36, paddingInlineEnd: 12, paddingBlock: 8,
        border: '1.5px solid var(--border)', borderRadius: 8,
        fontSize: 14, background: 'var(--surface)', color: 'var(--text-1)',
        outline: 'none', fontFamily: 'var(--font)', width: 240,
        transition: 'border-color .15s, width .2s',
      }}
      onFocus={(e) => { e.target.style.borderColor = 'var(--primary)'; e.target.style.width = '280px'; }}
      onBlur={(e)  => { e.target.style.borderColor = 'var(--border)';  e.target.style.width = '240px'; }}
    />
  </div>
);
