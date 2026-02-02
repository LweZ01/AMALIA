from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QTabWidget, QTableWidget,
                            QTableWidgetItem, QHeaderView, QMessageBox, QFrame,
                            QLineEdit, QComboBox, QDialog, QFormLayout, QDateEdit, QInputDialog,
                            QCheckBox, QScrollArea)
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFont, QIcon, QColor
from database.supabase_client import SupabaseClient
from typing import Dict, Any, List
from models.dialogs import (EstudianteDialog, DocenteDialog, AsignaturaDialog,
                        GradoDialog, PeriodoDialog, CalificacionesDialog)
import re

class MainWindow(QMainWindow):

    #FUNCIONES DE INICIALIZACIÓN Y AUXILIARES

    """Ventana principal para administradores"""
    
    def __init__(self, supabase_client: SupabaseClient, user_data: Dict[str, Any]):
        super().__init__()
        self.supabase_client = supabase_client
        self.user_data = user_data
        
        # ============ VARIABLES DE PAGINACIÓN ============
        self.estudiantes_por_pagina = 50
        self.pagina_actual_estudiantes = 0
        self.total_estudiantes = 0
        self.estudiantes_filtrados = []
        
        # ============ VARIABLES DE PAGINACIÓN ASIGNATURAS ============
        self.asignaturas_por_pagina = 50
        self.pagina_actual_asignaturas = 0
        self.total_asignaturas = 0
        self.asignaturas_filtradas = []
        
        # ============ VARIABLES DE PAGINACIÓN GRADOS ============
        self.estudiantes_grado_por_pagina = 50
        self.pagina_actual_grado = 0
        self.total_estudiantes_grado = 0
        self.estudiantes_grado_filtrados = []
        
        # ============ VARIABLES DE CHECKBOXES ============
        self.checkboxes_estudiantes = []  
        self.select_all_checkbox = None    
        self.grado_actual_mostrado = None  
        
        self.setup_ui()
        self.load_initial_data()

    def logout(self):
        """Cierra sesión y vuelve al login"""
        reply = QMessageBox.question(
            self, 'Cerrar Sesión',
            '¿Está seguro de cerrar sesión?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow(self.supabase_client)
            self.login_window.show()
            self.close()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.setWindowTitle("AMALIA - Panel de Administración")
        self.setMinimumSize(1200, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        # Barra superior
        self.create_header(main_layout)
        
        # Pestañas principales
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        main_layout.addWidget(self.tabs)
        
        # Crear pestañas
        self.create_estudiantes_tab()
        self.create_docentes_tab()
        self.create_asignaturas_tab()
        self.create_calificaciones_tab()
        self.create_grados_tab()
        self.create_periodos_tab()
        self.create_historial_tab()
        
        # Centrar ventana
        self.center_window()
        # Aplicar estilos globales
        # Reemplaza el setStyleSheet() en setup_ui() con este código completo:

        self.setStyleSheet("""
            /* Campos de texto */
            QLineEdit {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                border: 1px solid #2563eb;
                background-color: white;
            }
            
            /* Pestañas */
            QTabWidget::pane {
                border: none;
                background-color: #f0f4f8;
            }
            
            QTabBar::tab {
                background-color: #dae3ed;
                color: #4a5568;
                padding: 10px 20px;
                border: none;
                border-bottom: 2px solid transparent;
                font-size: 14px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: #f0f4f8;
                color: #0d1f3d;
                border-bottom: 2px solid #2563eb;
                font-weight: bold;
            }
            
            QTabBar::tab:hover {
                background-color: #c9d6e3;
                color: #0d1f3d;
            }
            
            /* Tablas */
            QTableWidget {
                border: 2px solid #2563eb;
                border-radius: 8px;
                background-color: white;
                gridline-color: #e5e7eb;
            }
            
            QTableWidget::item {
                padding: 8px;
                font-size: 13px;
                color: #333;
                background-color: white;
            }
            
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1565c0;
            }
            
            /* Headers de tabla */
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #1f2937;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
                font-size: 13px;
            }
            
            /* Números de fila */
            QHeaderView::section:vertical {
                background-color: #f8f9fa;
                color: #666;
                padding: 5px;
                border: none;
                border-right: 1px solid #e0e0e0;
                border-bottom: 1px solid #f0f0f0;
                font-size: 12px;
                min-width: 40px;
                max-width: 40px;
            }
            
            QTableCornerButton::section {
                background-color: #f8f9fa;
                border: none;
            }
            
            /* Scrollbars */
            QScrollBar:vertical {
                background: #f0f4f8;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            
            QScrollBar:horizontal {
                background: #f0f4f8;
                height: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:horizontal {
                background: #cbd5e1;
                border-radius: 6px;
                min-width: 20px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: #94a3b8;
            }
            
            QScrollBar::add-line, QScrollBar::sub-line {
                border: none;
                background: none;
            }
            
            /* ============ ESTILOS DE BOTONES ============ */
            
            /* Botones principales */
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
                min-width: 120px;
            }
            
            /* Botones de acción (pequeños, en tablas) */
            QPushButton#action_btn {
                padding: 2px 4px;
                font-size: 14px;
                min-width: 23px;
                max-width: 25px;
                min-height: 23px;
                max-height: 25px;
                border-radius: 4px;
                
            }
            
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            
            QPushButton:pressed {
                background-color: #1e40af;
            }
            
            QPushButton:disabled {
                background-color: #cbd5e1;
                color: #94a3b8;
            }
            
            /* Botón de cerrar sesión */
            QPushButton#logout_btn {
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                min-width: 100px;
            }
            
            QPushButton#logout_btn:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            
            /* Botón de volver */
            QPushButton#volver_btn {
                background-color: #64748b;
            }
            
            QPushButton#volver_btn:hover {
                background-color: #475569;
            }
            
            /* Botón de búsqueda */
            QPushButton#search_btn {
                background-color: #10b981;
                min-width: 100px;
            }
            
            QPushButton#search_btn:hover {
                background-color: #059669;
            }
            
            /* Botón de actualizar */
            QPushButton#refresh_btn {
                background-color: #2563eb;
                min-width: 100px;
            }
            
            QPushButton#refresh_btn:hover {
                background-color: #1d4ed8;
            }
            
            /* Botón de agregar */
            QPushButton#add_btn {
                background-color: #2563eb;
            }
            
            QPushButton#add_btn:hover {
                background-color: #1d4ed8;
            }
            
            /* Botón de mover seleccionados */
            QPushButton#mover_btn {
                background-color: #2196F3;
                font-weight: bold;
                padding: 8px 16px;
            }
            
            QPushButton#mover_btn:hover {
                background-color: #1976D2;
            }
            /* Campos de fecha (DateEdit) */
            QDateEdit {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #333;
            }
            QDateEdit:focus {
                border: 1px solid #2563eb;
                background-color: white;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #e0e0e0;
                border-radius: 0 6px 6px 0;
            }
            
            /* Combos (QComboBox) */
            QComboBox {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #333;
                min-height: 40px;
            }
            QComboBox:focus {
                border: 1px solid #2563eb;
                background-color: white;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #e0e0e0;
                border-radius: 0 6px 6px 0;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 4px;
                selection-background-color: #e3f2fd;
                selection-color: #1565c0;
            }
        """)
    def center_window(self):
        """Centra la ventana en la pantalla"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def extraer_numero_grado(self, nombre_grado):
        """Extrae el número del grado para ordenamiento"""
        if not nombre_grado:
            return 999
        
        nombre = nombre_grado.lower()
        
        # Mapear nombres comunes
        if '1er' in nombre or '1ro' in nombre or 'primero' in nombre:
            return 1
        elif '2do' in nombre or '2ndo' in nombre or 'segundo' in nombre:
            return 2
        elif '3er' in nombre or '3ro' in nombre or 'tercero' in nombre:
            return 3
        elif '4to' in nombre or 'cuarto' in nombre:
            return 4
        elif '5to' in nombre or 'quinto' in nombre:
            return 5
        elif '6to' in nombre or 'sexto' in nombre:
            return 6
        elif 'egresado' in nombre or 'graduado' in nombre:
            return 7
        
        # Buscar el primer número en el nombre del grado
        import re
        match = re.search(r'(\d+)', nombre)
        if match:
            return int(match.group(1))

        return 999  # coloca al final

    def show_error(self, message: str):
        """Muestra un mensaje de error"""
        QMessageBox.critical(self, "Error", message)

    def show_success(self, message: str):
        """Muestra un mensaje de éxito"""
        QMessageBox.information(self, "Éxito", message)

    def show_info(self, message: str):
        """Muestra un mensaje informativo"""
        QMessageBox.information(self, "Información", message)

    def get_estudiantes_seleccionados(self):
        """Obtiene las cédulas de los estudiantes seleccionados (VERSIÓN ANTI-FANTASMA)"""

        if not hasattr(self, 'checkboxes_estudiantes'):
            self.checkboxes_estudiantes = []
            return []
        
        if not self.checkboxes_estudiantes:
            return []
        
        seleccionados = []
        checkboxes_validos = 0
        
        for i, checkbox in enumerate(self.checkboxes_estudiantes):
            if checkbox is None:
                continue
            
            try:
                # Verificar si el checkbox todavía existe en la UI
                if not checkbox.isVisible():
                    continue
                
                checkboxes_validos += 1
                is_checked = checkbox.isChecked()
                cedula = checkbox.property('cedula')
                
                if is_checked and cedula:
                    seleccionados.append(cedula)
                    
            except RuntimeError as e:
                
                continue
            except Exception as e:
                continue
        
        return seleccionados

    def toggle_select_all(self, state):
        """Selecciona o deselecciona todos los checkboxes (VERSIÓN ANTI-FANTASMA)"""
        
        if not hasattr(self, 'checkboxes_estudiantes'):
            self.checkboxes_estudiantes = []
            return
        
        if not self.checkboxes_estudiantes:
            return
        
        is_checked = (state == Qt.CheckState.Checked.value or state == Qt.CheckState.Checked)
        
        modificados = 0
        errores = 0
        
        for i, checkbox in enumerate(self.checkboxes_estudiantes):
            if checkbox is None:
                errores += 1
                continue
            
            try:
                if checkbox.isVisible():
                    checkbox.setChecked(is_checked)
                    modificados += 1
                else:
                    errores += 1
            except RuntimeError:
                errores += 1
            except Exception as e:
                errores += 1
        
    def mover_estudiantes_seleccionados(self, grado_actual):
        """Mueve todos los estudiantes seleccionados a otro grado (VERSIÓN ANTI-FANTASMA)"""
        
        #  OBTENER ESTUDIANTES SELECCIONADOS (con verificación)
        estudiantes_seleccionados = self.get_estudiantes_seleccionados()
        
        if not estudiantes_seleccionados:
            QMessageBox.warning(
                self, 
                "Sin selección", 
                " No hay estudiantes seleccionados.\n\n"
                "Por favor, marque al menos un estudiante usando los checkboxes."
            )
            return
        
        # Obtener todos los grados
        grados = self.supabase_client.get_all_grados()
        
        # Filtrar el grado actual
        grados_disponibles = [g for g in grados if g['id_grado'] != grado_actual]
        
        if not grados_disponibles:
            QMessageBox.warning(self, "Error", "No hay otros grados disponibles")
            return
        
        # Crear lista de nombres de grados
        nombres_grados = [g['nombre_grado'] for g in grados_disponibles]
        
        # Mostrar diálogo de selección
        nuevo_grado_nombre, ok = QInputDialog.getItem(
            self,
            "Mover Estudiantes Seleccionados",
            f" {len(estudiantes_seleccionados)} estudiante(s) seleccionado(s)\n\n"
            f"Seleccione el nuevo grado:",
            nombres_grados,
            0,
            False
        )
        
        if ok and nuevo_grado_nombre:
            # Encontrar el ID del nuevo grado
            nuevo_grado_id = next(
                (g['id_grado'] for g in grados_disponibles if g['nombre_grado'] == nuevo_grado_nombre),
                None
            )
            
            if nuevo_grado_id:
                # Confirmar acción
                reply = QMessageBox.question(
                    self, 
                    'Confirmar movimiento',
                    f'¿Está seguro de mover {len(estudiantes_seleccionados)} estudiante(s) a {nuevo_grado_nombre}?\n\n'
                    f'Esta acción no se puede deshacer.',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    
                    # Mover cada estudiante seleccionado
                    exitosos = 0
                    fallidos = 0
                    
                    for cedula in estudiantes_seleccionados:
                        try:
                            if self.supabase_client.update_estudiante(cedula, id_grado=nuevo_grado_id):
                                exitosos += 1
                            else:
                                fallidos += 1
                        except Exception as e:
                            fallidos += 1
                    
                    # Mostrar resultado
                    mensaje = f" Se movieron {exitosos} estudiantes correctamente"
                    if fallidos > 0:
                        mensaje += f"\n {fallidos} estudiantes NO se pudieron mover"
                    
                    QMessageBox.information(self, "Resultado", mensaje)
                    
                    #  RECARGAR VISTA ACTUAL
                    grado_actual_obj = next((g for g in grados if g['id_grado'] == grado_actual), None)
                    if grado_actual_obj:
                        self.mostrar_estudiantes_grado(grado_actual_obj)
                    
                    #  ACTUALIZAR BOTONES DE GRADOS
                    self.load_grados_tab()
            else:
                QMessageBox.critical(self, "Error", "No se pudo obtener el ID del nuevo grado")

    def get_historial_academico(self, cedula_estudiante: str) -> List[Dict[str, Any]]:
        """Obtiene el historial académico de un estudiante"""
        query = """
            SELECT ha.id_historial, ha.cedula_estudiante, ha.codigo_asignatura,
                ha.nombre_asignatura, g.nombre_grado, ha.nota_final,
                ha.estado, ha.fecha_curso,
                e.nombre, e.apellido
            FROM historial_academico ha
            JOIN estudiante e ON ha.cedula_estudiante = e.cedula
            JOIN grado g ON ha.id_grado = g.id_grado
            WHERE ha.cedula_estudiante = %s
            ORDER BY ha.id_grado, ha.fecha_curso DESC
        """
        return self.execute_query(query, (cedula_estudiante,))

    # FUNCIONES DE CARGA DE DATOS

    def load_initial_data(self):
        """Carga los datos iniciales"""
        self.load_estudiantes()
        self.load_docentes()
        self.load_asignaturas()
        self.load_grados_tab()
        self.load_periodos()

    def load_estudiantes(self, reset_pagina=True):
        """Carga la lista de estudiantes CON PAGINACIÓN"""
        
        if reset_pagina:
            self.pagina_actual_estudiantes = 0
        
        # Obtener TODOS los estudiantes
        estudiantes = self.supabase_client.get_all_estudiantes()
        
        # Ordenar correctamente
        estudiantes_ordenados = sorted(
            estudiantes,
            key=lambda x: self.extraer_numero_grado(x.get('nombre_grado', ''))
        )
        
        # Guardar total
        self.total_estudiantes = len(estudiantes_ordenados)
        self.estudiantes_filtrados = estudiantes_ordenados
        
        # Calcular paginación
        total_paginas = max(1, (self.total_estudiantes + self.estudiantes_por_pagina - 1) // self.estudiantes_por_pagina)
        
        # Ajustar página actual si es necesario
        if self.pagina_actual_estudiantes >= total_paginas:
            self.pagina_actual_estudiantes = max(0, total_paginas - 1)
        
        # Calcular índices
        inicio = self.pagina_actual_estudiantes * self.estudiantes_por_pagina
        fin = min(inicio + self.estudiantes_por_pagina, self.total_estudiantes)
        
        # Obtener estudiantes de la página actual
        estudiantes_pagina = estudiantes_ordenados[inicio:fin]
        
        # Limpiar tabla
        self.estudiantes_table.setRowCount(0)
        menciones = {
        1: "Media General",
        2: "Técnico Superior"
        }
        
        # Llenar tabla
        for estudiante in estudiantes_pagina:
            row = self.estudiantes_table.rowCount()
            self.estudiantes_table.insertRow(row)
            
            # Columna 0: Cédula
            self.estudiantes_table.setItem(row, 0, QTableWidgetItem(estudiante['cedula']))
            # Columna 1: Nombre
            self.estudiantes_table.setItem(row, 1, QTableWidgetItem(estudiante['nombre']))
            # Columna 2: Apellido
            self.estudiantes_table.setItem(row, 2, QTableWidgetItem(estudiante['apellido']))
            # Columna 3: Fecha Nacimiento
            self.estudiantes_table.setItem(row, 3, QTableWidgetItem(str(estudiante['fecha_nacimiento'])))
            # Columna 4: Teléfono
            self.estudiantes_table.setItem(row, 4, QTableWidgetItem(estudiante.get('telefono') or ''))
            # Columna 5: País
            self.estudiantes_table.setItem(row, 5, QTableWidgetItem(estudiante.get('pais') or ''))
            # Columna 6: Estado
            self.estudiantes_table.setItem(row, 6, QTableWidgetItem(estudiante.get('estado') or ''))
            # Columna 7: Municipio
            self.estudiantes_table.setItem(row, 7, QTableWidgetItem(estudiante.get('municipio') or ''))
            # Columna 8: Grado
            self.estudiantes_table.setItem(row, 8, QTableWidgetItem(estudiante.get('nombre_grado') or ''))
            # Columna 9: Sección
            self.estudiantes_table.setItem(row, 9, QTableWidgetItem(estudiante.get('seccion') or ''))
            # Columna 9: Mención
            id_mencion = estudiante.get('id_mencion')
            mencion_texto = menciones.get(id_mencion, '') if id_mencion else ''
            self.estudiantes_table.setItem(row, 10, QTableWidgetItem(mencion_texto))
            # Columna 11: Observaciones
            self.estudiantes_table.setItem(row, 11, QTableWidgetItem(estudiante.get('observacion') or ''))
            
            # Columna 12: Botones de acción
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_widget.setLayout(actions_layout)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setObjectName("action_btn")
            edit_btn.setMaximumWidth(32)
            edit_btn.setMinimumHeight(32)
            edit_btn.setStyleSheet("QPushButton { background-color: #2196F3; }")
            edit_btn.clicked.connect(lambda checked, e=estudiante: self.edit_estudiante(e))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setObjectName("action_btn")
            delete_btn.setMaximumWidth(32)
            delete_btn.setMinimumHeight(32)
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
            delete_btn.clicked.connect(lambda checked, cedula=estudiante['cedula']: self.delete_estudiante(cedula))
            actions_layout.addWidget(delete_btn)
            
            self.estudiantes_table.setCellWidget(row, 12, actions_widget)
        
        # Actualizar controles de paginación
        self.actualizar_controles_paginacion_estudiantes()

    def delete_estudiante(self, cedula):
        """Elimina un estudiante y actualiza todas las vistas (SIN TIMERS PELIGROSOS)"""
        reply = QMessageBox.question(
            self, 'Confirmar eliminación',
            f'¿Está seguro de eliminar el estudiante con cédula {cedula}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # 1. GUARDAR ESTADO ANTES DE ELIMINAR
                grado_estaba_visible = (
                    hasattr(self, 'estudiantes_grado_container') and 
                    self.estudiantes_grado_container.isVisible()
                )
                grado_a_recargar = None
                
                if grado_estaba_visible and hasattr(self, 'grado_actual_mostrado'):
                    #  COPIAR el grado para evitar referencias
                    grado_a_recargar = self.grado_actual_mostrado.copy()
                
                # 2. ELIMINAR DE LA BASE DE DATOS
                if self.supabase_client.delete_estudiante(cedula):
                    
                    # 3. RECARGAR TABLA PRINCIPAL
                    self.load_estudiantes()
                    
                    # 4. ACTUALIZAR VISTA DE GRADOS SI ESTABA VISIBLE
                    if grado_estaba_visible and grado_a_recargar:
                        
                        #  FORZAR ACTUALIZACIÓN DE LA UI
                        self.estudiantes_grado_container.hide()
                        
                        #  PROCESAR EVENTOS PENDIENTES (reemplazo seguro del timer)
                        from PyQt6.QtCore import QCoreApplication
                        QCoreApplication.processEvents()
                        
                        #  MOSTRAR Y RECARGAR
                        self.estudiantes_grado_container.show()
                        self.mostrar_estudiantes_grado(grado_a_recargar)
                    
                    # 5. ACTUALIZAR BOTONES DE GRADOS
                    self.load_grados_tab()
                    
                    # 6. ACTUALIZAR BÚSQUEDA DE CALIFICACIONES SI ESTÁ ACTIVA
                    if hasattr(self, 'search_input') and self.search_input.text().strip():
                        self.perform_search()
                    
                    # MENSAJE DE ÉXITO
                    self.show_success(f"Estudiante con cédula {cedula} eliminado correctamente")
                    
                else:
                    self.show_error("Error al eliminar el estudiante de la base de datos")
                    
            except Exception as e:
                self.show_error(f"Error inesperado: {str(e)}")
                import traceback

    def actualizar_controles_paginacion_estudiantes(self):
        
        total_paginas = max(1, (self.total_estudiantes + self.estudiantes_por_pagina - 1) // self.estudiantes_por_pagina)
        pagina_mostrar = self.pagina_actual_estudiantes + 1
        
        # Calcular índices mostrados
        inicio = self.pagina_actual_estudiantes * self.estudiantes_por_pagina + 1
        fin = min((self.pagina_actual_estudiantes + 1) * self.estudiantes_por_pagina, self.total_estudiantes)
        
        # Actualizar labels
        self.estudiantes_page_info.setText(
            f"Mostrando {inicio}-{fin} de {self.total_estudiantes} estudiantes"
        )
        self.estudiantes_page_number.setText(f"Página {pagina_mostrar} de {total_paginas}")
        
        # Habilitar/deshabilitar botones
        self.estudiantes_first_btn.setEnabled(self.pagina_actual_estudiantes > 0)
        self.estudiantes_prev_btn.setEnabled(self.pagina_actual_estudiantes > 0)
        self.estudiantes_next_btn.setEnabled(self.pagina_actual_estudiantes < total_paginas - 1)
        self.estudiantes_last_btn.setEnabled(self.pagina_actual_estudiantes < total_paginas - 1)

    def cambiar_pagina_estudiantes(self, accion):
        """Cambia la página actual de estudiantes"""
        total_paginas = max(1, (self.total_estudiantes + self.estudiantes_por_pagina - 1) // self.estudiantes_por_pagina)
        
        if accion == 'first':
            self.pagina_actual_estudiantes = 0
        elif accion == 'prev':
            self.pagina_actual_estudiantes = max(0, self.pagina_actual_estudiantes - 1)
        elif accion == 'next':
            self.pagina_actual_estudiantes = min(total_paginas - 1, self.pagina_actual_estudiantes + 1)
        elif accion == 'last':
            self.pagina_actual_estudiantes = total_paginas - 1
        
        # Recargar sin resetear la página
        self.load_estudiantes(reset_pagina=False)

    def load_docentes(self):
        """Carga la lista de docentes"""
        docentes = self.supabase_client.get_all_docentes()
        self.docentes_table.setRowCount(0)
        self.docentes_table.verticalHeader().setDefaultSectionSize(45)
        for docente in docentes:
            row = self.docentes_table.rowCount()
            self.docentes_table.insertRow(row)
            
            self.docentes_table.setItem(row, 0, QTableWidgetItem(str(docente['cedula'])))
            self.docentes_table.setItem(row, 1, QTableWidgetItem(docente['nombre']))
            self.docentes_table.setItem(row, 2, QTableWidgetItem(docente['apellido']))
            self.docentes_table.setItem(row, 3, QTableWidgetItem(docente['correo'] or ''))
            self.docentes_table.setItem(row, 4, QTableWidgetItem(docente['telefono'] or ''))
            self.docentes_table.setItem(row, 5, QTableWidgetItem(docente['especialidad'] or ''))
            
            # Botones de acción
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_widget.setLayout(actions_layout)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setObjectName("action_btn")
            edit_btn.setMaximumWidth(32)
            edit_btn.setMinimumHeight(32)
            edit_btn.setStyleSheet("QPushButton { background-color: #2196F3; }")
            edit_btn.setToolTip("Editar docente")
            edit_btn.clicked.connect(lambda checked, d=docente: self.edit_docente(d))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setObjectName("action_btn")
            delete_btn.setMaximumWidth(32)
            delete_btn.setMinimumHeight(32)
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
            delete_btn.setToolTip("Eliminar docente")
            delete_btn.clicked.connect(lambda checked, id=docente['cedula']: self.delete_docente(id))
            actions_layout.addWidget(delete_btn)
            
            self.docentes_table.setCellWidget(row, 6, actions_widget)

    def load_asignaturas(self, reset_pagina=True):
        """Carga la lista de asignaturas CON PAGINACIÓN"""
        
        if reset_pagina:
            self.pagina_actual_asignaturas = 0
        
        # Obtener TODAS las asignaturas
        asignaturas = self.supabase_client.get_all_asignaturas()
        
        # Ordenar por nombre
        asignaturas_ordenadas = sorted(asignaturas, key=lambda x: x.get('nombre_asignatura', ''))
        
        # Guardar total
        self.total_asignaturas = len(asignaturas_ordenadas)
        self.asignaturas_filtradas = asignaturas_ordenadas
        
        # Calcular paginación
        total_paginas = max(1, (self.total_asignaturas + self.asignaturas_por_pagina - 1) // self.asignaturas_por_pagina)
        
        # Ajustar página actual si es necesario
        if self.pagina_actual_asignaturas >= total_paginas:
            self.pagina_actual_asignaturas = max(0, total_paginas - 1)
        
        # Calcular índices
        inicio = self.pagina_actual_asignaturas * self.asignaturas_por_pagina
        fin = min(inicio + self.asignaturas_por_pagina, self.total_asignaturas)
        
        # Obtener asignaturas de la página actual
        asignaturas_pagina = asignaturas_ordenadas[inicio:fin]
        
        # Limpiar tabla
        self.asignaturas_table.setRowCount(0)
        
        # Diccionario de menciones
        menciones = {
            1: "Media General",
            2: "Técnico Superior"
        }
        
        # Llenar tabla
        for asignatura in asignaturas_pagina:
            row = self.asignaturas_table.rowCount()
            self.asignaturas_table.insertRow(row)
            
            docente_nombre = ''
            if asignatura.get('docente_nombre') and asignatura.get('docente_apellido'):
                docente_nombre = f"{asignatura['docente_nombre']} {asignatura['docente_apellido']}"
            
            # Obtener el texto de la mención
            id_mencion = asignatura.get('id_mencion')
            mencion_texto = menciones.get(id_mencion, '') if id_mencion else ''
            
            self.asignaturas_table.setItem(row, 0, QTableWidgetItem(str(asignatura['codigo'])))
            self.asignaturas_table.setItem(row, 1, QTableWidgetItem(asignatura['nombre_asignatura']))
            self.asignaturas_table.setItem(row, 2, QTableWidgetItem(mencion_texto))
            self.asignaturas_table.setItem(row, 3, QTableWidgetItem(asignatura['nombre_grado'] or ''))
            self.asignaturas_table.setItem(row, 4, QTableWidgetItem(docente_nombre))
            
            # Botones de acción
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_widget.setLayout(actions_layout)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setObjectName("action_btn")
            edit_btn.setMaximumWidth(32)
            edit_btn.setMinimumHeight(32)
            edit_btn.setStyleSheet("QPushButton { background-color: #2196F3; }")
            edit_btn.clicked.connect(lambda checked, a=asignatura: self.edit_asignatura(a))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setObjectName("action_btn")
            delete_btn.setMaximumWidth(32)
            delete_btn.setMinimumHeight(32)
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
            delete_btn.clicked.connect(lambda checked, id=asignatura['codigo']: self.delete_asignatura(id))
            actions_layout.addWidget(delete_btn)
            
            self.asignaturas_table.setCellWidget(row, 5, actions_widget)
        
        # Actualizar controles de paginación
        self.actualizar_controles_paginacion_asignaturas()

    def actualizar_controles_paginacion_asignaturas(self):
        """Actualiza los controles de paginación de asignaturas"""
        total_paginas = max(1, (self.total_asignaturas + self.asignaturas_por_pagina - 1) // self.asignaturas_por_pagina)
        pagina_mostrar = self.pagina_actual_asignaturas + 1
        
        # Calcular índices mostrados
        inicio = self.pagina_actual_asignaturas * self.asignaturas_por_pagina + 1
        fin = min((self.pagina_actual_asignaturas + 1) * self.asignaturas_por_pagina, self.total_asignaturas)
        
        # Actualizar labels
        self.asignaturas_page_info.setText(
            f"Mostrando {inicio}-{fin} de {self.total_asignaturas} asignaturas"
        )
        self.asignaturas_page_number.setText(f"Página {pagina_mostrar} de {total_paginas}")
        
        # Habilitar/deshabilitar botones
        self.asignaturas_first_btn.setEnabled(self.pagina_actual_asignaturas > 0)
        self.asignaturas_prev_btn.setEnabled(self.pagina_actual_asignaturas > 0)
        self.asignaturas_next_btn.setEnabled(self.pagina_actual_asignaturas < total_paginas - 1)
        self.asignaturas_last_btn.setEnabled(self.pagina_actual_asignaturas < total_paginas - 1)

    def cambiar_pagina_asignaturas(self, accion):
        """Cambia la página actual de asignaturas"""
        total_paginas = max(1, (self.total_asignaturas + self.asignaturas_por_pagina - 1) // self.asignaturas_por_pagina)
        
        if accion == 'first':
            self.pagina_actual_asignaturas = 0
        elif accion == 'prev':
            self.pagina_actual_asignaturas = max(0, self.pagina_actual_asignaturas - 1)
        elif accion == 'next':
            self.pagina_actual_asignaturas = min(total_paginas - 1, self.pagina_actual_asignaturas + 1)
        elif accion == 'last':
            self.pagina_actual_asignaturas = total_paginas - 1
        
        # Recargar sin resetear la página
        self.load_asignaturas(reset_pagina=False)

    def filter_asignaturas(self, text):
        """Filtra la tabla de asignaturas Y ACTUALIZA PAGINACIÓN"""
        if not text.strip():
            # Si no hay filtro, mostrar todas
            self.load_asignaturas(reset_pagina=True)
            return
        
        # Filtrar asignaturas
        text_lower = text.lower()
        asignaturas_filtradas = []
        
        menciones = {
            1: "Media General",
            2: "Técnico Superior"
        }
        
        for asignatura in self.asignaturas_filtradas:
            # Buscar en todos los campos
            id_mencion = asignatura.get('id_mencion')
            mencion_texto = menciones.get(id_mencion, '') if id_mencion else ''
            
            docente_nombre = ''
            if asignatura.get('docente_nombre') and asignatura.get('docente_apellido'):
                docente_nombre = f"{asignatura['docente_nombre']} {asignatura['docente_apellido']}"
            
            campos = [
                asignatura.get('codigo', ''),
                asignatura.get('nombre_asignatura', ''),
                mencion_texto,
                asignatura.get('nombre_grado', ''),
                docente_nombre
            ]
            
            if any(text_lower in str(campo).lower() for campo in campos):
                asignaturas_filtradas.append(asignatura)
        
        # Actualizar total
        self.total_asignaturas = len(asignaturas_filtradas)
        self.pagina_actual_asignaturas = 0
        
        # Calcular índices
        inicio = 0
        fin = min(self.asignaturas_por_pagina, self.total_asignaturas)
        
        asignaturas_pagina = asignaturas_filtradas[inicio:fin]
        
        # Limpiar y llenar tabla
        self.asignaturas_table.setRowCount(0)
        
        menciones = {
            1: "Media General",
            2: "Técnico Superior"
        }
        
        for asignatura in asignaturas_pagina:
            row = self.asignaturas_table.rowCount()
            self.asignaturas_table.insertRow(row)
            
            docente_nombre = ''
            if asignatura.get('docente_nombre') and asignatura.get('docente_apellido'):
                docente_nombre = f"{asignatura['docente_nombre']} {asignatura['docente_apellido']}"
            
            id_mencion = asignatura.get('id_mencion')
            mencion_texto = menciones.get(id_mencion, '') if id_mencion else ''
            
            self.asignaturas_table.setItem(row, 0, QTableWidgetItem(str(asignatura['codigo'])))
            self.asignaturas_table.setItem(row, 1, QTableWidgetItem(asignatura['nombre_asignatura']))
            self.asignaturas_table.setItem(row, 2, QTableWidgetItem(mencion_texto))
            self.asignaturas_table.setItem(row, 3, QTableWidgetItem(asignatura['nombre_grado'] or ''))
            self.asignaturas_table.setItem(row, 4, QTableWidgetItem(docente_nombre))
            
            # Botones
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_widget.setLayout(actions_layout)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setObjectName("action_btn")
            edit_btn.setMaximumWidth(32)
            edit_btn.setMinimumHeight(32)
            edit_btn.setStyleSheet("QPushButton { background-color: #2196F3; }")
            edit_btn.clicked.connect(lambda checked, a=asignatura: self.edit_asignatura(a))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setObjectName("action_btn")
            delete_btn.setMaximumWidth(32)
            delete_btn.setMinimumHeight(32)
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
            delete_btn.clicked.connect(lambda checked, id=asignatura['codigo']: self.delete_asignatura(id))
            actions_layout.addWidget(delete_btn)
            
            self.asignaturas_table.setCellWidget(row, 5, actions_widget)
        
        # Actualizar controles
        self.actualizar_controles_paginacion_asignaturas()

    def load_grados(self):
        """Carga la lista de grados"""
        grados = self.supabase_client.get_all_grados()
        self.grados_table.setRowCount(0)
        
        for grado in grados:
            row = self.grados_table.rowCount()
            self.grados_table.insertRow(row)
            
            self.grados_table.setItem(row, 0, QTableWidgetItem(str(grado['id_grado'])))
            self.grados_table.setItem(row, 1, QTableWidgetItem(grado['nombre_grado']))

    def load_periodos(self):
        """Carga la lista de períodos académicos"""
        periodos = self.supabase_client.get_all_periodos()
        self.periodos_table.setRowCount(0)
        
        for periodo in periodos:
            row = self.periodos_table.rowCount()
            self.periodos_table.insertRow(row)
            
            self.periodos_table.setItem(row, 0, QTableWidgetItem(str(periodo['anio'])))
            self.periodos_table.setItem(row, 1, QTableWidgetItem(str(periodo['fecha_inicio'])))
            self.periodos_table.setItem(row, 2, QTableWidgetItem(str(periodo['fecha_fin'])))

    def load_calificaciones(self):
        """Carga todas las calificaciones"""
        calificaciones = self.supabase_client.get_all_calificaciones()
        self.calificaciones_table.setRowCount(0)

        for cal in calificaciones:
            row = self.calificaciones_table.rowCount()
            self.calificaciones_table.insertRow(row)

            self.calificaciones_table.setItem(row, 0, QTableWidgetItem(cal['nombre_asignatura']))
            self.calificaciones_table.setItem(row, 1, QTableWidgetItem(cal['codigo']))
            self.calificaciones_table.setItem(row, 2, QTableWidgetItem(str(cal['nota_1']) if cal['nota_1'] else '-'))
            self.calificaciones_table.setItem(row, 3, QTableWidgetItem(str(cal['ajuste_1']) if cal['ajuste_1'] else '0'))
            self.calificaciones_table.setItem(row, 4, QTableWidgetItem(str(cal['nota_2']) if cal['nota_2'] else '-'))
            self.calificaciones_table.setItem(row, 5, QTableWidgetItem(str(cal['ajuste_2']) if cal['ajuste_2'] else '0'))
            self.calificaciones_table.setItem(row, 6, QTableWidgetItem(str(cal['nota_3']) if cal['nota_3'] else '-'))
            self.calificaciones_table.setItem(row, 7, QTableWidgetItem(str(cal['ajuste_3']) if cal['ajuste_3'] else '0'))
            self.calificaciones_table.setItem(row, 8, QTableWidgetItem(str(cal['nota_final']) if cal['nota_final'] else '0'))

    # FUNCIONES DE FILTRADO Y BUSQUEDA

    def perform_search(self):
        """Ejecuta la búsqueda después del retraso del temporizador"""
        cedula = self.search_input.text().strip()
        self.calificaciones_table.setRowCount(0)
        if not cedula:
            return
        calificaciones = self.supabase_client.get_calificaciones_by_estudiante(cedula)
        for cal in calificaciones:
            row = self.calificaciones_table.rowCount()
            self.calificaciones_table.insertRow(row)
            self.calificaciones_table.setItem(row, 0, QTableWidgetItem(cal['nombre_asignatura']))
            self.calificaciones_table.setItem(row, 1, QTableWidgetItem(cal['codigo']))
            self.calificaciones_table.setItem(row, 2, QTableWidgetItem(str(cal['nota_1']) if cal['nota_1'] else '-'))
            self.calificaciones_table.setItem(row, 3, QTableWidgetItem(str(cal['ajuste_1']) if cal['ajuste_1'] else '0'))
            self.calificaciones_table.setItem(row, 4, QTableWidgetItem(str(cal['nota_2']) if cal['nota_2'] else '-'))
            self.calificaciones_table.setItem(row, 5, QTableWidgetItem(str(cal['ajuste_2']) if cal['ajuste_2'] else '0'))
            self.calificaciones_table.setItem(row, 6, QTableWidgetItem(str(cal['nota_3']) if cal['nota_3'] else '-'))
            self.calificaciones_table.setItem(row, 7, QTableWidgetItem(str(cal['ajuste_3']) if cal['ajuste_3'] else '0'))
            self.calificaciones_table.setItem(row, 8, QTableWidgetItem(str(cal['nota_final']) if cal['nota_final'] else '0'))

    def clear_calificaciones_table(self):
        """Limpia la tabla y el campo de búsqueda"""
        self.calificaciones_table.setRowCount(0)
        self.search_input.clear()

    def filter_estudiantes(self, text):
        """Filtra la tabla de estudiantes Y ACTUALIZA PAGINACIÓN"""
        if not text.strip():
            # Si no hay filtro, mostrar todas
            self.load_estudiantes(reset_pagina=True)
            return
        
        # Filtrar estudiantes
        text_lower = text.lower()
        estudiantes_filtrados = []
        
        # Diccionario de menciones
        menciones = {
            1: "Media General",
            2: "Técnico Superior"
        }
        
        for estudiante in self.estudiantes_filtrados:
            # Buscar en todos los campos (incluyendo mención)
            id_mencion = estudiante.get('id_mencion')
            mencion_texto = menciones.get(id_mencion, '') if id_mencion else ''
            
            campos = [
                estudiante.get('cedula', ''),
                estudiante.get('nombre', ''),
                estudiante.get('apellido', ''),
                estudiante.get('telefono', ''),
                estudiante.get('correo', ''),
                estudiante.get('pais', ''),
                estudiante.get('estado', ''),
                estudiante.get('municipio', ''),
                estudiante.get('nombre_grado', ''),
                estudiante.get('seccion', ''),
                mencion_texto,
                estudiante.get('observacion', '')
            ]
            
            if any(text_lower in str(campo).lower() for campo in campos):
                estudiantes_filtrados.append(estudiante)
        
        # Actualizar total
        self.total_estudiantes = len(estudiantes_filtrados)
        self.pagina_actual_estudiantes = 0
        
        # Calcular índices
        inicio = 0
        fin = min(self.estudiantes_por_pagina, self.total_estudiantes)
        
        estudiantes_pagina = estudiantes_filtrados[inicio:fin]
        
        # Limpiar y llenar tabla
        self.estudiantes_table.setRowCount(0)
        
        for estudiante in estudiantes_pagina:
            row = self.estudiantes_table.rowCount()
            self.estudiantes_table.insertRow(row)
            
            # Columna 0: Cédula
            self.estudiantes_table.setItem(row, 0, QTableWidgetItem(estudiante['cedula']))
            # Columna 1: Nombre
            self.estudiantes_table.setItem(row, 1, QTableWidgetItem(estudiante['nombre']))
            # Columna 2: Apellido
            self.estudiantes_table.setItem(row, 2, QTableWidgetItem(estudiante['apellido']))
            # Columna 3: Fecha Nacimiento
            self.estudiantes_table.setItem(row, 3, QTableWidgetItem(str(estudiante['fecha_nacimiento'])))
            # Columna 4: Teléfono
            self.estudiantes_table.setItem(row, 4, QTableWidgetItem(estudiante.get('telefono') or ''))
            # Columna 5: País
            self.estudiantes_table.setItem(row, 5, QTableWidgetItem(estudiante.get('pais') or ''))
            # Columna 6: Estado
            self.estudiantes_table.setItem(row, 6, QTableWidgetItem(estudiante.get('estado') or ''))
            # Columna 7: Municipio
            self.estudiantes_table.setItem(row, 7, QTableWidgetItem(estudiante.get('municipio') or ''))
            # Columna 8: Grado
            self.estudiantes_table.setItem(row, 8, QTableWidgetItem(estudiante.get('nombre_grado') or ''))
            # Columna 9: Sección
            self.estudiantes_table.setItem(row, 9, QTableWidgetItem(estudiante.get('seccion') or ''))
            # Columna 10: Mención
            id_mencion = estudiante.get('id_mencion')
            mencion_texto = menciones.get(id_mencion, '') if id_mencion else ''
            self.estudiantes_table.setItem(row, 10, QTableWidgetItem(mencion_texto))
            # Columna 11: Observaciones
            self.estudiantes_table.setItem(row, 11, QTableWidgetItem(estudiante.get('observacion') or ''))
            
            # Columna 12: Botones de acción
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_widget.setLayout(actions_layout)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setObjectName("action_btn")
            edit_btn.setMaximumWidth(32)
            edit_btn.setMinimumHeight(32)
            edit_btn.setStyleSheet("QPushButton { background-color: #2196F3; }")
            edit_btn.clicked.connect(lambda checked, e=estudiante: self.edit_estudiante(e))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setObjectName("action_btn")
            delete_btn.setMaximumWidth(32)
            delete_btn.setMinimumHeight(32)
            delete_btn.setStyleSheet("QPushButton { background-color: #f44336; }")
            delete_btn.clicked.connect(lambda checked, cedula=estudiante['cedula']: self.delete_estudiante(cedula))
            actions_layout.addWidget(delete_btn)
            
            self.estudiantes_table.setCellWidget(row, 12, actions_widget)
        
        # Actualizar controles
        self.actualizar_controles_paginacion_estudiantes()

    def filter_docentes(self, text):
        """Filtra la tabla de docentes"""
        for row in range(self.docentes_table.rowCount()):
            match = False
            for col in range(self.docentes_table.columnCount() - 1):
                item = self.docentes_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break
            self.docentes_table.setRowHidden(row, not match)

    def filter_asignaturas(self, text):
        """Filtra la tabla de asignaturas"""
        for row in range(self.asignaturas_table.rowCount()):
            match = False
            for col in range(self.asignaturas_table.columnCount() - 1):
                item = self.asignaturas_table.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break
            self.asignaturas_table.setRowHidden(row, not match)

    #FUNCIONES PARA GRADOS EXPANDIBLES 

    def cambiar_grado_estudiante(self, cedula_estudiante, grado_actual):
        """Abre diálogo para cambiar un estudiante de grado"""
        # Obtener todos los grados
        grados = self.supabase_client.get_all_grados()
        
        # Filtrar el grado actual
        grados_disponibles = [g for g in grados if g['id_grado'] != grado_actual]
        
        if not grados_disponibles:
            QMessageBox.warning(self, "Error", "No hay otros grados disponibles")
            return
        
        # Crear lista de nombres de grados
        nombres_grados = [g['nombre_grado'] for g in grados_disponibles]
        
        # Mostrar diálogo de selección
        nuevo_grado_nombre, ok = QInputDialog.getItem(
            self,
            "Cambiar Grado",
            "Seleccione el nuevo grado:",
            nombres_grados,
            0,
            False
        )
        
        if ok and nuevo_grado_nombre:
            # Encontrar el ID del nuevo grado
            nuevo_grado_id = next(
                (g['id_grado'] for g in grados_disponibles if g['nombre_grado'] == nuevo_grado_nombre),
                None
            )
            
            if nuevo_grado_id:
                try:
                    # Actualizar el grado del estudiante
                    if self.supabase_client.update_estudiante(cedula_estudiante, id_grado=nuevo_grado_id):
                        QMessageBox.information(
                            self,
                            "Éxito",
                            f"Estudiante cambiado a {nuevo_grado_nombre} correctamente"
                        )
                        # Recargar la tabla de grados
                        self.load_grados()
                    else:
                        QMessageBox.critical(self, "Error", "No se pudo cambiar el grado del estudiante")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al cambiar grado: {str(e)}")

# FUNCIONES CRUD - ESTUDIANTES

    def add_estudiante(self):
        """Abre diálogo para agregar estudiante"""
        dialog = EstudianteDialog(self, self.supabase_client)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_estudiantes()

    def edit_estudiante(self, estudiante):
        """Abre diálogo para editar estudiante"""
        dialog = EstudianteDialog(self, self.supabase_client, estudiante)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_estudiantes()

    def mostrar_estudiantes_grado(self, grado):
        """Muestra los estudiantes de un grado específico (VERSIÓN ANTI-FANTASMA)"""
        
        # Obtener estudiantes del grado
        estudiantes = self.supabase_client.get_estudiantes_by_grado(grado['id_grado'])
        
        #  GUARDAR GRADO ACTUAL
        self.grado_actual_mostrado = grado.copy()
        
        # Actualizar label
        total_estudiantes = len(estudiantes)
        self.grado_label.setText(
            f"{grado['nombre_grado']} - {total_estudiantes} estudiante{'s' if total_estudiantes != 1 else ''}"
        )
        
        #  LIMPIAR CHECKBOXES ANTIGUOS (CRÍTICO)
        self.checkboxes_estudiantes.clear()  # Limpiar la lista
        
        # Limpiar tabla
        self.estudiantes_grado_table.setRowCount(0)
        
        # Configurar columnas (solo 7 columnas: Cédula, Nombre, Apellido, Fecha Nac., Teléfono, Correo, Checkbox)
        self.estudiantes_grado_table.setColumnCount(7)
        self.estudiantes_grado_table.setHorizontalHeaderLabels([
            "Cédula", "Nombre", "Apellido", "Fecha Nac.", 
            "Teléfono", "Correo", "☑️"  
        ])
        
        #  CREAR NUEVOS CHECKBOXES
        
        for row, estudiante in enumerate(estudiantes):
            self.estudiantes_grado_table.insertRow(row)
            
            # Datos del estudiante
            # Columna 0: Cédula
            self.estudiantes_grado_table.setItem(row, 0, QTableWidgetItem(estudiante['cedula']))
            # Columna 1: Nombre
            self.estudiantes_grado_table.setItem(row, 1, QTableWidgetItem(estudiante['nombre']))
            # Columna 2: Apellido
            self.estudiantes_grado_table.setItem(row, 2, QTableWidgetItem(estudiante['apellido']))
            # Columna 3: Fecha Nacimiento
            self.estudiantes_grado_table.setItem(row, 3, QTableWidgetItem(str(estudiante['fecha_nacimiento'])))
            # Columna 4: Teléfono
            self.estudiantes_grado_table.setItem(row, 4, QTableWidgetItem(estudiante.get('telefono') or ''))
            # Columna 5: Correo
            self.estudiantes_grado_table.setItem(row, 5, QTableWidgetItem(estudiante.get('correo') or ''))
            
            # Columna 6: CREAR CHECKBOX (con verificación)
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout()
            checkbox_layout.setContentsMargins(5, 0, 5, 0)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            checkbox = QCheckBox()
            checkbox.setProperty('cedula', estudiante['cedula'])
            
            #  VERIFICAR QUE SE CREÓ CORRECTAMENTE
            if checkbox is None:
                continue
            
            checkbox_layout.addWidget(checkbox)
            checkbox_widget.setLayout(checkbox_layout)
            self.estudiantes_grado_table.setCellWidget(row, 6, checkbox_widget)
            
            #  AGREGAR A LA LISTA
            self.checkboxes_estudiantes.append(checkbox)
        
        # Mostrar contenedor
        self.estudiantes_grado_container.setVisible(True)
        
        # Agregar barra de acciones en masa
        self.agregar_barra_acciones_masa(grado)
        
        #  RESETEAR CHECKBOX "SELECCIONAR TODOS"
        if self.select_all_checkbox:
            self.select_all_checkbox.setChecked(False)

# FUNCIONES CRUD - DOCENTES

    def add_docente(self):
        """Abre diálogo para agregar docente"""
        dialog = DocenteDialog(self, self.supabase_client)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_docentes()

    def edit_docente(self, docente):
        """Abre diálogo para editar docente"""
        dialog = DocenteDialog(self, self.supabase_client, docente)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_docentes()

    def delete_docente(self, docente_id):
        """Elimina un docente"""
        reply = QMessageBox.question(
            self, 'Confirmar eliminación',
            '¿Está seguro de eliminar este docente?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) 
        if reply == QMessageBox.StandardButton.Yes:
            if self.supabase_client.delete_docente(docente_id):
                self.show_success("Docente eliminado correctamente")
                self.load_docentes()
            else:
                self.show_error("Error al eliminar el docente")

    #FUNCIONES CRUD - ASIGNATURAS

    def add_asignatura(self):
        """Abre diálogo para agregar asignatura"""
        dialog = AsignaturaDialog(self, self.supabase_client)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_asignaturas()

    def edit_asignatura(self, asignatura):
        """Abre diálogo para editar asignatura"""
        dialog = AsignaturaDialog(self, self.supabase_client, asignatura)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_asignaturas()

    def delete_asignatura(self, codigo):
        """Elimina una asignatura"""
        reply = QMessageBox.question(
            self, 'Confirmar eliminación',
            f'¿Está seguro de eliminar la asignatura con código {codigo}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.supabase_client.delete_asignatura(codigo):
                self.show_success("Asignatura eliminada correctamente")
                self.load_asignaturas()
            else:
                self.show_error("Error al eliminar la asignatura")

    #FUNCIONES CRUD - GRADOS

    def add_grado(self):
        """Abre diálogo para agregar grado"""
        dialog = GradoDialog(self, self.supabase_client)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_grados()

    def delete_grado(self, id_grado):
        """Elimina un grado"""
        reply = QMessageBox.question(
            self, 'Confirmar eliminación',
            f'¿Está seguro de eliminar este grado?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.supabase_client.delete_grado(id_grado):
                self.show_success("Grado eliminado correctamente")
                self.load_grados()
            else:
                self.show_error("Error al eliminar el grado")

    #FUNCIONES CRUD - CALIFICACIONES

    def open_calificaciones_dialog(self):
        """Abre el diálogo de gestión de calificaciones"""
        dialog = CalificacionesDialog(self, self.supabase_client)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Recargar la tabla si había una búsqueda activa
            if self.search_input.text().strip():
                self.perform_search()

    #FUNCIONES CRUD - PERIODOS

    def add_periodo(self):
        """Abre diálogo para agregar período"""
        dialog = PeriodoDialog(self, self.supabase_client)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_periodos()

    def delete_periodo(self, anio):
        """Elimina un período"""
        reply = QMessageBox.question(
            self, 'Confirmar eliminación',
            f'¿Está seguro de eliminar el período del año {anio}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.supabase_client.delete_periodo(anio):
                self.show_success("Período eliminado correctamente")
                self.load_periodos()
            else:
                self.show_error("Error al eliminar el período")

    #FUNCIONES DE CREACIÓN DE UI

    def create_header(self, parent_layout):
        """Crea la barra superior"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #0d1f3d;
                padding: 15px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)
        
        # Título
        title = QLabel("U.E Nueva Esparta")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Información del usuario
        user_info = QLabel(f"Bienvenido, {self.user_data.get('nombre_completo', 'Administrador')}")
        header_layout.addWidget(user_info)
        
        # Botón de cerrar sesión
        logout_btn = QPushButton("Cerrar Sesión")
        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)
        
        parent_layout.addWidget(header)

    def create_estudiantes_tab(self):
        """Crea la pestaña de estudiantes CON PAGINACIÓN"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        tab.setLayout(layout)
        
        # ========== BARRA DE HERRAMIENTAS SUPERIOR ==========
        toolbar = QHBoxLayout()
        
        self.estudiantes_search_input = QLineEdit()
        self.estudiantes_search_input.setPlaceholderText("Buscar estudiante...")
        self.estudiantes_search_input.setMaximumWidth(300)
        self.estudiantes_search_input.textChanged.connect(self.filter_estudiantes)
        toolbar.addWidget(self.estudiantes_search_input)
        
        toolbar.addStretch()
        
        add_btn = QPushButton("✚ Nuevo Estudiante")
        add_btn.setObjectName("add_btn")
        add_btn.clicked.connect(self.add_estudiante)
        toolbar.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setObjectName("refresh_btn")
        refresh_btn.clicked.connect(self.load_estudiantes)
        toolbar.addWidget(refresh_btn)
        
        layout.addLayout(toolbar)
        
        # ========== TABLA DE ESTUDIANTES ==========
        self.estudiantes_table = QTableWidget()
        self.estudiantes_table.setColumnCount(13)  # Columnas
        self.estudiantes_table.setHorizontalHeaderLabels([
            "Cédula", "Nombre", "Apellido", "Fecha Nac.", 
            "Teléfono", "País", "Estado", "Municipio", "Grado", "Sección", "Mención", "Observaciones", "Acciones"
        ])

        self.estudiantes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.estudiantes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.estudiantes_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.estudiantes_table.verticalHeader().setDefaultSectionSize(45)
        layout.addWidget(self.estudiantes_table)
        
        # ========== CONTROLES DE PAGINACIÓN ==========
        pagination_frame = QFrame()
        pagination_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
                padding: 10px;
            }
        """)
        pagination_layout = QHBoxLayout()
        pagination_layout.setContentsMargins(10, 5, 10, 5)
        pagination_frame.setLayout(pagination_layout)
        
        # Información de página
        self.estudiantes_page_info = QLabel("Mostrando 0-0 de 0 estudiantes")
        self.estudiantes_page_info.setStyleSheet("color: #666; font-weight: bold;")
        pagination_layout.addWidget(self.estudiantes_page_info)
        
        pagination_layout.addStretch()
        
        # Botones de navegación
        self.estudiantes_first_btn = QPushButton("⏮ Primera")
        self.estudiantes_first_btn.setObjectName("refresh_btn")
        self.estudiantes_first_btn.setMaximumWidth(100)
        self.estudiantes_first_btn.clicked.connect(lambda: self.cambiar_pagina_estudiantes('first'))
        pagination_layout.addWidget(self.estudiantes_first_btn)
        
        self.estudiantes_prev_btn = QPushButton("◀ Anterior")
        self.estudiantes_prev_btn.setObjectName("refresh_btn")
        self.estudiantes_prev_btn.setMaximumWidth(100)
        self.estudiantes_prev_btn.clicked.connect(lambda: self.cambiar_pagina_estudiantes('prev'))
        pagination_layout.addWidget(self.estudiantes_prev_btn)
        
        self.estudiantes_page_number = QLabel("Página 1 de 1")
        self.estudiantes_page_number.setStyleSheet("""
            color: #2563eb; 
            font-weight: bold; 
            font-size: 14px;
            padding: 0 15px;
        """)
        pagination_layout.addWidget(self.estudiantes_page_number)
        
        self.estudiantes_next_btn = QPushButton("Siguiente ▶")
        self.estudiantes_next_btn.setObjectName("refresh_btn")
        self.estudiantes_next_btn.setMaximumWidth(100)
        self.estudiantes_next_btn.clicked.connect(lambda: self.cambiar_pagina_estudiantes('next'))
        pagination_layout.addWidget(self.estudiantes_next_btn)
        
        self.estudiantes_last_btn = QPushButton("Última ⏭")
        self.estudiantes_last_btn.setObjectName("refresh_btn")
        self.estudiantes_last_btn.setMaximumWidth(100)
        self.estudiantes_last_btn.clicked.connect(lambda: self.cambiar_pagina_estudiantes('last'))
        pagination_layout.addWidget(self.estudiantes_last_btn)
        
        layout.addWidget(pagination_frame)
        
        self.tabs.addTab(tab, "Estudiantes")

    def create_docentes_tab(self):
        """Crea la pestaña de docentes"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        tab.setLayout(layout)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Buscar docente...")
        search_input.setMaximumWidth(300)
        search_input.textChanged.connect(self.filter_docentes)
        toolbar.addWidget(search_input)
        
        toolbar.addStretch()
        
        add_btn = QPushButton("✚ Nuevo Docente")
        add_btn.setObjectName("add_btn")
        add_btn.clicked.connect(self.add_docente)
        toolbar.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setObjectName("refresh_btn")
        refresh_btn.clicked.connect(self.load_docentes)
        toolbar.addWidget(refresh_btn)
        
        layout.addLayout(toolbar)
        
        # Tabla de docentes
        self.docentes_table = QTableWidget()
        self.docentes_table.setColumnCount(7)
        self.docentes_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellido", "Correo", "Teléfono", "Especialidad", "Acciones"
        ])
        self.docentes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.docentes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.docentes_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.docentes_table)
        
        self.tabs.addTab(tab, "Docentes")

    def create_asignaturas_tab(self):
        """Crea la pestaña de asignaturas CON PAGINACIÓN"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        tab.setLayout(layout)
        
        # ========== BARRA DE HERRAMIENTAS SUPERIOR ==========
        toolbar = QHBoxLayout()
        
        self.asignaturas_search_input = QLineEdit()
        self.asignaturas_search_input.setPlaceholderText("Buscar asignatura...")
        self.asignaturas_search_input.setMaximumWidth(300)
        self.asignaturas_search_input.textChanged.connect(self.filter_asignaturas)
        toolbar.addWidget(self.asignaturas_search_input)
        
        toolbar.addStretch()
        
        add_btn = QPushButton("✚ Nueva Asignatura")
        add_btn.setObjectName("add_btn")
        add_btn.clicked.connect(self.add_asignatura)
        toolbar.addWidget(add_btn)
        
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setObjectName("refresh_btn")
        refresh_btn.clicked.connect(self.load_asignaturas)
        toolbar.addWidget(refresh_btn)
        
        layout.addLayout(toolbar)
        
        # ========== TABLA DE ASIGNATURAS ==========
        self.asignaturas_table = QTableWidget()
        self.asignaturas_table.setColumnCount(6)
        self.asignaturas_table.setHorizontalHeaderLabels([
            "Código", "Nombre", "Mención", "Grado", "Docente", "Acciones"
        ])
        self.asignaturas_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.asignaturas_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.asignaturas_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.asignaturas_table.verticalHeader().setDefaultSectionSize(45)
        layout.addWidget(self.asignaturas_table)
        
        # ========== CONTROLES DE PAGINACIÓN ==========
        pagination_frame = QFrame()
        pagination_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
                padding: 10px;
            }
        """)
        pagination_layout = QHBoxLayout()
        pagination_layout.setContentsMargins(10, 5, 10, 5)
        pagination_frame.setLayout(pagination_layout)
        
        # Información de página
        self.asignaturas_page_info = QLabel("Mostrando 0-0 de 0 asignaturas")
        self.asignaturas_page_info.setStyleSheet("color: #666; font-weight: bold;")
        pagination_layout.addWidget(self.asignaturas_page_info)
        
        pagination_layout.addStretch()
        
        # Botones de navegación
        self.asignaturas_first_btn = QPushButton("⏮ Primera")
        self.asignaturas_first_btn.setObjectName("refresh_btn")
        self.asignaturas_first_btn.setMaximumWidth(100)
        self.asignaturas_first_btn.clicked.connect(lambda: self.cambiar_pagina_asignaturas('first'))
        pagination_layout.addWidget(self.asignaturas_first_btn)
        
        self.asignaturas_prev_btn = QPushButton("◀ Anterior")
        self.asignaturas_prev_btn.setObjectName("refresh_btn")
        self.asignaturas_prev_btn.setMaximumWidth(100)
        self.asignaturas_prev_btn.clicked.connect(lambda: self.cambiar_pagina_asignaturas('prev'))
        pagination_layout.addWidget(self.asignaturas_prev_btn)
        
        self.asignaturas_page_number = QLabel("Página 1 de 1")
        self.asignaturas_page_number.setStyleSheet("""
            color: #2563eb; 
            font-weight: bold; 
            font-size: 14px;
            padding: 0 15px;
        """)
        pagination_layout.addWidget(self.asignaturas_page_number)
        
        self.asignaturas_next_btn = QPushButton("Siguiente ▶")
        self.asignaturas_next_btn.setObjectName("refresh_btn")
        self.asignaturas_next_btn.setMaximumWidth(100)
        self.asignaturas_next_btn.clicked.connect(lambda: self.cambiar_pagina_asignaturas('next'))
        pagination_layout.addWidget(self.asignaturas_next_btn)
        
        self.asignaturas_last_btn = QPushButton("Última ⏭")
        self.asignaturas_last_btn.setObjectName("refresh_btn")
        self.asignaturas_last_btn.setMaximumWidth(100)
        self.asignaturas_last_btn.clicked.connect(lambda: self.cambiar_pagina_asignaturas('last'))
        pagination_layout.addWidget(self.asignaturas_last_btn)
        
        layout.addWidget(pagination_frame)
        
        self.tabs.addTab(tab, "Asignaturas")

    def create_calificaciones_tab(self):
        """Crea la pestaña de calificaciones optimizada (buscar por cédula)"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        tab.setLayout(layout)
        # --- Barra superior con buscador y botón ---
        filters = QHBoxLayout()
        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Introduzca la cédula del estudiante...")
        self.search_input.setMaximumWidth(300)
        filters.addWidget(self.search_input)
        filters.addStretch()
        # Boton para gestionar calificaciones
        add_cal_btn = QPushButton("✚ Gestionar Calificaciones")
        add_cal_btn.setObjectName("add_btn")
        add_cal_btn.clicked.connect(self.open_calificaciones_dialog)
        filters.addWidget(add_cal_btn)
        # Botón de limpiar/actualizar
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setObjectName("refresh_btn")
        refresh_btn.clicked.connect(self.clear_calificaciones_table)
        filters.addWidget(refresh_btn)
        layout.addLayout(filters)
        # --- Tabla de calificaciones ---
        self.calificaciones_table = QTableWidget()
        self.calificaciones_table.setColumnCount(9)
        self.calificaciones_table.verticalHeader().setDefaultSectionSize(45)
        self.calificaciones_table.setHorizontalHeaderLabels([
            "Asignatura", "Código",
            "Nota 1", "Ajuste 1",  
            "Nota 2", "Ajuste 2", 
            "Nota 3", "Ajuste 3", 
            "Nota Final"
        ])
        self.calificaciones_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.calificaciones_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.calificaciones_table)
        # Agregar pestaña
        self.tabs.addTab(tab, "Calificaciones")
        # --- Temporizador (mejora el rendimiento del filtrado) ---
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        # Cada vez que se escribe algo, reinicia el temporizador
        self.search_input.textChanged.connect(lambda: self.search_timer.start(400))

    def create_grados_tab(self):
        """Crea la pestaña de grados con botones por año"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        tab.setLayout(layout)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Contenedor para los botones de grados
        self.grados_container = QWidget()
        self.grados_layout = QHBoxLayout()
        self.grados_layout.setContentsMargins(0, 10, 0, 10)
        self.grados_layout.setSpacing(10)
        self.grados_container.setLayout(self.grados_layout)
        
        layout.addWidget(self.grados_container)
        
        # Contenedor para la tabla de estudiantes del grado seleccionado
        self.estudiantes_grado_container = QWidget()
        self.estudiantes_grado_layout = QVBoxLayout()
        self.estudiantes_grado_container.setLayout(self.estudiantes_grado_layout)
        self.estudiantes_grado_container.setVisible(False)  # Oculto inicialmente
        
        # Label para mostrar qué grado se está viendo
        self.grado_label = QLabel("")
        self.grado_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.grado_label.setStyleSheet("color: #2196F3;")
        self.estudiantes_grado_layout.addWidget(self.grado_label)
        
        # Tabla para mostrar estudiantes del grado seleccionado
        self.estudiantes_grado_table = QTableWidget()
        self.estudiantes_grado_table.setColumnCount(9)
        self.estudiantes_grado_table.verticalHeader().setDefaultSectionSize(45)
        self.estudiantes_grado_table.setHorizontalHeaderLabels([
                "Cédula", "Nombre", "Apellido", "Fecha Nac.", 
                "Teléfono", "Correo", "Mención", "Sección", ""
            ])
        self.estudiantes_grado_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.estudiantes_grado_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.estudiantes_grado_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        self.estudiantes_grado_layout.addWidget(self.estudiantes_grado_table)
        
        # ========== CONTROLES DE PAGINACIÓN ==========
        pagination_frame = QFrame()
        pagination_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
            }
        """)
        pagination_layout = QHBoxLayout()
        pagination_layout.setContentsMargins(10, 5, 10, 5)
        pagination_frame.setLayout(pagination_layout)
        
        # Info de registros mostrados
        self.grado_page_info = QLabel("Mostrando 0-0 de 0 estudiantes")
        self.grado_page_info.setStyleSheet("color: #666; font-weight: bold;")
        pagination_layout.addWidget(self.grado_page_info)
        
        pagination_layout.addStretch()
        
        # Botones de navegación
        self.grado_first_btn = QPushButton("⏮ Primera")
        self.grado_first_btn.setObjectName("refresh_btn")
        self.grado_first_btn.setMaximumWidth(100)
        self.grado_first_btn.clicked.connect(lambda: self.cambiar_pagina_grado('first'))
        pagination_layout.addWidget(self.grado_first_btn)
        
        self.grado_prev_btn = QPushButton("◀ Anterior")
        self.grado_prev_btn.setObjectName("refresh_btn")
        self.grado_prev_btn.setMaximumWidth(100)
        self.grado_prev_btn.clicked.connect(lambda: self.cambiar_pagina_grado('prev'))
        pagination_layout.addWidget(self.grado_prev_btn)
        
        self.grado_page_number = QLabel("Página 1 de 1")
        self.grado_page_number.setStyleSheet("""
            color: #2563eb; 
            font-weight: bold; 
            font-size: 14px;
            padding: 0 15px;
        """)
        pagination_layout.addWidget(self.grado_page_number)
        
        self.grado_next_btn = QPushButton("Siguiente ▶")
        self.grado_next_btn.setObjectName("refresh_btn")
        self.grado_next_btn.setMaximumWidth(100)
        self.grado_next_btn.clicked.connect(lambda: self.cambiar_pagina_grado('next'))
        pagination_layout.addWidget(self.grado_next_btn)
        
        self.grado_last_btn = QPushButton("Última ⏭")
        self.grado_last_btn.setObjectName("refresh_btn")
        self.grado_last_btn.setMaximumWidth(100)
        self.grado_last_btn.clicked.connect(lambda: self.cambiar_pagina_grado('last'))
        pagination_layout.addWidget(self.grado_last_btn)
        
        self.estudiantes_grado_layout.addWidget(pagination_frame)
        pagination_frame.setVisible(False)  # Oculto inicialmente
        self.grado_pagination_frame = pagination_frame  # Guardar referencia
        
        layout.addWidget(self.estudiantes_grado_container)
        
        self.tabs.addTab(tab, "Grados")

    def load_grados_tab(self):
        """Carga los botones de grados y sus estudiantes (FILTRANDO GRADOS INVÁLIDOS)"""
        # Limpiar botones anteriores
        while self.grados_layout.count():
            item = self.grados_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Obtener todos los grados
        grados = self.supabase_client.get_all_grados()
        
        # ✅ FILTRAR GRADOS INVÁLIDOS O SIN NOMBRE ESPECÍFICO
        grados_validos = []
        for grado in grados:
            nombre = grado.get('nombre_grado', '').strip()
            
            # Filtrar grados sin nombre o con nombre genérico
            if not nombre:
                continue
            
            # Filtrar "Grado" genérico sin número
            if nombre.lower() == 'grado':
                continue
            
            grados_validos.append(grado)
        
        if not grados_validos:
            # Mostrar mensaje si no hay grados válidos
            no_grados_label = QLabel("No hay grados creados. Crea uno nuevo usando el botón '+ Nuevo Grado'")
            no_grados_label.setStyleSheet("color: #666; font-style: italic;")
            self.grados_layout.addWidget(no_grados_label)
            return
        
        # Ordenar grados válidos
        grados_ordenados = sorted(grados_validos, key=lambda x: self.extraer_numero_grado(x['nombre_grado']))
        
        # Obtener todos los estudiantes UNA SOLA VEZ para optimizar
        todos_estudiantes = self.supabase_client.get_all_estudiantes()
        
        # Contar estudiantes por grado
        conteo_por_grado = {}
        for estudiante in todos_estudiantes:
            id_grado = estudiante.get('id_grado')
            if id_grado:
                conteo_por_grado[id_grado] = conteo_por_grado.get(id_grado, 0) + 1
        
        # Crear botón para cada grado
        for grado in grados_ordenados:
            # Crear botón personalizado
            grado_btn = QPushButton()
            grado_btn.setFixedSize(150, 100)
            
            # Obtener conteo de estudiantes desde el diccionario
            total_estudiantes = conteo_por_grado.get(grado['id_grado'], 0)
            
            # Texto del botón
            btn_text = f"{grado['nombre_grado']}\n\n"
            btn_text += f"👨‍🎓 {total_estudiantes} estudiante"
            btn_text += "s" if total_estudiantes != 1 else ""
            
            grado_btn.setText(btn_text)
            
            # Estilo del botón
            grado_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #ffffff;
                    color: #2c3e50;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    font-size: 13px;
                    font-weight: 600;
                    padding: 12px;
                    text-align: center;
                    border-bottom: 4px solid #e0e0e0;
                }}
                QPushButton:hover {{
                    background-color: #f8f9fa;
                    border-color: #3498db;
                    border-bottom: 4px solid #3498db;
                }}
                QPushButton:pressed {{
                    background-color: #e3f2fd;
                    border-color: #2980b9;
                    border-bottom: 2px solid #2980b9;
                    margin-top: 2px;
                }}
            """)
            
            # Conectar señal
            grado_btn.clicked.connect(lambda checked, g=grado: self.mostrar_estudiantes_grado(g))
            
            self.grados_layout.addWidget(grado_btn)
        
        # Agregar stretch
        self.grados_layout.addStretch()

    def mostrar_estudiantes_grado(self, grado):
        """Muestra los estudiantes de un grado específico con checkboxes al final"""
        # Limpiar filtros y paginación al cambiar de grado
        self.filtro_seccion_actual = None
        self.filtro_mencion_actual = None
        self.pagina_actual_grado = 0
        
        self.grado_actual_mostrado = grado.copy()  
        
        # Configurar columnas
        self.estudiantes_grado_table.setColumnCount(9)
        self.estudiantes_grado_table.setHorizontalHeaderLabels([
            "Cédula", "Nombre", "Apellido", "Fecha Nac.", 
            "Teléfono", "Correo", "Mención", "Sección", ""
        ])
        
        # Cargar estudiantes con paginación
        self.recargar_estudiantes_con_filtros(grado, reset_pagina=True)
        
        # Mostrar contenedor de estudiantes
        self.estudiantes_grado_container.setVisible(True)
        
        # Agregar barra de herramientas para acciones en masa
        self.agregar_barra_acciones_masa(grado)

    def agregar_barra_acciones_masa(self, grado):
        """Agrega barra de herramientas para acciones en masa (VERSIÓN ANTI-FANTASMA)"""
        
        # Limpiar barra anterior si existe
        if hasattr(self, 'acciones_masa_container') and self.acciones_masa_container:
            try:
                self.acciones_masa_container.deleteLater()
            except RuntimeError:
                pass  # Barra ya fue eliminada
        
        # Crear contenedor
        self.acciones_masa_container = QWidget()
        acciones_masa_layout = QHBoxLayout()
        acciones_masa_layout.setContentsMargins(10, 5, 10, 5)
        self.acciones_masa_container.setLayout(acciones_masa_layout)
        self.acciones_masa_container.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
        """)
        
        #  CHECKBOX "SELECCIONAR TODOS" (con referencia guardada)
        self.select_all_checkbox = QCheckBox("Seleccionar todos")
        self.select_all_checkbox.setStyleSheet("font-weight: bold; color: #333;")
        self.select_all_checkbox.stateChanged.connect(self.toggle_select_all)
        acciones_masa_layout.addWidget(self.select_all_checkbox)
        
        # Info de selección
        self.selection_info_label = QLabel("0 seleccionados")
        self.selection_info_label.setStyleSheet("color: #666; font-style: italic;")
        acciones_masa_layout.addWidget(self.selection_info_label)
        
        #  CONECTAR CHECKBOXES INDIVIDUALES PARA ACTUALIZAR CONTADOR
        for checkbox in self.checkboxes_estudiantes:
            if checkbox:
                checkbox.stateChanged.connect(self.actualizar_contador_seleccion)
        
        acciones_masa_layout.addStretch()
        
        # Botón "Mover seleccionados"
        mover_seleccionados_btn = QPushButton(" Mover Seleccionados")
        mover_seleccionados_btn.setObjectName("mover_btn")
        mover_seleccionados_btn.setToolTip("Mover todos los estudiantes seleccionados a otro grado")
        mover_seleccionados_btn.clicked.connect(
            lambda: self.mover_estudiantes_seleccionados(grado['id_grado'])
        )
        mover_seleccionados_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        acciones_masa_layout.addWidget(mover_seleccionados_btn)
        
        # Botón "Filtrar por" con menú desplegable
        filtrar_btn = QPushButton("🔍 Filtrar por")
        filtrar_btn.setObjectName("filtrar_btn")
        filtrar_btn.setToolTip("Filtrar estudiantes por sección o mención")
        filtrar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton::menu-indicator {
                width: 0px;
            }
        """)
        
        # Crear menú para el botón de filtros
        from PyQt6.QtWidgets import QMenu
        filtrar_menu = QMenu(filtrar_btn)
        filtrar_menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 2px solid #2196F3;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #1976D2;
            }
            QMenu::separator {
                height: 1px;
                background: #e0e0e0;
                margin: 5px 0px;
            }
        """)
        
        # Submenú Sección
        seccion_submenu = QMenu("📋 Sección", filtrar_menu)
        seccion_submenu.addAction("Todas", lambda: self.aplicar_filtro_seccion(None, grado))
        seccion_submenu.addSeparator()
        seccion_submenu.addAction("A", lambda: self.aplicar_filtro_seccion("A", grado))
        seccion_submenu.addAction("B", lambda: self.aplicar_filtro_seccion("B", grado))
        seccion_submenu.addAction("C", lambda: self.aplicar_filtro_seccion("C", grado))
        seccion_submenu.addAction("D", lambda: self.aplicar_filtro_seccion("D", grado))
        seccion_submenu.addAction("E", lambda: self.aplicar_filtro_seccion("E", grado))
        seccion_submenu.addAction("F", lambda: self.aplicar_filtro_seccion("F", grado))
        seccion_submenu.addAction("G", lambda: self.aplicar_filtro_seccion("G", grado))
        seccion_submenu.addSeparator()
        seccion_submenu.addAction("Sin sección", lambda: self.aplicar_filtro_seccion("sin_seccion", grado))
        
        # Submenú Mención
        mencion_submenu = QMenu("🎓 Mención", filtrar_menu)
        mencion_submenu.addAction("Todas", lambda: self.aplicar_filtro_mencion(None, grado))
        mencion_submenu.addSeparator()
        mencion_submenu.addAction("Media General", lambda: self.aplicar_filtro_mencion(1, grado))
        mencion_submenu.addAction("Técnico Superior", lambda: self.aplicar_filtro_mencion(2, grado))
        mencion_submenu.addSeparator()
        mencion_submenu.addAction("Sin mención", lambda: self.aplicar_filtro_mencion("sin_mencion", grado))
        
        # Agregar submenús al menú principal
        filtrar_menu.addMenu(seccion_submenu)
        filtrar_menu.addMenu(mencion_submenu)
        filtrar_menu.addSeparator()
        filtrar_menu.addAction("🔄 Limpiar todos los filtros", lambda: self.limpiar_todos_filtros(grado))
        
        filtrar_btn.setMenu(filtrar_menu)
        acciones_masa_layout.addWidget(filtrar_btn)
        
        # Inicializar variables de filtro si no existen
        if not hasattr(self, 'filtro_seccion_actual'):
            self.filtro_seccion_actual = None
        if not hasattr(self, 'filtro_mencion_actual'):
            self.filtro_mencion_actual = None
        
        # Insertar barra
        self.estudiantes_grado_layout.insertWidget(1, self.acciones_masa_container)

    def actualizar_contador_seleccion(self):
        """Actualiza el contador de estudiantes seleccionados"""
        seleccionados = self.get_estudiantes_seleccionados()
        total = len(seleccionados)
        
        if hasattr(self, 'selection_info_label') and self.selection_info_label:
            if total == 0:
                self.selection_info_label.setText("0 seleccionados")
                self.selection_info_label.setStyleSheet("color: #666; font-style: italic;")
            else:
                self.selection_info_label.setText(f"{total} seleccionado{'s' if total != 1 else ''}")
                self.selection_info_label.setStyleSheet("color: #2196F3; font-weight: bold;")

    def aplicar_filtro_seccion(self, seccion, grado):
        """Aplica filtro de sección y recarga la tabla"""
        self.filtro_seccion_actual = seccion
        self.recargar_estudiantes_con_filtros(grado)
    
    def aplicar_filtro_mencion(self, mencion, grado):
        """Aplica filtro de mención y recarga la tabla"""
        self.filtro_mencion_actual = mencion
        self.recargar_estudiantes_con_filtros(grado)
    
    def limpiar_todos_filtros(self, grado):
        """Limpia todos los filtros aplicados"""
        self.filtro_seccion_actual = None
        self.filtro_mencion_actual = None
        self.recargar_estudiantes_con_filtros(grado)
    
    def recargar_estudiantes_con_filtros(self, grado, reset_pagina=True):
        """Recarga la tabla de estudiantes aplicando los filtros actuales con paginación"""
        # Obtener todos los estudiantes del grado
        estudiantes = self.supabase_client.get_estudiantes_by_grado(grado['id_grado'])
        
        # Aplicar filtros
        estudiantes_filtrados = []
        for estudiante in estudiantes:
            # Filtro de sección
            if self.filtro_seccion_actual is not None:
                estudiante_seccion = estudiante.get('seccion', '')
                if self.filtro_seccion_actual == "sin_seccion":
                    if estudiante_seccion:  # Si tiene sección, no incluir
                        continue
                elif estudiante_seccion != self.filtro_seccion_actual:
                    continue
            
            # Filtro de mención
            if self.filtro_mencion_actual is not None:
                estudiante_mencion = estudiante.get('id_mencion')
                if self.filtro_mencion_actual == "sin_mencion":
                    if estudiante_mencion:  # Si tiene mención, no incluir
                        continue
                elif estudiante_mencion != self.filtro_mencion_actual:
                    continue
            
            estudiantes_filtrados.append(estudiante)
        
        # Guardar lista filtrada y total
        self.estudiantes_grado_filtrados = estudiantes_filtrados
        self.total_estudiantes_grado = len(estudiantes_filtrados)
        
        # Resetear página si es necesario
        if reset_pagina:
            self.pagina_actual_grado = 0
        
        # Calcular paginación
        total_paginas = max(1, (self.total_estudiantes_grado + self.estudiantes_grado_por_pagina - 1) // self.estudiantes_grado_por_pagina)
        
        # Ajustar página si está fuera de rango
        if self.pagina_actual_grado >= total_paginas:
            self.pagina_actual_grado = max(0, total_paginas - 1)
        
        # Calcular índices para la página actual
        inicio = self.pagina_actual_grado * self.estudiantes_grado_por_pagina
        fin = min(inicio + self.estudiantes_grado_por_pagina, self.total_estudiantes_grado)
        
        estudiantes_pagina = estudiantes_filtrados[inicio:fin]
        
        # Actualizar label con información de filtros
        total_original = len(estudiantes)
        
        if self.filtro_seccion_actual or self.filtro_mencion_actual:
            filtros_texto = []
            if self.filtro_seccion_actual:
                if self.filtro_seccion_actual == "sin_seccion":
                    filtros_texto.append("Sin sección")
                else:
                    filtros_texto.append(f"Sección {self.filtro_seccion_actual}")
            if self.filtro_mencion_actual:
                if self.filtro_mencion_actual == "sin_mencion":
                    filtros_texto.append("Sin mención")
                elif self.filtro_mencion_actual == 1:
                    filtros_texto.append("Media General")
                elif self.filtro_mencion_actual == 2:
                    filtros_texto.append("Técnico Superior")
            
            self.grado_label.setText(
                f"{grado['nombre_grado']} - {self.total_estudiantes_grado} de {total_original} estudiante{'s' if total_original != 1 else ''} "
                f"({', '.join(filtros_texto)})"
            )
        else:
            self.grado_label.setText(
                f"{grado['nombre_grado']} - {self.total_estudiantes_grado} estudiante{'s' if self.total_estudiantes_grado != 1 else ''}"
            )
        
        # Limpiar y recargar tabla
        self.estudiantes_grado_table.setRowCount(0)
        self.checkboxes_estudiantes = []
        
        for estudiante in estudiantes_pagina:
            row = self.estudiantes_grado_table.rowCount()
            self.estudiantes_grado_table.insertRow(row)
            
            # Datos del estudiante
            self.estudiantes_grado_table.setItem(row, 0, QTableWidgetItem(estudiante['cedula']))
            self.estudiantes_grado_table.setItem(row, 1, QTableWidgetItem(estudiante['nombre']))
            self.estudiantes_grado_table.setItem(row, 2, QTableWidgetItem(estudiante['apellido']))
            self.estudiantes_grado_table.setItem(row, 3, QTableWidgetItem(str(estudiante.get('fecha_nacimiento', ''))))
            self.estudiantes_grado_table.setItem(row, 4, QTableWidgetItem(estudiante.get('telefono') or ''))
            self.estudiantes_grado_table.setItem(row, 5, QTableWidgetItem(estudiante.get('correo') or ''))
            
            # Mención
            mencion_id = estudiante.get('id_mencion')
            mencion_texto = ""
            if mencion_id == 1:
                mencion_texto = "Media General"
            elif mencion_id == 2:
                mencion_texto = "Técnico Superior"
            self.estudiantes_grado_table.setItem(row, 6, QTableWidgetItem(mencion_texto))
            
            # Sección
            seccion = estudiante.get('seccion', '')
            self.estudiantes_grado_table.setItem(row, 7, QTableWidgetItem(seccion or '-'))
            
            # Checkbox
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout()
            checkbox_layout.setContentsMargins(5, 0, 5, 0)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox = QCheckBox()
            checkbox.setProperty('cedula', estudiante['cedula'])
            checkbox.stateChanged.connect(self.actualizar_contador_seleccion)
            checkbox_layout.addWidget(checkbox)
            checkbox_widget.setLayout(checkbox_layout)
            self.estudiantes_grado_table.setCellWidget(row, 8, checkbox_widget)
            self.checkboxes_estudiantes.append(checkbox)
        
        # Actualizar contador de selección
        self.actualizar_contador_seleccion()
        
        # Actualizar estado del checkbox "Seleccionar todos"
        if hasattr(self, 'select_all_checkbox') and self.select_all_checkbox:
            self.select_all_checkbox.setChecked(False)
        
        # Actualizar controles de paginación
        self.actualizar_controles_paginacion_grado()
        
        # Mostrar/ocultar controles de paginación según sea necesario
        if hasattr(self, 'grado_pagination_frame'):
            # Mostrar si hay al menos 1 estudiante
            self.grado_pagination_frame.setVisible(self.total_estudiantes_grado > 0)
    
    def actualizar_controles_paginacion_grado(self):
        """Actualiza los controles de paginación para la tabla de grado"""
        if not hasattr(self, 'grado_page_info'):
            return
        
        if self.total_estudiantes_grado == 0:
            # Caso especial: no hay estudiantes
            self.grado_page_info.setText("Mostrando 0 de 0 estudiantes")
            self.grado_page_number.setText("Página 1 de 1")
            self.grado_first_btn.setEnabled(False)
            self.grado_prev_btn.setEnabled(False)
            self.grado_next_btn.setEnabled(False)
            self.grado_last_btn.setEnabled(False)
            return
        
        total_paginas = max(1, (self.total_estudiantes_grado + self.estudiantes_grado_por_pagina - 1) // self.estudiantes_grado_por_pagina)
        pagina_mostrar = self.pagina_actual_grado + 1
        
        # Calcular índices mostrados
        inicio = self.pagina_actual_grado * self.estudiantes_grado_por_pagina + 1
        fin = min((self.pagina_actual_grado + 1) * self.estudiantes_grado_por_pagina, self.total_estudiantes_grado)
        
        # Actualizar labels
        self.grado_page_info.setText(
            f"Mostrando {inicio}-{fin} de {self.total_estudiantes_grado} estudiantes"
        )
        self.grado_page_number.setText(f"Página {pagina_mostrar} de {total_paginas}")
        
        # Habilitar/deshabilitar botones
        self.grado_first_btn.setEnabled(self.pagina_actual_grado > 0)
        self.grado_prev_btn.setEnabled(self.pagina_actual_grado > 0)
        self.grado_next_btn.setEnabled(self.pagina_actual_grado < total_paginas - 1)
        self.grado_last_btn.setEnabled(self.pagina_actual_grado < total_paginas - 1)
    
    def cambiar_pagina_grado(self, accion):
        """Cambia la página actual de la tabla de grado"""
        if not hasattr(self, 'grado_actual_mostrado') or not self.grado_actual_mostrado:
            return
        
        total_paginas = max(1, (self.total_estudiantes_grado + self.estudiantes_grado_por_pagina - 1) // self.estudiantes_grado_por_pagina)
        
        if accion == 'first':
            self.pagina_actual_grado = 0
        elif accion == 'prev':
            self.pagina_actual_grado = max(0, self.pagina_actual_grado - 1)
        elif accion == 'next':
            self.pagina_actual_grado = min(total_paginas - 1, self.pagina_actual_grado + 1)
        elif accion == 'last':
            self.pagina_actual_grado = total_paginas - 1
        
        # Recargar sin resetear la página
        self.recargar_estudiantes_con_filtros(self.grado_actual_mostrado, reset_pagina=False)

    def create_periodos_tab(self):
        """Crea la pestaña de períodos académicos"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        tab.setLayout(layout)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        toolbar.addStretch()
        
        add_btn = QPushButton("✚ Nuevo Período")
        add_btn.setObjectName("add_btn")
        add_btn.clicked.connect(self.add_periodo)
        toolbar.addWidget(add_btn)
        
        refresh_btn = QPushButton(" Actualizar")
        refresh_btn.setObjectName("refresh_btn")
        refresh_btn.clicked.connect(self.load_periodos)
        toolbar.addWidget(refresh_btn)
        
        layout.addLayout(toolbar)
        
        # Tabla de períodos
        self.periodos_table = QTableWidget()
        self.periodos_table.setColumnCount(3)
        self.periodos_table.setHorizontalHeaderLabels([
            "Año", "Fecha Inicio", "Fecha Fin"
        ])
        self.periodos_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.periodos_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.periodos_table)
        
        self.tabs.addTab(tab, "Períodos Académicos")

    def create_historial_tab(self):
            """Crea la pestaña de historial académico mejorado"""
            tab = QWidget()
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(20, 20, 20, 20)
            main_layout.setSpacing(15)
            tab.setLayout(main_layout)
            
            # ========== SECCIÓN DE BÚSQUEDA ==========
            search_frame = QFrame()
            search_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                    color: #555;
                }
            """)
            search_layout = QHBoxLayout()
            search_layout.setContentsMargins(15, 15, 15, 15)
            search_frame.setLayout(search_layout)
            
            search_label = QLabel("Cédula del Estudiante:")
            search_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            search_layout.addWidget(search_label)
            
            self.historial_search = QLineEdit()
            self.historial_search.setPlaceholderText("Ingrese la cédula...")
            self.historial_search.setMaximumWidth(250)
            self.historial_search.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 14px;
                }
            """)
            self.historial_search.returnPressed.connect(self.load_historial_completo)
            search_layout.addWidget(self.historial_search)
            
            search_btn = QPushButton("🔍 Buscar")
            search_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 8px 20px;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)
            search_btn.clicked.connect(self.load_historial_completo)
            search_layout.addWidget(search_btn)
            
            # SI ESTAS VIENDO ESTO SEGURAMENTE QUIERES LA FUNCIÓN DE IMPRIMIR PARA IMPRIMIR EL HISTORIAL ACADÉMICO COMPLETO, ASI QUE BUENA SUERTE CRACK
            # Botón imprimir (inicialmente oculto)
            #self.imprimir_historial_btn = QPushButton("🖨️ Imprimir Historial")
            #self.imprimir_historial_btn.setStyleSheet("""
            #"""QPushButton {
            #        background-color: #4CAF50;
            #        color: white;
            #        border: none;
            #        padding: 8px 20px;
            #        border-radius: 4px;
            #        font-size: 14px;
            #        font-weight: bold;
            #    }
            #    QPushButton:hover {
            #        background-color: #45a049;
            #    }
            #""")
            #self.imprimir_historial_btn.clicked.connect(self.imprimir_historial)
            #self.imprimir_historial_btn.setVisible(False)
            #search_layout.addWidget(self.imprimir_historial_btn)
            
            search_layout.addStretch()
            
            main_layout.addWidget(search_frame)
            
            # ========== ÁREA DE CONTENIDO DEL HISTORIAL ==========
            # Scroll area para el historial
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background-color: transparent;
                                    color
                }
            """)
            
            # Widget contenedor del historial
            self.historial_content = QWidget()
            self.historial_layout = QVBoxLayout()
            self.historial_layout.setSpacing(20)
            self.historial_content.setLayout(self.historial_layout)
            
            scroll_area.setWidget(self.historial_content)
            main_layout.addWidget(scroll_area)
            
            # Mensaje inicial
            self.show_historial_placeholder()
            
            self.tabs.addTab(tab, "Historial Académico")

    def show_historial_placeholder(self):
        """Muestra un mensaje placeholder cuando no hay historial cargado"""
        # Limpiar layout
        while self.historial_layout.count():
            child = self.historial_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        placeholder = QLabel("👤 Busque un estudiante por su cédula para ver su historial académico completo")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("""
            QLabel {
                color: #999;
                font-size: 16px;
                padding: 100px;
            }
        """)
        self.historial_layout.addWidget(placeholder)

    def load_historial_completo(self):
        """Carga y muestra el historial académico completo del estudiante"""
        cedula = self.historial_search.text().strip()
        
        if not cedula:
            QMessageBox.warning(self, "Advertencia", "Por favor ingrese la cédula del estudiante")
            return
        
        # Obtener historial completo
        historial_data = self.supabase_client.get_historial_completo_estudiante(cedula)
        
        if not historial_data:
            QMessageBox.information(
                self, 
                "No encontrado", 
                f"No se encontró ningún estudiante con la cédula {cedula}"
            )
            self.show_historial_placeholder()
            self.imprimir_historial_btn.setVisible(False)
            return
        
        # Guardar datos para impresión
        self.current_historial_data = historial_data
        
        # Mostrar botón de imprimir
        # self.imprimir_historial_btn.setVisible(True)
        
        # Limpiar layout anterior
        while self.historial_layout.count():
            child = self.historial_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        info_estudiante = historial_data['info_estudiante']
        historial_por_año = historial_data['historial_por_año']
        
        # ========== INFORMACIÓN DEL ESTUDIANTE ==========
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 2px solid #2196F3;
            }
        """)
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_frame.setLayout(info_layout)
        
        # Título
        titulo = QLabel(f"📋 Historial Académico")
        titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 10px;
        """)
        info_layout.addWidget(titulo)
        
        # Información del estudiante
        nombre_completo = f"{info_estudiante['nombre']} {info_estudiante['apellido']}"
        
        # Mención
        menciones = {
            1: "Media General",
            2: "Técnico Superior"
        }
        id_mencion = info_estudiante.get('id_mencion')
        mencion_texto = menciones.get(id_mencion, 'No asignada') if id_mencion else 'No asignada'
        
        # Domicilio
        pais = info_estudiante.get('pais') or 'N/A'
        estado = info_estudiante.get('estado') or 'N/A'
        municipio = info_estudiante.get('municipio') or 'N/A'
        domicilio = f"{pais}, {estado}, {municipio}"
        
        # Observaciones
        observacion = info_estudiante.get('observacion') or 'Sin observaciones'
        seccion = info_estudiante.get('seccion') or 'No asignada'

        info_text = f"""
        <p style='font-size: 14px; line-height: 1.8; color: #555;'>
            <b>Nombre:</b> {nombre_completo}<br>
            <b>Cédula:</b> {info_estudiante['cedula']}<br>
            <b>Grado Actual:</b> {info_estudiante['nombre_grado'] or 'No asignado'}<br>
            <b>Sección:</b> {seccion}<br>
            <b>Mención:</b> {mencion_texto}<br>
            <b>Fecha de Nacimiento:</b> {info_estudiante['fecha_nacimiento']}<br>
            <b>Domicilio:</b> {domicilio}<br>
            <b>Observaciones:</b> {observacion}
        </p>
        """
        info_label = QLabel(info_text)
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        self.historial_layout.addWidget(info_frame)
        
        # ========== TABLAS POR AÑO (1RO A 6TO) ==========
        años = ['1', '2', '3', '4', '5', '6']
        nombres_años = {
            '1': '1er Año',
            '2': '2do Año',
            '3': '3er Año',
            '4': '4to Año',
            '5': '5to Año',
            '6': '6to Año'
        }
        
        for año in años:
            materias = historial_por_año.get(año, [])
            
            # Frame para cada año
            año_frame = QFrame()
            año_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                }
            """)
            año_layout = QVBoxLayout()
            año_layout.setContentsMargins(15, 15, 15, 15)
            año_frame.setLayout(año_layout)
            
            # Título del año
            año_titulo = QLabel(f"📚 {nombres_años[año]}")
            año_titulo.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                color: #333;
                padding: 5px;
            """)
            año_layout.addWidget(año_titulo)
            
            # Tabla de materias
            table = QTableWidget()
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Asignatura", "Nota Final", "Estado"])
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
            table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
            table.setColumnWidth(1, 100)
            table.setColumnWidth(2, 120)
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            table.setStyleSheet("""
                QTableWidget {
                    border: 1px solid #ddd;
                    gridline-color: #2196f3;
                }
                QHeaderView::section {
                    background-color: #f5f5f5;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                    color:#555;
                }
            """)
            
            if materias:
                table.setRowCount(len(materias))
                for row, materia in enumerate(materias):
                    # Asignatura
                    asig_item = QTableWidgetItem(materia['nombre_asignatura'])
                    table.setItem(row, 0, asig_item)
                    
                    # Nota Final
                    nota = materia['nota_final']
                    nota_text = f"{nota:.2f}" if nota is not None else "N/A"
                    nota_item = QTableWidgetItem(nota_text)
                    nota_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, 1, nota_item)
                    
                    # Estado
                    estado = materia.get('estado', 'N/A')
                    estado_item = QTableWidgetItem(estado)
                    estado_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    # Colores según el estado
                    if estado == 'APROBADO':
                        estado_item.setBackground(QColor("#d4edda"))
                        estado_item.setForeground(QColor("#155724"))
                    elif estado == 'REPROBADO':
                        estado_item.setBackground(QColor("#f8d7da"))
                        estado_item.setForeground(QColor("#721c24"))
                    elif estado == 'EN CURSO':
                        estado_item.setBackground(QColor("#fff3cd"))
                        estado_item.setForeground(QColor("#856404"))
                    
                    table.setItem(row, 2, estado_item)
                
                # Ajustar altura de la tabla
                table.setMinimumHeight(60 + (len(materias) * 12))
                table.setMaximumHeight(300)
            else:
                # Mostrar mensaje cuando no hay materias
                table.setRowCount(1)
                no_data_item = QTableWidgetItem("No hay materias registradas para este año")
                no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                no_data_item.setForeground(QColor("#999"))
                table.setItem(0, 0, no_data_item)
                table.setSpan(0, 0, 1, 3)
                table.setMinimumHeight(80)
            
            año_layout.addWidget(table)
            self.historial_layout.addWidget(año_frame)
        
        # Espaciador al final
        self.historial_layout.addStretch()

    def imprimir_historial(self):
        """Genera e imprime/guarda el historial académico en PDF"""
        if not hasattr(self, 'current_historial_data') or not self.current_historial_data:
            QMessageBox.warning(self, "Advertencia", "No hay historial cargado para imprimir")
            return
        
        try:
            from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
            from PyQt6.QtGui import QPainter, QPageLayout, QPageSize
            from PyQt6.QtCore import QMarginsF
            from PyQt6.QtWidgets import QFileDialog
            
            # Preguntar dónde guardar
            cedula = self.current_historial_data['info_estudiante']['cedula']
            default_filename = f"Historial_Academico_{cedula}.pdf"
            
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar Historial Académico",
                default_filename,
                "PDF Files (*.pdf)"
            )
            
            if not filename:
                return  # Usuario canceló
            
            # Crear PDF
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)
            
            # Configurar página
            page_layout = QPageLayout()
            page_layout.setPageSize(QPageSize(QPageSize.PageSizeId.Letter))
            page_layout.setOrientation(QPageLayout.Orientation.Portrait)
            page_layout.setMargins(QMarginsF(20, 20, 20, 20))
            printer.setPageLayout(page_layout)
            
            # Generar el contenido del PDF
            self.generar_pdf_historial(printer)
            
            QMessageBox.information(
                self,
                "Éxito",
                f"El historial académico se guardó correctamente en:\n{filename}"
            )
            
        except ImportError:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo importar los módulos necesarios para generar el PDF"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al generar el PDF:\n{str(e)}"
            )
            import traceback

    def generar_pdf_historial(self, printer):
        """
        Genera el contenido del PDF del historial
        
        Args:
            printer: Objeto QPrinter configurado
        """
        from PyQt6.QtGui import QPainter, QFont, QPen
        from PyQt6.QtCore import Qt, QRect
        
        painter = QPainter()
        painter.begin(printer)
        
        # Configuración de fuentes
        font_titulo = QFont("Arial", 16, QFont.Weight.Bold)
        font_subtitulo = QFont("Arial", 12, QFont.Weight.Bold)
        font_normal = QFont("Arial", 10)
        font_small = QFont("Arial", 9)
        
        # Obtener dimensiones de la página
        page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
        width = int(page_rect.width())
        height = int(page_rect.height())
        
        y_position = 50  # Posición vertical inicial
        line_height = 25
        
        info_estudiante = self.current_historial_data['info_estudiante']
        historial_por_año = self.current_historial_data['historial_por_año']
        
        # ========== ENCABEZADO ==========
        painter.setFont(font_titulo)
        painter.drawText(QRect(50, y_position, width - 100, 50), 
                        Qt.AlignmentFlag.AlignCenter, 
                        "HISTORIAL ACADÉMICO")
        y_position += 60
        
        painter.setFont(font_subtitulo)
        painter.drawText(QRect(50, y_position, width - 100, 30),
                        Qt.AlignmentFlag.AlignCenter,
                        "U.E Liceo Nueva Esparta")
        y_position += 50
        
        # ========== INFORMACIÓN DEL ESTUDIANTE ==========
        painter.setFont(font_normal)
        nombre_completo = f"{info_estudiante['nombre']} {info_estudiante['apellido']}"
        
        painter.drawText(50, y_position, f"Nombre: {nombre_completo}")
        y_position += line_height
        
        painter.drawText(50, y_position, f"Cédula: {info_estudiante['cedula']}")
        y_position += line_height
        
        painter.drawText(50, y_position, f"Grado Actual: {info_estudiante['nombre_grado'] or 'No asignado'}")
        y_position += line_height
        
        painter.drawText(50, y_position, f"Fecha de Nacimiento: {info_estudiante['fecha_nacimiento']}")
        y_position += line_height + 20
        
        # Línea separadora
        painter.drawLine(50, y_position, width - 50, y_position)
        y_position += 30
        
        # ========== TABLAS POR AÑO ==========
        años = ['1', '2', '3', '4', '5', '6']
        nombres_años = {
            '1': '1er Año',
            '2': '2do Año',
            '3': '3er Año',
            '4': '4to Año',
            '5': '5to Año',
            '6': '6to Año'
        }
        
        for año in años:
            materias = historial_por_año.get(año, [])
            
            # Verificar si necesitamos nueva página
            espacio_necesario = 100 + (len(materias) * 25) if materias else 100
            if y_position + espacio_necesario > height - 100:
                printer.newPage()
                y_position = 50
            
            # Título del año
            painter.setFont(font_subtitulo)
            painter.drawText(50, y_position, nombres_años[año])
            y_position += 30
            
            if materias:
                # Encabezados de tabla
                painter.setFont(font_small)
                painter.setPen(QPen(Qt.GlobalColor.black, 2))
                
                col1_x = 70
                col2_x = width - 250
                col3_x = width - 150
                
                painter.drawText(col1_x, y_position, "Asignatura")
                painter.drawText(col2_x, y_position, "Nota Final")
                painter.drawText(col3_x, y_position, "Estado")
                y_position += 5
                
                # Línea bajo encabezados
                painter.drawLine(50, y_position, width - 50, y_position)
                y_position += 20
                
                # Filas de materias
                for materia in materias:
                    painter.drawText(col1_x, y_position, materia['nombre_asignatura'])
                    
                    nota = materia['nota_final']
                    nota_text = f"{nota:.2f}" if nota is not None else "N/A"
                    painter.drawText(col2_x, y_position, nota_text)
                    
                    estado = materia.get('estado', 'N/A')
                    painter.drawText(col3_x, y_position, estado)
                    
                    y_position += 25
                
                y_position += 15
            else:
                painter.setFont(font_small)
                painter.drawText(70, y_position, "No hay materias registradas para este año")
                y_position += 40
            
            # Línea separadora entre años
            painter.drawLine(50, y_position, width - 50, y_position)
            y_position += 25
        
        painter.end()