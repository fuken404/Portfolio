import { useState } from 'react'
import { useLanguage } from '../i18n/context'
import CertificateModal from './CertificateModal'
import Section from './Section'

const CATEGORIES = ['development', 'security', 'agile', 'infra']

export default function Education({ educationApi, certificationsApi, index }) {
  const { lang, t } = useLanguage()
  const [viewing, setViewing] = useState(null)
  const monthYear = new Intl.DateTimeFormat(lang, { month: 'short', year: 'numeric' })
  const year = (iso) => iso.slice(0, 4)

  return (
    <Section
      id="formacion"
      index={index}
      title={t.sections.education}
      api={[educationApi, certificationsApi]}
    >
      <div className="education">
        <div className="education__degrees">
          <h3 className="education__label">{t.education.degrees}</h3>
          <ol>
            {educationApi.data.map((e) => (
              <li key={e.id}>
                <span className="education__years">
                  {year(e.start)} — {e.end ? year(e.end) : t.experience.present}
                </span>
                <strong>{e.degree}</strong>
                <span className="education__school">
                  {e.institution}
                  {e.location && ` · ${e.location}`}
                </span>
              </li>
            ))}
          </ol>
        </div>

        <div className="education__certs">
          <h3 className="education__label">{t.education.certifications}</h3>
          {CATEGORIES.map((key) => {
            const items = certificationsApi.data.filter((c) => c.category === key)
            if (!items.length) return null
            return (
              <div key={key} className="certs">
                <h4 className="certs__cat">{t.education.categories[key]}</h4>
                <ul>
                  {items.map((c) => (
                    <li key={c.id} className="cert">
                      {c.file ? (
                        <button
                          type="button"
                          className="cert__name cert__name--link"
                          aria-haspopup="dialog"
                          title={t.education.viewCertificate}
                          onClick={() => setViewing(c)}
                        >
                          {c.name}
                        </button>
                      ) : (
                        <span className="cert__name">{c.name}</span>
                      )}
                      <span className="cert__meta">
                        {c.issuer} · {monthYear.format(new Date(`${c.issued}T00:00`))}
                        {c.hours && ` · ${t.education.hours(c.hours)}`}
                      </span>
                      {c.credential_url && (
                        <span className="cert__links">
                          <a href={c.credential_url} target="_blank" rel="noreferrer">{t.education.verify} ↗</a>
                        </span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )
          })}
        </div>
      </div>
      <CertificateModal cert={viewing} onClose={() => setViewing(null)} />
    </Section>
  )
}
