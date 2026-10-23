import { useEffect, useRef } from 'react'
import { useLanguage } from '../i18n/context'

/** Muestra el archivo de una certificación en un <dialog> modal (Esc o clic afuera para cerrar). */
export default function CertificateModal({ cert, onClose }) {
  const { lang, t } = useLanguage()
  const dialog = useRef(null)

  useEffect(() => {
    const el = dialog.current
    if (!cert || !el) return
    el.showModal()
    document.documentElement.classList.add('no-scroll')
    return () => {
      document.documentElement.classList.remove('no-scroll')
      if (el.open) el.close()
    }
  }, [cert])

  if (!cert) return null

  const isPdf = cert.file.toLowerCase().endsWith('.pdf')
  const issued = new Intl.DateTimeFormat(lang, { month: 'short', year: 'numeric' })
    .format(new Date(`${cert.issued}T00:00`))

  return (
    <dialog
      ref={dialog}
      className="cert-modal"
      aria-labelledby="cert-modal-title"
      onClose={onClose}
      // Un clic en el fondo (fuera del contenido) llega al propio <dialog>.
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="cert-modal__inner">
        <header className="cert-modal__head">
          <div>
            <h3 id="cert-modal-title">{cert.name}</h3>
            <p>{cert.issuer} · {issued}</p>
          </div>
          <div className="cert-modal__actions">
            <a href={cert.file} download className="cert-modal__download">{t.education.download}</a>
            <button className="cert-modal__close" onClick={onClose} aria-label={t.education.close}>
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" /></svg>
            </button>
          </div>
        </header>
        <div className="cert-modal__body">
          {isPdf ? (
            <iframe src={cert.file} title={cert.name} />
          ) : (
            <img src={cert.file} alt={cert.name} />
          )}
        </div>
      </div>
    </dialog>
  )
}
