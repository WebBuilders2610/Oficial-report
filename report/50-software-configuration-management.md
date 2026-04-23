# Capítulo V: Product Implementation, Validation & Deployment

## 5.1. Software Configuration Management

## 5.1.1. Software Development Environment Configuration

Para el desarrollo del Sistema Inteligente de Registro y Alerta Neonatal (SIRAN), se utilizó un enfoque basado en tecnologías web estándar, priorizando la simplicidad, accesibilidad y facilidad de implementación, especialmente en la construcción de la Landing Page, la cual representa el primer punto de contacto con los usuarios.

### Landing Page Development

La Landing Page fue desarrollada utilizando **HTML, CSS y JavaScript**, lo que permitió construir una interfaz ligera, rápida y compatible con múltiples dispositivos sin depender de frameworks complejos. Esta decisión está alineada con el objetivo del proyecto de ofrecer una experiencia intuitiva y clara para padres y profesionales de la salud.

- **HTML** se utilizó para estructurar el contenido de la página, empleando etiquetas semánticas que mejoran la accesibilidad y el posicionamiento.
- **CSS** permitió diseñar una interfaz visual limpia, orientada a transmitir tranquilidad y confianza, aspectos clave para el contexto neonatal.
- **JavaScript** se utilizó para añadir interactividad básica, como navegación dinámica o mejoras en la experiencia del usuario.

Para el desarrollo, se utilizó **Visual Studio Code** como entorno de programación, debido a su ligereza, soporte para múltiples extensiones y herramientas integradas como autocompletado, resaltado de sintaxis y terminal.

Para el control de versiones y colaboración, se utilizó **Git** junto con **GitHub**, lo cual permitió:
- Mantener un historial organizado de cambios  
- Facilitar el trabajo colaborativo  
- Gestionar versiones del producto de manera eficiente  

### Herramientas utilizadas

- HTML  
- CSS  
- JavaScript  
- Visual Studio Code  
- Git  
- GitHub  

### Rutas de referencia

- GitHub: https://github.com  
- HTML: https://developer.mozilla.org/es/docs/Web/HTML  
- CSS: https://developer.mozilla.org/es/docs/Web/CSS  
- JavaScript: https://developer.mozilla.org/es/docs/Web/JavaScript  
- Visual Studio Code: https://code.visualstudio.com/  

---

## 5.1.2. Source Code Management

Para la gestión del código fuente del proyecto SIRAN se utilizó **Git** como sistema de control de versiones y **GitHub** como plataforma de alojamiento de repositorios.

Esto permitió organizar el desarrollo del proyecto, mantener trazabilidad de los cambios y facilitar la colaboración entre los integrantes del equipo.

### Repositorio del proyecto

Se creó un repositorio para la Landing Page del sistema:

- URL del repositorio:  
https://github.com/WebBuilders2610/LandingPageOficial

---

### Estrategia de ramas

Se utilizó una estrategia basada en GitFlow simplificado:

| Tipo de rama | Prefijo | Ejemplo |
|--------------|--------|--------|
| Principal | main | main |
| Desarrollo | develop | develop |
| Feature | feature/ | feature/landing-page |
| Bugfix | bugfix/ | bugfix/fix-navbar |

---

### Flujo de trabajo

- La rama **main** contiene versiones estables del proyecto  
- La rama **develop** integra los avances en desarrollo  
- Las funcionalidades se desarrollan en ramas **feature**  
- Los errores se corrigen en ramas **bugfix**  

---

### Convención de commits

Se utilizó el estándar **Conventional Commits**:

```bash
git commit -m "feat: add landing page structure"
git commit -m "fix: correct responsive layout issue"
git commit -m "style: improve button design"
```
## 5.1.3. Source Code Style Guide & Conventions

En esta sección se definen las convenciones de estilo adoptadas para asegurar la calidad, legibilidad y mantenibilidad del código del proyecto SIRAN.

### Convenciones generales

- Código limpio y bien indentado  
- Uso de nombres descriptivos  
- Evitar duplicación de código  
- Separación clara entre estructura, estilo y lógica  

---

### HTML

| Convención | Descripción |
|-----------|------------|
| Semántica | Uso de etiquetas como `header`, `main`, `section`, `footer` |
| Indentación | 2 espacios |
| Atributos | Uso de comillas dobles `"` |
| Nombres | kebab-case (`main-section`) |

**Buenas prácticas:**
- Evitar código innecesario o comentado  
- Uso de atributos `alt` en imágenes  
- Estructura clara y organizada  

---

### CSS

| Convención | Descripción |
|-----------|------------|
| Nombres de clases | kebab-case (`main-container`) |
| Organización | Agrupar estilos por secciones |
| Reutilización | Uso de clases reutilizables |
| Diseño | Enfoque responsive (mobile-first) |

**Buenas prácticas:**
- Evitar estilos inline  
- Mantener consistencia visual  
- Uso de variables CSS cuando sea necesario  

---

### JavaScript

| Convención | Descripción |
|-----------|------------|
| Variables | camelCase |
| Constantes | UPPER_SNAKE_CASE |
| Funciones | camelCase descriptivo |
| Organización | Separar lógica por funciones |

**Buenas prácticas:**
- Evitar código global innecesario  
- Uso de funciones reutilizables  
- Manejo claro de eventos  

---

## 5.1.4. Software Deployment Configuration

Para el despliegue de la Landing Page del sistema SIRAN se utilizó un enfoque basado en hosting web estático, adecuado para aplicaciones desarrolladas con HTML, CSS y JavaScript.

### Estrategia de despliegue

El proyecto fue desplegado con

- GitHub Pages  


Estas plataformas permiten publicar aplicaciones web de manera rápida, gratuita y con integración directa desde repositorios Git.

---

### Proceso de despliegue

1. Subir el código al repositorio en GitHub  
2. Configurar el servicio de hosting (por ejemplo, GitHub Pages o Netlify)  
3. Seleccionar la rama principal (`main`)  
4. Publicar el sitio automáticamente  

---

### URL del despliegue

https://webbuilders2610.github.io/LandingPageOficial/

---

### Consideraciones

- El sistema es accesible desde navegadores modernos  
- No requiere instalación adicional  
- Permite futuras integraciones con servicios backend y módulos inteligentes  
