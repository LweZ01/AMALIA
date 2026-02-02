from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QPixmap, QFont, QMouseEvent
import os  # <-- AÑADE ESTA IMPORTACIÓN
import sys  # <-- AÑADE ESTA IMPORTACIÓN
from database.supabase_client import SupabaseClient
from ui.custom_title_bar import CustomTitleBar


def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class LoginWindow(QMainWindow):
    """Ventana de inicio de sesión"""
    
    # Señal que se emite cuando el login es exitoso
    login_successful = pyqtSignal(dict)
    
    def __init__(self, supabase_client: SupabaseClient):
        super().__init__()
        self.supabase_client = supabase_client
        self.main_window = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Quitar la barra de título nativa
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setFixedSize(500, 640)
        
        # Widget central principal
        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #003366;")  # Agregar fondo
        self.setCentralWidget(main_widget)
        
        # Layout principal que contiene todo
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        main_widget.setLayout(container_layout)
        
        # Agregar barra de título personalizada
        self.title_bar = CustomTitleBar(self)
        self.title_bar.set_title("AMALIA - Inicio de Sesión")
        container_layout.addWidget(self.title_bar)
        
        # Widget de contenido (el azul oscuro)
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background-color: #0d1f3d;
            }
        """)
        container_layout.addWidget(content_widget)
        
        # Layout del contenido
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 40, 50, 60)
        main_layout.setSpacing(30)
        content_widget.setLayout(main_layout)
        
        # Espacio superior
        main_layout.addStretch(0)
        
        # Logo/Escudo - USANDO resource_path
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setMinimumHeight(200)
        logo_label.setStyleSheet("background-color: transparent;")
        
        # Intentar cargar el logo CON resource_path
        try:
            # Usar resource_path para obtener la ruta correcta
            icon_path = resource_path("assets/escudo.png")
            
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, 
                                             Qt.TransformationMode.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
                print(f"Icono cargado correctamente desde: {icon_path}")  # Para debug
            else:
                raise FileNotFoundError("El archivo de imagen está vacío o dañado")
                
        except Exception as e:
            # Si no se encuentra la imagen, mostrar texto
            print(f"Error cargando el logo: {e}")
            logo_label.setText("icono")
            logo_label.setStyleSheet("""
                font-size: 120px;
                color: white;
                background-color: transparent;
            """)
        
        main_layout.addWidget(logo_label)
        
        main_layout.addStretch(0)
        
        
        # Frame de login (blanco)
        login_frame = QFrame()
        login_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)
        login_layout = QVBoxLayout()
        login_layout.setContentsMargins(35, 35, 35, 35)
        login_layout.setSpacing(18)
        login_frame.setLayout(login_layout)
        
        # Título de la institución
        title_label = QLabel("U.E Liceo Nueva Esparta")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            color: #1f2937;
            margin-bottom: 10px;
        """)
        login_layout.addWidget(title_label)
        
        # Campo de usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setMinimumHeight(50)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: none;
                border-radius: 6px;
                padding: 0 15px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                background-color: #ebebeb;
            }
        """)
        self.username_input.returnPressed.connect(self.handle_login)
        login_layout.addWidget(self.username_input)
        
        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(50)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: none;
                border-radius: 6px;
                padding: 0 15px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                background-color: #ebebeb;
            }
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        login_layout.addWidget(self.password_input)
        
        # Botón de login
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setMinimumHeight(50)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
            QPushButton:disabled {
                background-color: #93c5fd;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        login_layout.addWidget(self.login_button)
        
        main_layout.addWidget(login_frame)
        
        # Espaciador
        main_layout.addStretch(3)
        
        # Centrar la ventana en la pantalla
        self.center_window()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def handle_login(self):
        """Maneja el proceso de inicio de sesión"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        # Validación básica
        if not username or not password:
            self.show_error("Por favor, ingresa tu usuario y contraseña")
            return
        
        # Deshabilitar el botón mientras se procesa
        self.login_button.setEnabled(False)
        self.login_button.setText("Iniciando sesión...")
        
        # Intentar iniciar sesión
        try:
            user = self.supabase_client.get_user_by_credentials(username, password)
            
            if user:
                # Obtener información adicional según el rol
                user_info = self.get_user_full_info(user)
                
                self.login_successful.emit(user_info)
                
                # Abrir la ventana principal según el rol
                self.open_main_window(user_info)
            else:
                self.show_error("Usuario o contraseña incorrectos")
                
        except Exception as e:
            self.show_error(f"Error al conectar con el servidor:\n{str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Rehabilitar el botón
            self.login_button.setEnabled(True)
            self.login_button.setText("Iniciar Sesión")
    
    def get_user_full_info(self, user: dict) -> dict:
        """
        Obtiene información completa del usuario según su rol
        
        Args:
            user: Diccionario básico del usuario
            
        Returns:
            Diccionario con información completa del usuario
        """
        user_info = user.copy()
        
        try:
            if user['rol'] == 'docente' and user.get('cedula'):
                # Obtener información del docente
                docente = self.supabase_client.get_docente_by_id(user['cedula'])
                if docente:
                    user_info['nombre_completo'] = f"{docente['nombre']} {docente['apellido']}"
                    user_info['correo'] = docente['correo']
                    user_info['telefono'] = docente['telefono']
                    user_info['especialidad'] = docente['especialidad']
                else:
                    user_info['nombre_completo'] = user['nombre_usuario']
                    
            else:  # admin
                user_info['nombre_completo'] = user['nombre_usuario']
                
        except Exception as e:
            print(f"Error al obtener información del usuario: {e}")
            user_info['nombre_completo'] = user['nombre_usuario']
        
        return user_info
    
    def open_main_window(self, user_data: dict):
        """
        Abre la ventana principal según el rol del usuario
        
        Args:
            user_data: Diccionario con los datos del usuario
        """
        rol = user_data.get('rol', '')
        
        try:
            # Importar la ventana correspondiente
            if rol == 'admin':
                from ui.main_window import MainWindow
                self.main_window = MainWindow(self.supabase_client, user_data)
            elif rol == 'docente':
                from ui.docente_window import DocenteWindow
                self.main_window = DocenteWindow(self.supabase_client, user_data)
            else:
                self.show_error(f"Rol de usuario no reconocido: {rol}")
                return
            self.main_window.show()
            self.close()
            
        except ImportError as e:
            # Si las ventanas aún no existen, mostrar mensaje temporal
            self.show_info(
                f"Login exitoso como {rol}!\n\n"
                f"Usuario: {user_data.get('nombre_completo', 'N/A')}\n"
                f"Rol: {rol}\n\n"
                f"La ventana principal aún no está implementada.\n"
                f"Error: {str(e)}"
            )
    
    def show_error(self, message: str):
        """Muestra un mensaje de error"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def show_success(self, message: str):
        """Muestra un mensaje de éxito"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Éxito")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
    
    def show_info(self, message: str):
        """Muestra un mensaje informativo"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Información")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()