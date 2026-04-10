import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';
import { doctorAPI, appointmentAPI, orderAPI } from '../services/api';
import { useStore } from '../store';
import { StatCard, Card, PageHeader, StatusBadge, Table, Spinner } from '../components/ui';
import { format } from 'date-fns';

/* ── Mock chart data ─────────────────────────── */
const AREA_DATA = [
  { name: 'Mon', appointments: 12, orders: 8 },
  { name: 'Tue', appointments: 19, orders: 14 },
  { name: 'Wed', appointments: 15, orders: 11 },
  { name: 'Thu', appointments: 24, orders: 18 },
  { name: 'Fri', appointments: 21, orders: 16 },
  { name: 'Sat', appointments: 9,  orders: 6  },
  { name: 'Sun', appointments: 7,  orders: 4  },
];
const SPECIALTY_DATA = [
  { name: 'General',     value: 32, color: '#4ECDC4' },
  { name: 'Cardiology',  value: 20, color: '#FF6B6B' },
  { name: 'Dermatology', value: 15, color: '#FFE66D' },
  { name: 'Neurology',   value: 12, color: '#A8E6CF' },
  { name: 'Other',       value: 21, color: '#C3B1E1' },
];

export default function DashboardPage() {
  const { t } = useTranslation();
  const { user } = useStore();
  const [doctors,      setDoctors]      = useState<any[]>([]);
  const [appointments, setAppointments] = useState<any[]>([]);
  const [orders,       setOrders]       = useState<any[]>([]);
  const [loading,      setLoading]      = useState(true);

  useEffect(() => {
    Promise.all([
      doctorAPI.list({ available_only: false }),
      appointmentAPI.list(),
      orderAPI.list(),
    ]).then(([d, a, o]) => {
      setDoctors(d.data);
      setAppointments(a.data);
      setOrders(o.data);
    }).finally(() => setLoading(false));
  }, []);

  const pendingOrders = orders.filter((o) => o.status === 'pending').length;
  const todayAppts = appointments.filter((a) => {
    const d = new Date(a.scheduled_at);
    const n = new Date();
    return d.getDate() === n.getDate() && d.getMonth() === n.getMonth();
  }).length;

  if (loading) return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: 80 }}><Spinner size="lg" /></div>
  );

  return (
    <div style={{ animation: 'fadeSlideIn .3s ease' }}>
      <PageHeader
        title={`${t('welcome_back')}, ${user?.full_name?.split(' ')[0]} 👋`}
        subtitle={format(new Date(), 'EEEE, MMMM d yyyy')}
      />

      {/* Stat cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 28 }}>
        <StatCard icon="👨‍⚕️" label={t('total_doctors')}      value={doctors.length}      trend={8}  color="var(--primary)"   delay={0} />
        <StatCard icon="📅" label={t('today_appointments')}   value={todayAppts}          trend={12} color="var(--secondary)"  delay={60} />
        <StatCard icon="📦" label={t('pending_orders')}       value={pendingOrders}       trend={-3} color="var(--warning)"    delay={120} />
        <StatCard icon="📋" label={t('total_appointments')}   value={appointments.length} trend={5}  color="var(--info)"       delay={180} />
      </div>

      {/* Charts row */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20, marginBottom: 28 }}>

        {/* Area chart */}
        <Card style={{ padding: 20 }}>
          <h3 style={{ margin: '0 0 20px', fontSize: 15, color: 'var(--text-1)' }}>
            📈 {t('appointments')} & {t('orders')}
          </h3>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={AREA_DATA}>
              <defs>
                <linearGradient id="gradA" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="var(--primary)"   stopOpacity={0.3} />
                  <stop offset="95%" stopColor="var(--primary)"   stopOpacity={0}   />
                </linearGradient>
                <linearGradient id="gradO" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="var(--secondary)" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="var(--secondary)" stopOpacity={0}   />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="name" tick={{ fontSize: 12, fill: 'var(--text-3)' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 12, fill: 'var(--text-3)' }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ borderRadius: 8, border: '1px solid var(--border)', fontSize: 13 }} />
              <Area type="monotone" dataKey="appointments" stroke="var(--primary)"   strokeWidth={2} fill="url(#gradA)" name={t('appointments')} />
              <Area type="monotone" dataKey="orders"       stroke="var(--secondary)" strokeWidth={2} fill="url(#gradO)" name={t('orders')} />
            </AreaChart>
          </ResponsiveContainer>
        </Card>

        {/* Pie chart */}
        <Card style={{ padding: 20 }}>
          <h3 style={{ margin: '0 0 16px', fontSize: 15 }}>🩺 {t('specialty')}</h3>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie data={SPECIALTY_DATA} cx="50%" cy="50%" innerRadius={40} outerRadius={70} paddingAngle={3} dataKey="value">
                {SPECIALTY_DATA.map((entry, i) => <Cell key={i} fill={entry.color} />)}
              </Pie>
              <Tooltip formatter={(v, n) => [v, n]} contentStyle={{ borderRadius: 8, fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 8 }}>
            {SPECIALTY_DATA.map((s) => (
              <div key={s.name} style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 11, color: 'var(--text-2)' }}>
                <div style={{ width: 8, height: 8, borderRadius: '50%', background: s.color }} />
                {s.name} {s.value}%
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Recent appointments table */}
      <Card style={{ overflow: 'hidden' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ margin: 0 }}>📅 {t('appointments')}</h3>
        </div>
        <Table
          columns={[
            { key: 'patient',      label: t('patient'),  render: (r: any) => <span style={{ fontWeight: 500 }}>#{r.patient_id.slice(0,8)}</span> },
            { key: 'scheduled_at', label: t('date'),     render: (r: any) => format(new Date(r.scheduled_at), 'dd MMM · HH:mm') },
            { key: 'type',         label: t('type'),     render: (r: any) => <span>{r.type === 'video' ? '📹' : '💬'} {t(r.type)}</span> },
            { key: 'status',       label: t('status'),   render: (r: any) => <StatusBadge status={r.status} /> },
          ]}
          data={appointments.slice(0, 8)}
        />
      </Card>
    </div>
  );
}
