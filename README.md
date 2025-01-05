# NEXUS Image Analysis System

A sci-fi themed desktop application for image matching and analysis using SIFT algorithm. This application helps you find similar images in a directory by comparing their visual features.

![App Screenshot](path_to_your_screenshot.png)

## Features

- 🔍 Advanced image matching using SIFT (Scale-Invariant Feature Transform)
- 🎯 Visual target image selection and preview
- 📁 Batch processing of image directories
- 📊 Real-time progress tracking and match percentage display
- 🎨 Sci-fi themed UI with animated scanning effects
- 📱 Responsive and user-friendly interface

## Prerequisites

Before installing the application, ensure you have the following prerequisites:

- Python 3.7 or higher
- pip (Python package installer)
- OpenCV with contrib modules
- Qt5

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Nadeera3784/nexus-image-analysis.git
cd nexus-image-analysis
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

### Manual Dependencies Installation

If you prefer to install dependencies manually:

```bash
pip install PyQt5
pip install opencv-contrib-python
pip install numpy
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Using the application:
   - Click "SELECT TARGET IMAGE" to choose your reference image
   - Click "SELECT SEARCH ZONE" to select the directory containing images to compare
   - Click "INITIATE SCAN" to begin the matching process
   - View results in the right panel, sorted by match percentage

## Requirements

Create a `requirements.txt` file with the following dependencies:

```
PyQt5>=5.15.0
opencv-contrib-python>=4.5.0
numpy>=1.19.0
```

## Project Structure

```
nexus-image-analysis/
│
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
```

## How It Works

The application uses OpenCV's SIFT (Scale-Invariant Feature Transform) algorithm to detect and match key features between images. Here's the process:

1. **Feature Detection**: SIFT identifies key points in both the target and comparison images
2. **Feature Matching**: The algorithm matches similar features between images
3. **Match Filtering**: A ratio test is applied to ensure quality matches
4. **Scoring**: A match percentage is calculated based on the number of good feature matches

## Troubleshooting

### Common Issues

1. **OpenCV Installation Issues**:
   ```bash
   pip uninstall opencv-python
   pip uninstall opencv-contrib-python
   pip install opencv-contrib-python
   ```

2. **PyQt5 Display Problems**:
   - Ensure your system has the latest graphics drivers
   - Try installing system-level Qt dependencies:
     ```bash
     # Ubuntu/Debian
     sudo apt-get install python3-pyqt5
     
     # Fedora
     sudo dnf install python3-qt5
     
     # macOS
     brew install pyqt@5
     ```

3. **Performance Issues**:
   - Reduce the size of image directories for better performance
   - Consider using smaller resolution images for faster processing

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

