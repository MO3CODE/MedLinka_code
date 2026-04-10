import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import { useStore } from '../store';

const BASE = 'http://localhost:8000/api/v1';

export default function LoginPage() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const setAuth  = useStore((s) => s.setAuth);

  const [email,    setEmail]    = useState('');
  const [password, setPassword] = useState('');
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); setError('');
    try {
      // Step 1: login
      const loginResp = await axios.post(`${BASE}/auth/login`, {
        email: email.trim(),
        password,
      });
      const { access_token, refresh_token } = loginResp.data;

      // Step 2: save tokens FIRST
      localStorage.setItem('access_token',  access_token);
      localStorage.setItem('refresh_token', refresh_token);

      // Step 3: fetch user profile with token
      const meResp = await axios.get(`${BASE}/users/me`, {
        headers: { Authorization: `Bearer ${access_token}` },
      });

      // Step 4: save to store
      setAuth(meResp.data, access_token, refresh_token);
      navigate('/');
    } catch (err: any) {
      const msg = err?.response?.data?.detail ?? t('error');
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%)',
      padding: 24,
    }}>
      <div style={{ position: 'absolute', inset: 0, backgroundImage: 'radial-gradient(circle at 1px 1px, rgba(255,255,255,.06) 1px, transparent 0)', backgroundSize: '32px 32px', pointerEvents: 'none' }} />

      <div style={{ position: 'relative', width: '100%', maxWidth: 440 }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{
            width: 64, height: 64, borderRadius: 18, background: '#1A8CFF',
            margin: '0 auto 16px', display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 28, fontWeight: 800, color: '#fff',
            boxShadow: '0 0 0 6px rgba(26,140,255,.2)',
          }}>M</div>
          <h1 style={{ color: '#fff', fontSize: '1.6rem', fontWeight: 700, marginBottom: 4 }}>MedLinka</h1>
          <p style={{ color: '#64748b', fontSize: 14 }}>Healthcare Dashboard</p>
        </div>

        <div style={{
          background: 'rgba(255,255,255,.05)', backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255,255,255,.1)', borderRadius: 20,
          padding: 32, boxShadow: '0 20px 60px rgba(0,0,0,.4)',
        }}>
          <h2 style={{ color: '#f1f5f9', marginBottom: 24, fontWeight: 600, fontSize: '1.1rem' }}>
            مرحباً بعودتك 👋
          </h2>

          {error && (
            <div style={{ background: '#FFF0F0', border: '1px solid #FF4D4D', color: '#FF4D4D', padding: '10px 14px', borderRadius: 8, fontSize: 13, marginBottom: 16 }}>
              {error}
            </div>
          )}

          <form onSubmit={handleLogin}>
            <div style={{ marginBottom: 12 }}>
              <label style={{ display: 'block', fontSize: 13, fontWeight: 500, color: '#94a3b8', marginBottom: 6 }}>البريد الإلكتروني</label>
              <input
                type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                placeholder="ahmed@medlinka.com" required
                style={{ width: '100%', padding: '10px 14px', borderRadius: 8, background: 'rgba(255,255,255,.08)', border: '1.5px solid rgba(255,255,255,.12)', color: '#f1f5f9', fontSize: 14, fontFamily: 'var(--font)', outline: 'none', boxSizing: 'border-box' }}
              />
            </div>

            <div style={{ marginBottom: 24 }}>
              <label style={{ display: 'block', fontSize: 13, fontWeight: 500, color: '#94a3b8', marginBottom: 6 }}>كلمة المرور</label>
              <input
                type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••" required
                style={{ width: '100%', padding: '10px 14px', borderRadius: 8, background: 'rgba(255,255,255,.08)', border: '1.5px solid rgba(255,255,255,.12)', color: '#f1f5f9', fontSize: 14, fontFamily: 'var(--font)', outline: 'none', boxSizing: 'border-box' }}
              />
            </div>

            <button type="submit" disabled={loading} style={{
              width: '100%', padding: '11px', borderRadius: 10, border: 'none',
              background: loading ? '#334155' : '#1A8CFF', color: '#fff',
              fontSize: 15, fontWeight: 600, cursor: loading ? 'not-allowed' : 'pointer',
              fontFamily: 'var(--font)',
            }}>
              {loading ? '...' : 'تسجيل الدخول'}
            </button>
          </form>

          <div style={{ marginTop: 24, padding: 14, background: 'rgba(26,140,255,.08)', borderRadius: 10, border: '1px solid rgba(26,140,255,.2)' }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: '#60a5fa', marginBottom: 8 }}>🧪 Demo Accounts</div>
            {[
              { role: 'Admin',    email: 'ahmed@medlinka.com' },
              { role: 'Doctor',   email: 'dr.sarah@medlinka.com' },
              { role: 'Pharmacy', email: 'pharmacy@medlinka.com' },
            ].map((d) => (
              <button key={d.email} onClick={() => { setEmail(d.email); setPassword('Test1234'); }}
                style={{ display: 'block', width: '100%', textAlign: 'start', background: 'none', border: 'none', padding: '4px 0', cursor: 'pointer', color: '#94a3b8', fontSize: 12, fontFamily: 'var(--font)' }}>
                <span style={{ color: '#60a5fa', fontWeight: 600 }}>{d.role}:</span> {d.email} / Test1234
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
