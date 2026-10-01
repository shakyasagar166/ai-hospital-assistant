import api from './client';

export const authLogin = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  return response.data;
};

export const authRegister = async (userData) => {
  const response = await api.post('/auth/register', userData);
  return response.data;
};

export const getMe = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const getDepartments = async (params = {}) => {
  const response = await api.get('/departments', { params });
  return response.data;
};

export const getDepartmentById = async (id) => {
  const response = await api.get(`/departments/${id}`);
  return response.data;
};

export const getDoctors = async (params = {}) => {
  const response = await api.get('/doctors', { params });
  return response.data;
};

export const getLabTests = async (params = {}) => {
  const response = await api.get('/lab-tests', { params });
  return response.data;
};

export const bookAppointment = async (appointmentData) => {
  const response = await api.post('/appointments', appointmentData);
  return response.data;
};

export const getMyAppointments = async () => {
  const response = await api.get('/appointments');
  return response.data;
};

export const cancelAppointment = async (appointmentId) => {
  const response = await api.delete(`/appointments/${appointmentId}`);
  return response.data;
};

export const sendClinicalChat = async (message, conversation_id = null) => {
  const response = await api.post('/chat', { message, conversation_id });
  return response.data;
};
