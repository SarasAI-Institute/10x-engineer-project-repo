import { api } from './client';

export const getPrompts = (params = {}) => {
  const query = new URLSearchParams();
  if (params.collection_id) query.set('collection_id', params.collection_id);
  if (params.search) query.set('search', params.search);
  const qs = query.toString();
  return api.get(`/prompts${qs ? `?${qs}` : ''}`);
};

export const getPrompt = (id) => api.get(`/prompts/${id}`);

export const createPrompt = (data) => api.post('/prompts', data);

export const updatePrompt = (id, data) => api.put(`/prompts/${id}`, data);

export const deletePrompt = (id) => api.delete(`/prompts/${id}`);
