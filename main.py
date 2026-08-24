#main.py of sgse(i want to see language - python 100%)

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SceneWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.objects = []
        self.dragging_index = -1
        self.drag_offset = None
        
    def set_objects(self, objects):
        self.objects = objects
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Фон
        painter.fillRect(self.rect(), QColor(40, 40, 50))
        
        # Сетка
        painter.setPen(QPen(QColor(60, 60, 70), 1))
        for x in range(0, self.width(), 50):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 50):
            painter.drawLine(0, y, self.width(), y)
        
        # Центральная линия
        painter.setPen(QPen(QColor(100, 100, 120), 1, Qt.DashLine))
        painter.drawLine(self.width()//2, 0, self.width()//2, self.height())
        painter.drawLine(0, self.height()//2, self.width(), self.height()//2)
        
        # Объекты
        for obj in self.objects:
            x = int(obj['x'])
            y = int(obj['y'])
            size = int(obj['size'])
            color = obj['color']
            
            r = int(color[0] * 255)
            g = int(color[1] * 255)
            b = int(color[2] * 255)
            
            painter.setBrush(QColor(r, g, b))
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            
            if obj['type'] == 'square':
                painter.drawRect(x - size//2, y - size//2, size, size)
            elif obj['type'] == 'circle':
                painter.drawEllipse(QPointF(x, y), size/2, size/2)
            elif obj['type'] == 'triangle':
                path = QPainterPath()
                path.moveTo(x, y - size//2)
                path.lineTo(x - size//2, y + size//2)
                path.lineTo(x + size//2, y + size//2)
                path.closeSubpath()
                painter.drawPath(path)
            elif obj['type'] == 'cube':
                h = size//2
                points = [
                    QPoint(x, y - h),
                    QPoint(x + int(h*0.866), y - int(h*0.5)),
                    QPoint(x + int(h*0.866), y + int(h*0.5)),
                    QPoint(x, y + h),
                    QPoint(x - int(h*0.866), y + int(h*0.5)),
                    QPoint(x - int(h*0.866), y - int(h*0.5))
                ]
                painter.drawPolygon(points)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for i, obj in enumerate(self.objects):
                size = int(obj['size'])
                x = int(obj['x'])
                y = int(obj['y'])
                rect = QRect(x - size//2, y - size//2, size, size)
                if rect.contains(event.pos()):
                    self.dragging_index = i
                    self.drag_offset = QPoint(int(obj['x'] - event.pos().x()), int(obj['y'] - event.pos().y()))
                    self.setCursor(Qt.ClosedHandCursor)
                    return
    
    def mouseMoveEvent(self, event):
        if self.dragging_index >= 0:
            obj = self.objects[self.dragging_index]
            obj['x'] = event.pos().x() + self.drag_offset.x()
            obj['y'] = event.pos().y() + self.drag_offset.y()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if self.dragging_index >= 0:
            self.dragging_index = -1
            self.setCursor(Qt.ArrowCursor)
            self.update()

class SceneEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SGS Scene Editor v2.0")
        self.setGeometry(100, 100, 1200, 700)
        
        self.objects = []
        self.selected_index = -1
        
        self.init_ui()
        
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setSpacing(0)
        
        # СЦЕНА
        self.scene = SceneWidget()
        layout.addWidget(self.scene, 2)
        
        # ПАНЕЛЬ ИНСПЕКТОРА
        inspector = QWidget()
        inspector.setMaximumWidth(300)
        inspector.setStyleSheet("background: #2d2d2d; color: white;")
        inspector_layout = QVBoxLayout(inspector)
        layout.addWidget(inspector)
        
        title = QLabel("INSPECTOR")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        inspector_layout.addWidget(title)
        
        # Добавление объектов
        add_group = QGroupBox("Add Object")
        add_group.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        add_layout = QHBoxLayout(add_group)
        
        btn_square = QPushButton("□ Square")
        btn_square.clicked.connect(lambda: self.add_object("square"))
        btn_square.setStyleSheet("background: #3d3d3d; color: white; padding: 5px;")
        add_layout.addWidget(btn_square)
        
        btn_circle = QPushButton("○ Circle")
        btn_circle.clicked.connect(lambda: self.add_object("circle"))
        btn_circle.setStyleSheet("background: #3d3d3d; color: white; padding: 5px;")
        add_layout.addWidget(btn_circle)
        
        btn_triangle = QPushButton("△ Triangle")
        btn_triangle.clicked.connect(lambda: self.add_object("triangle"))
        btn_triangle.setStyleSheet("background: #3d3d3d; color: white; padding: 5px;")
        add_layout.addWidget(btn_triangle)
        
        btn_cube = QPushButton("▣ Cube")
        btn_cube.clicked.connect(lambda: self.add_object("cube"))
        btn_cube.setStyleSheet("background: #3d3d3d; color: white; padding: 5px;")
        add_layout.addWidget(btn_cube)
        
        inspector_layout.addWidget(add_group)
        
        # Список объектов
        list_label = QLabel("Objects")
        list_label.setStyleSheet("font-weight: bold; padding: 10px 0 5px 0;")
        inspector_layout.addWidget(list_label)
        
        self.object_list = QListWidget()
        self.object_list.setStyleSheet("background: #1d1d1d; color: white; border: none;")
        self.object_list.itemClicked.connect(self.select_object)
        inspector_layout.addWidget(self.object_list)
        
        # Свойства
        props_group = QGroupBox("Properties")
        props_group.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        props_layout = QGridLayout(props_group)
        
        props_layout.addWidget(QLabel("X:"), 0, 0)
        self.pos_x = QDoubleSpinBox()
        self.pos_x.setRange(-1000, 1000)
        self.pos_x.valueChanged.connect(self.update_object)
        props_layout.addWidget(self.pos_x, 0, 1)
        
        props_layout.addWidget(QLabel("Y:"), 1, 0)
        self.pos_y = QDoubleSpinBox()
        self.pos_y.setRange(-1000, 1000)
        self.pos_y.valueChanged.connect(self.update_object)
        props_layout.addWidget(self.pos_y, 1, 1)
        
        props_layout.addWidget(QLabel("Size:"), 2, 0)
        self.size_val = QDoubleSpinBox()
        self.size_val.setRange(1, 500)
        self.size_val.setValue(100)
        self.size_val.valueChanged.connect(self.update_object)
        props_layout.addWidget(self.size_val, 2, 1)
        
        # Цвет
        color_label = QLabel("Color:")
        color_label.setStyleSheet("font-weight: bold; padding-top: 10px;")
        props_layout.addWidget(color_label, 3, 0, 1, 2)
        
        props_layout.addWidget(QLabel("R:"), 4, 0)
        self.color_r = QSlider(Qt.Horizontal)
        self.color_r.setRange(0, 255)
        self.color_r.valueChanged.connect(self.update_color)
        props_layout.addWidget(self.color_r, 4, 1)
        
        props_layout.addWidget(QLabel("G:"), 5, 0)
        self.color_g = QSlider(Qt.Horizontal)
        self.color_g.setRange(0, 255)
        self.color_g.valueChanged.connect(self.update_color)
        props_layout.addWidget(self.color_g, 5, 1)
        
        props_layout.addWidget(QLabel("B:"), 6, 0)
        self.color_b = QSlider(Qt.Horizontal)
        self.color_b.setRange(0, 255)
        self.color_b.valueChanged.connect(self.update_color)
        props_layout.addWidget(self.color_b, 6, 1)
        
        self.color_preview = QLabel()
        self.color_preview.setFixedHeight(30)
        self.color_preview.setStyleSheet("background: orange; border: 1px solid white;")
        props_layout.addWidget(self.color_preview, 7, 0, 1, 2)
        
        inspector_layout.addWidget(props_group)
        
        # Экспорт
        export_group = QGroupBox("Export")
        export_group.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        export_layout = QVBoxLayout(export_group)
        
        btn_export = QPushButton("📁 Export .sgss")
        btn_export.clicked.connect(self.export_sgss)
        btn_export.setStyleSheet("background: #3d3d3d; color: white; padding: 8px; font-weight: bold;")
        export_layout.addWidget(btn_export)
        
        btn_clear = QPushButton("🗑 Clear Scene")
        btn_clear.clicked.connect(self.clear_scene)
        btn_clear.setStyleSheet("background: #5d2d2d; color: white; padding: 8px;")
        export_layout.addWidget(btn_clear)
        
        inspector_layout.addWidget(export_group)
        inspector_layout.addStretch()
        
        self.add_object("square")
        
    def add_object(self, obj_type):
        obj = {
            'type': obj_type,
            'x': float(self.scene.width()//2 + len(self.objects) * 30),
            'y': float(self.scene.height()//2 + len(self.objects) * 30),
            'size': 100.0,
            'color': [1.0, 0.5, 0.0]
        }
        self.objects.append(obj)
        self.object_list.addItem(f"{obj_type} #{len(self.objects)}")
        self.scene.set_objects(self.objects)
        self.object_list.setCurrentRow(len(self.objects)-1)
        self.select_object(self.object_list.currentItem())
        
    def select_object(self, item):
        idx = self.object_list.row(item)
        if idx < len(self.objects):
            self.selected_index = idx
            obj = self.objects[idx]
            self.pos_x.setValue(obj['x'])
            self.pos_y.setValue(obj['y'])
            self.size_val.setValue(obj['size'])
            self.color_r.setValue(int(obj['color'][0] * 255))
            self.color_g.setValue(int(obj['color'][1] * 255))
            self.color_b.setValue(int(obj['color'][2] * 255))
            self.update_color()
        
    def update_object(self):
        if self.selected_index >= 0 and self.selected_index < len(self.objects):
            obj = self.objects[self.selected_index]
            obj['x'] = self.pos_x.value()
            obj['y'] = self.pos_y.value()
            obj['size'] = self.size_val.value()
            self.scene.update()
        
    def update_color(self):
        if self.selected_index >= 0 and self.selected_index < len(self.objects):
            r = self.color_r.value() / 255.0
            g = self.color_g.value() / 255.0
            b = self.color_b.value() / 255.0
            obj = self.objects[self.selected_index]
            obj['color'] = [r, g, b]
            self.color_preview.setStyleSheet(f"background: rgb({int(r*255)}, {int(g*255)}, {int(b*255)}); border: 1px solid white;")
            self.scene.update()
        
    def clear_scene(self):
        self.objects.clear()
        self.object_list.clear()
        self.selected_index = -1
        self.scene.set_objects([])
        
    def export_sgss(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Scene", "", "SGSS Files (*.sgss)")
        if path:
            with open(path, 'w') as f:
                f.write("window 800 600\n")
                f.write("title \"Snow Graphics System Scene\"\n\n")
                
                for obj in self.objects:
                    obj_type = obj['type']
                    size = int(obj['size'])
                    r, g, b = obj['color']
                    
                    if obj_type == 'square':
                        f.write(f"square\n")
                        f.write(f"{obj['x']:.1f} {obj['y']:.1f} {size}\n")
                        f.write(f"{r:.2f} {g:.2f} {b:.2f}\n\n")
                        
                    elif obj_type == 'circle':
                        radius = size / 2
                        segments = 32
                        f.write(f"circle\n")
                        f.write(f"{obj['x']:.1f} {obj['y']:.1f} {radius:.1f} {segments}\n")
                        f.write(f"{r:.2f} {g:.2f} {b:.2f}\n\n")
                        
                    elif obj_type == 'triangle':
                        half = size / 2
                        f.write(f"triangle\n")
                        f.write(f"{obj['x']:.1f} {obj['y'] - half:.1f}\n")
                        f.write(f"{obj['x'] - half:.1f} {obj['y'] + half:.1f}\n")
                        f.write(f"{obj['x'] + half:.1f} {obj['y'] + half:.1f}\n")
                        f.write(f"{r:.2f} {g:.2f} {b:.2f}\n\n")
                        
                    elif obj_type == 'cube':
                        f.write(f"# Cube (3D) - экспортирован как square\n")
                        f.write(f"square\n")
                        f.write(f"{obj['x']:.1f} {obj['y']:.1f} {size}\n")
                        f.write(f"{r:.2f} {g:.2f} {b:.2f}\n\n")
                
                f.write("# Сцена создана в SGS Scene Editor v2.0\n")
                
            QMessageBox.information(self, "Exported", f"Scene exported to {path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    editor = SceneEditor()
    editor.show()
    sys.exit(app.exec_())
