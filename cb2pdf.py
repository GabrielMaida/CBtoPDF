import os
import shutil
import zipfile
import tempfile
import logging
import gc

# External libraries required
try:
    import rarfile
    import img2pdf
    from natsort import natsorted
    from PIL import Image
    from tqdm import tqdm
except ImportError:
    print("ERROR: Missing libraries.")
    print("Install with: pip install img2pdf natsort rarfile pillow tqdm")
    exit(1)

# Explicitly declaring UnRAR path
UNRAR_PATH = "C:/Programs/WinRar/UnRAR.exe"
# UNRAR_PATH = "C:/Program Files/WinRAR/UnRAR.exe"

if os.path.exists(UNRAR_PATH):
    rarfile.UNRAR_TOOL = UNRAR_PATH
else:
    # Tries to find in Program Files (x86)
    UNRAR_X86_PATH = "C:/Program Files (x86)/WinRAR/UnRAR.exe"
    if os.path.exists(UNRAR_X86_PATH):
       rarfile.UNRAR_TOOL = UNRAR_X86_PATH
    else:
        print("WARNING: UnRAR.exe couldn't be found")
        print("Make sure WinRAR is installed or put UnRAR.exe on the script folder")


# --- Configuration ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OLD_DIR = os.path.join(CURRENT_DIR, 'old_files')
LOG_FILE = os.path.join(CURRENT_DIR ,'conversion_error_log.txt')
IMAGE_EXTENSIONS = ['.jpg','.jpeg','.png','.webp','.bmp','.tiff','.gif']

# System folders to ignore (Avoid errors with hidden files)
IGNORED_FOLDERS = ['__MACOSX', '.git', '.ds_store']


# --- Log Setup ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# --- Functions ---
# Print to screen and save to log
def log_msg(msg, type='info'):
    print(msg)
    if type == 'info':
        logging.info(msg)
    elif type == 'error':
        logging.error(msg)

# Setup folders
def setup_folders():
    if not os.path.exists(OLD_DIR):
        os.makedirs(OLD_DIR)

# Extracts CBZ or CBR, dealing with common errors
def extract_files(file_path, destination_folder):
    try:
        if file_path.lower().endswith('.cbz'):
            with zipfile.ZipFile(file_path, 'r') as zf:
                zf.extractall(destination_folder)
            return True
        elif file_path.lower().endswith('.cbr'):
            # Note: To run CBR on Windows, you need WinRAR/UnRAR installed and in your PATH
            with rarfile.RarFile(file_path, 'r') as rf:
                rf.extractall(destination_folder)
            return True
    except Exception as e:
        log_msg(f"  [ERROR] Failed on extracting '{os.path.basename(file_path)}': {e}", 'error')
        return False
    return False

# Search ALL the subfolders for images. Returns a list of absolute paths naturally sorted
def find_images_recursively(root_folder):
    image_files = []

    for root, dirs, files in os.walk(root_folder):
        # Remove ignored folders on search
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]
        
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS) and not file.startswith('._'):
                complete_path = os.path.join(root, file)
                image_files.append(complete_path)
    
    # Natural sorting
    return natsorted(image_files)

# Grants the image being compatible with PDF. Converts WebP/GIF/CMYK to JPEG RGB if necessary
def convert_image_to_compatible(image_path):
    try:
        with Image.open(image_path) as img:
            # If regular JPEG/PNG, uses the original file (much quicker)
            if img.format in ['JPEG', 'PNG'] and img.mode in ['RGB', 'L']:
                return image_path
            
            # If not, converts to temporary JPEG
            new_path = os.path.splitext(image_path)[0] + ".temp.jpg"
            # Converts to RGB (removes alpha transparency which breaks JPG)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                bg.paste(img, mask=img.split()[3])
                bg.save(new_path, quality=90)
            else:
                img.convert('RGB').save(new_path, quality=90)
            
            return new_path
    except Exception as e:
        log_msg(f"  [WARNING] Image ignored (corrupted/invalid): {os.path.basename(image_path)} - {e}", 'error')
        return None

# Generates the final PDF from the list of processed images
def create_pdf(image_list, pdf_out_path):
    final_images = []
    
    # Prepara imagens
    for img in image_list:
        img_ok = convert_image_to_compatible(img)
        if img_ok:
            final_images.append(img_ok)
            
    if not final_images:
        return False

    try:
        with open(pdf_out_path, "wb") as f:
            f.write(img2pdf.convert(final_images))
        return True
    except Exception as e:
        log_msg(f"  [ERROR] Failed on saving PDF '{os.path.basename(pdf_out_path)}': {e}", 'error')
        # Tries to remove the corrupted PDF if created
        if os.path.exists(pdf_out_path):
            os.remove(pdf_out_path)
        return False

def process_file(file):
    file_path = os.path.join(CURRENT_DIR, file)
    pdf_name = os.path.splitext(file)[0] + ".pdf"
    pdf_path = os.path.join(CURRENT_DIR, pdf_name)

    # Creates temporary isolated folder
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Extraction
        if not extract_files(file_path, temp_dir):
            return

        # 2. Recursive search (Deep Scan)
        imagens = find_images_recursively(temp_dir)
        
        if not imagens:
            log_msg(f"  [ERRO] Nenhuma imagem encontrada dentro de {file} (Verifique se o arquivo não está vazio).", 'error')
            return

        # Informative log to debug
        log_msg(f"  -> Encontradas {len(imagens)} imagens (Estrutura: {os.path.dirname(imagens[0])})")

        # 3. PDF generation
        sucesso = create_pdf(imagens, pdf_path)

        # 4. Cleaning and movimentation
        if sucesso:
            try:
                shutil.move(file_path, os.path.join(OLD_DIR, file))
                log_msg(f"  [SUCESSO] {pdf_name} criado.")
            except Exception as e:
                log_msg(f"  [ERRO] PDF criado, mas falha ao mover original: {e}", 'error')

def main():
    setup_folders()
    
    arquivos = [f for f in os.listdir(CURRENT_DIR) if f.lower().endswith(('.cbz', '.cbr'))]
    
    if not arquivos:
        print("Nenhum arquivo .cbz ou .cbr encontrado.")
        return

    print(f"Iniciando processamento de {len(arquivos)} arquivos...")
    print("="*60)

    with tqdm(total=len(arquivos), unit="vol") as pbar:
        for arquivo in arquivos:
            pbar.set_description(f"Processando {arquivo[:15]}...")
            process_file(arquivo)
            pbar.update(1)
            gc.collect()

    print("="*60)
    print("Processo finalizado. Verifique 'conversion_log.txt' em caso de erros.")

if __name__ == "__main__":
    main()
