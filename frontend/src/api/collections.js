import { api } from './client';

export const getCollections = () => api.get('/collections');

export const createCollection = (data) => api.post('/collections', data);

export const deleteCollection = (id) => api.delete(`/collections/${id}`);
