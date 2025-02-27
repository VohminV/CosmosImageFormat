import numpy as np
import pickle
import lzma
from PIL import Image
import io
from crc8 import crc8

class CIFCompressor:
    def __init__(self):
        pass

    def compress(self, image_path):
        # Открываем изображение
        image = Image.open(image_path)
        image = image.convert("RGB")  # Конвертируем изображение в формат RGB

        # Сжимаем изображение в формат PNG
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            image_bytes = output.getvalue()

        print(f"Размер изображения в байтах (PNG): {len(image_bytes)}")

        # Сжимаем байты изображения с использованием lzma
        compressed_data = lzma.compress(image_bytes)
        print(f"Размер сжатого изображения с использованием lzma: {len(compressed_data)}")

        # Вычисляем CRC8 для сжатых данных
        crc = crc8()
        crc.update(compressed_data)
        crc_checksum = crc.hexdigest()  # Возвращает строку в hex формате

        print(f"CRC8 для сжатых данных: {crc_checksum}")

        # Сохраняем метаданные изображения
        metadata = {
            'shape': image.size + (3,),  # Размер изображения (ширина, высота, каналы)
            'original_size': len(image_bytes),  # Оригинальный размер изображения
            'crc': crc_checksum  # CRC8 контрольная сумма
        }

        # Сериализуем метаданные
        metadata_serialized = pickle.dumps(metadata)
        metadata_size = len(metadata_serialized).to_bytes(4, byteorder='big')

        # Возвращаем метаданные и сжатые данные
        return metadata_size + metadata_serialized + compressed_data

# Пример использования
if __name__ == "__main__":
    image_path = "test.png"  # Замените на путь к своему изображению
    compressor = CIFCompressor()
    compressed_data = compressor.compress(image_path)

    # Сохраняем сжатые данные в файл
    with open("output_image.cif", "wb") as f:
        f.write(compressed_data)
    print("Изображение успешно сжато и сохранено как CIF.")
