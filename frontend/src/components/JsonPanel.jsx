import EndpointTag from './EndpointTag'

const TOKEN = /("(?:\\.|[^"\\])*")(\s*:)?|\b(true|false|null)\b|(-?\d+(?:\.\d+)?)/g

/** Resalta un JSON formateado como elementos React (sin innerHTML). */
function highlight(json) {
  const out = []
  let last = 0
  for (const m of json.matchAll(TOKEN)) {
    if (m.index > last) out.push(json.slice(last, m.index))
    const [full, str, colon, literal, num] = m
    let cls = 'num'
    if (str) cls = colon ? 'key' : 'str'
    else if (literal) cls = 'lit'
    else if (num) cls = 'num'
    out.push(
      <span key={m.index} className={`tok-${cls}`}>
        {colon ? str : full}
      </span>,
    )
    if (colon) out.push(colon)
    last = m.index + full.length
  }
  out.push(json.slice(last))
  return out
}

export default function JsonPanel({ api, data }) {
  const json = JSON.stringify(data, null, 2)
  return (
    <figure className="json-panel">
      <figcaption className="json-panel__bar">
        <span className="json-panel__dots" aria-hidden="true">
          <i /> <i /> <i />
        </span>
        <EndpointTag api={api} />
      </figcaption>
      <pre className="json-panel__code">
        <code>{highlight(json)}</code>
      </pre>
    </figure>
  )
}
