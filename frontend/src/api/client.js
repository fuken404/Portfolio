const BASE = import.meta.env.VITE_API_URL ?? '/api'

/** Django elige el idioma de la respuesta con el encabezado Accept-Language. */
export async function request(path, { method = 'GET', body, lang, signal } = {}) {
  const headers = {}
  if (body) headers['Content-Type'] = 'application/json'
  if (lang) headers['Accept-Language'] = lang

  const started = performance.now()
  const res = await fetch(`${BASE}${path}`, {
    method,
    signal,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })
  const ms = Math.round(performance.now() - started)
  const data = await res.json().catch(() => null)
  return { ok: res.ok, code: res.status, ms, data }
}
