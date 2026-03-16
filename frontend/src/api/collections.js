import request from './client';

const basePath = '/collections';

export const getCollections = () => request(basePath);
export const createCollection = (data) => request(basePath, { method: 'POST', body: data });
export const deleteCollection = (id) => request(`${basePath}/${id}`, { method: 'DELETE' });
