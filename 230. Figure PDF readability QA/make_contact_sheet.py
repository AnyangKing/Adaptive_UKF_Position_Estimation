from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
FIGDIR = ROOT / "paper" / "figures"
OUT = Path(__file__).resolve().parent / "figure_contact_sheet.png"


def main() -> None:
    files = sorted(
        f
        for f in FIGDIR.glob("*.png")
        if f.name.startswith("fig") and not f.name.startswith("_")
    )
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        im.thumbnail((900, 520), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (940, 600), "white")
        canvas.paste(im, ((940 - im.width) // 2, 48))
        d = ImageDraw.Draw(canvas)
        d.text((20, 14), f.name, fill=(0, 0, 0))
        thumbs.append(canvas)

    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 940, rows * 600), "white")
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((i % cols) * 940, (i // cols) * 600))
    sheet.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()

