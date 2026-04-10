/**
 * MedLinka Dashboard — Feature Pages
 * DoctorsPage · AppointmentsPage · MedicinesPage · OrdersPage · DoctorSchedulePage
 */

import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { format } from 'date-fns';
import { doctorAPI, appointmentAPI, pharmacyAPI, orderAPI } from '../services/api';
import {
  Card, PageHeader, Table, StatusBadge, Button, Modal,
  Input, Select, SearchBar, StatCard, Spinner,
} from '../components/ui';

/* ── Helpers ─────────────────────────────────────────── */
const SPECIALTY_OPTS = [
  'general', 'cardiology', 'dermatology', 'neurology',
  'orthopedics', 'pediatrics', 'psychiatry', 'gynecology',
  'ophthalmology', 'ent', 'dentistry', 'other',
];
const SPEC_ICONS: Record<string, string> = {
  cardiology: '❤️', general: '🩺', dermatology: '✨', neurology: '🧠',
  orthopedics: '🦴', pediatrics: '👶', psychiatry: '🧘', gynecology: '🌸',
  ophthalmology: '👁️', ent: '👂', dentistry: '🦷', other: '🏥',
};

/* ── Doctors Page ────────────────────────────────────── */
export function DoctorsPage() {
  const { t } = useTranslation();
  const [doctors, setDoctors] = useState<any[]>([]);
  const [search,  setSearch]  = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    doctorAPI.list({ available_only: false })
      .then((r) => setDoctors(r.data))
      .finally(() => setLoading(false));
  }, []);

  const filtered = doctors.filter((d) =>
    !search || d.user?.full_name?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <PageHeader title={`👨‍⚕️ ${t('doctors')}`} subtitle={`${doctors.length} total`} />

      {/* Specialty stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))', gap: 10, marginBottom: 24 }}>
        {SPECIALTY_OPTS.slice(0, 6).map((s, i) => {
          const count = doctors.filter((d) => d.specialty === s).length;
          return (
            <Card key={s} style={{ padding: 12, textAlign: 'center', animation: `fadeSlideIn .3s ease ${i * 50}ms both` }}>
              <div style={{ fontSize: 24, marginBottom: 4 }}>{SPEC_ICONS[s]}</div>
              <div style={{ fontSize: 18, fontWeight: 700 }}>{count}</div>
              <div style={{ fontSize: 11, color: 'var(--text-3)' }}>{t(s)}</div>
            </Card>
          );
        })}
      </div>

      <Card style={{ overflow: 'hidden' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12 }}>
          <h3 style={{ margin: 0 }}>{t('doctors')}</h3>
          <SearchBar value={search} onChange={setSearch} placeholder={t('search')} />
        </div>
        <Table
          loading={loading}
          columns={[
            { key: 'name',       label: t('doctor'),    render: (r: any) => (
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <div style={{ width: 36, height: 36, borderRadius: 10, background: 'var(--primary-light)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 18 }}>{SPEC_ICONS[r.specialty] ?? '🏥'}</div>
                <div>
                  <div style={{ fontWeight: 500 }}>{r.user?.full_name}</div>
                  <div style={{ fontSize: 12, color: 'var(--text-3)' }}>{r.user?.email}</div>
                </div>
              </div>
            )},
            { key: 'specialty',  label: t('specialty'), render: (r: any) => (
              <span style={{ background: 'var(--primary-light)', color: 'var(--primary)', padding: '2px 10px', borderRadius: 999, fontSize: 12, fontWeight: 500 }}>{t(r.specialty)}</span>
            )},
            { key: 'rating',     label: t('rating'),    render: (r: any) => <span>⭐ {r.rating.toFixed(1)}</span> },
            { key: 'fee',        label: t('fee'),        render: (r: any) => <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>${r.consultation_fee}</span> },
            { key: 'available',  label: t('status'),     render: (r: any) => (
              <span style={{ background: r.is_available ? 'var(--success-light)' : 'var(--danger-light)', color: r.is_available ? 'var(--success)' : 'var(--danger)', padding: '2px 10px', borderRadius: 999, fontSize: 12, fontWeight: 500 }}>
                {r.is_available ? `● ${t('available')}` : `○ ${t('unavailable')}`}
              </span>
            )},
            { key: 'exp',        label: 'Exp',           render: (r: any) => `${r.years_experience}y` },
          ]}
          data={filtered}
        />
      </Card>
    </div>
  );
}

/* ── Appointments Page ───────────────────────────────── */
export function AppointmentsPage() {
  const { t } = useTranslation();
  const [appts,   setAppts]   = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter,  setFilter]  = useState('all');

  const STATUSES = ['all', 'pending', 'confirmed', 'completed', 'cancelled'];

  useEffect(() => {
    appointmentAPI.list()
      .then((r) => setAppts(r.data))
      .finally(() => setLoading(false));
  }, []);

  const filtered = filter === 'all' ? appts : appts.filter((a) => a.status === filter);

  const stats = {
    total:     appts.length,
    pending:   appts.filter((a) => a.status === 'pending').length,
    confirmed: appts.filter((a) => a.status === 'confirmed').length,
    completed: appts.filter((a) => a.status === 'completed').length,
  };

  return (
    <div>
      <PageHeader title={`📅 ${t('appointments')}`} />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <StatCard icon="📋" label="Total"       value={stats.total}     color="var(--primary)"   delay={0}   />
        <StatCard icon="⏳" label={t('pending')} value={stats.pending}   color="var(--warning)"   delay={60}  />
        <StatCard icon="✅" label={t('confirmed')} value={stats.confirmed} color="var(--success)"  delay={120} />
        <StatCard icon="🏁" label={t('completed')} value={stats.completed} color="var(--secondary)" delay={180} />
      </div>

      <Card style={{ overflow: 'hidden' }}>
        <div style={{ padding: '12px 20px', borderBottom: '1px solid var(--border)', display: 'flex', gap: 8 }}>
          {STATUSES.map((s) => (
            <button key={s} onClick={() => setFilter(s)} style={{
              padding: '6px 14px', borderRadius: 8, border: 'none', cursor: 'pointer',
              background: filter === s ? 'var(--primary)' : 'transparent',
              color: filter === s ? '#fff' : 'var(--text-2)',
              fontSize: 13, fontWeight: filter === s ? 600 : 400, fontFamily: 'var(--font)',
              transition: 'all .15s',
            }}>
              {s === 'all' ? 'All' : t(s)}
            </button>
          ))}
        </div>
        <Table
          loading={loading}
          columns={[
            { key: 'patient',      label: t('patient'),  render: (r: any) => <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12 }}>#{r.patient_id.slice(0,8)}</span> },
            { key: 'scheduled_at', label: t('date'),     render: (r: any) => format(new Date(r.scheduled_at), 'dd MMM yyyy · HH:mm') },
            { key: 'type',         label: t('type'),     render: (r: any) => (
              <span style={{ background: r.type === 'video' ? 'var(--primary-light)' : 'var(--secondary-light)', color: r.type === 'video' ? 'var(--primary)' : 'var(--secondary)', padding: '2px 10px', borderRadius: 999, fontSize: 12 }}>
                {r.type === 'video' ? '📹' : '💬'} {t(r.type)}
              </span>
            )},
            { key: 'duration',    label: 'Duration', render: (r: any) => `${r.duration_minutes} min` },
            { key: 'status',      label: t('status'), render: (r: any) => <StatusBadge status={r.status} /> },
          ]}
          data={filtered}
        />
      </Card>
    </div>
  );
}

/* ── Doctor Schedule Page ────────────────────────────── */
export function DoctorSchedulePage() {
  const { t } = useTranslation();
  const [appts,   setAppts]   = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [noteModal, setNoteModal] = useState<any>(null);
  const [noteText,  setNoteText]  = useState('');
  const [newStatus, setNewStatus] = useState('completed');
  const [saving,    setSaving]    = useState(false);

  const fetch = () => {
    appointmentAPI.doctorSchedule()
      .then((r) => setAppts(r.data))
      .finally(() => setLoading(false));
  };
  useEffect(fetch, []);

  const handleSaveNote = async () => {
    setSaving(true);
    try {
      await appointmentAPI.updateNotes(noteModal.id, { notes_by_doctor: noteText, status: newStatus });
      setNoteModal(null);
      fetch();
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <PageHeader title={`📅 ${t('my_schedule')}`} subtitle={`${appts.length} upcoming appointments`} />

      {appts.length === 0 && !loading ? (
        <Card style={{ padding: 60, textAlign: 'center' }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>📭</div>
          <p style={{ color: 'var(--text-3)' }}>{t('no_data')}</p>
        </Card>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {appts.map((a, i) => (
            <Card key={a.id} style={{ padding: 20, animation: `fadeSlideIn .3s ease ${i * 40}ms both` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 16 }}>
                <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
                  <div style={{ width: 48, height: 48, borderRadius: 12, background: a.type === 'video' ? 'var(--primary-light)' : 'var(--secondary-light)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22, flexShrink: 0 }}>
                    {a.type === 'video' ? '📹' : '💬'}
                  </div>
                  <div>
                    <div style={{ fontWeight: 600, marginBottom: 4 }}>
                      {format(new Date(a.scheduled_at), 'EEEE, MMMM d · HH:mm')}
                    </div>
                    <div style={{ fontSize: 13, color: 'var(--text-3)', marginBottom: 6 }}>
                      {a.duration_minutes} min · {a.type === 'video' ? t('video_consultation') : t('chat_consultation')}
                    </div>
                    {a.notes_by_patient && (
                      <div style={{ fontSize: 13, color: 'var(--text-2)', background: 'var(--bg)', padding: '6px 10px', borderRadius: 6, maxWidth: 400 }}>
                        📝 {a.notes_by_patient}
                      </div>
                    )}
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexShrink: 0 }}>
                  <StatusBadge status={a.status} />
                  <Button variant="outline" size="sm" onClick={() => { setNoteModal(a); setNoteText(a.notes_by_doctor ?? ''); setNewStatus(a.status); }}>
                    {t('notes')}
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal open={!!noteModal} onClose={() => setNoteModal(null)} title={t('notes')}>
        <div style={{ marginBottom: 12, padding: '10px 14px', background: 'var(--bg)', borderRadius: 8, fontSize: 13, color: 'var(--text-2)' }}>
          📅 {noteModal && format(new Date(noteModal.scheduled_at), 'EEEE, MMMM d · HH:mm')}
        </div>
        <textarea
          value={noteText}
          onChange={(e) => setNoteText(e.target.value)}
          placeholder={t('notes')}
          rows={4}
          style={{ width: '100%', padding: '10px 12px', borderRadius: 8, border: '1.5px solid var(--border)', fontSize: 14, fontFamily: 'var(--font)', outline: 'none', resize: 'vertical', marginBottom: 12 }}
        />
        <Select
          label={t('update_status')}
          value={newStatus}
          onChange={(e) => setNewStatus(e.target.value)}
          options={[
            { value: 'pending',   label: t('pending')   },
            { value: 'confirmed', label: t('confirmed') },
            { value: 'completed', label: t('completed') },
            { value: 'cancelled', label: t('cancelled') },
          ]}
        />
        <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end', marginTop: 8 }}>
          <Button variant="outline" onClick={() => setNoteModal(null)}>{t('cancel')}</Button>
          <Button onClick={handleSaveNote} loading={saving}>{t('save')}</Button>
        </div>
      </Modal>
    </div>
  );
}

/* ── Medicines Page ──────────────────────────────────── */
export function MedicinesPage() {
  const { t, i18n } = useTranslation();
  const [medicines, setMedicines] = useState<any[]>([]);
  const [loading,   setLoading]   = useState(true);
  const [search,    setSearch]    = useState('');
  const [modal,     setModal]     = useState(false);
  const [form,      setForm]      = useState({ name_ar: '', name_tr: '', name_en: '', price: '', stock_quantity: '', category: '', requires_prescription: false });
  const [saving,    setSaving]    = useState(false);

  const fetch = () => pharmacyAPI.listMedicines().then((r) => setMedicines(r.data)).finally(() => setLoading(false));
  useEffect(fetch, []);

  const lang     = i18n.language;
  const filtered = medicines.filter((m) => {
    const name = m[`name_${lang}`] ?? m.name_ar ?? '';
    return !search || name.toLowerCase().includes(search.toLowerCase());
  });

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await pharmacyAPI.addMedicine({ ...form, price: parseFloat(form.price), stock_quantity: parseInt(form.stock_quantity) });
      setModal(false);
      fetch();
    } finally {
      setSaving(false);
    }
  };

  const upd = (k: string, v: any) => setForm((p) => ({ ...p, [k]: v }));

  return (
    <div>
      <PageHeader
        title={`💊 ${t('medicines')}`}
        subtitle={`${medicines.length} items`}
        action={<Button onClick={() => setModal(true)} icon="+">{t('add_medicine')}</Button>}
      />

      {/* Stock overview */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        <StatCard icon="💊" label="Total Items"   value={medicines.length}                                                    color="var(--primary)"  delay={0}  />
        <StatCard icon="⚠️" label="Low Stock"     value={medicines.filter((m) => m.stock_quantity < 20 && m.stock_quantity > 0).length} color="var(--warning)"  delay={60} />
        <StatCard icon="❌" label="Out of Stock"  value={medicines.filter((m) => m.stock_quantity === 0).length}              color="var(--danger)"   delay={120} />
      </div>

      <Card style={{ overflow: 'hidden' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ margin: 0 }}>{t('medicines')}</h3>
          <SearchBar value={search} onChange={setSearch} placeholder={t('search')} />
        </div>
        <Table
          loading={loading}
          columns={[
            { key: 'name', label: t('medicine_name'), render: (r: any) => (
              <div>
                <div style={{ fontWeight: 500 }}>{r[`name_${lang}`] ?? r.name_ar}</div>
                <div style={{ fontSize: 12, color: 'var(--text-3)' }}>{r.category ?? '—'}</div>
              </div>
            )},
            { key: 'price',  label: t('price'),  render: (r: any) => <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--primary)' }}>${r.price.toFixed(2)}</span> },
            { key: 'stock',  label: t('stock'),  render: (r: any) => (
              <span style={{
                padding: '2px 10px', borderRadius: 999, fontSize: 12, fontWeight: 500,
                background: r.stock_quantity === 0 ? 'var(--danger-light)' : r.stock_quantity < 20 ? 'var(--warning-light)' : 'var(--success-light)',
                color:      r.stock_quantity === 0 ? 'var(--danger)'      : r.stock_quantity < 20 ? 'var(--warning)'       : 'var(--success)',
              }}>
                {r.stock_quantity === 0 ? '✕ Out' : r.stock_quantity}
              </span>
            )},
            { key: 'rx', label: 'Rx', render: (r: any) => r.requires_prescription ? <span style={{ color: 'var(--warning)', fontWeight: 600 }}>Rx</span> : '—' },
          ]}
          data={filtered}
        />
      </Card>

      <Modal open={modal} onClose={() => setModal(false)} title={t('add_medicine')}>
        <form onSubmit={handleAdd}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12 }}>
            <Input label="اسم الدواء (AR)" value={form.name_ar} onChange={(e) => upd('name_ar', e.target.value)} required />
            <Input label="İlaç adı (TR)"  value={form.name_tr} onChange={(e) => upd('name_tr', e.target.value)} />
            <Input label="Name (EN)"       value={form.name_en} onChange={(e) => upd('name_en', e.target.value)} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12 }}>
            <Input label={t('price')}    type="number" step="0.01" value={form.price}          onChange={(e) => upd('price', e.target.value)} required />
            <Input label={t('stock')}    type="number" value={form.stock_quantity}              onChange={(e) => upd('stock_quantity', e.target.value)} required />
            <Input label={t('category')} value={form.category}                                  onChange={(e) => upd('category', e.target.value)} />
          </div>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 14, cursor: 'pointer', margin: '8px 0 20px' }}>
            <input type="checkbox" checked={form.requires_prescription} onChange={(e) => upd('requires_prescription', e.target.checked)} />
            {t('requires_prescription')}
          </label>
          <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
            <Button variant="outline" type="button" onClick={() => setModal(false)}>{t('cancel')}</Button>
            <Button type="submit" loading={saving}>{t('save')}</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}

/* ── Orders Page ─────────────────────────────────────── */
export function OrdersPage() {
  const { t } = useTranslation();
  const [orders,  setOrders]  = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter,  setFilter]  = useState('all');

  useEffect(() => {
    orderAPI.list()
      .then((r) => setOrders(r.data))
      .finally(() => setLoading(false));
  }, []);

  const STATUSES = ['all', 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'];
  const filtered = filter === 'all' ? orders : orders.filter((o) => o.status === filter);

  return (
    <div>
      <PageHeader title={`📦 ${t('orders')}`} subtitle={`${orders.length} total`} />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <StatCard icon="📦" label="Total"         value={orders.length}                                            color="var(--primary)"   delay={0}   />
        <StatCard icon="⏳" label={t('pending')}   value={orders.filter((o) => o.status === 'pending').length}    color="var(--warning)"   delay={60}  />
        <StatCard icon="🚚" label={t('shipped')}   value={orders.filter((o) => o.status === 'shipped').length}    color="var(--info)"      delay={120} />
        <StatCard icon="✅" label={t('delivered')} value={orders.filter((o) => o.status === 'delivered').length}  color="var(--success)"   delay={180} />
      </div>

      <Card style={{ overflow: 'hidden' }}>
        <div style={{ padding: '12px 20px', borderBottom: '1px solid var(--border)', display: 'flex', gap: 8 }}>
          {STATUSES.map((s) => (
            <button key={s} onClick={() => setFilter(s)} style={{
              padding: '6px 14px', borderRadius: 8, border: 'none', cursor: 'pointer',
              background: filter === s ? 'var(--primary)' : 'transparent',
              color: filter === s ? '#fff' : 'var(--text-2)',
              fontSize: 13, fontWeight: filter === s ? 600 : 400, fontFamily: 'var(--font)', transition: 'all .15s',
            }}>
              {s === 'all' ? 'All' : t(s)}
            </button>
          ))}
        </div>
        <Table
          loading={loading}
          columns={[
            { key: 'id',         label: 'Order ID',   render: (r: any) => <span style={{ fontFamily: 'var(--font-mono)', fontSize: 12 }}>#{r.id.slice(0,8)}</span> },
            { key: 'created_at', label: t('date'),    render: (r: any) => format(new Date(r.created_at), 'dd MMM yyyy · HH:mm') },
            { key: 'items',      label: 'Items',      render: (r: any) => `${r.items?.length ?? 0} items` },
            { key: 'total_price',label: t('price'),   render: (r: any) => <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--primary)' }}>${r.total_price.toFixed(2)}</span> },
            { key: 'status',     label: t('status'),  render: (r: any) => <StatusBadge status={r.status} /> },
          ]}
          data={filtered}
        />
      </Card>
    </div>
  );
}
