// Contenido local que se muestra mientras carga la API o si Django no está corriendo.
// fallback.json lo genera el backend con la misma forma que la API:
//   python manage.py export_fallback
// Volver a ejecutarlo después de cambiar contenido en el admin.
import data from './fallback.json'

// Objetos estables por idioma (useApi los usa como dependencia).
export const fallback = data
