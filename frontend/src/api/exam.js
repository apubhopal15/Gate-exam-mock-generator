import api from "./axios.js";

export const generateMock = async (examType) => {
  const res = await api.post(`/mock/generate?exam_type=${examType}`);
  return res.data;
};

export const getMock = async (mockId) => {
  const res = await api.get(`/mocks/${mockId}`);
  return res.data;
};
