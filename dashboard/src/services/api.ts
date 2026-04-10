import axios from 'axios';

const api = axios.create({
baseURL: 'http://localhost:8000/api/v1',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  const lang  = localStorage.getItem('dashboard_lang') ?? 'ar';
  if (token) config.headers.Authorization = `Bearer ${token}`;
  config.headers['Accept-Language'] = lang;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  async (err) => {
    if (err.response?.status === 401) {
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) {
        try {
          const r = await axios.post('/api/v1/auth/refresh', { refresh_token: refresh });
          localStorage.setItem('access_token',  r.data.access_token);
          localStorage.setItem('refresh_token', r.data.refresh_token);
          err.config.headers.Authorization = `Bearer ${r.data.access_token}`;
          return api(err.config);
        } catch {
          localStorage.clear();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(err);
  }
);

export const authAPI = {
  login:  (d: any) => api.post('/auth/login', d),
  logout: ()       => api.post('/auth/logout'),
  me:     ()       => api.get('/users/me'),
};
export const doctorAPI = {
  list:          (p?: any) => api.get('/doctors', { params: p }),
  get:           (id: string) => api.get(`/doctors/${id}`),
  createProfile: (d: any)  => api.post('/doctors/profile', d),
  updateProfile: (d: any)  => api.put('/doctors/profile', d),
};
export const appointmentAPI = {
  list:          () => api.get('/appointments'),
  doctorSchedule:() => api.get('/appointments/doctor/schedule'),
  updateNotes:   (id: string, d: any) => api.put(`/appointments/${id}/doctor-notes`, d),
  cancel:        (id: string) => api.delete(`/appointments/${id}`),
};
export const pharmacyAPI = {
  listMedicines:  (p?: any) => api.get('/pharmacy/medicines', { params: p }),
  addMedicine:    (d: any)  => api.post('/pharmacy/medicines', d),
  updateMedicine: (id: string, d: any) => api.put(`/pharmacy/medicines/${id}`, d),
};
export const orderAPI = {
  list:   () => api.get('/orders'),
};

export default api;
