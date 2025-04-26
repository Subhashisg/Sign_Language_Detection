# Sign Language Detection
 
This project implements a real-time American Sign Language (ASL) recognition system using hand tracking and computer vision. It detects hand gestures from a webcam feed, classifies them into ASL letters (A-Z), displays the results on a Streamlit web interface, and provides text-to-speech (TTS) output and keyboard typing functionality. The system bridges communication gaps by enabling deaf individuals to express thoughts seamlessly.
##   Presentation   
https://www.canva.com/design/DAGluLAU4TA/V0gjeZ67u64KoKSE82gk8g/view?utm_content=DAGluLAU4TA&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h1f23d4ba4d  
## Features

- **Real-Time Hand Tracking**: Uses a custom `HandTrackingModule` to detect and track hand landmarks via OpenCV.
- **ASL Letter Recognition**: Recognizes ASL letters (A-Z) based on finger positions and hand orientations.
- **Streamlit Interface**: Displays the video feed and recognized letters in a user-friendly web UI.
- **Text-to-Speech (TTS)**: Announces detected letters using `pyttsx3` for accessibility.
- **Keyboard Typing**: Types recognized letters into active applications using `pynput`.
- **Robust Detection**: Handles varying hand positions with confidence-based detection (0.8 threshold).

## Prerequisites

- Python 3.8+
- Webcam for video input
- Required Python libraries (see `requirements.txt`)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/sign-language-recognition-asl.git
   cd sign-language-recognition-asl
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should include:

   ```
   opencv-python
   streamlit
   pyttsx3
   numpy
   pynput
   ```

4. **Ensure HandTrackingModule**:

   - Place the `HandTrackingModule.py` file in the project directory (not included in this repository; ensure you have it from your source).
   - Alternatively, replace it with MediaPipe's hand tracking if adapting the code.

## Usage

1. **Run the Streamlit App**:

   ```bash
   streamlit run app.py
   ```

   Replace `app.py` with the name of your main script file.

2. **Interact with the Interface**:

   - Open the provided URL (e.g., `http://localhost:8501`) in your browser.
   - Check the "Start Camera" box to begin video capture.
   - Perform ASL hand signs in front of the webcam.
   - The recognized letter appears on the screen, is spoken aloud, and typed into the active application.

3. **Exit**:

   - Uncheck the "Start Camera" box to stop the webcam.
   - Close the terminal or browser to shut down the app.

## Project Structure

```
sign-language-recognition-asl/
│
├── app.py                  # Main script for Streamlit app and ASL recognition
├── HandTrackingModule.py   # Custom module for hand detection (ensure you have this)
├── requirements.txt        # List of required Python libraries
├── README.md               # Project documentation
```

## How It Works

- **Hand Detection**: The `HandTrackingModule` processes webcam frames to identify hand landmarks.
- **Finger State Analysis**: Determines finger positions (up, down, half-bent) using landmark coordinates.
- **ASL Classification**: Uses heuristic rules based on finger states and landmark positions to classify signs into letters (A-Z).
- **Output**:
  - Displays the letter on a semi-transparent overlay in the video feed.
  - Announces the letter via TTS using `pyttsx3`.
  - Types the letter using `pynput` with a 1-second debounce to prevent duplicates.
- **Streamlit UI**: Provides a checkbox to start/stop the camera and displays the live feed with results.

## Limitations

- Requires a well-lit environment and clear hand visibility.
- Limited to single-hand ASL letter recognition (A-Z).
- Dependent on the `HandTrackingModule` (not included; replace with MediaPipe if needed).
- TTS may have platform-specific issues (e.g., on Linux, additional setup for `pyttsx3` may be required).

## Future Improvements

- Add support for full words or phrases by detecting sequences of signs.
- Integrate MediaPipe for more robust and open-source hand tracking.
- Enhance UI with additional controls (e.g., volume for TTS, sensitivity adjustments).
- Support multiple languages or sign systems (e.g., BSL, ISL).

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Inspired by the need to bridge communication gaps for deaf communities.
- Built with open-source libraries: OpenCV, Streamlit, pyttsx3, and pynput.
- Special thanks to contributors of hand tracking solutions and ASL resources.

---


