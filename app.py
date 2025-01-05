from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                           QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QScrollArea,
                           QProgressBar)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPalette, QLinearGradient, QFont
import sys
import cv2
import numpy as np
import os

class ScanningOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.scanning = False
        self.scan_position = 0
        
    def start_scanning(self):
        self.scanning = True
        self.update()
        
    def stop_scanning(self):
        self.scanning = False
        self.update()
        
    def set_position(self, pos):
        self.scan_position = pos
        self.update()
        
    def paintEvent(self, event):
        if not self.scanning:
            return
            
        painter = QPainter(self)
        
        # Create a more sci-fi looking scan effect with cyan color
        gradient_color = QColor(0, 255, 255, 100)  # Semi-transparent cyan
        
        # Draw multiple scanning lines for a more high-tech look
        line_height = 2
        line_y = self.scan_position
        
        # Main scanning line
        painter.fillRect(0, line_y, self.width(), line_height, gradient_color)
        
        # Add digital noise effect
        for i in range(5):
            noise_y = line_y + np.random.randint(-20, 20)
            noise_width = np.random.randint(10, 50)
            noise_x = np.random.randint(0, self.width() - noise_width)
            painter.fillRect(noise_x, noise_y, noise_width, 1, gradient_color)
        
        # Enhanced glow effect
        glow_height = 20
        for i in range(glow_height):
            alpha = int(80 * (1 - i/glow_height))
            gradient_color.setAlpha(alpha)
            
            # Glow above and below
            painter.fillRect(0, line_y - i, self.width(), 1, gradient_color)
            painter.fillRect(0, line_y + line_height + i, self.width(), 1, gradient_color)

class ImageMatcherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEXUS Image Analysis System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set dark theme with cyan accents
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0A0A1A;
                color: #00FFFF;
            }
            QWidget {
                background-color: #0A0A1A;
                color: #00FFFF;
            }
            QPushButton {
                background-color: #001824;
                color: #00FFFF;
                border: 1px solid #00FFFF;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Courier';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #003344;
                border: 2px solid #00FFFF;
            }
            QLabel {
                color: #00FFFF;
                font-family: 'Courier';
            }
            QProgressBar {
                border: 1px solid #00FFFF;
                border-radius: 3px;
                text-align: center;
                color: #00FFFF;
                background-color: #001824;
            }
            QProgressBar::chunk {
                background-color: #00FFFF;
            }
            QScrollArea {
                border: 1px solid #00FFFF;
                border-radius: 5px;
            }
        """)
        
        # Store reference images and source image
        self.source_image_path = None
        self.source_image = None
        self.search_directory = None
        
        self.init_ui()
    
    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel for source image
        left_panel = QVBoxLayout()
        
        # Enhanced image container with sci-fi border
        self.image_container = QWidget()
        self.image_container.setFixedSize(400, 400)
        self.image_container.setStyleSheet("""
            border: 2px solid #00FFFF;
            border-radius: 10px;
            background-color: #001824;
        """)
        
        # Source image label with sci-fi overlay
        self.source_image_label = QLabel(self.image_container)
        self.source_image_label.setGeometry(0, 0, 400, 400)
        self.source_image_label.setAlignment(Qt.AlignCenter)
        
        # Enhanced scanning overlay
        self.scanning_overlay = ScanningOverlay(self.image_container)
        self.scanning_overlay.setGeometry(0, 0, 400, 400)
        
        # Create scanning animation with faster speed
        self.scan_animation = QPropertyAnimation(self, b"scanPosition")
        self.scan_animation.setEasingCurve(QEasingCurve.Linear)
        self.scan_animation.setDuration(1000)  # Faster scanning
        self.scan_animation.setStartValue(0)
        self.scan_animation.setEndValue(400)
        self.scan_animation.finished.connect(self.on_animation_finished)

        # Create sci-fi styled buttons
        browse_source_btn = QPushButton("▶ SELECT TARGET IMAGE")
        browse_source_btn.clicked.connect(self.browse_source_image)
        
        browse_search_btn = QPushButton("▶ SELECT SEARCH ZONE")
        browse_search_btn.clicked.connect(self.browse_search_directory)
        
        scan_btn = QPushButton("■ INITIATE SCAN")
        scan_btn.clicked.connect(self.perform_matching)
        scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #004455;
                color: #00FFFF;
                border: 2px solid #00FFFF;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #006677;
                border: 2px solid #80FFFF;
            }
        """)

        # Add title with sci-fi font
        title_label = QLabel("NEXUS IMAGE ANALYSIS SYSTEM")
        title_label.setStyleSheet("""
            font-family: 'Courier';
            font-size: 18px;
            font-weight: bold;
            color: #00FFFF;
            padding: 10px;
            border-bottom: 2px solid #00FFFF;
        """)

        # Add widgets to left panel
        left_panel.addWidget(title_label)
        left_panel.addWidget(QLabel("TARGET IMAGE PREVIEW"))
        left_panel.addWidget(self.image_container)
        left_panel.addWidget(browse_source_btn)
        left_panel.addWidget(browse_search_btn)
        left_panel.addWidget(scan_btn)
        left_panel.addStretch()
        
        # Right panel for results
        right_panel = QVBoxLayout()
        self.results_label = QLabel("MATCH ANALYSIS RESULTS")
        self.results_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
            border-bottom: 1px solid #00FFFF;
        """)
        
        # Enhanced progress section
        progress_group = QWidget()
        progress_group.setStyleSheet("""
            QWidget {
                background-color: #001824;
                border: 1px solid #00FFFF;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        progress_layout = QVBoxLayout(progress_group)
        
        self.current_file_label = QLabel("SYSTEM READY...")
        self.match_label = QLabel("MATCH INDEX: --")
        self.progress_label = QLabel("PROGRESS: --")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #00FFFF;
                border-radius: 3px;
                text-align: center;
                height: 20px;
                background-color: #001824;
            }
            QProgressBar::chunk {
                background-color: #00FFFF;
            }
        """)
        
        # Add widgets to progress layout
        progress_layout.addWidget(self.current_file_label)
        progress_layout.addWidget(self.match_label)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        # Enhanced scroll area for results
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #00FFFF;
                border-radius: 5px;
                background-color: #001824;
            }
        """)
        scroll_widget = QWidget()
        self.results_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        # Add widgets to right panel
        right_panel.addWidget(self.results_label)
        right_panel.addWidget(progress_group)
        right_panel.addWidget(scroll_area)
        
        # Add panels to main layout
        main_layout.addLayout(left_panel)
        main_layout.addLayout(right_panel)

    def browse_source_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Source Image", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.source_image_path = file_path
            self.load_source_image()
    
    def browse_search_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory to Search"
        )
        if directory:
            self.search_directory = directory
    
    def load_source_image(self):
        # Load and display source image
        pixmap = QPixmap(self.source_image_path)
        scaled_pixmap = pixmap.scaled(
            self.image_container.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.source_image_label.setPixmap(scaled_pixmap)
        
        # Load image for OpenCV processing
        self.source_image = cv2.imread(self.source_image_path)
    
    def clear_results(self):
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    @property
    def scanPosition(self):
        return self.scanning_overlay.scan_position
    
    @scanPosition.setter
    def scanPosition(self, pos):
        self.scanning_overlay.set_position(pos)
    
    def on_animation_finished(self):
        """Handle animation completion and restart if still scanning"""
        if self.scanning_overlay.scanning:
            # Reverse the animation direction
            start = self.scan_animation.startValue()
            end = self.scan_animation.endValue()
            self.scan_animation.setStartValue(end)
            self.scan_animation.setEndValue(start)
            self.scan_animation.start()
            
    def start_scanning(self):
        """Start the scanning animation"""
        self.scanning_overlay.start_scanning()
        self.scan_animation.setStartValue(0)
        self.scan_animation.setEndValue(400)
        self.scan_animation.start()
        
    def stop_scanning(self):
        """Stop the scanning animation"""
        self.scanning_overlay.stop_scanning()
        self.scan_animation.stop()
        
    def perform_matching(self):
        if not self.source_image_path or not self.search_directory:
            return
        
        # Start scanning animation
        self.start_scanning()
        
        self.clear_results()
        
        # Count total images to process
        image_files = [f for f in os.listdir(self.search_directory) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        total_images = len(image_files)
        
        if total_images == 0:
            self.scanning_overlay.stop_scanning()
            return
        
        # Initialize progress bar
        self.progress_bar.setMaximum(total_images)
        self.progress_bar.setValue(0)
        
        # Initialize SIFT detector
        sift = cv2.SIFT_create()
        
        # Get keypoints and descriptors of source image
        gray_source = cv2.cvtColor(self.source_image, cv2.COLOR_BGR2GRAY)
        keypoints1, descriptors1 = sift.detectAndCompute(gray_source, None)
            
        # Initialize matcher
        bf = cv2.BFMatcher()
        
        # Search through directory
        for i, filename in enumerate(image_files):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.search_directory, filename)
                target_image = cv2.imread(image_path)
                
                if target_image is None:
                    continue
                
                # Get keypoints and descriptors of target image
                gray_target = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
                keypoints2, descriptors2 = sift.detectAndCompute(gray_target, None)
                
                if descriptors2 is None:
                    continue
                
                # Match descriptors
                matches = bf.knnMatch(descriptors1, descriptors2, k=2)
                
                # Apply ratio test
                good_matches = []
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
                
                # Calculate matching percentage
                match_percentage = (len(good_matches) / len(keypoints1)) * 100
                
                # Update progress information
                self.current_file_label.setText(f"ANALYZING: {filename}")
                self.match_label.setText(f"MATCH INDEX: {match_percentage:.2f}%")
                self.progress_label.setText(f"SCAN PROGRESS: {i+1}/{total_images}")
                self.progress_bar.setValue(i + 1)
                
                # If match percentage is above threshold, add to results
                if match_percentage > 10:  # Adjust threshold as needed
                    self.add_result(image_path, match_percentage)
                
                QApplication.processEvents()
        
        # Stop scanning animation
        self.stop_scanning()
    
    def add_result(self, image_path, match_percentage, bbox=None):
        # Create sci-fi styled result widget
        result_widget = QWidget()
        result_widget.setStyleSheet("""
            QWidget {
                background-color: #001824;
                border: 1px solid #00FFFF;
                border-radius: 5px;
                margin: 2px;
            }
        """)
        result_layout = QHBoxLayout(result_widget)
        
        # Add image with detected face highlighted
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        
        if bbox:
            img = cv2.imread(image_path)
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 255), 2)
            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_img)
        
        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        
        # Add match percentage with sci-fi styling
        percentage_label = QLabel(f"MATCH INDEX: {match_percentage:.2f}%")
        percentage_label.setStyleSheet("""
            font-family: 'Courier';
            font-weight: bold;
            color: #00FFFF;
        """)
        
        result_layout.addWidget(image_label)
        result_layout.addWidget(percentage_label)
        result_layout.addStretch()
        
        self.results_layout.addWidget(result_widget)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageMatcherApp()
    window.show()
    sys.exit(app.exec_())