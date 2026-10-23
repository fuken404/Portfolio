import { useState } from 'react'
import { request } from '../api/client'
import { useLanguage } from '../i18n/context'
import Section from './Section'

const EMPTY = { name: '', email: '', message: '' }

export default function Contact({ index, profile }) {
  const { lang, t } = useLanguage()
  const [form, setForm] = useState(EMPTY)
  const [errors, setErrors] = useState({})
  const [result, setResult] = useState(null) // { state: 'sending' | 'ok' | 'error', code, ms }

  const update = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  async function submit(e) {
    e.preventDefault()
    setResult({ state: 'sending' })
    setErrors({})
    try {
      // Con `lang`, Django devuelve los errores de validación en ese idioma.
      const res = await request('/contact/', { method: 'POST', body: form, lang })
      if (res.ok) {
        setForm(EMPTY)
        setResult({ state: 'ok', code: res.code, ms: res.ms })
      } else {
        setErrors(res.data ?? {})
        setResult({ state: 'error', code: res.code, ms: res.ms })
      }
    } catch {
      setResult({ state: 'error', code: t.contact.offline })
    }
  }

  const field = (name, label, props = {}) => (
    <label className="field">
      <span className="field__label">{label}</span>
      {props.as === 'textarea' ? (
        <textarea name={name} value={form[name]} onChange={update} rows={5} required />
      ) : (
        <input name={name} value={form[name]} onChange={update} required {...props} />
      )}
      {errors[name] && <span className="field__error">{errors[name].join(' ')}</span>}
    </label>
  )

  const [before, highlight, after] = t.contact.headline

  return (
    <Section id="contacto" index={index} title={t.sections.contact}>
      <div className="contact">
        <div className="contact__intro">
          <p className="contact__big">
            {before}<em>{highlight}</em>{after}
          </p>
          <p>{t.contact.intro}</p>
          <ul className="contact__links">
            {profile.email && <li><a href={`mailto:${profile.email}`}>{profile.email}</a></li>}
            {profile.github && <li><a href={profile.github} target="_blank" rel="noreferrer">GitHub ↗</a></li>}
            {profile.linkedin && <li><a href={profile.linkedin} target="_blank" rel="noreferrer">LinkedIn ↗</a></li>}
          </ul>
        </div>

        <form className="contact__form" onSubmit={submit}>
          {field('name', t.contact.name, { autoComplete: 'name' })}
          {field('email', t.contact.email, { type: 'email', autoComplete: 'email' })}
          {field('message', t.contact.message, { as: 'textarea' })}
          <div className="contact__submit">
            <button className="btn btn--solid" disabled={result?.state === 'sending'}>
              {t.contact.send}
            </button>
            {result && (
              <code className={`contact__status contact__status--${result.state}`}>
                POST /api/contact/ →{' '}
                {result.state === 'sending' && t.contact.sending}
                {result.state === 'ok' && `${result.code} Created · ${result.ms}ms`}
                {result.state === 'error' && `${result.code}${result.ms ? ` · ${result.ms}ms` : ''}`}
              </code>
            )}
          </div>
        </form>
      </div>
    </Section>
  )
}
