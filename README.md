## Setup Instructions

### Requirements
- Python 3.9 or higher (https://www.python.org/downloads/)
- Up-to-date `pip`: `pip install --upgrade pip`
- Development tools for building native libraries (required on Windows):
  - [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
    - During installation, select:
      - MSVC (Microsoft C++ Compiler)
      - Windows 10 SDK
      - CMake tools

### Setup Steps
1. **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install --upgrade pip
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application:**
    ```bash
    python app.py
    ```

### Troubleshooting
- **Dependency installation issues on Windows:**  
  Ensure Visual Studio Build Tools is installed with:
  - MSVC (Microsoft C++ Compiler)
  - Windows 10 SDK
  - CMake Tools  

- **Issues with `scikit-image` or `scipy`:**  
  Verify that the above tools are installed and run:
  ```bash
  pip install scikit-image scipy


## Features
- Choose between working with Image files and Audio files.
- Upload an image.
- Apply Gaussian noise.
- View the original and noisy images.
- Compute PSNR and SSIM.
- Upload an audio.
- Apply noise to the audio.
- Play and stop both audios.
- Compute PESQ.



