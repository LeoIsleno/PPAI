# Mapa de Transiciones de Estados

## Diagrama de Flujo

```
                    ┌─────────────────┐
                    │ AutoDetectado   │
                    └────────┬────────┘
                             │ bloquear()
                             ▼
                    ┌─────────────────┐
             ┌─────▶│ BloqueadoEn     │
             │      │ Revision        │◀─────┐
             │      └────────┬────────┘      │
             │               │               │ bloquear()
             │      ┌────────┴────────┐      │
             │      │                 │      │
             │      │ confirmar()     │ rechazar()
             │      ▼                 ▼      │
    ┌────────┴──────────┐    ┌─────────────┴────┐
    │ ConfirmadoPor     │    │ Rechazado        │
    │ Personal          │    │ [FINAL]          │
    └────────┬──────────┘    └──────────────────┘
             │ cerrar()               ▲
             ▼                        │
    ┌───────────────────┐             │
    │ Cerrado           │             │
    │ [FINAL]           │             │
    └───────────────────┘             │
                                      │
    ┌─────────────────┐               │
    │ AutoConfirmado  │               │
    └────────┬────────┘               │
             │                        │
    ┌────────┴────────┐               │
    │                 │               │
    │ derivar()       │ auto          │
    ▼                 ▼               │
┌─────────┐    ┌─────────────────┐   │
│Derivado │    │ PendienteDe     │   │
└────┬────┘    │ Cierre          │   │
     │         └────────┬────────┘   │
     │                  │ cerrar()   │
     │                  ▼            │
     │         ┌───────────────────┐ │
     │         │ Cerrado           │ │
     │         │ [FINAL]           │ │
     │         └───────────────────┘ │
     │                               │
     │ confirmar()                   │
     ├──────────────────────────────►│
     │                 ConfirmadoPor │
     │                 Personal      │
     │                               │
     │ rechazar()                    │
     └───────────────────────────────┘


    ┌─────────────────┐
    │ PendienteDe     │
    │ Revision        │
    └────────┬────────┘
             │
    ┌────────┴────────┐
    │                 │
    │ bloquear()      │ anular()
    ▼                 ▼
┌─────────────┐  ┌─────────────┐
│BloqueadoEn  │  │SinRevision  │
│Revision     │  │[FINAL]      │
└─────────────┘  └─────────────┘
```

## Tabla de Transiciones

| Estado Origen | Acción | Estado Destino | Implementado |
|---------------|--------|----------------|--------------|
| AutoDetectado | `bloquear()` | BloqueadoEnRevision | ✅ |
| AutoConfirmado | `derivar()` | Derivado | ✅ |
| AutoConfirmado | Automático | PendienteDeCierre | ⚠️ |
| PendienteDeCierre | `cerrar()` | Cerrado | ✅ |
| Derivado | `confirmar()` | ConfirmadoPorPersonal | ✅ |
| Derivado | `rechazar()` | Rechazado | ✅ |
| ConfirmadoPorPersonal | `cerrar()` | Cerrado | ✅ |
| BloqueadoEnRevision | `confirmar()` | ConfirmadoPorPersonal | ✅ |
| BloqueadoEnRevision | `rechazar()` | Rechazado | ✅ |
| PendienteDeRevision | `bloquear()` | BloqueadoEnRevision | ✅ |
| PendienteDeRevision | `anular()` | SinRevision | ✅ |

**Leyenda:**
- ✅ Implementado completamente
- ⚠️ Transición automática (requiere lógica de negocio)

## Estados Finales

Los siguientes estados son **terminales** (no tienen transiciones de salida):

1. **Cerrado** - Evento procesado y cerrado exitosamente
2. **Rechazado** - Evento rechazado por el analista
3. **SinRevision** - Evento anulado sin revisión

## Métodos de Transición por Estado

### AutoDetectado
```python
def bloquear(self, evento, fechaHoraActual, usuario)
    # AutoDetectado → BloqueadoEnRevision
```

### AutoConfirmado
```python
def derivar(self, evento, fechaHoraActual, usuario)
    # AutoConfirmado → Derivado
```

### PendienteDeCierre
```python
def cerrar(self, evento, fechaHoraActual, usuario)
    # PendienteDeCierre → Cerrado
```

### Derivado
```python
def confirmar(self, evento, fechaHoraActual, usuario, ult_cambio)
    # Derivado → ConfirmadoPorPersonal

def rechazar(self, evento, fechaHoraActual, usuario, ult_cambio)
    # Derivado → Rechazado
```

### ConfirmadoPorPersonal
```python
def cerrar(self, evento, fechaHoraActual, usuario)
    # ConfirmadoPorPersonal → Cerrado
```

### BloqueadoEnRevision
```python
def confirmar(self, evento, fechaHoraActual, usuario, ult_cambio)
    # BloqueadoEnRevision → ConfirmadoPorPersonal

def rechazar(self, evento, fechaHoraActual, usuario, ult_cambio)
    # BloqueadoEnRevision → Rechazado
```

### PendienteDeRevision
```python
def bloquear(self, evento, fechaHoraActual, usuario)
    # PendienteDeRevision → BloqueadoEnRevision

def anular(self, evento, fechaHoraActual, usuario)
    # PendienteDeRevision → SinRevision
```

### Cerrado, Rechazado, SinRevision
```python
# Estados finales - sin transiciones
```

## Ejemplo de Uso Completo

```python
from datetime import datetime
from BACKEND.Modelos.estados import AutoDetectado, BloqueadoEnRevision
from BACKEND.Modelos.EventoSismico import EventoSismico
from BACKEND.Modelos.Usuario import Usuario

# Crear evento con estado inicial
estado_inicial = AutoDetectado("EventoSismico")
evento = EventoSismico(
    fechaHoraOcurrencia=datetime.now(),
    # ... otros parámetros
    estadoActual=estado_inicial,
    # ...
)

# Usuario que realiza la acción
usuario = Usuario("analista1", "password", datetime.now(), None)

# Realizar transición de estado
fecha_actual = datetime.now()
cambio = evento.bloquear(
    estado_bloqueado=BloqueadoEnRevision("EventoSismico"),
    fechaHoraActual=fecha_actual,
    usuario=usuario
)

# Verificar nuevo estado
print(evento.getEstadoActual().getNombreEstado())  # "Bloqueado en Revisión"
```

## Notas Importantes

1. **Cambios de Estado**: Cada transición crea un registro `CambioEstado` con:
   - Fecha/hora del cambio
   - Estado nuevo
   - Usuario responsable
   - Fecha/hora fin del estado anterior

2. **Validaciones**: Las transiciones pueden lanzar excepciones si:
   - El evento no tiene estado actual
   - La transición no está permitida
   - Faltan parámetros requeridos

3. **Persistencia**: Después de cada transición, el gestor debe:
   - Persistir el evento actualizado
   - Persistir el nuevo cambio de estado
   - Hacer commit de la transacción
