"""
Script per generare l'icona dell'applicazione YAML Excel Converter
Genera icone in formato PNG e ICO per Windows/Linux
"""
from PIL import Image, ImageDraw
import os

def create_icon(size=256):
    """Crea l'icona dell'applicazione"""
    # Crea un'immagine con sfondo trasparente
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colori
    yaml_color = (203, 94, 94)      # Rosso YAML
    excel_color = (33, 115, 70)     # Verde Excel
    arrow_color = (66, 135, 245)    # Blu per le frecce
    white = (255, 255, 255, 255)
    
    # Dimensioni relative
    margin = size * 0.1
    doc_width = size * 0.35
    doc_height = size * 0.5
    arrow_width = size * 0.15
    
    # Posizione documento YAML (sinistra)
    yaml_left = margin
    yaml_top = (size - doc_height) / 2
    yaml_right = yaml_left + doc_width
    yaml_bottom = yaml_top + doc_height
    
    # Disegna documento YAML con piega in alto a destra
    fold_size = doc_width * 0.2
    yaml_points = [
        (yaml_left, yaml_top + fold_size),
        (yaml_right - fold_size, yaml_top + fold_size),
        (yaml_right, yaml_top + fold_size * 2),
        (yaml_right, yaml_bottom),
        (yaml_left, yaml_bottom)
    ]
    draw.polygon(yaml_points, fill=yaml_color)
    
    # Piega del documento YAML
    fold_points = [
        (yaml_right - fold_size, yaml_top + fold_size),
        (yaml_right - fold_size, yaml_top + fold_size * 2),
        (yaml_right, yaml_top + fold_size * 2),
    ]
    draw.polygon(fold_points, fill=tuple([int(c * 0.7) for c in yaml_color[:3]] + [255]))
    
    # Linee di testo YAML
    line_margin = doc_width * 0.15
    line_spacing = doc_height * 0.12
    line_width = doc_width * 0.6
    for i in range(3):
        y = yaml_top + fold_size * 2.5 + i * line_spacing
        draw.rectangle(
            [yaml_left + line_margin, y, yaml_left + line_margin + line_width, y + size * 0.02],
            fill=white
        )
    
    # Posizione documento Excel (destra)
    excel_right = size - margin
    excel_left = excel_right - doc_width
    excel_top = yaml_top
    excel_bottom = yaml_bottom
    
    # Disegna documento Excel
    draw.rectangle(
        [excel_left, excel_top, excel_right, excel_bottom],
        fill=excel_color
    )
    
    # Griglia Excel
    grid_margin = doc_width * 0.1
    grid_left = excel_left + grid_margin
    grid_right = excel_right - grid_margin
    grid_top = excel_top + grid_margin
    grid_bottom = excel_bottom - grid_margin
    
    # Sfondo griglia
    draw.rectangle([grid_left, grid_top, grid_right, grid_bottom], fill=white)
    
    # Linee griglia
    rows = 4
    cols = 3
    for i in range(rows + 1):
        y = grid_top + (grid_bottom - grid_top) * i / rows
        draw.line([(grid_left, y), (grid_right, y)], fill=excel_color, width=max(1, size // 128))
    
    for i in range(cols + 1):
        x = grid_left + (grid_right - grid_left) * i / cols
        draw.line([(x, grid_top), (x, grid_bottom)], fill=excel_color, width=max(1, size // 128))
    
    # Frecce bidirezionali al centro
    center_x = size / 2
    center_y = size / 2
    arrow_length = arrow_width * 0.8
    arrow_head_size = size * 0.08
    arrow_thickness = max(2, size // 64)
    
    # Freccia destra
    arrow_y1 = center_y - size * 0.1
    draw.line(
        [(center_x - arrow_length / 2, arrow_y1), (center_x + arrow_length / 2, arrow_y1)],
        fill=arrow_color, width=arrow_thickness
    )
    # Punta freccia destra
    draw.polygon([
        (center_x + arrow_length / 2, arrow_y1),
        (center_x + arrow_length / 2 - arrow_head_size, arrow_y1 - arrow_head_size / 2),
        (center_x + arrow_length / 2 - arrow_head_size, arrow_y1 + arrow_head_size / 2),
    ], fill=arrow_color)
    
    # Freccia sinistra
    arrow_y2 = center_y + size * 0.1
    draw.line(
        [(center_x + arrow_length / 2, arrow_y2), (center_x - arrow_length / 2, arrow_y2)],
        fill=arrow_color, width=arrow_thickness
    )
    # Punta freccia sinistra
    draw.polygon([
        (center_x - arrow_length / 2, arrow_y2),
        (center_x - arrow_length / 2 + arrow_head_size, arrow_y2 - arrow_head_size / 2),
        (center_x - arrow_length / 2 + arrow_head_size, arrow_y2 + arrow_head_size / 2),
    ], fill=arrow_color)
    
    return img


def main():
    """Genera tutte le varianti dell'icona"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    icon_dir = os.path.join(project_dir, 'icons')
    
    # Crea la cartella icons se non esiste
    os.makedirs(icon_dir, exist_ok=True)
    
    print("Generazione icone in corso...")
    
    # Dimensioni standard per icone
    sizes = [16, 32, 48, 64, 128, 256, 512]
    
    # Genera PNG a varie dimensioni
    png_images = []
    for size in sizes:
        print(f"  Generando icona {size}x{size}...")
        icon = create_icon(size)
        png_path = os.path.join(icon_dir, f'icon_{size}x{size}.png')
        icon.save(png_path, 'PNG')
        png_images.append(icon)
        print(f"    ✓ Salvata: {png_path}")
    
    # Genera l'icona principale (256x256)
    main_icon = create_icon(256)
    main_icon_path = os.path.join(icon_dir, 'icon.png')
    main_icon.save(main_icon_path, 'PNG')
    print(f"  ✓ Icona principale salvata: {main_icon_path}")
    
    # Genera file ICO per Windows (contiene multiple dimensioni)
    ico_path = os.path.join(icon_dir, 'icon.ico')
    main_icon.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"  ✓ Icona Windows (.ico) salvata: {ico_path}")
    
    print("\n✓ Tutte le icone sono state generate con successo!")
    print(f"  Cartella: {icon_dir}")


if __name__ == '__main__':
    main()
