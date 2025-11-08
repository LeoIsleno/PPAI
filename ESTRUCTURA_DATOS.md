# 📊 Estructura y Ordenamiento de Datos

## 🔄 Jerarquía de Datos

```
EventoSismico
    └── Sismografo (múltiples)
            └── EstacionSismologica
            └── SerieTemporal (múltiples)
                    └── MuestraSismica (múltiples)
                            └── DetalleMuestraSismica (múltiples)
```

## 📋 Ordenamiento de Series Temporales

### Agrupación Principal
Las **Series Temporales** se agrupan por **Estación Sismológica**:

```javascript
seriesPorEstacion = {
    "Estación Central": [serie1, serie2, ...],
    "Estación Norte": [serie3, serie4, ...],
    "Estación Sur": [serie5, serie6, ...]
}
```

### Orden de Presentación
1. **Por Estación**: Se muestran todas las series de una estación antes de pasar a la siguiente
2. **Dentro de cada estación**: Las series se muestran en el orden en que fueron registradas
3. **Numeración**: Cada serie se numera secuencialmente dentro de su estación (#1, #2, #3...)

## 📈 Estructura de una Serie Temporal

Cada **Serie Temporal** contiene:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `fechaHoraInicioRegistroMuestras` | Inicio del registro | "2025-01-15 14:30:00" |
| `fechaHoraRegistro` | Hora de registro de la serie | "2025-01-15 14:35:00" |
| `frecuenciaMuestreo` | Frecuencia en Hz | "100 Hz" |
| `condicionAlarma` | Estado de alarma | true/false |
| `muestraSismica` | Array de muestras | [...] |
| `estado` | Estado de la serie | AutoDetectado, etc. |

## 🔬 Ordenamiento de Muestras Sísmicas

### Orden Cronológico
Las **Muestras Sísmicas** dentro de cada serie se ordenan por:
- `fechaHoraMuestra` (orden cronológico ascendente)
- La primera muestra es la más antigua
- La última muestra es la más reciente

### Numeración
Las muestras se numeran secuencialmente:
- Muestra #1, Muestra #2, Muestra #3...
- Cada muestra tiene su propia `fechaHoraMuestra`

## 📊 Estructura de una Muestra Sísmica

Cada **Muestra Sísmica** contiene:

```python
MuestraSismica
    └── fechaHoraMuestra: datetime
    └── detalleMuestraSismica: [
            DetalleMuestraSismica1,
            DetalleMuestraSismica2,
            ...
        ]
```

## 🔍 Detalles de Muestra Sísmica

Cada **Detalle** representa un tipo de dato específico:

| Tipo de Dato | Unidad | Descripción |
|--------------|--------|-------------|
| `Velocidad de onda` | m/s | Velocidad de propagación |
| `Frecuencia de onda` | Hz | Frecuencia de oscilación |
| `Longitud` | m | Longitud de onda |

### Estructura de Detalle
```javascript
{
    tipoDeDato: "Velocidad de onda",
    valor: "1234.56",
    unidad: "m/s"
}
```

## 📐 Ejemplo Completo

```
📍 Estación Central (EST-001)
    
    📊 Serie temporal #1
    ⏰ Inicio: 2025-01-15 14:30:00
    📡 Frecuencia: 100 Hz
    
        📝 Muestra #1 - 2025-01-15 14:30:01
            🏃 Velocidad de onda: 1234.56 m/s
            〰️ Frecuencia de onda: 5.2 Hz
            📏 Longitud: 45.3 m
        
        📝 Muestra #2 - 2025-01-15 14:30:02
            🏃 Velocidad de onda: 1245.32 m/s
            〰️ Frecuencia de onda: 5.5 Hz
            📏 Longitud: 46.1 m
    
    📊 Serie temporal #2
    ⏰ Inicio: 2025-01-15 15:00:00
    📡 Frecuencia: 100 Hz
    
        📝 Muestra #1 - 2025-01-15 15:00:01
            ...

📍 Estación Norte (EST-002)
    
    📊 Serie temporal #1
        ...
```

## 🎨 Visualización en la UI

### Colores por Componente

- **Estación Sismológica**: Azul oscuro (`#1a237e`)
- **Serie Temporal**: Borde azul primario (`#283593`)
- **Muestra Sísmica**: Fondo blanco con iconos verde azulado (`#00897b`)
- **Detalle**: Iconos según tipo de dato

### Iconografía

| Elemento | Icono | Color |
|----------|-------|-------|
| Estación | `bi-geo-fill` | Blanco (en header) |
| Serie | `bi-graph-up` | Azul primario |
| Fecha | `bi-calendar-event` / `bi-clock-history` | Gris / Verde azulado |
| Frecuencia | `bi-speedometer2` | Gris |
| Muestras | `bi-collection` | Azul primario |
| Velocidad | `bi-speedometer` | Verde azulado |
| Frecuencia | `bi-activity` | Verde azulado |
| Longitud | `bi-rulers` | Verde azulado |

## 💾 Almacenamiento en Código

### Backend (Python)
```python
class SerieTemporal:
    def __init__(self, ...):
        self._muestraSismica = []  # Lista de MuestraSismica
        # Las muestras se agregan con agregarMuestraSismica()

class MuestraSismica:
    def __init__(self, fechaHoraMuestra, detalleMuestraSismica):
        self.__fechaHoraMuestra = fechaHoraMuestra
        self.__detalleMuestraSismica = detalleMuestraSismica  # Lista de DetalleMuestraSismica
```

### Frontend (JavaScript)
```javascript
// Las series se agrupan por estación
const seriesPorEstacion = {};
seriesTemporales.forEach(serie => {
    const nombre = serie.estacionSismologica.nombreEstacion;
    if (!seriesPorEstacion[nombre]) {
        seriesPorEstacion[nombre] = [];
    }
    seriesPorEstacion[nombre].push(serie);
});

// Se renderizan por estación
Object.entries(seriesPorEstacion).forEach(([nombreEstacion, series]) => {
    // Renderizar estación
    series.forEach((serie, idx) => {
        // Renderizar serie #(idx + 1)
        serie.muestras.forEach((muestra, j) => {
            // Renderizar muestra #(j + 1)
            muestra.detalle.forEach(det => {
                // Renderizar detalle
            });
        });
    });
});
```

## 🔄 Flujo de Datos

1. **Backend** obtiene el evento sísmico de la BD
2. Recorre los **sismógrafos** asociados
3. Cada sismógrafo tiene **series temporales**
4. Cada serie tiene **muestras sísmicas**
5. Cada muestra tiene **detalles**
6. Se serializa todo a JSON
7. **Frontend** recibe el JSON
8. Agrupa por **estación sismológica**
9. Renderiza en orden jerárquico

## 📌 Notas Importantes

- ✅ Las series se ordenan por estación para facilitar la lectura
- ✅ Las muestras están en orden cronológico (más antigua primero)
- ✅ Cada detalle tiene su tipo de dato específico
- ✅ La UI usa colores consistentes con el tema sísmico
- ✅ Los iconos ayudan a identificar rápidamente cada tipo de dato

---

**Última actualización**: Noviembre 2025
