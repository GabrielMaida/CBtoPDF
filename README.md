# CBtoPDF

A robust, cross-platform Python script that converts `.cbz` and `.cbr` comic book archives into high-quality PDF format. After successful conversion, the original files are safely moved to an `old_files` directory to keep your workspace organized.

## ⚠️ Disclaimer

**Anti-Piracy Notice:** This software is developed solely as a personal utility to help users manage, format, and read their legally obtained, DRM-free digital comic book collections on devices that primarily support PDF formats. The authors and contributors of this repository do not endorse, promote, or condone the piracy of copyrighted materials. We are not responsible for how you use this tool or for the legality of the files you choose to process. Please support the comic book industry and original creators by purchasing official releases.

## Features

- **Cross-Platform:** Works seamlessly on Windows, macOS, and Linux.
- **Intelligent Resizing:** Automatically scales down excessively large images (colossal pages) to a maximum of 2560x2560 pixels while strictly preserving the aspect ratio. Uses the Lanczos filter to prevent Moiré patterns in comic halftones.
- **Format Normalization:** Automatically handles transparent images (RGBA) and unsupported formats (like WebP or GIF) by flattening them onto a white background and converting them to RGB JPEGs.
- **Natural Sorting:** Sorts pages logically (e.g., `page_2.jpg` comes before `page_10.jpg`).
- **Memory Management:** Includes explicit garbage collection to process multiple heavy archives without crashing.

## Requirements

### 1. Python Dependencies

- **Python 3.x** must be installed.
- Required pip packages: `img2pdf`, `natsort`, `rarfile`, `Pillow`, `tqdm`.

### 2. System Dependencies (UnRAR)

To process `.cbr` (RAR) files, your system must have an UnRAR executable available.

- **Windows:** The script automatically looks for WinRAR in the standard installation paths (`C:/Program Files/WinRAR/UnRAR.exe`). If you have WinRAR installed, you are good to go.
- **Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install unrar
```

- **Arch Linux:**

```bash
sudo pacman -S unrar
```

## Installation

1. **Clone the Repository**:
   Open a terminal and clone the repository from GitHub:

   ```bash
   git clone https://github.com/GabrielMaida/CBtoPDF.git
   cd CBtoPDF
   ```

2. **Install Required Libraries**:

   ```bash
   pip install img2pdf natsort rarfile pillow tqdm
   ```

## Usage

1. **Prepare Your Directory**:
   - Drop the `.cbz` or `.cbr` files into the same directory as the `cb2pdf.py` script.

2. **Run the Script**:
   - Open a terminal, navigate to the directory, and execute:

   ```bash
   python cb2pdf.py
   ```

   *(On some Linux distributions, you might need to use `python3 cb2pdf.py`)*

   The script will process all archives, display a progress bar, create the PDFs, and move the originals to the `old_files` folder. Any errors will be registered in `conversion_error_log.txt`.

## How It Works

1. **Directory Setup**: Creates the `old_files` output directory and initializes the logging system.
2. **Extraction Phase**: Extracts the contents of the CBZ (Zip) or CBR (RAR) archive into a temporary folder provided by the OS.
3. **Deep Scan Phase**: Recursively searches the temporary folder for supported images (`.jpg`, `.png`, `.webp`, etc.). It filters out hidden system folders like `__MACOSX` or `.git` to prevent compilation errors and applies natural sorting to the file names.
4. **Image Processing Phase**:
   - Checks the dimensions of each image. If an image exceeds 2560 pixels in width or height, it is proportionally downscaled.
   - Cleans up alpha channels (transparency) by pasting the image over a solid white background.
5. **PDF Generation Phase**: Uses `img2pdf` to losslessly compile the processed images directly into a PDF byte-stream, which is highly efficient.
6. **Cleanup Phase**: The temporary folder is automatically deleted by the system. If the PDF is generated successfully, the original archive is moved to the `old_files` folder.

## Troubleshooting

- **ModuleNotFoundError:**
  You are missing one of the Python libraries. Run the installation command:
  
  ```bash
  pip install img2pdf natsort rarfile pillow tqdm
  ```

- **WARNING: UnRAR.exe could not be found / rarfile.RarCannotExec:**
  The script cannot extract `.cbr` files because it cannot find the UnRAR tool.
  - *Windows:* Install WinRAR.
  - *Linux:* Install the `unrar` package using your system's package manager (e.g., `pacman` or `apt`).

- **PDF pages are out of order:**
  Ensure the internal files of your archive are numbered consistently. While the script uses `natsort` to handle numbers logically, wildly different naming schemes inside the same archive might cause issues.

- **Corrupted Image Warnings in the Log:**
  Sometimes downloaded archives contain broken image files. The script is designed to ignore them and log a warning in `conversion_error_log.txt`, allowing the rest of the comic to be converted safely.

## License

**This project is licensed under the MIT License. See the LICENSE file for details.**
