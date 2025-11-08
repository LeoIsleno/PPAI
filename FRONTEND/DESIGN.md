# 🌍 Sistema de Monitoreo Sísmico - Guía de Diseño

## Paleta de Colores

### Colores Principales
- **Azul Profundo** (`#1a237e`): Representa estabilidad y confiabilidad del sistema
- **Azul Índigo** (`#283593`): Color principal del sistema
- **Verde Azulado** (`#00897b`): Monitoreo activo y procesos en curso
- **Naranja** (`#f57c00`): Alertas y advertencias
- **Rojo** (`#c62828`): Eventos críticos y acciones destructivas
- **Verde** (`#2e7d32`): Confirmaciones y estados exitosos

### Gradientes
- **Principal**: `linear-gradient(135deg, #1a237e 0%, #283593 100%)`
- **Acento**: `linear-gradient(135deg, #00897b 0%, #26a69a 100%)`
- **Tierra**: `linear-gradient(135deg, #1a237e 0%, #004d40 50%, #f57c00 100%)`

## Patrones de Diseño Aplicados

### 1. **Autenticación**
- Login centralizado con validación
- Sesión persistente (localStorage/sessionStorage)
- Protección de rutas
- Timeout de sesión (24 horas)

### 2. **Navegación**
- Navbar fijo con información del usuario
- Breadcrumbs implícitos en títulos
- Botones de navegación contextuales

### 3. **Cards**
- Sombras suaves para profundidad
- Hover effects para interactividad
- Headers con gradientes
- Iconografía consistente

### 4. **Formularios**
- Labels descriptivos con iconos
- Validación visual
- Estados focus destacados
- Feedback inmediato

### 5. **Estados**
- Badges con colores semánticos
- Iconos representativos
- Animaciones sutiles
- Transiciones suaves

## Iconografía

### Bootstrap Icons
- `bi-broadcast-pin`: Logo del sistema (monitoreo sísmico)
- `bi-person-fill`: Usuario
- `bi-clipboard-data`: Registro de eventos
- `bi-graph-up`: Estadísticas
- `bi-lightning`: Actividad sísmica
- `bi-geo-alt`: Ubicación/Alcance
- `bi-speedometer`: Magnitud

## Tipografía

- **Familia**: Segoe UI (fallback: Tahoma, Geneva, Verdana, sans-serif)
- **Tamaños**:
  - H2: 1.5rem (Login header)
  - H4: 1.25rem (Card headers)
  - Body: 1rem
  - Small: 0.875rem

## Espaciado

- **Padding cards**: 1.5rem - 2rem
- **Gap entre elementos**: 1rem - 1.5rem
- **Margin bottom**: 1rem - 2rem
- **Border radius**: 8px - 16px

## Sombras

- **Pequeña**: `0 2px 4px rgba(0,0,0,0.1)`
- **Media**: `0 4px 8px rgba(0,0,0,0.15)`
- **Grande**: `0 8px 16px rgba(0,0,0,0.2)`
- **Extra Grande**: `0 12px 24px rgba(0,0,0,0.25)`

## Animaciones

### Duración estándar
- **Rápida**: 0.2s
- **Normal**: 0.3s
- **Lenta**: 0.6s

### Efectos aplicados
- Slide up al cargar páginas
- Pulse en iconos importantes
- Hover con transform: translateY(-5px)
- Fade in para contenido dinámico

## Responsive Design

### Breakpoints
- **Mobile**: < 576px
- **Tablet**: 576px - 992px
- **Desktop**: > 992px

### Adaptaciones
- Cards a ancho completo en mobile
- Grid de 1 columna en mobile
- Navegación colapsable
- Info cards en horizontal/vertical según tamaño

## Accesibilidad

- Contraste mínimo WCAG AA
- Focus states visibles
- Labels descriptivos
- ARIA labels cuando necesario
- Tamaños de touch targets > 44px

## Credenciales de Prueba

```
Usuario: nico
Contraseña: 123

Usuario: admin
Contraseña: admin123

Usuario: analista
Contraseña: analista123
```

## Estructura de Navegación

```
Login (/)
  └─> Panel de Control (index.html)
       ├─> Registrar Revisión Manual (registrar.html)
       │    └─> Datos del Evento (datos_evento.html)
       ├─> Visualizar Estadísticas
       ├─> Gestionar Alertas
       └─> Configuración del Sistema
```

## Mejores Prácticas Implementadas

1. ✅ **Separación de concerns**: CSS, JS y HTML en archivos separados
2. ✅ **DRY**: Variables CSS para colores y valores reutilizables
3. ✅ **Mobile First**: Diseño responsive desde el inicio
4. ✅ **Progressive Enhancement**: Funcionalidad básica sin JS
5. ✅ **Semantic HTML**: Uso correcto de etiquetas semánticas
6. ✅ **Consistent naming**: Convenciones claras en clases y IDs
7. ✅ **Loading states**: Feedback visual para operaciones asíncronas
8. ✅ **Error handling**: Mensajes claros y recuperación de errores

---

**Desarrollado para**: Sistema de Monitoreo Sísmico - UTN FRC  
**Última actualización**: Noviembre 2025
