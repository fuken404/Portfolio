import { useLanguage } from '../i18n/context'
import Section from './Section'

export default function About({ api, index }) {
  const { t } = useLanguage()
  const p = api.data
  const facts = [
    [t.about.role, p.role],
    [t.about.base, p.location],
    [t.about.focus, p.focus],
    [t.about.languages, p.languages],
    [t.about.status, p.available ? t.about.available : t.about.unavailable],
  ].filter(([, value]) => value)

  return (
    <Section id="sobre-mi" index={index} title={t.sections.about} api={api}>
      <div className="about">
        <p className="about__bio">{p.bio}</p>
        <dl className="about__facts">
          {facts.map(([k, v]) => (
            <div key={k}>
              <dt>{k}</dt>
              <dd>{v}</dd>
            </div>
          ))}
        </dl>
      </div>
    </Section>
  )
}
