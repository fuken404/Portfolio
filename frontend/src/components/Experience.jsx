import { useLanguage } from '../i18n/context'
import Section from './Section'

export default function Experience({ api, index }) {
  const { lang, t } = useLanguage()
  const fmt = new Intl.DateTimeFormat(lang, { month: 'short', year: 'numeric' })
  const date = (iso) => fmt.format(new Date(`${iso}T00:00`))
  const range = (start, end) => `${date(start)} — ${end ? date(end) : t.experience.present}`

  return (
    <Section id="experiencia" index={index} title={t.sections.experience} api={api}>
      <ol className="timeline">
        {api.data.map((job) => (
          <li key={job.id} className={`timeline__item ${job.end ? '' : 'is-current'}`}>
            <div className="timeline__when">
              <span className="timeline__date">{range(job.start, job.end)}</span>
              {job.location && <span className="timeline__place">{job.location}</span>}
            </div>
            <div className="timeline__content">
              <h3>
                {job.position} <span>@ {job.company}</span>
              </h3>
              <p>{job.description}</p>
              {job.highlights.length > 0 && (
                <ul>
                  {job.highlights.map((h) => (
                    <li key={h}>{h}</li>
                  ))}
                </ul>
              )}
            </div>
          </li>
        ))}
      </ol>
    </Section>
  )
}
