from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import random


# ============================================================
# USTAWIENIA
# ============================================================

OUTPUT = Path("interwaly_poltony_karta.pdf")

# Europejskie nazewnictwo:
# H = B natural
# B = B♭
NOTES = [
    "C",
    "CIS",
    "DES",
    "D",
    "DIS",
    "ES",
    "E",
    "F",
    "FIS",
    "GES",
    "G",
    "GIS",
    "AS",
    "A",
    "AIS",
    "B",
    "H",
]

CZY_TO_SAMO = [
    0, 1, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11
]

# Układ tabeli
COLS = 9
ROWS = 32

# Margines strony
MARGIN_X = 10
MARGIN_TOP = 50
MARGIN_BOTTOM = 10

# Odstęp między komórkami
GAP = 2

# ============================================================
# CZCIONKA Z POLSKIMI ZNAKAMI
# ============================================================

# Linux:
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Jeśli używasz Windows, możesz zamiast powyższych użyć np.:
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

pairs = []

for i, first_note in enumerate(NOTES):
    for j, second_note in enumerate(NOTES):
        if first_note != second_note and CZY_TO_SAMO[i] != CZY_TO_SAMO[j]:
            pairs.append((first_note, second_note))


random.shuffle(pairs)
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
        "ODLEGŁOŚCI MIĘDZY DŹWIĘKAMI – PÓŁTONY"
    )

    # Instrukcja
    c.setFont(
        "DejaVu",
        7
    )

    c.drawString(
        MARGIN_X,
        PAGE_H - 40,
        "Wpisz liczbę półtonów od pierwszego dźwięku do drugiego. "
        "H = B natural, B = B♭."
    )


# ============================================================
# POJEDYNCZA KOMÓRKA
# ============================================================

def draw_cell(c, x, y, note1, note2):

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
    # Para dźwięków
    # --------------------------------

    c.setFont(
        "DejaVu-Bold",
        6.5
    )

    text = f"{note1} → {note2}"

    c.drawString(
        x + 5,
        y + (CELL_H - 6.5) / 2,
        text
    )


# ============================================================
# TWORZENIE PDF
# ============================================================

c = canvas.Canvas(
    str(OUTPUT),
    pagesize=A4
)

c.setTitle(
    "Odległości między dźwiękami – półtony"
)


# ============================================================
# NAGŁÓWEK
# ============================================================

draw_header(c)


# ============================================================
# RYSOWANIE ZADAŃ
# ============================================================

for i, (note1, note2) in enumerate(pairs):

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

    draw_cell(c,x,y,note1,note2)


# ============================================================
# ZAPIS
# ============================================================

c.save()

print(
    f"PDF został zapisany jako: {OUTPUT}"
)