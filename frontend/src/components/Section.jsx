import EndpointTag from './EndpointTag'

/** `api` puede ser un endpoint o una lista, si la sección combina varios. */
export default function Section({ id, index, title, api, children }) {
  const apis = api ? [].concat(api) : []
  return (
    <section id={id} className="section" aria-labelledby={`${id}-title`}>
      <header className="section__head">
        <span className="section__index">{String(index).padStart(2, '0')}</span>
        <h2 id={`${id}-title`} className="section__title">{title}</h2>
        {apis.length > 0 && (
          <span className="section__endpoints">
            {apis.map((a) => <EndpointTag key={a.path} api={a} />)}
          </span>
        )}
      </header>
      <div className="section__body">{children}</div>
    </section>
  )
}
