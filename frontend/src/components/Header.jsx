import { useState } from 'react'
import { useLanguage } from '../i18n/context'
import LanguageToggle from './LanguageToggle'
import ThemeToggle from './ThemeToggle'

export default function Header({ sections, active, initials, isDark, onToggleTheme }) {
  const [open, setOpen] = useState(false)
  const { t } = useLanguage()

  return (
    <header className={`topbar ${open ? 'topbar--open' : ''}`}>
      <a href="#inicio" className="topbar__logo" aria-label={t.nav.home}>
        <span aria-hidden="true">&lt;</span>
        {initials}
        <span aria-hidden="true">/&gt;</span>
      </a>

      <nav className="topbar__nav" aria-label={t.nav.label}>
        {sections.map((s, i) => (
          <a
            key={s.id}
            href={`#${s.id}`}
            className={active === s.id ? 'is-active' : ''}
            onClick={() => setOpen(false)}
          >
            <span className="topbar__num">{String(i + 1).padStart(2, '0')}</span>
            {s.label}
          </a>
        ))}
      </nav>

      <div className="topbar__end">
        <LanguageToggle />
        <ThemeToggle isDark={isDark} onToggle={onToggleTheme} />
        <button
          className="topbar__menu"
          aria-expanded={open}
          aria-label={open ? t.nav.closeMenu : t.nav.openMenu}
          onClick={() => setOpen((o) => !o)}
        >
          <span />
          <span />
        </button>
      </div>
    </header>
  )
}
