import { useLanguage } from '../i18n/context'

export default function Footer({ name }) {
  const { t } = useLanguage()
  return (
    <footer className="footer">
      <span>© {new Date().getFullYear()} {name}</span>
      <span className="footer__stack">{t.footer.builtWith}</span>
      <a href="#inicio">{t.footer.backToTop}</a>
    </footer>
  )
}
