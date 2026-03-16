import request from './client';

const basePath = '/prompts';

export const getPrompts = (filters = {}) => request(basePath, { params: filters });
export const getPrompt = (id) => request(`${basePath}/${id}`);
export const createPrompt = (data) => request(basePath, { method: 'POST', body: data });
export const updatePrompt = (id, data) => request(`${basePath}/${id}`, { method: 'PUT', body: data });
export const deletePrompt = (id) => request(`${basePath}/${id}`, { method: 'DELETE' });
