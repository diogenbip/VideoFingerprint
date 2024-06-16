# VideoFingerprint

## Алгоритм создания хэша видеофайла

1. Видео разбивается на аудио и видео контент
2. Аудио
   2.1 Аудио переводится в моно формат и сжимается
   2.2 По аудио строится спектрограмма. Спектрограмма имеет размерность 32xN, где N - количество frames, 32 т.к. спектрограмма разбита на 32 mel-bands
   2.3 Для каждых 128 кадров в спектрограмме вычисляются пики и строится fingerprint
   2.4 Каждый фингерпринт строит MinHash по которым строится LSH кластеризация

3. Видео
   3.1 Видео переводится в моно формат и сжимается
   3.2 К каждому второму кадру применяется сжатие Хаара (вычисляются ключевые моменты) и строится fingerprint
   3.3 Для каждого фингерпринта строится MinHash по которым строится LSH кластеризация

## Files

1. ContentDataset.py - Для работы с датасетом из видеофайлов пример: `dataset = ContentDataset('static/init')` загрузит все видео из папки и сделает fingerprint для них
2. Lsh.py - LSH алгоритм для классификации видеофайлов
3. models/audio/AudioHashModel.py - Модель для аудиофайла бд
4. models/video/VideoHashModel.py - Модель для видеофайла бд

## End-Points

1. /init - Инициализация видеофайла
2. /search?id=out.mp4 - Поиск по видеофайлу
3. /upload - Загрузка видеофайла
4. /fingerprint?id=out.mp4 - Фингерпринт видеофайла загруженного в /upload
