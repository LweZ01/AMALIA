# 🔥 BIENVENIDOS AL INFIERNO: Sistema de Gestión Académica AMALIA 🔥

## ⚠️ ADVERTENCIA CRÍTICA ⚠️

**SI ESTÁS LEYENDO ESTO, PROBABLEMENTE HEREDASTE ESTE CÓDIGO. LO SENTIMOS MUCHO. REALMENTE LO SENTIMOS.**

Este no es un simple sistema de gestión académica. Es un campo minado de complejidad, referencias cruzadas, actualizaciones en cascada y suficiente código duplicado como para hacer llorar a un senior developer.

##  ¿Qué es esta cosa?

AMALIA es un Sistema de Gestión Académica desarrollado con PyQt6 y Supabase. Suena simple, ¿verdad? **MENTIRA.**

Este sistema gestiona:
- ✅ Docentes (que probablemente te culparán si algo falla)
- ✅ Asignaturas (con relaciones que te harán cuestionar tu carrera)
- ✅ Calificaciones (con ajustes, porque las notas simples son muy fáciles)
- ✅ Grados (con botones expandibles que son un infierno de mantener)
- ✅ Períodos académicos (fechas, porque no hay suficiente complejidad)
- ✅ Historial académico (con PDF, porque el sufrimiento debe documentarse)

### Lo que NO te dijeron:

- 🔥 Los estilos CSS están hardcodeados en un string de 400+ líneas
- 🔥 Los emojis en los botones pueden o no renderizarse según el sistema operativo (50/50)

---

##  Tecnologías (y por qué duelen)

### PyQt6
**Por qué duele:** Cada widget necesita configuración manual. Olvídate de hot-reload. Cada cmbaio requiere cerrar y reabrir la app.

### Supabase
**Por qué duele:** Si las credenciales cambian, TODO deja de funcionar. Sin rollback. Sin piedad.

### Python 3.8+
**Por qué duele:** Tipado dinámico significa que descubrirás errores EN PRODUCCIÓN.

### Dependencias Críticas:
supabase==1.x  # Si actualizas, RUEGA que siga compatible
python-dotenv  # Porque las credenciales NUNCA deben estar en el código (pero probablemente lo estén)

## Bugs Conocidos (Y los que NO conoces)

1. **Emojis en Botones**
   - En Windows: ✅ Se ven
   - En macOS: ✅ Se ven
   - **Solución:** Nadie quiere tocar esto

2. **Estilos CSS Hardcodeados**
   - 400+ líneas de CSS en `setup_ui()`
   - Cambiar un color = buscar en 15 lugares diferentes
   - **Recomendación:** Rezar y usar Ctrl+F (Recomendacion real quitarle los estilos te deja un programa manejable)


## 🛡️ Cómo NO Romper Todo

### Reglas de Oro para Sobrevivir:

#### 1️⃣ **NUNCA modifiques `delete_estudiante()` sin leer TODO el método**
```python
# Este método actualiza:
# - Tabla principal
# - Vista de grados expandida
# - Botones de grados
# - Búsqueda de calificaciones
# ¿Olvidaste uno? COSAS SE ROMPEN
```

#### 2️⃣ **SIEMPRE usa `hasattr()` antes de acceder a widgets dinámicos**
```python
# MAL
self.checkboxes_estudiantes[0].isChecked()

# BIEN
if hasattr(self, 'checkboxes_estudiantes'):
    if self.checkboxes_estudiantes:
        checkbox = self.checkboxes_estudiantes[0]
```

#### 3️⃣ **NO toques el límite de 50 estudiantes sin implementar paginación**
- O todos se quejan
- O el sistema colapsa
- O ambas

#### 4️⃣ **Cuidado con los QTimer**
```python
# Si usas lambdas con variables locales
# COPIA LA VARIABLE PRIMERO
grado_actual = grado_info.copy()  # ✅
QTimer.singleShot(100, lambda: self.show(grado_actual))
```

#### 5️⃣ **Antes de commitear, prueba:**
- [ ] Crear estudiante
- [ ] Editar estudiante
- [ ] **ELIMINAR estudiante** (el más crítico)
- [ ] Mover estudiante de grado
- [ ] Mover múltiples estudiantes
- [ ] Buscar calificaciones

## ❓ FAQ (Preguntas Frecuentemente Aterrorizantes)

### P: ¿Por qué hay código duplicado?
**R:** Nadie lo sabe. Probablemente un merge conflict que se resolvió con "aceptar ambos cambios".

### P: ¿Puedo usar un framework CSS moderno?
**R:** Técnicamente sí. Prácticamente, tendrías que reescribir TODO el sistema de estilos.

### P: ¿Los QTimer son necesarios?
**R:** Sí. PyQt6 a veces necesita "respirar" entre operaciones de UI. Sin ellos, las actualizaciones no se reflejan.

### P: ¿Qué pasa si Supabase cambia su API?
**R:** 🔥🔥🔥 TODO EXPLOTA 🔥🔥🔥

### P: ¿Hay tests?
**R:** JAJAJAJAJAJA... no.

### P: ¿Documentación adicional?
**R:** Este README es todo lo que hay. Y los comentarios en el código.

### P: ¿Puedo refactorizar esto?
**R:** Puedes. Pero cada cambio tiene el potencial de romper 3 cosas más. Procede con extrema precaución.

---

##  Consejos de Supervivencia

### 1. **Usa Git religiosamente**
```bash
git commit -m "Funcionaba antes de este cambio"
```

### 2. **Mantén copias de seguridad de la BD**
Supabase puede ser tu amigo o tu peor enemigo.

### 3. **Documenta TODO cambio**
```python
# NOTA: Agregué este try-except porque el sistema explotaba
# cuando el usuario presionaba Escape en el diálogo
# Fecha: 2025-01-25
# Autor: [Tu nombre aquí, para que te culpen después]
```

### 4. **Aprende a depurar con prints**
PyQt6 no tiene un debugger amigable. Los prints son tu mejor amigo

### 5. **No asumas NADA**
- ¿Ese widget existe? Verifica con `hasattr()`
- ¿Esa lista tiene elementos? Verifica con `if lista:`
- ¿Ese diccionario tiene esa clave? Usa `.get()`

### 6. **Mantén un diario de cambios**
```markdown
## 2025-01-25
- Arreglé el bug de los checkboxes
- ROMPÍ la actualización de grados
- Pasé 3 horas debuggeando
- Finalmente funcionó
- No sé por qué
```

### 7. **Conoce las partes críticas**

**🟡 ZONA DE PRECAUCIÓN:**
- Cualquier función `load_*()` - Recargan datos completos
- Cualquier función `filter_*()` - Iteran sobre TODAS las filas
- `perform_search()` - Tiene un timer de por medio

## 🎓 Lecciones Aprendidas (de la manera difícil)

1. **PyQt6 no actualiza automáticamente**
   - Debes llamar explícitamente a `update()`, `repaint()`, o recargar widgets

2. **Los lambdas en QTimer son peligrosas**
   - Capturan referencias, no valores
   - Usa `.copy()` o variables locales

3. **No confíes en que los widgets existen**
   - Usa `hasattr()` SIEMPRE

4. **El CSS inline es un infierno**
   - Pero cambiarlo ahora rompería TODO

5. **La documentación es crítica**
   - Este README existe porque sufrimos

---

## 🚀 Si vas a extender el sistema...

### Para agregar una nueva entidad (ej: "Cursos"):

1. **Crea la tabla en Supabase** ✅
2. **Agrega métodos en `supabase_client.py`** ✅
```python
   def get_all_cursos(self)
   def add_curso(self, data)
   def update_curso(self, id, data)
   def delete_curso(self, id)
```

3. **Crea un diálogo en `models/dialogs.py`** ✅
```python
   class CursoDialog(QDialog):
       # Copia la estructura de EstudianteDialog
```

4. **Agrega pestaña en `main_window.py`** ✅
```python
   def create_cursos_tab(self):
       # Copia la estructura de create_estudiantes_tab()
```

5. **Implementa las funciones CRUD** ✅
```python
   def add_curso(self)
   def edit_curso(self, curso)
   def delete_curso(self, id)
   def load_cursos(self)
```

6. **REZA para que funcione** 

## Soporte (o falta de él)

**¿Tienes un bug?**
1. Verifica que no esté en la lista de "Bugs Conocidos"
2. Agrega `print()` statements EVERYWHERE
3. Lee el stack trace completo
4. Google es tu amigo
5. Stack Overflow es tu salvador
6. Si nada funciona, llora un poco
7. Luego vuelve al paso 2

**¿Quieres contactar al desarrollador original?**
- Buena suerte con eso.


##  Palabras Finales

Este código es como una torre de Jenga: cada pieza sostiene a tres más. Retira la pieza equivocada y todo colapsa.

**Pero aquí estás**, leyendo este README, probablemente porque:
- Te asignaron mantener esto
- Heredaste este proyecto
- Eres el nuevo "el que sabe de programación"
- Cometiste algún pecado en una vida pasada

Sea cual sea la razón, **bienvenido al equipo**. 

Somos sobrevivientes. Somos guerreros. Somos los que mantienen vivo este código contra todo pronóstico.

**Cuando te toque pasarle esto a alguien más, actualiza este README.**

Añade tus propias batallas. Documenta tus propias pesadillas. Y sobre todo, sé honesto sobre las atrocidades que cometiste para hacer que "funcionara".

Porque el próximo desarrollador te lo agradecerá.

O al menos sabrá a qué se enfrenta.

---

## 📜 Licencia

**Licencia de Sufrimiento Compartido (LSC) v1.0**

Se permite:
- Usar este código
- Modificar este código
- Llorar por este código
- Maldecir este código

Se prohíbe:
- Culpar al próximo mantenedor
- No documentar tus cambios
- Asumir que "funciona en mi máquina" es suficiente
- Eliminar este README

---

**Última actualización:** 25 de Enero, 2026
**Última vez que todo funcionó simultáneamente:** ¿Alguna vez?


**¡BUENA SUERTE! ¡LA VAS A NECESITAR!** 

*"En este código, no hay errores. Solo características que aún no entendemos."*
*- Desarrollador Anónimo, probablemente llorando*
