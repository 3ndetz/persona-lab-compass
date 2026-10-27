"""Render the readable catalog from its structured source."""
import json
from pathlib import Path
from urllib.parse import urlsplit

root = Path(__file__).resolve().parents[1]
items = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
labels = {'tts': 'Синтез речи', 'stt': 'Распознавание речи', 'audio': 'Аудио',
          'llm': 'LLM', 'image': 'Изображения', 'video': 'Видео', 'harness': 'Агентные harness',
          'memory': 'Память и RAG', 'orchestration': 'Агентные системы', 'inference': 'Локальный запуск'}
assert isinstance(items, list) and items
assert len({item['id'] for item in items}) == len(items)
for item in items:
    assert item['id'].startswith('curated:') and urlsplit(item['url']).scheme == 'https'
    assert all(isinstance(item[key], str) and item[key] for key in ('name', 'category', 'url'))
lines = ['# Persona Lab Compass', '', 'Открытая подборка технологий для создания ИИ-персонажей.', '',
         '[Открыть Compass](https://course.personalabs.ru/compass/) · [Шаблон личного рейтинга](https://github.com/3ndetz/compass-rating-template)', '',
         'Подборка содержит ссылки на первоисточники. Для свежих рейтингов, цен и большего каталога используйте сервис. Предложения и исправления принимаются через issues и pull requests.', '']
categories = list(labels) + sorted({item['category'] for item in items} - set(labels))
for key in categories:
    group = [item for item in items if item['category'] == key]
    if not group:
        continue
    lines.extend(['## ' + labels.get(key, key), ''])
    for item in group:
        lines.append('- [' + item['name'] + '](' + item['url'] + ') — ' + item.get('description', ''))
    lines.append('')
lines.extend(['## Данные', '', '`catalog.json` содержит идентификаторы, описания и ссылки подборки. Источники сохраняют свои права и условия использования. Рейтинги Arena и данные внешних API доступны через сервис и указанные там источники.', '', 'README формируется из `catalog.json` скриптом `scripts/render.py`.', ''])
(root / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
