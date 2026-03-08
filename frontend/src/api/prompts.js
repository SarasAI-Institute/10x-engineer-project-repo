import { api } from './client';

/**
 * Fetches a paginated/filtered list of prompts from the API.
 *
 * Supports optional filtering by collection and a full-text search term.
 * Only defined params are appended to the query string.
 *
 * @param {Object} [params={}] - Optional filter parameters.
 * @param {string} [params.collection_id] - Filter prompts to this collection ID.
 * @param {string} [params.search] - Full-text search query string.
 * @returns {Promise<{prompts: Array<Object>}>} Object containing a `prompts` array.
 *
 * @example
 * // Fetch all prompts
 * const { prompts } = await getPrompts();
 *
 * @example
 * // Fetch prompts in a specific collection matching a search term
 * const { prompts } = await getPrompts({ collection_id: 'abc123', search: 'code review' });
 */
export const getPrompts = (params = {}) => {
  const query = new URLSearchParams();
  if (params.collection_id) query.set('collection_id', params.collection_id);
  if (params.search) query.set('search', params.search);
  const qs = query.toString();
  return api.get(`/prompts${qs ? `?${qs}` : ''}`);
};

/**
 * Fetches a single prompt by its ID.
 *
 * @param {string} id - The unique identifier of the prompt.
 * @returns {Promise<Object>} The prompt object.
 *
 * @example
 * const prompt = await getPrompt('abc123');
 */
export const getPrompt = (id) => api.get(`/prompts/${id}`);

/**
 * Creates a new prompt.
 *
 * @param {Object} data - Prompt payload.
 * @param {string} data.title - The prompt title (required).
 * @param {string} data.content - The prompt body text (required).
 * @param {string|null} [data.description] - Optional short description.
 * @param {string|null} [data.collection_id] - Optional collection to assign the prompt to.
 * @returns {Promise<Object>} The newly created prompt object.
 *
 * @example
 * const prompt = await createPrompt({
 *   title: 'Code Review Assistant',
 *   content: 'You are a senior engineer...',
 *   collection_id: 'abc123',
 * });
 */
export const createPrompt = (data) => api.post('/prompts', data);

/**
 * Updates an existing prompt by ID.
 *
 * @param {string} id - The unique identifier of the prompt to update.
 * @param {Object} data - Fields to update on the prompt.
 * @param {string} [data.title] - New title.
 * @param {string} [data.content] - New content body.
 * @param {string|null} [data.description] - New description.
 * @param {string|null} [data.collection_id] - New collection assignment.
 * @returns {Promise<Object>} The updated prompt object.
 *
 * @example
 * const updated = await updatePrompt('abc123', { title: 'Revised Title' });
 */
export const updatePrompt = (id, data) => api.put(`/prompts/${id}`, data);

/**
 * Deletes a prompt by ID.
 *
 * @param {string} id - The unique identifier of the prompt to delete.
 * @returns {Promise<null>} Resolves to null on successful deletion (204 No Content).
 *
 * @example
 * await deletePrompt('abc123');
 */
export const deletePrompt = (id) => api.delete(`/prompts/${id}`);
