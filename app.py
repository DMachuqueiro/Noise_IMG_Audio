import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QFileDialog, QSpacerItem, QSizePolicy
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap
from utils.noise import add_gaussian_noise
from utils.metrics import calculate_metrics
from utils.noise import add_noise_to_audio
from utils.metrics import calculate_pesq_score
from utils.metrics import resample_audio
from PyQt6.QtWidgets import QLabel, QPushButton, QSlider, QHBoxLayout, QVBoxLayout, QFileDialog, QWidget, QMainWindow




class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quality of Service Application")
        self.setGeometry(200, 200, 600, 400)  # Initial window size
        self.initUI()

    def initUI(self):
        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout for the main menu
        self.main_layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel("Welcome to the Quality of Service Application")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Buttons for "Noise in Images" and "Noise in Audio"
        self.noise_images_btn = QPushButton("Noise in Images")
        self.noise_images_btn.setFixedSize(200, 50)
        self.noise_images_btn.clicked.connect(self.open_image_noise_app)

        self.noise_audio_btn = QPushButton("Noise in Audio")
        self.noise_audio_btn.setFixedSize(200, 50)
        self.noise_audio_btn.clicked.connect(self.open_audio_noise_app)

        # Add widgets to the layout
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.noise_images_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.noise_audio_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch()

        # Set the layout
        self.central_widget.setLayout(self.main_layout)

    #Open the Image Noise application
    def open_image_noise_app(self):
        self.image_app = ImageApp(self)
        self.image_app.show()
        self.close()
    #Open the audio noise application
    def open_audio_noise_app(self):
        
        self.audio_app = AudioApp(self)
        self.audio_app.show()
        self.close()


class ImageApp(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Image Noise and Quality Assessment")
        self.setGeometry(200, 200, 1000, 600)
        self.initUI()

    def initUI(self):
        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout()
        self.image_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.noise_param_layout = QVBoxLayout()

        # Labels for "Old Image" and "New Image"
        self.original_label = QLabel("Old Image")
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setFixedSize(450, 450)

        self.noisy_label = QLabel("New Image")
        self.noisy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.noisy_label.setFixedSize(450, 450)

        # Add labels to the image layout
        self.image_layout.addWidget(self.original_label)
        self.image_layout.addWidget(self.noisy_label)

        # Metrics Label
        self.metrics_label = QLabel("PSNR and SSIM will be displayed here.")
        self.metrics_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Explanation Labels for PSNR and SSIM
        self.psnr_explanation_label = QLabel(
            "PSNR: Peak Signal-to-Noise Ratio measures image quality (higher is better). "
            "For example, PSNR > 30 indicates good quality, while PSNR < 20 indicates poor quality."
        )
        self.psnr_explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.psnr_explanation_label.setWordWrap(True)

        self.ssim_explanation_label = QLabel(
            "SSIM: Structural Similarity Index measures similarity (1 = identical). "
            "Values closer to 1 indicate higher similarity and better quality."
        )
        self.ssim_explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ssim_explanation_label.setWordWrap(True)

        # Noise Parameters with Sliders
        self.noise_mean_label = QLabel("Mean (Noise): Controls the brightness shift of noise (0 = neutral).")
        self.mean_slider = QSlider(Qt.Orientation.Horizontal)
        self.mean_slider.setRange(-50, 50)
        self.mean_slider.setValue(0)
        self.mean_slider.valueChanged.connect(self.update_mean_label)

        self.noise_std_label = QLabel("Standard Deviation (Noise): Controls the intensity of the noise.")
        self.std_slider = QSlider(Qt.Orientation.Horizontal)
        self.std_slider.setRange(1, 100)
        self.std_slider.setValue(25)
        self.std_slider.valueChanged.connect(self.update_std_label)

        # Current Noise Labels
        self.mean_value_label = QLabel("Current Mean: 0")
        self.mean_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.std_value_label = QLabel("Current Std Dev: 25")
        self.std_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add sliders and labels to the layout
        self.noise_param_layout.addWidget(self.noise_mean_label)
        self.noise_param_layout.addWidget(self.mean_slider)
        self.noise_param_layout.addWidget(self.mean_value_label)
        self.noise_param_layout.addWidget(self.noise_std_label)
        self.noise_param_layout.addWidget(self.std_slider)
        self.noise_param_layout.addWidget(self.std_value_label)

        # Buttons
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.upload_image)

        self.apply_noise_btn = QPushButton("Apply Noise")
        self.apply_noise_btn.clicked.connect(self.apply_noise)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_app)

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back_to_menu)

        # Add buttons to the layout
        self.button_layout.addWidget(self.upload_btn)
        self.button_layout.addWidget(self.apply_noise_btn)
        self.button_layout.addWidget(self.reset_btn)
        self.button_layout.addWidget(self.back_btn)

        # Add layouts to the main layout
        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addLayout(self.noise_param_layout)
        self.main_layout.addWidget(self.metrics_label)
        self.main_layout.addWidget(self.psnr_explanation_label)
        self.main_layout.addWidget(self.ssim_explanation_label)
        self.main_layout.addLayout(self.button_layout)

        self.central_widget.setLayout(self.main_layout)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)")
        if file_path:
            self.original_image_path = file_path
            pixmap = QPixmap(file_path)
            self.original_label.setPixmap(pixmap.scaled(self.original_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.noisy_label.clear()
            self.metrics_label.setText("PSNR and SSIM will be displayed here.")

    def apply_noise(self):
        if hasattr(self, 'original_image_path'):
            try:
                mean = self.mean_slider.value()
                stddev = self.std_slider.value()
                noisy_image = add_gaussian_noise(self.original_image_path, mean=mean, stddev=stddev)
                os.makedirs("output", exist_ok=True)
                noisy_image_path = os.path.join("output", "noisy_image.png")
                noisy_image.save(noisy_image_path)
                pixmap = QPixmap(noisy_image_path)
                self.noisy_label.setPixmap(pixmap.scaled(self.noisy_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
                psnr_value, ssim_value = calculate_metrics(self.original_image_path, noisy_image_path)
                self.metrics_label.setText(f"PSNR: {psnr_value:.2f}, SSIM: {ssim_value:.3f}")
            except Exception as e:
                self.metrics_label.setText(f"Error: {e}")
        else:
            self.metrics_label.setText("Please upload an image first.")

    def reset_app(self):
        self.original_label.clear()
        self.noisy_label.clear()
        self.metrics_label.setText("PSNR and SSIM will be displayed here.")
        self.mean_slider.setValue(0)
        self.std_slider.setValue(1)

    def update_mean_label(self):
        current_mean = self.mean_slider.value()
        self.mean_value_label.setText(f"Current Mean: {current_mean}")

    def update_std_label(self):
        current_stddev = self.std_slider.value()
        self.std_value_label.setText(f"Current Std Dev: {current_stddev}")

    def go_back_to_menu(self):
        self.close()
        self.parent.show()


class AudioApp(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Audio Noise and Quality Assessment")
        self.setGeometry(200, 200, 1000, 600)
        self.initUI()

    def initUI(self):
        # Central Widget and Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()

        # Audio Player Layouts
        self.audio_layout = QHBoxLayout()
        self.controls_layout = QVBoxLayout()

        # Labels for Original and Noisy Audio
        self.original_audio_label = QLabel("Original Audio")
        self.original_audio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.noisy_audio_label = QLabel("Noisy Audio")
        self.noisy_audio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Media Players with QAudioOutput
        self.original_audio_output = QAudioOutput()
        self.original_audio_player = QMediaPlayer()
        self.original_audio_player.setAudioOutput(self.original_audio_output)
        self.original_audio_output.setVolume(1.0)  # Volume range is 0.0 to 1.0

        self.noisy_audio_output = QAudioOutput()
        self.noisy_audio_player = QMediaPlayer()
        self.noisy_audio_player.setAudioOutput(self.noisy_audio_output)
        self.noisy_audio_output.setVolume(1.0)  # Volume range is 0.0 to 1.0

        # Audio Controls
        self.original_audio_controls = self.create_audio_controls(self.original_audio_player)
        self.noisy_audio_controls = self.create_audio_controls(self.noisy_audio_player)

        # Add Players and Controls to Layout
        self.audio_layout.addWidget(self.original_audio_label)
        self.audio_layout.addLayout(self.original_audio_controls)

        self.audio_layout.addWidget(self.noisy_audio_label)
        self.audio_layout.addLayout(self.noisy_audio_controls)

        # Upload and Noise Controls
        self.upload_btn = QPushButton("Upload Audio")
        self.upload_btn.clicked.connect(self.upload_audio)

        self.apply_noise_btn = QPushButton("Apply Noise")
        self.apply_noise_btn.clicked.connect(self.apply_noise)
        self.apply_noise_btn.setEnabled(False)

        # Noise Level Slider
        self.noise_level_label = QLabel("Noise Level: 0")
        self.noise_level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.noise_level_slider = QSlider(Qt.Orientation.Horizontal)
        self.noise_level_slider.setRange(0, 100)
        self.noise_level_slider.setValue(0)
        self.noise_level_slider.valueChanged.connect(self.update_noise_level)

        self.noise_level_explanation = QLabel(
            "Adjusts the intensity of the added noise. \n"
            "Range: 0 (no noise) to 100 (high noise). Higher values create more distortion."
        )
        self.noise_level_explanation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Metrics Label and PESQ Explanation
        self.metrics_label = QLabel("PESQ Score will be displayed here.")
        self.metrics_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pesq_explanation = QLabel(
            "PESQ (Perceptual Evaluation of Speech Quality): \n"
            "- Above 4.0: Excellent\n"
            "- 3.0 to 3.9: Good\n"
            "- Below 3.0: Poor"
        )
        self.pesq_explanation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Back Button
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back_to_menu)

        # Add Controls to Layout
        self.controls_layout.addWidget(self.upload_btn)
        self.controls_layout.addWidget(self.apply_noise_btn)
        self.controls_layout.addWidget(self.noise_level_label)
        self.controls_layout.addWidget(self.noise_level_slider)
        self.controls_layout.addWidget(self.noise_level_explanation)
        self.controls_layout.addWidget(self.metrics_label)
        self.controls_layout.addWidget(self.pesq_explanation)
        self.controls_layout.addWidget(self.back_btn)

        # Add to Main Layout
        self.main_layout.addLayout(self.audio_layout)
        self.main_layout.addLayout(self.controls_layout)

        self.central_widget.setLayout(self.main_layout)
    #Creates play, pause, and stop controls for an audio player.
    def create_audio_controls(self, player):
        controls_layout = QHBoxLayout()

        play_button = QPushButton("Play")
        play_button.clicked.connect(player.play)
        controls_layout.addWidget(play_button)

        pause_button = QPushButton("Pause")
        pause_button.clicked.connect(player.pause)
        controls_layout.addWidget(pause_button)

        return controls_layout
    

    #Allow the user to upload an audio file.
    def upload_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Audio", "", "Audio Files (*.wav *.mp3)")
        if file_path:
            self.original_audio_path = file_path
            self.original_audio_label.setText(f"Original Audio: {os.path.basename(file_path)}")
            self.original_audio_player.setSource(QUrl.fromLocalFile(file_path))
            self.apply_noise_btn.setEnabled(True)
            
    #Apply noise to the uploaded audio and calculate PESQ.
    def apply_noise(self):
        if hasattr(self, 'original_audio_path'):
            try:
                noise_level = self.noise_level_slider.value()
                os.makedirs("output", exist_ok=True)
                noisy_audio_path = add_noise_to_audio(self.original_audio_path, noise_level)
                self.noisy_audio_player.setSource(QUrl.fromLocalFile(noisy_audio_path))
                self.noisy_audio_label.setText(f"Noisy Audio: {os.path.basename(noisy_audio_path)}")
                # Resample audio to 16 kHz for PESQ compatibility
                resampled_original = "resampled/resampled_original.wav"
                resampled_noisy = "resampled/resampled_noisy.wav"
                resample_audio(self.original_audio_path, resampled_original, target_samplerate=16000)
                resample_audio(noisy_audio_path, resampled_noisy, target_samplerate=16000)

                # Calculate PESQ score
                pesq_score = calculate_pesq_score(resampled_original, resampled_noisy)
                self.metrics_label.setText(f"PESQ Score: {pesq_score:.2f}")
            except Exception as e:
                self.metrics_label.setText(f"Error: {e}")
        else:
            self.metrics_label.setText("Please upload an audio file first.")

    #Update noise level based on the slider
    def update_noise_level(self):
        self.noise_level_label.setText(f"Noise Level: {self.noise_level_slider.value()}")
        self.noise_level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


    #Return main manu
    def go_back_to_menu(self):
        self.close()
        self.parent.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())
