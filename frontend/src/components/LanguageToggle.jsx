import { useLanguage } from '../i18n/context'

const OPTIONS = [
  { code: 'es', label: 'ES', name: 'Español' },
  { code: 'en', label: 'EN', name: 'English' },
]

export default function LanguageToggle() {
  const { lang, setLang, t } = useLanguage()
  return (
    <div className="lang-toggle" role="group" aria-label={t.nav.language}>
      {OPTIONS.map((o) => (
        <button
          key={o.code}
          lang={o.code}
          aria-pressed={lang === o.code}
          aria-label={o.name}
          title={o.name}
          onClick={() => setLang(o.code)}
        >
          {o.label}
        </button>
      ))}
    </div>
  )
}
