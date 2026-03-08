const BASE_URL = '/api';

/**
 * Makes an HTTP request to the backend API and returns the parsed JSON response.
 *
 * Automatically sets the Content-Type header to application/json, throws a
 * human-readable error when the server is unreachable, and surfaces the
 * `detail` field from error response bodies.
 *
 * @param {string} path - The API path to request (e.g. '/prompts').
 * @param {RequestInit} [options={}] - Fetch options to merge (method, body, headers, etc.).
 * @returns {Promise<Object|null>} Parsed JSON response body, or null for 204 No Content.
 * @throws {Error} When the server cannot be reached or returns a non-2xx status.
 *
 * @example
 * // GET request
 * const data = await request('/prompts');
 *
 * @example
 * // POST request with body
 * const created = await request('/prompts', {
 *   method: 'POST',
 *   body: JSON.stringify({ title: 'My Prompt', content: 'You are...' }),
 * });
 */
async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  let res;
  try {
    res = await fetch(url, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options,
    });
  } catch {
    throw new Error('Cannot reach the server. Is the backend running?');
  }

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const data = await res.json();
      detail = data.detail || detail;
    } catch {}
    throw new Error(detail);
  }

  if (res.status === 204) return null;
  return res.json();
}

/**
 * Thin HTTP client wrapping the `request` helper with named methods for each
 * HTTP verb. All methods prepend `BASE_URL` to the given path.
 *
 * @namespace api
 *
 * @example
 * // GET
 * const prompts = await api.get('/prompts');
 *
 * @example
 * // POST
 * const prompt = await api.post('/prompts', { title: 'Test', content: '...' });
 *
 * @example
 * // PUT
 * const updated = await api.put('/prompts/1', { title: 'Updated' });
 *
 * @example
 * // PATCH
 * const patched = await api.patch('/prompts/1', { title: 'Patched' });
 *
 * @example
 * // DELETE
 * await api.delete('/prompts/1');
 */
export const api = {
  /**
   * Sends a GET request to the given API path.
   *
   * @param {string} path - The API path (e.g. '/prompts').
   * @returns {Promise<Object|null>} Parsed JSON response.
   */
  get: (path) => request(path),

  /**
   * Sends a POST request with a JSON-serialised body.
   *
   * @param {string} path - The API path.
   * @param {Object} body - Data to serialise as the request body.
   * @returns {Promise<Object|null>} Parsed JSON response.
   */
  post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) }),

  /**
   * Sends a PUT request with a JSON-serialised body.
   *
   * @param {string} path - The API path.
   * @param {Object} body - Data to serialise as the request body.
   * @returns {Promise<Object|null>} Parsed JSON response.
   */
  put: (path, body) => request(path, { method: 'PUT', body: JSON.stringify(body) }),

  /**
   * Sends a PATCH request with a JSON-serialised body.
   *
   * @param {string} path - The API path.
   * @param {Object} body - Data to serialise as the request body.
   * @returns {Promise<Object|null>} Parsed JSON response.
   */
  patch: (path, body) => request(path, { method: 'PATCH', body: JSON.stringify(body) }),

  /**
   * Sends a DELETE request to the given API path.
   *
   * @param {string} path - The API path.
   * @returns {Promise<Object|null>} Parsed JSON response, or null for 204.
   */
  delete: (path) => request(path, { method: 'DELETE' }),
};
