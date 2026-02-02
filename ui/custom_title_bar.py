
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent

class CustomTitleBar(QWidget):
    """Barra de título personalizada reusable"""
    
    def __init__(self, parent=None, title="AMALIA - Sistema Académico"):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
        # Variables para arrastrar la ventana
        self.drag_position = QPoint()
        
        if title:
            self.set_title(title)
        
    def setup_ui(self):
        """Configura la interfaz de la barra de título"""
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QWidget {
                background-color: #003366;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 10, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        # Título de la ventana
        self.title_label = QLabel("AMALIA - Sistema Académico")
        self.title_label.setStyleSheet("""
            color: white;
            font-size: 13px;
            font-weight: bold;
        """)
        layout.addWidget(self.title_label)
        
        # Espaciador
        layout.addStretch()
        
        # Botón minimizar
        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(40, 40)
        self.minimize_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.minimize_button.clicked.connect(self.minimize_window)
        layout.addWidget(self.minimize_button)
        
        # Botón cerrar
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(40, 40)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        self.close_button.clicked.connect(self.close_window)
        layout.addWidget(self.close_button)
    
    def minimize_window(self):
        """Minimiza la ventana"""
        if self.parent:
            self.parent.showMinimized()
    
    def close_window(self):
        """Cierra la ventana"""
        if self.parent:
            self.parent.close()
    
    def set_title(self, title: str):
        """Cambia el título de la ventana"""
        self.title_label.setText(title)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Inicia el arrastre de la ventana"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Mueve la ventana mientras se arrastra"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.parent.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()