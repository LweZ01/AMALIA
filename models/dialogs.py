from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                            QLabel, QLineEdit, QPushButton, QComboBox, 
                            QDateEdit, QMessageBox, QDialogButtonBox,
                            QTableWidget, QTableWidgetItem, QHeaderView, QWidget)
from PyQt6.QtCore import Qt, QDate
from database.supabase_client import SupabaseClient
from typing import Dict, Any, Optional


class EstudianteDialog(QDialog):
    """Diálogo para agregar o editar un estudiante"""
    
    def __init__(self, parent=None, supabase_client: SupabaseClient = None, estudiante: Optional[Dict] = None):
        super().__init__(parent)
        self.supabase_client = supabase_client
        self.estudiante = estudiante
        self.is_edit = estudiante is not None
        
        self.setWindowTitle("Editar Estudiante" if self.is_edit else "Nuevo Estudiante")
        self.setMinimumWidth(500)
        self.setup_ui()
        
        if self.is_edit:
            self.load_estudiante_data()
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Cédula
        self.cedula_input = QLineEdit()
        self.cedula_input.setPlaceholderText("Ej: 1234567890")
        form_layout.addRow("Cédula:*", self.cedula_input)
        
        # Nombre
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del estudiante")
        form_layout.addRow("Nombre:*", self.nombre_input)
        
        # Apellido
        self.apellido_input = QLineEdit()
        self.apellido_input.setPlaceholderText("Apellido del estudiante")
        form_layout.addRow("Apellido:*", self.apellido_input)
        
        # Fecha de nacimiento
        self.fecha_nac_input = QDateEdit()
        self.fecha_nac_input.setCalendarPopup(True)
        self.fecha_nac_input.setDate(QDate.currentDate().addYears(-10))
        self.fecha_nac_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Fecha de Nacimiento:*", self.fecha_nac_input)
        
        # Teléfono
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Ej: 0999999999")
        form_layout.addRow("Teléfono:", self.telefono_input)
        
        # Correo
        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("correo@ejemplo.com")
        form_layout.addRow("Correo:", self.correo_input)
        
        # País
        self.pais_input = QLineEdit()
        self.pais_input.setPlaceholderText("Ej: Venezuela")
        form_layout.addRow("País:", self.pais_input)
        
        # Estado
        self.estado_input = QLineEdit()
        self.estado_input.setPlaceholderText("Ej: Nueva Esparta")
        form_layout.addRow("Estado:", self.estado_input)
        
        # Municipio
        self.municipio_input = QLineEdit()
        self.municipio_input.setPlaceholderText("Ej: Mariño")
        form_layout.addRow("Municipio:", self.municipio_input)
        
        # Grado
        self.grado_combo = QComboBox()
        self.load_grados()
        form_layout.addRow("Grado:", self.grado_combo)
        
        # Sección
        self.seccion_combo = QComboBox()
        self.seccion_combo.addItem("Seleccione una sección", None)
        self.seccion_combo.addItem("A", "A")
        self.seccion_combo.addItem("B", "B")
        self.seccion_combo.addItem("C", "C")
        self.seccion_combo.addItem("D", "D")
        self.seccion_combo.addItem("E", "E")
        self.seccion_combo.addItem("F", "F")
        self.seccion_combo.addItem("G", "G")
        form_layout.addRow("Sección:", self.seccion_combo)
        
        # Mención
        self.mencion_combo = QComboBox()
        self.mencion_combo.addItem("Seleccione una mención", None)
        self.mencion_combo.addItem("1 - Mención General", 1)
        self.mencion_combo.addItem("2 - Técnico Superior", 2)
        form_layout.addRow("Mención:", self.mencion_combo)
        
        # Observaciones
        self.observacion_input = QLineEdit()
        self.observacion_input.setPlaceholderText("Observaciones adicionales")
        form_layout.addRow("Observaciones:", self.observacion_input)
        
        layout.addLayout(form_layout)

        # Nota de campos requeridos
        nota_label = QLabel("* Campos obligatorios")
        nota_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(nota_label)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def load_grados(self):
        """Carga los grados disponibles"""
        self.grado_combo.clear()
        grados = self.supabase_client.get_all_grados()
        for grado in grados:
            self.grado_combo.addItem(grado['nombre_grado'], grado['id_grado'])

    
    def load_estudiante_data(self):
        """Carga los datos del estudiante a editar"""
        self.cedula_input.setText(self.estudiante['cedula'])
        self.cedula_input.setEnabled(False)  # No permitir editar cédula
        self.cedula_input.setStyleSheet("background-color: #e0e0e0; color: #666;")
        self.nombre_input.setText(self.estudiante['nombre'])
        self.apellido_input.setText(self.estudiante['apellido'])
        
        # Fecha de nacimiento
        fecha = QDate.fromString(str(self.estudiante['fecha_nacimiento']), "yyyy-MM-dd")
        self.fecha_nac_input.setDate(fecha)
        
        self.telefono_input.setText(self.estudiante.get('telefono') or '')
        self.correo_input.setText(self.estudiante.get('correo') or '')
        self.pais_input.setText(self.estudiante.get('pais') or '')
        self.estado_input.setText(self.estudiante.get('estado') or '')
        self.municipio_input.setText(self.estudiante.get('municipio') or '')
        self.observacion_input.setText(self.estudiante.get('observacion') or '')
        
        # Seleccionar grado
        index = self.grado_combo.findData(self.estudiante.get('id_grado'))
        if index >= 0:
            self.grado_combo.setCurrentIndex(index)
        
        # Seleccionar mención
        id_mencion = self.estudiante.get('id_mencion')
        if id_mencion:
            mencion_index = self.mencion_combo.findData(id_mencion)
            if mencion_index >= 0:
                self.mencion_combo.setCurrentIndex(mencion_index)
        
        # Seleccionar sección
        seccion = self.estudiante.get('seccion')
        if seccion:
            seccion_index = self.seccion_combo.findData(seccion)
            if seccion_index >= 0:
                self.seccion_combo.setCurrentIndex(seccion_index)
        
    
    def validate(self) -> bool:
        """Valida los datos del formulario"""
        
        # Validar cédula
        cedula = self.cedula_input.text().strip()
        if not cedula:
            QMessageBox.warning(self, "Error", "La cédula es obligatoria")
            self.cedula_input.setFocus()
            return False
        
        # Validar que la cédula sea numérica
        if not cedula.isdigit():
            QMessageBox.warning(self, "Error", "La cédula debe contener solo números")
            self.cedula_input.setFocus()
            return False
        
        # Validar longitud de cédula (10 dígitos)
        if len(cedula) < 7 or len(cedula) > 10:
            QMessageBox.warning(self, "Error", "La cédula debe tener entre 7 y 10 dígitos")
            self.cedula_input.setFocus()
            return False
        
        # Validar que la cédula no exista (solo al crear)
        if not self.is_edit:
            estudiante_existente = self.supabase_client.get_estudiante_by_cedula(cedula)
            if estudiante_existente:
                QMessageBox.warning(self, "Error", f"Ya existe un estudiante con la cédula {cedula}")
                self.cedula_input.setFocus()
                return False
        
        # Validar nombre
        nombre = self.nombre_input.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            self.nombre_input.setFocus()
            return False
        
        if len(nombre) < 2:
            QMessageBox.warning(self, "Error", "El nombre debe tener al menos 2 caracteres")
            self.nombre_input.setFocus()
            return False
        
        # Validar apellido
        apellido = self.apellido_input.text().strip()
        if not apellido:
            QMessageBox.warning(self, "Error", "El apellido es obligatorio")
            self.apellido_input.setFocus()
            return False
        
        if len(apellido) < 2:
            QMessageBox.warning(self, "Error", "El apellido debe tener al menos 2 caracteres")
            self.apellido_input.setFocus()
            return False
        
        # Validar fecha de nacimiento
        fecha_nac = self.fecha_nac_input.date()
        fecha_actual = QDate.currentDate()
        
        # Verificar que no sea una fecha futura
        if fecha_nac >= fecha_actual:
            QMessageBox.warning(self, "Error", "La fecha de nacimiento no puede ser futura")
            self.fecha_nac_input.setFocus()
            return False
        
        # Verificar edad mínima (5 años) y máxima (100 años)
        edad = fecha_actual.year() - fecha_nac.year()
        if edad < 5:
            QMessageBox.warning(self, "Error", "El estudiante debe tener al menos 5 años")
            self.fecha_nac_input.setFocus()
            return False
        
        if edad > 100:
            QMessageBox.warning(self, "Error", "La fecha de nacimiento no es válida")
            self.fecha_nac_input.setFocus()
            return False
        
        # Validar teléfono (si se ingresó)
        telefono = self.telefono_input.text().strip()
        if telefono:
            # Eliminar guiones y espacios
            telefono_limpio = telefono.replace("-", "").replace(" ", "")
            if not telefono_limpio.isdigit():
                QMessageBox.warning(self, "Error", "El teléfono debe contener solo números")
                self.telefono_input.setFocus()
                return False
            
            if len(telefono_limpio) < 7 or len(telefono_limpio) > 15:
                QMessageBox.warning(self, "Error", "El teléfono debe tener entre 7 y 15 dígitos")
                self.telefono_input.setFocus()
                return False
        
        # Validar correo (si se ingresó)
        correo = self.correo_input.text().strip()
        if correo:
            # Validación básica de formato de correo
            if "@" not in correo or "." not in correo.split("@")[-1]:
                QMessageBox.warning(self, "Error", "El formato del correo no es válido")
                self.correo_input.setFocus()
                return False
            
            if len(correo) < 5:
                QMessageBox.warning(self, "Error", "El correo es demasiado corto")
                self.correo_input.setFocus()
                return False
        
        # Validar grado
        if self.grado_combo.currentIndex() < 0:
            QMessageBox.warning(self, "Error", "Debe seleccionar un grado")
            self.grado_combo.setFocus()
            return False
        
        return True
    
    def save(self):
        """Guarda los datos del estudiante"""
        if not self.validate():
            return
        
        try:
            # Obtener y limpiar datos
            cedula = self.cedula_input.text().strip()
            nombre = self.nombre_input.text().strip().title()
            apellido = self.apellido_input.text().strip().title()
            fecha_nacimiento = self.fecha_nac_input.date().toString("yyyy-MM-dd")
            telefono = self.telefono_input.text().strip() or None
            correo = self.correo_input.text().strip().lower() or None
            pais = self.pais_input.text().strip() or None
            estado = self.estado_input.text().strip() or None
            municipio = self.municipio_input.text().strip() or None
            observacion = self.observacion_input.text().strip() or None
            id_grado = self.grado_combo.currentData()
            id_mencion = self.mencion_combo.currentData()
            seccion = self.seccion_combo.currentData()
            
            # DEBUG
            print("=" * 50)
            print("DATOS A GUARDAR:")
            print(f"Cédula: {cedula}")
            print(f"Nombre: {nombre}")
            print(f"Apellido: {apellido}")
            print(f"Fecha Nacimiento: {fecha_nacimiento}")
            print(f"Teléfono: {telefono}")
            print(f"Correo: {correo}")
            print(f"País: {pais}")
            print(f"Estado: {estado}")
            print(f"Municipio: {municipio}")
            print(f"Observación: {observacion}")
            print(f"ID Grado: {id_grado}")
            print(f"ID Mención: {id_mencion}")
            print(f"Sección: {seccion}")
            print(f"Es edición: {self.is_edit}")
            print("=" * 50)
            
            # Validar que se haya seleccionado un grado válido
            if id_grado is None:
                QMessageBox.critical(self, "Error", "Debe seleccionar un grado válido")
                return
            
            if self.is_edit:
                # Actualizar
                print(f"Actualizando estudiante con cédula: {self.estudiante['cedula']}")
                success = self.supabase_client.update_estudiante(
                    self.estudiante['cedula'],
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=fecha_nacimiento,
                    telefono=telefono,
                    correo=correo,
                    pais=pais,
                    estado=estado,
                    municipio=municipio,
                    observacion=observacion,
                    id_grado=id_grado,
                    id_mencion=id_mencion,
                    seccion=seccion
                )
                mensaje = "Estudiante actualizado correctamente"
            else:
                # Crear
                print("Creando nuevo estudiante...")
                success = self.supabase_client.create_estudiante(
                    cedula=cedula,
                    nombre=nombre,
                    apellido=apellido,
                    fecha_nacimiento=fecha_nacimiento,
                    telefono=telefono,
                    correo=correo,
                    pais=pais,
                    estado=estado,
                    municipio=municipio,
                    observacion=observacion,
                    id_grado=id_grado,
                    id_mencion=id_mencion,
                    seccion=seccion
                )
                mensaje = "Estudiante creado correctamente"
            
            print(f"Resultado de la operación: {success}")
            
            if success:
                QMessageBox.information(self, "Éxito", mensaje)
                self.accept()
            else:
                QMessageBox.critical(
                    self, 
                    "Error", 
                    "No se pudo guardar el estudiante. Verifica la consola para más detalles."
                )
                
        except ValueError as e:
            error_msg = f"Datos inválidos: {str(e)}"
            print(f"ERROR ValueError: {error_msg}")
            QMessageBox.critical(self, "Error de validación", error_msg)
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(f"ERROR Exception: {error_msg}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", error_msg)


class DocenteDialog(QDialog):
    """Diálogo para agregar o editar un docente"""
    
    def __init__(self, parent=None, supabase_client: SupabaseClient = None, docente: Optional[Dict] = None):
        super().__init__(parent)
        self.supabase_client = supabase_client
        self.docente = docente
        self.is_edit = docente is not None
        
        self.setWindowTitle("Editar Docente" if self.is_edit else "Nuevo Docente")
        self.setMinimumWidth(500)
        self.setup_ui()
        
        if self.is_edit:
            self.load_docente_data()
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Cédula
        self.cedula_input = QLineEdit()
        self.cedula_input.setPlaceholderText("Ej: 1234567890")
        form_layout.addRow("Cédula:*", self.cedula_input)
        
        # Nombre
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del docente")
        form_layout.addRow("Nombre:*", self.nombre_input)
        
        # Apellido
        self.apellido_input = QLineEdit()
        self.apellido_input.setPlaceholderText("Apellido del docente")
        form_layout.addRow("Apellido:*", self.apellido_input)
        
        # Correo
        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("correo@ejemplo.com")
        form_layout.addRow("Correo:", self.correo_input)
        
        # Teléfono
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Ej: 0999999999")
        form_layout.addRow("Teléfono:", self.telefono_input)
        
        # Especialidad
        self.especialidad_input = QLineEdit()
        self.especialidad_input.setPlaceholderText("Ej: Matemáticas, Lenguaje, etc.")
        form_layout.addRow("Especialidad:", self.especialidad_input)
        
        layout.addLayout(form_layout)
        
        # Nota de campos requeridos
        nota_label = QLabel("* Campos obligatorios")
        nota_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(nota_label)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def load_docente_data(self):
        """Carga los datos del docente a editar"""
        self.cedula_input.setText(self.docente['cedula'])
        self.cedula_input.setEnabled(False)
        self.cedula_input.setStyleSheet("background-color: #e0e0e0; color: #666;")
        
        self.nombre_input.setText(self.docente['nombre'])
        self.apellido_input.setText(self.docente['apellido'])
        self.correo_input.setText(self.docente['correo'] or '')
        self.telefono_input.setText(self.docente['telefono'] or '')
        self.especialidad_input.setText(self.docente['especialidad'] or '')
    
    def validate(self) -> bool:
        """Valida los datos del formulario"""
        
        # Validar cédula
        cedula = self.cedula_input.text().strip()
        if not cedula:
            QMessageBox.warning(self, "Error", "La cédula es obligatoria")
            self.cedula_input.setFocus()
            return False
        
        # Validar que la cédula sea numérica
        if not cedula.isdigit():
            QMessageBox.warning(self, "Error", "La cédula debe contener solo números")
            self.cedula_input.setFocus()
            return False
        
        # Validar longitud de cédula (10 dígitos)
        if len(cedula) < 7 or len(cedula) > 10:
            QMessageBox.warning(self, "Error", "La cédula debe tener entre 7 y 10 dígitos")
            self.cedula_input.setFocus()
            return False
        
        # Validar que la cédula no exista (solo al crear)
        if not self.is_edit:
            docente_existente = self.supabase_client.get_docente_by_cedula(cedula)
            if docente_existente:
                QMessageBox.warning(self, "Error", f"Ya existe un docente con la cédula {cedula}")
                self.cedula_input.setFocus()
                return False
        
        # Validar nombre
        nombre = self.nombre_input.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            self.nombre_input.setFocus()
            return False
        
        if len(nombre) < 2:
            QMessageBox.warning(self, "Error", "El nombre debe tener al menos 2 caracteres")
            self.nombre_input.setFocus()
            return False
        
        # Validar apellido
        apellido = self.apellido_input.text().strip()
        if not apellido:
            QMessageBox.warning(self, "Error", "El apellido es obligatorio")
            self.apellido_input.setFocus()
            return False
        
        if len(apellido) < 2:
            QMessageBox.warning(self, "Error", "El apellido debe tener al menos 2 caracteres")
            self.apellido_input.setFocus()
            return False
        
        # Validar teléfono (si se ingresó)
        telefono = self.telefono_input.text().strip()
        if telefono:
            telefono_limpio = telefono.replace("-", "").replace(" ", "")
            if not telefono_limpio.isdigit():
                QMessageBox.warning(self, "Error", "El teléfono debe contener solo números")
                self.telefono_input.setFocus()
                return False
            
            if len(telefono_limpio) < 7 or len(telefono_limpio) > 15:
                QMessageBox.warning(self, "Error", "El teléfono debe tener entre 7 y 15 dígitos")
                self.telefono_input.setFocus()
                return False
        
        # Validar correo (si se ingresó)
        correo = self.correo_input.text().strip()
        if correo:
            if "@" not in correo or "." not in correo.split("@")[-1]:
                QMessageBox.warning(self, "Error", "El formato del correo no es válido")
                self.correo_input.setFocus()
                return False
            
            if len(correo) < 5:
                QMessageBox.warning(self, "Error", "El correo es demasiado corto")
                self.correo_input.setFocus()
                return False
        
        # Validar especialidad (opcional pero recomendada)
        especialidad = self.especialidad_input.text().strip()
        if especialidad and len(especialidad) < 3:
            QMessageBox.warning(self, "Error", "La especialidad debe tener al menos 3 caracteres")
            self.especialidad_input.setFocus()
            return False
        
        return True
    
    def save(self):
        """Guarda los datos del docente"""
        if not self.validate():
            return
        
        try:
            cedula = self.cedula_input.text().strip()
            nombre = self.nombre_input.text().strip().title()
            apellido = self.apellido_input.text().strip().title()
            correo = self.correo_input.text().strip().lower() or None
            telefono = self.telefono_input.text().strip() or None
            especialidad = self.especialidad_input.text().strip() or None
            
            if self.is_edit:
                success = self.supabase_client.update_docente(
                    self.docente['cedula'],
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo,
                    telefono=telefono,
                    especialidad=especialidad
                )
                mensaje = "Docente actualizado correctamente"
            else:
                success = self.supabase_client.create_docente(
                    cedula,
                    nombre,
                    apellido,
                    correo,
                    telefono,
                    especialidad
                )
                mensaje = "Docente creado correctamente"
            
            if success:
                QMessageBox.information(self, "Éxito", mensaje)
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No se pudo guardar el docente. Verifica que los datos sean correctos."
                )
                
        except ValueError as e:
            QMessageBox.critical(self, "Error de validación", f"Datos inválidos: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado al guardar: {str(e)}")
            print(f"Error detallado: {e}")


class AsignaturaDialog(QDialog):
    """Diálogo para agregar o editar una asignatura"""
    
    def __init__(self, parent=None, supabase_client: SupabaseClient = None, asignatura: Optional[Dict] = None):
        super().__init__(parent)
        self.supabase_client = supabase_client
        self.asignatura = asignatura
        self.is_edit = asignatura is not None
        
        self.setWindowTitle("Editar Asignatura" if self.is_edit else "Nueva Asignatura")
        self.setMinimumWidth(500)
        self.setup_ui()
        
        if self.is_edit:
            self.load_asignatura_data()
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Código
        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("Ej: MAT-01-46070")
        form_layout.addRow("Código:*", self.codigo_input)
        
        # Nombre
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre de la asignatura")
        form_layout.addRow("Nombre:*", self.nombre_input)
        
        # Mención
        self.mencion_combo = QComboBox()
        self.mencion_combo.addItem("Seleccione una mención", None)
        self.mencion_combo.addItem("1 - Media General", 1)
        self.mencion_combo.addItem("2 - Técnico Superior", 2)
        form_layout.addRow("Mención:*", self.mencion_combo)
        
        # Grado
        self.grado_combo = QComboBox()
        self.load_grados()
        form_layout.addRow("Grado:*", self.grado_combo)
        
        # Docente
        self.docente_combo = QComboBox()
        self.load_docentes()
        form_layout.addRow("Docente:", self.docente_combo)
        
        layout.addLayout(form_layout)
        
        # Nota de campos requeridos
        nota_label = QLabel("* Campos obligatorios")
        nota_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(nota_label)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def load_grados(self):
        """Carga los grados disponibles"""
        self.grado_combo.clear()
        grados = self.supabase_client.get_all_grados()
        for grado in grados:
            self.grado_combo.addItem(grado['nombre_grado'], grado['id_grado'])
    
    def load_docentes(self):
        """Carga los docentes disponibles"""
        self.docente_combo.clear()
        self.docente_combo.addItem("Sin asignar", None)  
        docentes = self.supabase_client.get_all_docentes()
        for docente in docentes:
            nombre_completo = f"{docente['nombre']} {docente['apellido']}"
            self.docente_combo.addItem(nombre_completo, docente['cedula'])
    
    def load_asignatura_data(self):
        """Carga los datos de la asignatura a editar"""
        self.codigo_input.setText(self.asignatura['codigo'])
        self.codigo_input.setEnabled(False)  # No permitir editar código
        self.codigo_input.setStyleSheet("background-color: #e0e0e0; color: #666;")
        
        self.nombre_input.setText(self.asignatura['nombre_asignatura'])
        
        # Seleccionar mención
        id_mencion = self.asignatura.get('id_mencion')
        if id_mencion:
            mencion_index = self.mencion_combo.findData(id_mencion)
            if mencion_index >= 0:
                self.mencion_combo.setCurrentIndex(mencion_index)
        
        # Seleccionar grado
        index = self.grado_combo.findData(self.asignatura.get('id_grado'))
        if index >= 0:
            self.grado_combo.setCurrentIndex(index)
        
        # Seleccionar docente (incluyendo opción "Sin asignar")
        cedula_docente = self.asignatura.get('cedula_docente')
        if cedula_docente:
            docente_index = self.docente_combo.findData(cedula_docente)
            if docente_index >= 0:
                self.docente_combo.setCurrentIndex(docente_index)
            else:
                # Si el docente no existe, seleccionar "Sin asignar"
                self.docente_combo.setCurrentIndex(0)
        else:
            # Si no tiene docente asignado, seleccionar "Sin asignar"
            self.docente_combo.setCurrentIndex(0)

    
    def validate(self) -> bool:
        """Valida los datos del formulario"""
        
        # Validar código
        codigo = self.codigo_input.text().strip()
        if not codigo:
            QMessageBox.warning(self, "Error", "El código es obligatorio")
            self.codigo_input.setFocus()
            return False
        
        if len(codigo) < 3:
            QMessageBox.warning(self, "Error", "El código debe tener al menos 3 caracteres")
            self.codigo_input.setFocus()
            return False
        
        # Validar formato de código (solo letras, números y guiones)
        if not all(c.isalnum() or c in ['-', '_'] for c in codigo):
            QMessageBox.warning(
                self, 
                "Error", 
                "El código solo puede contener letras, números, guiones (-) y guiones bajos (_)"
            )
            self.codigo_input.setFocus()
            return False
        
        # Validar que el código no exista (solo al crear)
        if not self.is_edit:
            asignatura_existente = self.supabase_client.get_asignatura_by_codigo(codigo)
            if asignatura_existente:
                QMessageBox.warning(self, "Error", f"Ya existe una asignatura con el código {codigo}")
                self.codigo_input.setFocus()
                return False
        
        # Validar nombre
        nombre = self.nombre_input.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre de la asignatura es obligatorio")
            self.nombre_input.setFocus()
            return False
        
        if len(nombre) < 3:
            QMessageBox.warning(self, "Error", "El nombre debe tener al menos 3 caracteres")
            self.nombre_input.setFocus()
            return False
        
        # Validar mención
        if self.mencion_combo.currentData() is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar una mención")
            self.mencion_combo.setFocus()
            return False
        
        # Validar grado
        if self.grado_combo.currentData() is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar un grado")
            self.grado_combo.setFocus()
            return False
        
        # Validar docente (OPCIONAL - el docente puede ser None)
        # Si quieres que sea obligatorio, descomenta estas líneas:
        # if self.docente_combo.currentData() is None:
        #     QMessageBox.warning(self, "Error", "Debe seleccionar un docente")
        #     self.docente_combo.setFocus()
        #     return False
        
        return True

    
    def save(self):
        """Guarda los datos de la asignatura"""
        if not self.validate():
            return
        
        try:
            # Obtener y limpiar datos
            codigo = self.codigo_input.text().strip()
            nombre = self.nombre_input.text().strip()
            id_mencion = self.mencion_combo.currentData()
            id_grado = self.grado_combo.currentData()
            cedula_docente = self.docente_combo.currentData()
            
            # DEBUG
            print("=" * 50)
            print("DATOS DE ASIGNATURA A GUARDAR:")
            print(f"Código: {codigo}")
            print(f"Nombre: {nombre}")
            print(f"ID Mención: {id_mencion}")
            print(f"ID Grado: {id_grado}")
            print(f"Cédula Docente: {cedula_docente}")
            print(f"Es edición: {self.is_edit}")
            print("=" * 50)
            
            if self.is_edit:
                # Actualizar
                success = self.supabase_client.update_asignatura(
                    codigo,
                    nombre_asignatura=nombre,
                    id_mencion=id_mencion,
                    id_grado=id_grado,
                    cedula_docente=cedula_docente
                )
                mensaje = "Asignatura actualizada correctamente"
            else:
                # Crear
                success = self.supabase_client.create_asignatura(
                    codigo=codigo,
                    nombre_asignatura=nombre,
                    id_mencion=id_mencion,
                    id_grado=id_grado,
                    cedula_docente=cedula_docente
                )
                mensaje = "Asignatura creada correctamente"
            
            if success:
                QMessageBox.information(self, "Éxito", mensaje)
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No se pudo guardar la asignatura. Verifica la consola para más detalles."
                )
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
            import traceback
            traceback.print_exc()

class GradoDialog(QDialog):
    """Diálogo para agregar un grado"""
    
    def __init__(self, parent=None, supabase_client: SupabaseClient = None):
        super().__init__(parent)
        self.supabase_client = supabase_client
        
        self.setWindowTitle("Nuevo Grado")
        self.setMinimumWidth(400)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Nombre del grado
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ej: 1ro Básica, 2do Básica, etc.")
        form_layout.addRow("Nombre del Grado:*", self.nombre_input)
        
        layout.addLayout(form_layout)
        
        # Nota de campos requeridos
        nota_label = QLabel("* Campos obligatorios")
        nota_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(nota_label)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def validate(self) -> bool:
        """Valida los datos del formulario"""
        if not self.nombre_input.text().strip():
            QMessageBox.warning(self, "Error", "El nombre del grado es obligatorio")
            return False
        return True
    
    def save(self):
        """Guarda los datos del grado"""
        if not self.validate():
            return
        
        try:
            nombre = self.nombre_input.text().strip()
            
            if self.supabase_client.create_grado(nombre):
                QMessageBox.information(self, "Éxito", "Grado creado correctamente")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo crear el grado")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")


class PeriodoDialog(QDialog):
    """Diálogo para agregar un período académico"""
    
    def __init__(self, parent=None, supabase_client: SupabaseClient = None):
        super().__init__(parent)
        self.supabase_client = supabase_client
        
        self.setWindowTitle("Nuevo Período Académico")
        self.setMinimumWidth(400)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Año
        self.anio_input = QLineEdit()
        self.anio_input.setPlaceholderText("Ej: 2024")
        form_layout.addRow("Año:*", self.anio_input)
        
        # Fecha inicio
        self.fecha_inicio_input = QDateEdit()
        self.fecha_inicio_input.setCalendarPopup(True)
        self.fecha_inicio_input.setDate(QDate.currentDate())
        self.fecha_inicio_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Fecha Inicio:*", self.fecha_inicio_input)
        
        # Fecha fin
        self.fecha_fin_input = QDateEdit()
        self.fecha_fin_input.setCalendarPopup(True)
        self.fecha_fin_input.setDate(QDate.currentDate().addMonths(6))
        self.fecha_fin_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Fecha Fin:*", self.fecha_fin_input)
        
        layout.addLayout(form_layout)
        
        # Nota de campos requeridos
        nota_label = QLabel("* Campos obligatorios")
        nota_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(nota_label)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def validate(self) -> bool:
        """Valida los datos del formulario"""
        if not self.anio_input.text().strip():
            QMessageBox.warning(self, "Error", "El año es obligatorio")
            return False
        
        try:
            anio = int(self.anio_input.text().strip())
            if anio < 2000 or anio > 2100:
                QMessageBox.warning(self, "Error", "El año debe estar entre 2000 y 2100")
                return False
        except ValueError:
            QMessageBox.warning(self, "Error", "El año debe ser un número válido")
            return False
        
        if self.fecha_inicio_input.date() >= self.fecha_fin_input.date():
            QMessageBox.warning(self, "Error", "La fecha de inicio debe ser anterior a la fecha de fin")
            return False
        
        return True
    
    def save(self):
        """Guarda los datos del período"""
        if not self.validate():
            return
        
        try:
            anio = int(self.anio_input.text().strip())
            fecha_inicio = self.fecha_inicio_input.date().toString("yyyy-MM-dd")
            fecha_fin = self.fecha_fin_input.date().toString("yyyy-MM-dd")
            
            if self.supabase_client.create_periodo(anio, fecha_inicio, fecha_fin):
                QMessageBox.information(self, "Éxito", "Período académico creado correctamente")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo crear el período")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")


class CalificacionesDialog(QDialog):
    """Diálogo para gestionar calificaciones de un estudiante"""
    
    def __init__(self, parent=None, supabase_client: SupabaseClient = None):
        super().__init__(parent)
        self.supabase_client = supabase_client
        self.calificaciones_data = []
        
        self.setWindowTitle("Gestionar Calificaciones")
        self.setMinimumWidth(900)
        self.setMinimumHeight(600)
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Sección de búsqueda de estudiante
        search_layout = QHBoxLayout()
        
        cedula_label = QLabel("Cédula del Estudiante:*")
        search_layout.addWidget(cedula_label)
        
        self.cedula_input = QLineEdit()
        self.cedula_input.setPlaceholderText("Ej: 1234567890")
        self.cedula_input.setMaximumWidth(200)
        search_layout.addWidget(self.cedula_input)
        
        buscar_btn = QPushButton("🔍 Buscar")
        buscar_btn.clicked.connect(self.load_calificaciones)
        search_layout.addWidget(buscar_btn)
        
        search_layout.addStretch()
        
        layout.addLayout(search_layout)
        
        # Label para mostrar información del estudiante
        self.estudiante_info_label = QLabel("")
        self.estudiante_info_label.setStyleSheet("color: #2196F3; font-weight: bold; padding: 10px;")
        layout.addWidget(self.estudiante_info_label)
        
        # Tabla de calificaciones (editable)
        self.calificaciones_table = QTableWidget()
        self.calificaciones_table.setColumnCount(8)
        self.calificaciones_table.setHorizontalHeaderLabels([
            "Materia", "Nota 1", "Ajuste 1", 
            "Nota 2", "Ajuste 2", "Nota 3", 
            "Ajuste 3", "Nota Final"
            ])
        self.calificaciones_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.calificaciones_table.verticalHeader().setDefaultSectionSize(48)
        
        # Hacer editables solo las columnas de notas y ajustes (columnas 1-6)
        self.calificaciones_table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.calificaciones_table.itemChanged.connect(self.recalcular_nota_final)
        layout.addWidget(self.calificaciones_table)
        
        # Botones de acción
        buttons = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Apply | 
        QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Apply).setText("Aplicar Cambios")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        buttons.clicked.connect(self.handle_button_click)
        layout.addWidget(buttons)


    def load_calificaciones(self):
        """Carga las calificaciones del estudiante por cédula"""
        cedula = self.cedula_input.text().strip()
        
        if not cedula:
            QMessageBox.warning(self, "Error", "Debe ingresar una cédula")
            return
        
        # Obtener información del estudiante
        estudiante = self.supabase_client.get_estudiante_by_cedula(cedula)
        if not estudiante:
            QMessageBox.warning(self, "Error", "No se encontró un estudiante con esa cédula")
            self.estudiante_info_label.setText("")
            self.calificaciones_table.setRowCount(0)
            return
        
        # Mostrar info del estudiante
        self.estudiante_info_label.setText(
            f"Estudiante: {estudiante['nombre']} {estudiante['apellido']} - Año: {estudiante['nombre_grado']}"
        )
        
        # Cargar calificaciones
        self.calificaciones_data = self.supabase_client.get_calificaciones_by_estudiante(cedula)
        self.populate_table()

    def populate_table(self):
        """Llena la tabla con las calificaciones"""
        self.calificaciones_table.setRowCount(0)
        
        for cal in self.calificaciones_data:
            row = self.calificaciones_table.rowCount()
            self.calificaciones_table.insertRow(row)
            
            # Materia (no editable)
            materia_item = QTableWidgetItem(cal['nombre_asignatura'])
            materia_item.setFlags(materia_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.calificaciones_table.setItem(row, 0, materia_item)
            
            # Notas y ajustes (editables)
            self.calificaciones_table.setItem(row, 1, QTableWidgetItem(str(cal['nota_1']) if cal['nota_1'] else ''))
            self.calificaciones_table.setItem(row, 2, QTableWidgetItem(str(cal['ajuste_1']) if cal['ajuste_1'] else '0'))
            self.calificaciones_table.setItem(row, 3, QTableWidgetItem(str(cal['nota_2']) if cal['nota_2'] else ''))
            self.calificaciones_table.setItem(row, 4, QTableWidgetItem(str(cal['ajuste_2']) if cal['ajuste_2'] else '0'))
            self.calificaciones_table.setItem(row, 5, QTableWidgetItem(str(cal['nota_3']) if cal['nota_3'] else ''))
            self.calificaciones_table.setItem(row, 6, QTableWidgetItem(str(cal['ajuste_3']) if cal['ajuste_3'] else '0'))
            
            # Nota final (no editable, se calcula automáticamente)
            nota_final_item = QTableWidgetItem(str(cal['nota_final']) if cal['nota_final'] else '0')
            nota_final_item.setFlags(nota_final_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.calificaciones_table.setItem(row, 7, nota_final_item)
            self.calificaciones_table.itemChanged.connect(self.recalcular_nota_final)


    def recalcular_nota_final(self, item):
        """Recalcula la nota final cuando se edita una nota o ajuste"""
        # Solo recalcular si se editó una columna de nota o ajuste (1, 2, 3, 4, 5, 6)
        if item.column() not in [1, 2, 3, 4, 5, 6]:
            return
        
        row = item.row()
        
        try:
            # Obtener las notas y ajustes
            nota_1_text = self.calificaciones_table.item(row, 1).text().strip()
            ajuste_1_text = self.calificaciones_table.item(row, 2).text().strip()
            nota_2_text = self.calificaciones_table.item(row, 3).text().strip()
            ajuste_2_text = self.calificaciones_table.item(row, 4).text().strip()
            nota_3_text = self.calificaciones_table.item(row, 5).text().strip()
            ajuste_3_text = self.calificaciones_table.item(row, 6).text().strip()
            
            # Calcular cada nota con su ajuste
            notas_finales = []
            
            # Nota 1 + Ajuste 1
            if nota_1_text:
                nota_1 = float(nota_1_text)
                # Validar que la nota esté entre 0 y 20
                if not (0 <= nota_1 <= 20):
                    QMessageBox.warning(self, "Error", "La Nota 1 debe estar entre 0 y 20")
                    self.calificaciones_table.item(row, 1).setText("")
                    return
                
                ajuste_1 = float(ajuste_1_text) if ajuste_1_text else 0.0
                # Validar que el ajuste esté entre -5 y 5
                if not (-5 <= ajuste_1 <= 5):
                    QMessageBox.warning(self, "Error", "El Ajuste 1 debe estar entre -5 y 5")
                    self.calificaciones_table.item(row, 2).setText("0")
                    return
                
                nota_final_1 = nota_1 + ajuste_1
                # Validar que la nota final no sea negativa ni mayor a 10
                if nota_final_1 < 0:
                    nota_final_1 = 0
                elif nota_final_1 > 20:
                    nota_final_1 = 20
                
                notas_finales.append(nota_final_1)
            
            # Nota 2 + Ajuste 2
            if nota_2_text:
                nota_2 = float(nota_2_text)
                # Validar que la nota esté entre 0 y 20
                if not (0 <= nota_2 <= 20):
                    QMessageBox.warning(self, "Error", "La Nota 2 debe estar entre 0 y 20")
                    self.calificaciones_table.item(row, 3).setText("")
                    return
                
                ajuste_2 = float(ajuste_2_text) if ajuste_2_text else 0.0
                # Validar que el ajuste esté entre -5 y 5
                if not (-5 <= ajuste_2 <= 5):
                    QMessageBox.warning(self, "Error", "El Ajuste 2 debe estar entre -5 y 5")
                    self.calificaciones_table.item(row, 4).setText("0")
                    return
                
                nota_final_2 = nota_2 + ajuste_2
                # Validar que la nota final no sea negativa ni mayor a 20
                if nota_final_2 < 0:
                    nota_final_2 = 0
                elif nota_final_2 > 20:
                    nota_final_2 = 20
                
                notas_finales.append(nota_final_2)
            
            # Nota 3 + Ajuste 3
            if nota_3_text:
                nota_3 = float(nota_3_text)
                # Validar que la nota esté entre 0 y 20
                if not (0 <= nota_3 <= 20):
                    QMessageBox.warning(self, "Error", "La Nota 3 debe estar entre 0 y 20")
                    self.calificaciones_table.item(row, 5).setText("")
                    return
                
                ajuste_3 = float(ajuste_3_text) if ajuste_3_text else 0.0
                # Validar que el ajuste esté entre -5 y 5
                if not (-5 <= ajuste_3 <= 5):
                    QMessageBox.warning(self, "Error", "El Ajuste 3 debe estar entre -5 y 5")
                    self.calificaciones_table.item(row, 6).setText("0")
                    return
                
                nota_final_3 = nota_3 + ajuste_3
                # Validar que la nota final no sea negativa ni mayor a 20
                if nota_final_3 < 0:
                    nota_final_3 = 0
                elif nota_final_3 > 20:
                    nota_final_3 = 20
                
                notas_finales.append(nota_final_3)
            
            # Calcular promedio de las notas finales
            if notas_finales:
                nota_final = sum(notas_finales) / len(notas_finales)
                self.calificaciones_table.item(row, 7).setText(f"{nota_final:.2f}")
            else:
                self.calificaciones_table.item(row, 7).setText("0.00")
                
        except ValueError:
            # Si hay (texto no numérico)
            QMessageBox.warning(self, "Error", "Debe ingresar valores numéricos válidos")
            item.setText("")
        except AttributeError:
            # Si hay error al acceder a los items
            pass

    def handle_button_click(self, button):
        """Maneja los clicks en los botones"""
        role = button.parent().buttonRole(button)
            
        if role == QDialogButtonBox.ButtonRole.ApplyRole:
            self.save_calificaciones()
        elif role == QDialogButtonBox.ButtonRole.RejectRole:
           self.reject()

    def save_calificaciones(self):
        """Guarda todas las calificaciones modificadas"""
        if not self.calificaciones_data:
            QMessageBox.warning(self, "Error", "No hay calificaciones para guardar")
            return
        
        try:
            for row in range(self.calificaciones_table.rowCount()):
                cal = self.calificaciones_data[row]
                
                # Obtener valores de la tabla
                nota_1 = self.calificaciones_table.item(row, 1).text() or None
                ajuste_1 = self.calificaciones_table.item(row, 2).text() or '0'
                nota_2 = self.calificaciones_table.item(row, 3).text() or None
                ajuste_2 = self.calificaciones_table.item(row, 4).text() or '0'
                nota_3 = self.calificaciones_table.item(row, 5).text() or None
                ajuste_3 = self.calificaciones_table.item(row, 6).text() or '0'
                
                # Convertir a números
                nota_1 = float(nota_1) if nota_1 else None
                ajuste_1 = float(ajuste_1)
                nota_2 = float(nota_2) if nota_2 else None
                ajuste_2 = float(ajuste_2)
                nota_3 = float(nota_3) if nota_3 else None
                ajuste_3 = float(ajuste_3)
                
                # Actualizar en la base de datos
                self.supabase_client.update_calificacion(
                    cal['codigo_calificacion'],
                    nota_1=nota_1,
                    ajuste_1=ajuste_1,
                    nota_2=nota_2,
                    ajuste_2=ajuste_2,
                    nota_3=nota_3,
                    ajuste_3=ajuste_3
                )
            
            QMessageBox.information(self, "Éxito", "Calificaciones actualizadas correctamente")
            self.accept()
            
        except ValueError:
            QMessageBox.critical(self, "Error", "Las notas deben ser números válidos")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
