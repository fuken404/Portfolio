import { useEffect, useState } from 'react'

// Musgo es el modo oscuro y Arcilla el claro (ver styles/tokens.css).
const DARK = 'musgo'
const LIGHT = 'arcilla'
const KEY = 'portfolio-theme'

const systemDark = window.matchMedia('(prefers-color-scheme: dark)')

function savedTheme() {
  try {
    const t = localStorage.getItem(KEY)
    return t === DARK || t === LIGHT ? t : null
  } catch {
    return null
  }
}

export function useTheme() {
  const [theme, setTheme] = useState(() => savedTheme() ?? (systemDark.matches ? DARK : LIGHT))

  useEffect(() => {
    document.documentElement.dataset.theme = theme
  }, [theme])

  // Mientras la persona no elija un modo, seguimos el del sistema.
  useEffect(() => {
    const onChange = (e) => {
      if (!savedTheme()) setTheme(e.matches ? DARK : LIGHT)
    }
    systemDark.addEventListener('change', onChange)
    return () => systemDark.removeEventListener('change', onChange)
  }, [])

  const toggle = () => {
    const next = theme === DARK ? LIGHT : DARK
    setTheme(next)
    try {
      localStorage.setItem(KEY, next)
    } catch {
      // Almacenamiento bloqueado: el modo simplemente no se recuerda.
    }
  }

  return { isDark: theme === DARK, toggle }
}
