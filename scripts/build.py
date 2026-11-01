"""Build a tiny dependency-free static website."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def build(source_dir=None, output_dir=None):
    source = Path(source_dir) if source_dir else ROOT / 'site'
    output = Path(output_dir) if output_dir else ROOT / 'dist'
    output.mkdir(parents=True, exist_ok=True)
    for filename in ('index.html', 'styles.css'):
        shutil.copyfile(source / filename, output / filename)
    return output


if __name__ == '__main__':
    folder = build()
    print(f'Built site successfully: {folder}')
    for item in folder.iterdir():
        print(f'  - {item.name} ({item.stat().st_size} bytes)')
