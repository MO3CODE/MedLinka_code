import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useStore } from './store';
import { Shell } from './components/layout';
import LoginPage     from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import {
  DoctorsPage, AppointmentsPage, DoctorSchedulePage,
  MedicinesPage, OrdersPage,
} from './pages/FeaturePages';

/* ── Protected route ─────────────────────────────── */
function Protected({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useStore((s) => s.isAuthenticated);
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}

/* ── Dashboard home per role ─────────────────────── */
function RoleHome() {
  const user = useStore((s) => s.user);
  if (user?.role === 'doctor')   return <DoctorSchedulePage />;
  if (user?.role === 'pharmacy') return <MedicinesPage />;
  return <DashboardPage />;
}

export default function App() {
  const loadFromStorage = useStore((s) => s.loadFromStorage);
  useEffect(() => { loadFromStorage(); }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/*" element={
          <Protected>
            <Shell>
              <Routes>
                <Route path="/"            element={<RoleHome />} />
                <Route path="/doctors"     element={<DoctorsPage />} />
                <Route path="/appointments"element={<AppointmentsPage />} />
                <Route path="/schedule"    element={<DoctorSchedulePage />} />
                <Route path="/medicines"   element={<MedicinesPage />} />
                <Route path="/pharmacy"    element={<MedicinesPage />} />
                <Route path="/orders"      element={<OrdersPage />} />
                <Route path="/analytics"   element={<DashboardPage />} />
                <Route path="*"            element={<Navigate to="/" replace />} />
              </Routes>
            </Shell>
          </Protected>
        } />
      </Routes>
    </BrowserRouter>
  );
}
