import { createContext, useContext } from 'react'

export const LanguageContext = createContext(null)

/** { lang, setLang, t } — `t` son los textos de la interfaz en el idioma activo. */
export function useLanguage() {
  return useContext(LanguageContext)
}
