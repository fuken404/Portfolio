import { useLanguage } from '../i18n/context'
import Section from './Section'

function GitHubIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.53-1.33-1.28-1.69-1.28-1.69-1.05-.71.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.71 1.26 3.37.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.78 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.84 1.19 3.1 0 4.42-2.7 5.4-5.26 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z" />
    </svg>
  )
}

export default function Projects({ api, index }) {
  const { t } = useLanguage()
  return (
    <Section id="proyectos" index={index} title={t.sections.projects} api={api}>
      <ol className="projects">
        {api.data.map((p, i) => (
          <li key={p.id} className="project">
            <span className="project__num">{String(i + 1).padStart(2, '0')}</span>
            <div className="project__main">
              <h3 className="project__title">
                {p.title}
                {p.featured && <span className="tag tag--accent">{t.projects.featured}</span>}
              </h3>
              <p className="project__summary">{p.summary}</p>
              <span className="project__stack">{p.stack.join(' · ')}</span>
            </div>
            <div className="project__side">
              <span className="project__year">{p.year}</span>
              <div className="project__actions">
                {p.live_url ? (
                  <a className="btn btn--solid btn--sm" href={p.live_url} target="_blank" rel="noreferrer">
                    {t.projects.live} ↗
                  </a>
                ) : (
                  <span className="btn btn--sm btn--disabled" aria-disabled="true" title={t.projects.noLiveHint}>
                    {t.projects.noLive}
                  </span>
                )}
                {p.repo_url && (
                  <a className="btn btn--ghost btn--sm" href={p.repo_url} target="_blank" rel="noreferrer">
                    <GitHubIcon />
                    {t.projects.repo}
                  </a>
                )}
              </div>
            </div>
          </li>
        ))}
      </ol>
    </Section>
  )
}
