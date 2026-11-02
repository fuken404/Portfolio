// Medición de visitas con Application Insights. Sin cadena de conexión (desarrollo) no hace nada.
// La librería se carga aparte para no pesar en la primera pintura, y no usa cookies.
const connectionString = import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING

let client = null

export function startAnalytics() {
  if (!connectionString) return
  client = import('@microsoft/applicationinsights-web')
    .then(({ ApplicationInsights }) => {
      const insights = new ApplicationInsights({
        config: {
          connectionString,
          disableCookiesUsage: true,
          disableAjaxTracking: true,
          disableFetchTracking: true,
          autoTrackPageVisitTime: true,
        },
      })
      insights.loadAppInsights()
      insights.trackPageView()
      return insights
    })
    .catch(() => null) // Un bloqueador de anuncios no debe afectar al sitio.
}

export function trackEvent(name, properties) {
  client?.then((insights) => insights?.trackEvent({ name }, properties))
}
