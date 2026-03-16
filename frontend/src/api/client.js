const API_BASE_URL = import.meta.env.VITE_API_URL ?? '';

const defaultHeaders = {
  'Content-Type': 'application/json',
};

const normalizeUrl = (path) => {
  if (path.startsWith('http')) return path;

  if (API_BASE_URL) {
    const trimmedBase = API_BASE_URL.replace(/\/+$/u, '');
    const trimmedPath = path.replace(/^\/+/, '');
    return `${trimmedBase}/${trimmedPath}`;
  }




  const relativePath = path.startsWith('/') ? path : `/${path}`;
  const origin = typeof globalThis !== 'undefined' && globalThis.location ? globalThis.location.origin : 'http://localhost';
  return `${origin}${relativePath}`;
};

const buildUrl = (path, params) => {

  const normalized = normalizeUrl(path);
  const url = new URL(normalized);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value === undefined || value === null || value === '') return;
      url.searchParams.set(key, String(value));
    });
  }

  return url.toString();
};

const parseResponse = async (response) => {
  const text = await response.text().catch(() => '');
  if (!text) return null;

  try {
    return JSON.parse(text);
  } catch (error) {
    return text;
  }
};

const request = async (path, options = {}) => {
  const { body, headers, params, ...rest } = options;
  const config = {
    ...rest,
    headers: {
      ...defaultHeaders,
      ...headers,
    },
  };

  if (body !== undefined) {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(buildUrl(path, params), config);
  const payload = await parseResponse(response);

  if (!response.ok) {
    const errorMessage = payload?.message || payload || 'Request failed';
    throw new Error(errorMessage);
  }

  return payload;
};

export default request;
