import About from './components/About'
import Contact from './components/Contact'
import Education from './components/Education'
import Experience from './components/Experience'
import Footer from './components/Footer'
import Header from './components/Header'
import Hero from './components/Hero'
import Projects from './components/Projects'
import Skills from './components/Skills'
import StackBridge from './components/StackBridge'
import { fallback } from './data/fallback'
import { useActiveSection } from './hooks/useActiveSection'
import { useApi } from './hooks/useApi'
import { useTheme } from './hooks/useTheme'
import { useLanguage } from './i18n/context'

const SECTIONS = [
  { id: 'sobre-mi', key: 'about' },
  { id: 'stack', key: 'stack' },
  { id: 'proyectos', key: 'projects' },
  { id: 'experiencia', key: 'experience' },
  { id: 'formacion', key: 'education' },
  { id: 'contacto', key: 'contact' },
]
// 'inicio' se observa para que ningún enlace quede activo sobre el hero.
const SECTION_IDS = ['inicio', ...SECTIONS.map((s) => s.id)]

export default function App() {
  const { isDark, toggle: toggleTheme } = useTheme()
  const { lang, t } = useLanguage()
  const active = useActiveSection(SECTION_IDS)

  const local = fallback[lang]
  const profile = useApi('/profile/', local.profile, lang)
  const skills = useApi('/skills/', local.skills, lang)
  const projects = useApi('/projects/', local.projects, lang)
  const experience = useApi('/experience/', local.experience, lang)
  const education = useApi('/education/', local.education, lang)
  const certifications = useApi('/certifications/', local.certifications, lang)

  const sections = SECTIONS.map((s) => ({ id: s.id, label: t.sections[s.key] }))
  const initials = profile.data.name
    .split(' ')
    .map((w) => w[0])
    .join('')
    .slice(0, 2)
  const coreStack = skills.data.filter((s) => s.is_core).map((s) => s.name)

  return (
    <>
      <div className="grid-bg" aria-hidden="true" />
      <Header sections={sections} active={active} initials={initials} isDark={isDark} onToggleTheme={toggleTheme} />
      <main className="page">
        <Hero profileApi={profile} coreStack={coreStack} />
        <StackBridge />
        <About api={profile} index={1} />
        <Skills api={skills} index={2} />
        <Projects api={projects} index={3} />
        <Experience api={experience} index={4} />
        <Education educationApi={education} certificationsApi={certifications} index={5} />
        <Contact index={6} profile={profile.data} />
      </main>
      <Footer name={profile.data.name} />
    </>
  )
}
