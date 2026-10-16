const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

function apiUrl(path) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE_URL}${normalizedPath}`
}

function friendlyMessage(payload, fallback) {
  if (typeof payload?.detail === 'string') return payload.detail
  if (Array.isArray(payload?.detail)) {
    return payload.detail
      .map((item) => item.msg?.replace(/^Value error, /, '') ?? 'Invalid value')
      .join('. ')
  }
  return fallback
}

async function request(path, options = {}) {
  let response
  try {
    response = await fetch(apiUrl(path), {
      ...options,
      headers: {
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
    })
  } catch {
    throw new ApiError('IncidentOps API is unavailable. Confirm the backend is running.', 0)
  }

  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    throw new ApiError(
      friendlyMessage(payload, 'The request could not be completed. Please try again.'),
      response.status,
    )
  }

  return response.status === 204 ? null : response.json()
}

function queryString(filters) {
  const params = new URLSearchParams()
  Object.entries(filters).forEach(([key, value]) => {
    if (value) params.set(key, value)
  })
  const query = params.toString()
  return query ? `?${query}` : ''
}

export const servicesApi = {
  list: () => request('/services'),
  create: (payload) => request('/services', { method: 'POST', body: JSON.stringify(payload) }),
  update: (id, payload) => request(`/services/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  remove: (id) => request(`/services/${id}`, { method: 'DELETE' }),
}

export const incidentsApi = {
  list: (filters = {}) => request(`/incidents${queryString(filters)}`),
  stats: () => request('/incidents/stats'),
  create: (payload) => request('/incidents', { method: 'POST', body: JSON.stringify(payload) }),
  update: (id, payload) => request(`/incidents/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  remove: (id) => request(`/incidents/${id}`, { method: 'DELETE' }),
}

export { API_BASE_URL }
