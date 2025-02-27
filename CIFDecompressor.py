import numpy as np
import pickle
import lzma
from PIL import Image
import io
from crc8 import crc8

class CIFDecompressor:
    def decompress(self, cif_file_path):
        # Чтение сжатых данных
        with open(cif_file_path, "rb") as f:
            file_data = f.read()

        # Извлекаем метаданные
        metadata_size = int.from_bytes(file_data[:4], byteorder='big')
        metadata_serialized = file_data[4:4 + metadata_size]
        metadata = pickle.loads(metadata_serialized)
        print(f"Метаданные: {metadata}")

        # Проверка CRC8
        crc_checksum = metadata['crc']
        compressed_data = file_data[4 + metadata_size:]
        
        crc = crc8()
        crc.update(compressed_data)
        computed_crc = crc.hexdigest()

        print(f"CRC8 из файла: {crc_checksum}")
        print(f"Вычисленный CRC8: {computed_crc}")

        if crc_checksum != computed_crc:
            raise ValueError("Ошибка: CRC8 контрольная сумма не совпадает. Данные повреждены!")

        # Декомпрессируем данные изображения
        image_bytes = lzma.decompress(compressed_data)
        print(f"Размер декомпрессированных данных: {len(image_bytes)}")

        # Восстанавливаем изображение
        expected_size = metadata['original_size']
        if len(image_bytes) != expected_size:
            raise ValueError(f"Размер декомпрессированных данных не совпадает с ожидаемым. "
                             f"Получено: {len(image_bytes)}, ожидается: {expected_size}")

        # Восстанавливаем изображение из байтов
        image = Image.open(io.BytesIO(image_bytes))
        
        # Вернем восстановленное изображение
        return image

# Пример использования
if __name__ == "__main__":
    decompressor = CIFDecompressor()
    restored_image = decompressor.decompress("output_image.cif")
    
    # Сохранение восстановленного изображения
    restored_image.save("restored_image.png")
    print("Изображение успешно восстановлено и сохранено.")
