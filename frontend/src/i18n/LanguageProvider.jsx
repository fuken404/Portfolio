import { useEffect, useState } from 'react'
import { LanguageContext } from './context'
import { LANGS, strings } from './strings'

const KEY = 'portfolio-lang'

function initialLang() {
  try {
    const saved = localStorage.getItem(KEY)
    if (LANGS.includes(saved)) return saved
  } catch {
    // Almacenamiento bloqueado: se usa el idioma del navegador.
  }
  // Español para navegadores en español; inglés para el resto del mundo.
  return navigator.language?.toLowerCase().startsWith('es') ? 'es' : 'en'
}

export default function LanguageProvider({ children }) {
  const [lang, setLangState] = useState(initialLang)
  const t = strings[lang]

  useEffect(() => {
    document.documentElement.lang = lang
    document.title = t.meta.title
    document.querySelector('meta[name="description"]')?.setAttribute('content', t.meta.description)
  }, [lang, t])

  const setLang = (next) => {
    setLangState(next)
    try {
      localStorage.setItem(KEY, next)
    } catch {
      // Sin almacenamiento el idioma no se recuerda entre visitas.
    }
  }

  return <LanguageContext.Provider value={{ lang, setLang, t }}>{children}</LanguageContext.Provider>
}
