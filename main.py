import sys
from dotenv import load_dotenv
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon   
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from database.supabase_client import SupabaseClient


def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


# Cargar variables de entorno 
if getattr(sys, 'frozen', False):
    # Ejecutable
    base_path = sys._MEIPASS
else:
    # Desarrollo
    base_path = os.path.dirname(os.path.abspath(__file__))


env_path = os.path.join(base_path, '.env')
load_dotenv(env_path)

class AcademicSystem:
    """Clase principal del sistema académico"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("AMALIA")
        self.app.setOrganizationName("U.E Nueva Esparta")
        
        # Configurar el estilo de la aplicación
        self.setup_style()
        
        # Configurar icono de la aplicación
        self.setup_icon()
        
        # Obtener la URL de la base de datos
        self.database_url = os.getenv("DATABASE_URL")
        
        if not self.database_url:
            self.show_error("No se encontró DATABASE_URL en el archivo .env")
            sys.exit(1)
        
        # Inicializar conexiones
        self.supabase_client = SupabaseClient(self.database_url)
        
        
        # Ventana de login como punto de inicio
        self.login_window = None
        
    def setup_icon(self):
        """Configura el icono de la aplicación"""
        try:
            # Usar resource_path para obtener la ruta correcta
            icon_path = resource_path("assets/escudo.png")
            
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                self.app.setWindowIcon(icon)
                print(f"Icono cargado desde: {icon_path}")
            else:
                print(f"Advertencia: No se encontró el icono en {icon_path}")
        except Exception as e:
            print(f"Error al cargar el icono: {e}")
    
    def setup_style(self):
        """Configura el estilo visual de la aplicación"""
        try:
            # Usar resource_path para obtener la ruta correcta
            style_path = resource_path('assets/style.qss')
            
            if os.path.exists(style_path):
                with open(style_path, 'r', encoding='utf-8') as f:
                    self.app.setStyleSheet(f.read())
                print(f"Estilos cargados desde: {style_path}")
            else:
                print(f"Advertencia: No se encontró style.qss en {style_path}")
                self.apply_default_styles()
                
        except Exception as e:
            print(f"Error al cargar estilos: {e}")
            self.apply_default_styles()
            
    def apply_default_styles(self):
        """Aplica estilos por defecto si no se encuentra el archivo QSS"""
        self.app.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
            QTableWidget {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
    
    def show_error(self, message):
        """Muestra un mensaje de error"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec()
    
    def ejecutar_mantenimiento_grado(self):
        """Ejecuta la función de mantenimiento del grado test"""
        try:
            # Ejecutar la función de PostgreSQL
            success = self.supabase_client.execute_function('mantener_grado_test')
            
            if success:
                print(" Mantenimiento de grado test ejecutado correctamente")
            else:
                print(" Error al ejecutar mantenimiento de grado")
                
        except Exception as e:
            print(f" Error al ejecutar mantenimiento de grado: {e}")
    
    def run(self):
        """Inicia la aplicación"""
        
        print("Verificando conexión a la base de datos...")
        if not self.check_database_connection():
            self.show_error("No se pudo conectar a la base de datos.\nVerifica tu archivo .env y la conexión a internet.")
            return 1
        
        print("Conexión establecida correctamente\n")
        
        # Ejecutar mantenimiento de grado test
        print("Ejecutando mantenimiento de grado test...")
        self.ejecutar_mantenimiento_grado()
        
        # Mostrar ventana de login
        self.login_window = LoginWindow(
            supabase_client=self.supabase_client,
        )
        self.login_window.show()
        
        # Ejecutar el loop de eventos de Qt
        return self.app.exec()
    
    def check_database_connection(self):
        """Verifica la conexión con las bases de datos"""
        try:
            # Verificar conexión a Supabase
            supabase_ok = self.supabase_client.test_connection()
            
            if supabase_ok:
                print("Conexión con la base de datos establecida")
            else:
                print("Error al conectar con la base de datos")
            
            
            # Retornar True si la conexión principal funciona
            return supabase_ok
            
        except Exception as e:
            print(f"Error al verificar conexiones: {e}")
            return False


def main():
    """Función principal"""
    # Habilitar High DPI scaling para pantallas de alta resolución
    if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Crear y ejecutar la aplicación
    system = AcademicSystem()
    sys.exit(system.run())


if __name__ == "__main__":
    main()