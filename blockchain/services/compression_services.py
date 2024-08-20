import zipfile
import os


async def zip_block(filename: str):
    # Ruta completa del archivo a comprimir
    file_path = filename

    # Verificar si el archivo existe
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")

    # Nombre del archivo ZIP basado en el nombre del archivo original
    zip_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}.zip"
    zip_path = os.path.join(os.path.dirname(file_path), zip_filename)

    try:
        # Comprimir el archivo en un ZIP
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(
                file_path, os.path.basename(file_path)
            )  # Agrega el archivo con el nombre original

        print(f"Archivo comprimido exitosamente: {zip_path}")
        return zip_path

    except Exception as e:
        print(f"Error al comprimir el archivo: {str(e)}")
        raise


def unzip_file(zip_filename, extract_to):
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(extract_to)
