import api from "./axios";

export const startAttempt = async (mockId) => {
  const res = await api.post(`/attempts/${mockId}/start`);
  return res.data;
};

export const saveAnswer = async (attemptId, data) => {
  const res = await api.post(`/attempts/${attemptId}/answer`, data);
  return res.data;
};

export const submitAttempt = async (attemptId) => {
  const res = await api.post(`/attempts/${attemptId}/submit`);
  return res.data;
};

export const getResult = async (attemptId) => {
  const res = await api.get(`/attempts/${attemptId}/result`);
  return res.data;
};

export const getAnalytics = async (attemptId) => {
  const res = await api.get(`/attempts/${attemptId}/analytics`);
  return res.data;
};

export const getDashboard = async () => {
  const res = await api.get("/users/me/dashboard");
  return res.data;
};

export const getHistory = async (page = 1, size = 10) => {
  const res = await api.get(`/users/me/attempts?page=${page}&size=${size}`);
  return res.data;
};
