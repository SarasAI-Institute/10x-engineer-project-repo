import { api } from './client';

/**
 * Fetches all collections from the API.
 *
 * @returns {Promise<{collections: Array<Object>}>} Object containing a `collections` array.
 *
 * @example
 * const { collections } = await getCollections();
 */
export const getCollections = () => api.get('/collections');

/**
 * Creates a new collection.
 *
 * @param {Object} data - Collection payload.
 * @param {string} data.name - The collection name (required).
 * @param {string|null} [data.description] - Optional description of the collection.
 * @returns {Promise<Object>} The newly created collection object.
 *
 * @example
 * const collection = await createCollection({
 *   name: 'Marketing Prompts',
 *   description: 'Prompts for marketing copy',
 * });
 */
export const createCollection = (data) => api.post('/collections', data);

/**
 * Deletes a collection by ID.
 *
 * Prompts belonging to the deleted collection are NOT deleted — they become
 * uncategorised.
 *
 * @param {string} id - The unique identifier of the collection to delete.
 * @returns {Promise<null>} Resolves to null on successful deletion (204 No Content).
 *
 * @example
 * await deleteCollection('abc123');
 */
export const deleteCollection = (id) => api.delete(`/collections/${id}`);
