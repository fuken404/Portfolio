import { useLanguage } from '../i18n/context'

/** Etiqueta que muestra de qué endpoint de Django sale el contenido. */
export default function EndpointTag({ api, method = 'GET' }) {
  const { t } = useLanguage()
  const { status, code, ms, path } = api
  return (
    <span className={`endpoint endpoint--${status}`}>
      <span className="endpoint__method">{method}</span>
      <span className="endpoint__path">/api{path}</span>
      <span className="endpoint__status">
        {status === 'loading' && t.endpoint.loading}
        {status === 'ok' && `${code} · ${ms}ms`}
        {status === 'offline' && t.endpoint.offline}
      </span>
    </span>
  )
}
