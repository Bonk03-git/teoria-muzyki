from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import random


# ============================================================
# USTAWIENIA
# ============================================================

OUTPUT = Path("akordy_dur_moll_karta.pdf")

# Europejskie nazewnictwo:
# H = B natural
# B = B♭


# ============================================================
# AKORDY
# ============================================================

CHORDS = [
    ("C", "dur"),
    ("C", "moll"),

    ("D", "dur"),
    ("D", "moll"),

    ("E", "dur"),
    ("E", "moll"),

    ("F", "dur"),
    ("F", "moll"),

    ("G", "dur"),
    ("G", "moll"),

    ("A", "dur"),
    ("A", "moll"),

    ("H", "dur"),
    ("H", "moll"),
]


# ============================================================
# UKŁAD TABELI
# ============================================================

COLS = 7
ROWS = 20

MARGIN_X = 10
MARGIN_TOP = 50
MARGIN_BOTTOM = 10

GAP = 2


# ============================================================
# CZCIONKA
# ============================================================

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Windows:
# FONT_PATH = "C:/Windows/Fonts/arial.ttf"
# FONT_BOLD_PATH = "C:/Windows/Fonts/arialbd.ttf"

pdfmetrics.registerFont(
    TTFont("DejaVu", FONT_PATH)
)

pdfmetrics.registerFont(
    TTFont("DejaVu-Bold", FONT_BOLD_PATH)
)


# ============================================================
# PRZYGOTOWANIE ZADAŃ
# ============================================================

TOTAL_CELLS = COLS * ROWS

pairs = []

while len(pairs) < TOTAL_CELLS:

    # Tworzymy nowy zestaw wszystkich 14 akordów
    batch = CHORDS.copy()

    # Losujemy kolejność bez powtarzania
    random.shuffle(batch)

    # Dodajemy cały zestaw do zadań
    pairs.extend(batch)

# Przycinamy do liczby komórek na stronie
pairs = pairs[:TOTAL_CELLS]


# ============================================================
# PARAMETRY STRONY
# ============================================================

PAGE_W, PAGE_H = A4

CELL_W = (
    PAGE_W
    - 2 * MARGIN_X
    - (COLS - 1) * GAP
) / COLS

CELL_H = (
    PAGE_H
    - MARGIN_TOP
    - MARGIN_BOTTOM
    - (ROWS - 1) * GAP
) / ROWS


# ============================================================
# NAGŁÓWEK
# ============================================================

def draw_header(c):

    # Tytuł
    c.setFont(
        "DejaVu-Bold",
        13
    )

    c.drawString(
        MARGIN_X,
        PAGE_H - 27,
        "AKORDY DUR I MOLL"
    )

    # Instrukcja
    c.setFont(
        "DejaVu",
        7
    )

    c.drawString(
        MARGIN_X,
        PAGE_H - 40,
        "Wypisz trzy dźwięki tworzące podany akord. "
        "Używaj poprawnej pisowni dźwięków."
    )


# ============================================================
# POJEDYNCZA KOMÓRKA
# ============================================================

def draw_cell(c, x, y, root, quality):

    # Obramowanie
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.4)

    c.rect(
        x,
        y,
        CELL_W,
        CELL_H
    )

    # --------------------------------
    # Nazwa akordu
    # --------------------------------

    c.setFont(
        "DejaVu-Bold",
        7
    )

    if quality == "dur":
        chord_name = f"{root}-dur"
    else:
        chord_name = f"{root}-moll"

    # Nazwa akordu
    c.drawString(
        x + 5,
        y + CELL_H - 10,
        chord_name
    )

    # --------------------------------
    # Miejsce na odpowiedź
    # --------------------------------

    c.setFont(
        "DejaVu",
        7
    )

    c.drawString(
        x + 5,
        y + 5,
        "____  ____  ____"
    )


# ============================================================
# TWORZENIE PDF
# ============================================================

c = canvas.Canvas(
    str(OUTPUT),
    pagesize=A4
)

c.setTitle(
    "Akordy dur i moll – karta pracy"
)


# ============================================================
# NAGŁÓWEK
# ============================================================

draw_header(c)


# ============================================================
# RYSOWANIE ZADAŃ
# ============================================================

for i, (root, quality) in enumerate(pairs):

    row = i // COLS
    col = i % COLS

    x = (
        MARGIN_X
        + col * (CELL_W + GAP)
    )

    y = (
        PAGE_H
        - MARGIN_TOP
        - (row + 1) * CELL_H
        - row * GAP
    )

    draw_cell(
        c,
        x,
        y,
        root,
        quality
    )


# ============================================================
# ZAPIS
# ============================================================

c.save()

print(
    f"PDF został zapisany jako: {OUTPUT}"
)