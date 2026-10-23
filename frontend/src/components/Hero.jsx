import { useLanguage } from '../i18n/context'
import JsonPanel from './JsonPanel'

export default function Hero({ profileApi, coreStack }) {
  const { t } = useLanguage()
  const p = profileApi.data
  const words = p.name.split(' ')
  const last = words.pop()

  const preview = {
    name: p.name,
    role: p.role,
    location: p.location,
    available: p.available,
    core_stack: coreStack,
  }

  return (
    <section id="inicio" className="hero">
      <div className="hero__text">
        <p className="hero__kicker">
          <span className={`pulse ${p.available ? '' : 'pulse--off'}`} aria-hidden="true" />
          {p.available ? t.hero.available : t.hero.unavailable} · {p.location}
        </p>
        <h1 className="hero__name">
          {words.join(' ')} <em>{last}</em>
        </h1>
        <p className="hero__role">{p.role}</p>
        <p className="hero__tagline">{p.tagline}</p>
        <div className="hero__actions">
          <a href="#proyectos" className="btn btn--solid">{t.hero.viewProjects}</a>
          <a href="#contacto" className="btn btn--ghost">{t.hero.contact}</a>
        </div>
      </div>
      <JsonPanel api={profileApi} data={preview} />
    </section>
  )
}
