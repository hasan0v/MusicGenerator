# Melody Generator

This project is a web application that generates melodies using a trained deep learning model. The user can input parameters to generate a new melody, which is then saved as a MIDI file.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)

## Features

- Generate melodies using a trained LSTM model.
- Save generated melodies as MIDI files.
- Download generated MIDI files.
- Simple web interface for interaction.

## Technologies Used

- Python
- Flask
- TensorFlow/Keras
- NumPy
- music21
- HTML
- CSS
- JavaScript

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/hasan0v/melody-generator.git
    ```

2. Navigate to the project directory:
    ```sh
    cd melody-generator
    ```

3. Set up a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

5. Ensure you have a folder named `generated_midi` in the project root directory. This is where the generated MIDI files will be saved.

6. Place the trained model architecture file (`model_architecture.json`), the model weights file (`final_model_weights.h5`), and the `X_seed.npy` file in a folder named `content` in the project root directory.

7. Run the application:
    ```sh
    python app.py
    ```

8. Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1. **Home Page**: The main interface where you can generate new melodies.

2. **Generate Melody**: Click the "Generate" button to create a new melody based on the model's predictions. The generated melody will be saved as a MIDI file.

3. **Download MIDI**: After generating a melody, a download link will appear. Click the link to download the generated MIDI file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to contribute to this project by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

If you find this project useful, please consider giving it a star on GitHub. Your feedback and support are greatly appreciated!
