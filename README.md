# CBtoPDF

This Python script converts `.cbz` and `.cbr` files to PDF format and moves the original files to a folder named `old_files` within the same directory.

## Requirements

- **Python 3.x**: Must be installed on your system.

## Installation

1. **Clone the Repository**:
   Open a terminal and clone the repository from GitHub:

    ```bash
    git clone https://github.com/GabrielMaida/CBtoPDF
    ```

2. **Install Required Libraries**:

## Usage (on Windows)

1. **Prepare Your Directory**:
   - Drop the `cbtopdf.py` script into the directory containing your `.cbz` or `.cbr` files.

2. **Open a terminal, navigate to the directory and run the Script**:
   - Execute the script by running:

   ```bash
   python ./cbtopdf.py
   ```

   This will process all `.cbz` and `.cbr` files in the directory, convert them to PDF, and move the original files to a folder called `old_files`.

## How It Works

```comment
1. **Directory Setup**:
   - The script starts by identifying the current directory and setting up an `old` directory where the original files will be moved after conversion.

2. **File Processing**:
   - The script scans the current directory for files with `.cbz` or `.cbr` extensions.
   - For each file, it identifies whether it is a CBZ (ZIP archive) or CBR (RAR archive).

3. **Conversion**:
   - For `.cbz` files, the script extracts images from the ZIP archive and combines them into a single PDF.
   - For `.cbr` files, it uses the `rarfile` library to extract images from the RAR archive and then converts them to PDF.

4. **Batch Processing**:
   - The script processes files in batches to manage memory usage and system resources effectively. After processing a batch, it pauses to free up resources before moving on to the next batch.

5. **Progress Bar**:
   - The script uses `tqdm` to display a progress bar while processing each file, providing visual feedback on the conversion status.

6. **File Management**:
   - After successfully converting a file, the script moves the original file to the `old` directory to keep the working directory organized.
```

## Troubleshooting

- **ModuleNotFoundError:**
  Ensure you have installed all the required libraries from [Requirements](#requirements). You can install it with:

  ```bash
  pip install ...
  ```

## License

**This project is licensed under the MIT License. See the LICENSE file for details.**
