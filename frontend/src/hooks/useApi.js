import { useEffect, useState } from 'react'
import { request } from '../api/client'

/**
 * Lee un endpoint de Django en el idioma `lang`. Mientras carga la primera vez
 * (o si falla) devuelve `fallback`, así la maqueta siempre tiene contenido.
 * Al cambiar de idioma conserva los datos anteriores hasta que llegan los nuevos.
 * status: 'loading' | 'ok' | 'offline'
 */
export function useApi(path, fallback, lang) {
  const [state, setState] = useState({ data: fallback, status: 'loading', code: null, ms: null })

  useEffect(() => {
    const controller = new AbortController()
    setState((s) => ({ ...s, status: 'loading' }))
    request(path, { lang, signal: controller.signal })
      .then(({ ok, code, ms, data }) => {
        if (!ok) throw new Error(code)
        setState({ data, status: 'ok', code, ms })
      })
      .catch((err) => {
        if (err.name === 'AbortError') return
        setState({ data: fallback, status: 'offline', code: null, ms: null })
      })
    return () => controller.abort()
  }, [path, lang, fallback])

  return { ...state, path }
}
