import { useLanguage } from '../i18n/context'
import Section from './Section'

// Categorías con nivel: van en la tabla con medidores.
const TABLE = ['languages', 'backend', 'frontend', 'data', 'tools']
// Categorías sin nivel: van debajo, como listas.
const LISTS = ['ai', 'practices']

function Meter({ level, label }) {
  return (
    <span className="meter" role="img" aria-label={label}>
      {[1, 2, 3, 4, 5].map((n) => (
        <i key={n} className={n <= level ? 'on' : ''} />
      ))}
    </span>
  )
}

export default function Skills({ api, index }) {
  const { t } = useLanguage()
  const byCategory = (key) => api.data.filter((s) => s.category === key)

  return (
    <Section id="stack" index={index} title={t.sections.stack} api={api}>
      <div className="skills">
        {TABLE.map((key) => {
          const items = byCategory(key)
          if (!items.length) return null
          return (
            <div key={key} className="skills__group">
              <h3 className="skills__cat">{t.skills[key]}</h3>
              <ul>
                {items.map((s) => (
                  <li key={s.id} className={s.is_core ? 'is-core' : ''}>
                    <span className="skills__name">
                      {s.name}
                      {s.is_core && <span className="tag tag--accent">{t.skills.core}</span>}
                    </span>
                    {s.level && <Meter level={s.level} label={t.skills.level(s.level)} />}
                  </li>
                ))}
              </ul>
            </div>
          )
        })}
      </div>

      <div className="skills-lists">
        {LISTS.map((key) => {
          const items = byCategory(key)
          if (!items.length) return null
          return (
            <div key={key} className="skills-lists__group">
              <h3 className="skills__cat">{t.skills[key]}</h3>
              <ul>
                {items.map((s) => (
                  <li key={s.id} className={s.is_core ? 'is-core' : ''}>{s.name}</li>
                ))}
              </ul>
            </div>
          )
        })}
      </div>
    </Section>
  )
}
