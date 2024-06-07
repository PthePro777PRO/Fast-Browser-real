from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)  # Set the height of the title bar

        # Styling the title bar
        self.setStyleSheet("""
            background-color: #333;
            color: white;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            padding: 5px;
        """)

        # Create layout for the title bar
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create custom buttons
        self.minimize_button = QLabel("–")
        self.maximize_button = QLabel("□")
        self.close_button = QLabel("✕")

        # Set object names for styling
        self.minimize_button.setObjectName("minimize_button")
        self.maximize_button.setObjectName("maximize_button")
        self.close_button.setObjectName("close_button")

        # Add buttons to the title bar layout
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

        # Set layout
        self.setLayout(layout)

        # Connect buttons to their actions
        self.minimize_button.mousePressEvent = lambda event: parent.showMinimized()
        self.maximize_button.mousePressEvent = lambda event: self.toggleMaximized(parent)
        self.close_button.mousePressEvent = lambda event: parent.close()

        # Event handling for window dragging
        self.draggable = True
        self.drag_pos = None

    def toggleMaximized(self, window):
        if window.isMaximized():
            window.showNormal()
        else:
            window.showMaximized()