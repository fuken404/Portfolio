import { useLanguage } from '../i18n/context'

export default function ThemeToggle({ isDark, onToggle }) {
  const { t } = useLanguage()
  const label = isDark ? t.theme.toLight : t.theme.toDark
  return (
    <button className="theme-toggle" onClick={onToggle} aria-label={label} title={label}>
      <svg viewBox="0 0 24 24" aria-hidden="true">
        {/* Sol: visible en modo oscuro (lleva al claro) */}
        <g className="theme-toggle__sun">
          <circle cx="12" cy="12" r="4" />
          <path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4" />
        </g>
        {/* Luna: visible en modo claro (lleva al oscuro) */}
        <path className="theme-toggle__moon" d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z" />
      </svg>
    </button>
  )
}
