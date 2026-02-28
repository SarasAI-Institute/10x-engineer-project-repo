const BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

async function request(path, options = {}){
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  })
  if (!res.ok){
    const text = await res.text()
    throw new Error(`${res.status} ${res.statusText}: ${text}`)
  }
  if (res.status === 204) return null
  return res.json()
}

export async function fetchPrompts(query = ''){
  const q = query ? `?search=${encodeURIComponent(query)}` : ''
  return request(`/prompts${q}`)
}

export async function createPrompt(payload){
  return request('/prompts', { method: 'POST', body: JSON.stringify(payload) })
}

export async function updatePrompt(id, payload){
  return request(`/prompts/${id}`, { method: 'PUT', body: JSON.stringify(payload) })
}

export async function patchPrompt(id, payload){
  return request(`/prompts/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
}

export async function deletePrompt(id){
  return request(`/prompts/${id}`, { method: 'DELETE' })
}

export async function fetchCollections(){
  return request('/collections')
}

export async function createCollection(payload){
  return request('/collections', { method: 'POST', body: JSON.stringify(payload) })
}

export async function deleteCollection(id){
  return request(`/collections/${id}`, { method: 'DELETE' })
}
