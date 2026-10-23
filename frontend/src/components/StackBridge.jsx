import { useLanguage } from '../i18n/context'

/** Diagrama de cómo está hecho este mismo sitio: Django sirve JSON, React lo pinta. */
export default function StackBridge() {
  const { t } = useLanguage()
  return (
    <div className="bridge" aria-label={t.bridge.label}>
      <div className="bridge__node">
        <span className="bridge__label">Backend</span>
        <strong>Django</strong>
        <span className="bridge__sub">{t.bridge.backendSub}</span>
      </div>
      <div className="bridge__wire" aria-hidden="true">
        <span className="bridge__packet" />
        <span className="bridge__packet bridge__packet--late" />
        <span className="bridge__wire-label">JSON</span>
      </div>
      <div className="bridge__node">
        <span className="bridge__label">Frontend</span>
        <strong>React</strong>
        <span className="bridge__sub">{t.bridge.frontendSub}</span>
      </div>
      <p className="bridge__note">{t.bridge.note}</p>
    </div>
  )
}
