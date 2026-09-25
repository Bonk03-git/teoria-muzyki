import sys
import random
import numpy as np
import sounddevice as sd
from PySide6.QtCore import Qt, QTimer, QEvent
from PySide6.QtWidgets import (
    QApplication, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget,
)
from PySide6.QtGui import QFont

sd.default.device = 3   # numer urządzenia wyjściowego

# ============================================================
# KAFEL
# ============================================================

class MenuTile(QPushButton):
    def __init__(self, title, description):
        super().__init__()

        self.setText(f"{title}\n\n{description}")

        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(300, 220)

        self.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        self.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: white;
                border: 2px solid #333333;
                border-radius: 18px;
                padding: 25px;
                text-align: center;
            }

            QPushButton:hover {
                background-color: #292929;
                border: 2px solid #777777;
            }

            QPushButton:pressed {
                background-color: #151515;
            }
        """)


# ============================================================
# EKRAN BAZOWY
# ============================================================

class BaseScreen(QWidget):
    def __init__(self, title, subtitle=""):
        super().__init__()

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(60, 50, 60, 50)
        self.layout.setSpacing(30)

        # Tytuł
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))

        title_label.setStyleSheet("""
            color: white;
        """)

        self.layout.addWidget(title_label)

        # Podtytuł
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setAlignment(Qt.AlignCenter)
            subtitle_label.setFont(QFont("Arial", 15))

            subtitle_label.setStyleSheet("""
                color: #aaaaaa;
            """)

            self.layout.addWidget(subtitle_label)

        self.setLayout(self.layout)


# ============================================================
# MENU GŁÓWNE
# ============================================================

class MainMenu(BaseScreen):
    def __init__(self, main_window):
        super().__init__(
            "TEORIA MUZYKI",
            "Nauka teorii muzyki i dźwięków"
        )

        tiles = QGridLayout()
        tiles.setSpacing(25)

        # Akordy
        chords = MenuTile(
            "AKORDY",
            "Nauka i rozpoznawanie akordów"
        )

        chords.clicked.connect(main_window.show_chords)

        # Półtony
        semitones = MenuTile(
            "PÓŁTONY",
            "Odległości między dźwiękami"
        )

        semitones.clicked.connect(main_window.show_semitones)

        tiles.addWidget(chords, 0, 0)
        tiles.addWidget(semitones, 0, 1)

        self.layout.addLayout(tiles)

        footer = QLabel("Wybierz moduł, aby rozpocząć naukę")
        footer.setAlignment(Qt.AlignCenter)

        footer.setStyleSheet("""
            color: #666666;
            font-size: 13px;
        """)

        self.layout.addWidget(footer)


# ============================================================
# MENU AKORDÓW
# ============================================================

class ChordsMenu(BaseScreen):
    def __init__(self, main_window):
        super().__init__(
            "AKORDY",
            "Wybierz sposób nauki akordów"
        )

        tiles = QGridLayout()
        tiles.setSpacing(25)

        # Dźwięki
        sounds = MenuTile(
            "🎵  DŹWIĘKI",
            "Nauka dźwięków w akordach"
        )

        sounds.clicked.connect(main_window.show_chord_sounds)

        # Teoria
        theory = MenuTile(
            "📖  TEORIA",
            "Budowa i zasady tworzenia akordów"
        )

        theory.clicked.connect(main_window.show_chord_theory)

        tiles.addWidget(sounds, 0, 0)
        tiles.addWidget(theory, 0, 1)

        self.layout.addLayout(tiles)

        # Powrót
        back = QPushButton("←  Wróć")

        back.setCursor(Qt.PointingHandCursor)

        back.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaaaaa;
                border: none;
                font-size: 15px;
                padding: 10px;
            }

            QPushButton:hover {
                color: white;
            }
        """)

        back.clicked.connect(main_window.show_main_menu)

        self.layout.addWidget(back, alignment=Qt.AlignCenter)


# ============================================================
# EKRAN DŹWIĘKÓW
# ============================================================

class ChordSoundsScreen(BaseScreen):
    def __init__(self, main_window):
        super().__init__(
            "DŹWIĘKI",
            "Nauka dźwięków występujących w akordach"
        )

        info = QLabel(
            "Tutaj później stworzymy ćwiczenia dotyczące dźwięków."
        )

        info.setAlignment(Qt.AlignCenter)

        info.setStyleSheet("""
            color: #aaaaaa;
            font-size: 16px;
        """)

        self.layout.addWidget(info)

        back = QPushButton("←  Wróć do akordów")

        back.clicked.connect(main_window.show_chords)

        self.layout.addWidget(back, alignment=Qt.AlignCenter)


# ============================================================
# EKRAN TEORII
# ============================================================

class ChordTheoryScreen(BaseScreen):
    def __init__(self, main_window):
        super().__init__(
            "TEORIA AKORDÓW",
            "Budowa i zasady tworzenia akordów"
        )

        info = QLabel(
            "Tutaj później dodamy teorię dotyczącą akordów."
        )

        info.setAlignment(Qt.AlignCenter)

        info.setStyleSheet("""
            color: #aaaaaa;
            font-size: 16px;
        """)

        self.layout.addWidget(info)

        back = QPushButton("←  Wróć do akordów")

        back.clicked.connect(main_window.show_chords)

        self.layout.addWidget(back, alignment=Qt.AlignCenter)


# ============================================================
# EKRAN PÓŁTONÓW
# ============================================================

class SemitonesScreen(BaseScreen):
    def __init__(self, main_window):
        super().__init__(
            "PÓŁTONY",
            "Nauka odległości między dźwiękami"
        )

        info = QLabel(
            "Tutaj później stworzymy moduł nauki półtonów."
        )

        info.setAlignment(Qt.AlignCenter)

        info.setStyleSheet("""
            color: #aaaaaa;
            font-size: 16px;
        """)

        self.layout.addWidget(info)

        back = QPushButton("←  Wróć")

        back.clicked.connect(main_window.show_main_menu)

        self.layout.addWidget(back, alignment=Qt.AlignCenter)


# ============================================================
# GŁÓWNE OKNO
# ============================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teoria Muzyki")
        self.setMinimumSize(900, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.screens = {
            "main_menu": MainMenu(self),
            "chords_menu": ChordsMenu(self),
            "chord_sounds_menu": ChordSoundsMenu(self),
            "easy_chords": EasyChordExerciseScreen(self),
            "hard_chords": HardChordExerciseScreen(self),
            "chord_theory_menu": ChordTheoryMenu(self),
            "theory_normal": TheoryNormalScreen(self),
            "theory_accidentals": TheoryAccidentalsScreen(self),
            "semitones": SemitonesScreen(self),
        }
        for screen in self.screens.values():
            self.stack.addWidget(screen)

        self.setStyleSheet("""
            QWidget { background-color: #101010; color: white; }
        """)

        self.show_screen("main_menu")

    def show_screen(self, name):
        screen = self.screens[name]
        # zawsze zaczynaj ćwiczenie od nowa
        if hasattr(screen, "start_exercise"):
            screen.start_exercise()
        self.stack.setCurrentWidget(screen)

    def show_main_menu(self):    self.show_screen("main_menu")
    def show_chords(self):       self.show_screen("chords_menu")
    def show_chord_sounds(self): self.show_screen("chord_sounds_menu")
    def show_chord_theory(self): self.show_screen("chord_theory_menu")
    def show_semitones(self):    self.show_screen("semitones")


class ChordSoundsMenu(BaseScreen):

    def __init__(self, main_window):
        super().__init__("DŹWIĘKI AKORDÓW", "Wybierz poziom trudności")
        self.main_window = main_window

        layout = self.layout

        easy_button = MenuTile(
            "🎵 ŁATWY",
            "Usłysz akord i wybierz 1 z 4 odpowiedzi"
        )
        easy_button.clicked.connect(
            lambda: main_window.show_screen("easy_chords")
        )

        hard_button = MenuTile(
            "🎧 TRUDNY",
            "Wpisz dźwięk i wybierz DUR / MOLL"
        )
        hard_button.clicked.connect(
            lambda: main_window.show_screen("hard_chords")
        )

        layout.addWidget(easy_button)
        layout.addWidget(hard_button)

        layout.addStretch()

        back_button = QPushButton("← Wróć")
        back_button.clicked.connect(
            lambda: main_window.show_screen("chords_menu")
        )

        layout.addWidget(back_button)

class EasyChordExerciseScreen(BaseScreen):

    def __init__(self, main_window):
        super().__init__("ŁATWY")

        self.main_window = main_window

        self.question_number = 0
        self.score = 0
        self.current_chord = None
        self.answer_buttons = []

        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("""
            font-size: 20px;
        """)

        self.play_button = QPushButton("🔊 Odtwórz akord")
        self.play_button.setMinimumHeight(50)
        self.play_button.clicked.connect(self.play_current_chord)

        self.answers_layout = QGridLayout()

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        self.layout.addWidget(self.question_label)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.play_button)
        self.layout.addSpacing(20)
        self.layout.addLayout(self.answers_layout)
        self.layout.addWidget(self.result_label)

    def clear_answers(self):
        while self.answers_layout.count():
            item = self.answers_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.answer_buttons = []

    def start_exercise(self):
        self.question_number = 0
        self.score = 0
        self.result_label.setText("")
        self.next_question()

    def next_question(self):

        if self.question_number >= 10:
            self.show_summary()
            return

        self.question_number += 1

        self.question_label.setText(
            f"Pytanie {self.question_number}/10"
        )

        self.current_chord = random.choice(CHORDS)

        # 4 różne odpowiedzi
        answers = random.sample(CHORDS, 4)

        # upewniamy się, że poprawna odpowiedź jest wśród nich
        if self.current_chord not in answers:
            answers[random.randrange(4)] = self.current_chord

        random.shuffle(answers)

        self.clear_answers()

        for index, chord in enumerate(answers):

            root, quality = chord

            text = f"{root} {quality.upper()}"

            button = QPushButton(text)
            button.setMinimumHeight(65)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #444444;
                }
            """)

            button.clicked.connect(
                lambda checked=False, c=chord:
                    self.check_answer(c)
            )

            row = index // 2
            column = index % 2

            self.answers_layout.addWidget(
                button,
                row,
                column
            )

            self.answer_buttons.append(button)

        self.play_current_chord()

    def play_current_chord(self):
        if self.current_chord:
            play_chord(self.current_chord)

    def check_answer(self, answer):

        for button in self.answer_buttons:
            button.setEnabled(False)

        if answer == self.current_chord:

            self.score += 1

            self.result_label.setText("✓ Dobrze!")

        else:

            root, quality = self.current_chord

            self.result_label.setText(
                f"✗ Źle — poprawna odpowiedź: "
                f"{root} {quality.upper()}"
            )

        # następne pytanie
        from PySide6.QtCore import QTimer

        QTimer.singleShot(
            900,
            self.next_question
        )

    def show_summary(self):

        self.clear_answers()

        self.play_button.hide()

        self.question_label.setText(
            "KONIEC ĆWICZENIA"
        )

        self.result_label.setText(
            f"Wynik: {self.score}/10"
        )

        restart_button = QPushButton("🔄 Od nowa")
        restart_button.setMinimumHeight(55)
        restart_button.clicked.connect(
            self.restart
        )

        menu_button = QPushButton("← Wybór trybu")
        menu_button.setMinimumHeight(55)
        menu_button.clicked.connect(
            lambda: self.main_window.show_screen(
                "chord_sounds_menu"
            )
        )

        self.answers_layout.addWidget(
            restart_button,
            0,
            0
        )

        self.answers_layout.addWidget(
            menu_button,
            0,
            1
        )

    def restart(self):
        self.play_button.show()
        self.start_exercise()

class HardChordExerciseScreen(BaseScreen):

    def __init__(self, main_window):
        super().__init__("TRUDNY")

        self.main_window = main_window

        self.question_number = 0
        self.score = 0
        self.current_chord = None
        self.selected_quality = None

        # layout z BaseScreen (tytuł "TRUDNY" jest już w nim dodany)
        layout = self.layout

        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("""
            font-size: 20px;
        """)

        self.play_button = QPushButton("🔊 Odtwórz akord")
        self.play_button.setMinimumHeight(50)
        self.play_button.clicked.connect(self.play_current_chord)

        self.root_input = QLineEdit()
        self.root_input.setPlaceholderText(
            "Wpisz dźwięk: C, D, E, F, G, A lub H"
        )
        self.root_input.setAlignment(Qt.AlignCenter)
        self.root_input.setMaxLength(1)
        self.root_input.setMinimumHeight(50)
        self.root_input.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                font-weight: bold;
            }
        """)

        quality_layout = QHBoxLayout()

        self.dur_button = QPushButton("DUR")
        self.moll_button = QPushButton("MOLL")

        self.dur_button.setMinimumHeight(60)
        self.moll_button.setMinimumHeight(60)

        self.dur_button.clicked.connect(
            lambda: self.select_quality("dur")
        )
        self.moll_button.clicked.connect(
            lambda: self.select_quality("moll")
        )

        quality_layout.addWidget(self.dur_button)
        quality_layout.addWidget(self.moll_button)

        self.check_button = QPushButton("✓ SPRAWDŹ")
        self.check_button.setMinimumHeight(55)
        self.check_button.clicked.connect(self.check_answer)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        # Przyciski końcowe tworzymy RAZ i tylko pokazujemy / ukrywamy
        self.restart_button = QPushButton("🔄 Od nowa")
        self.restart_button.setMinimumHeight(55)
        self.restart_button.clicked.connect(self.start_exercise)

        self.menu_button = QPushButton("← Wybór trybu")
        self.menu_button.setMinimumHeight(55)
        self.menu_button.clicked.connect(
            lambda: self.main_window.show_screen("chord_sounds_menu")
        )

        layout.addWidget(self.question_label)
        layout.addSpacing(10)
        layout.addWidget(self.play_button)
        layout.addSpacing(20)
        layout.addWidget(self.root_input)
        layout.addLayout(quality_layout)
        layout.addWidget(self.check_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.restart_button)
        layout.addWidget(self.menu_button)

        self.restart_button.hide()
        self.menu_button.hide()

        # UWAGA: nie wywołujemy tu start_exercise() —
        # robi to MainWindow.show_screen()

    def start_exercise(self):
        self.question_number = 0
        self.score = 0

        self.result_label.setText("")

        self.root_input.show()
        self.play_button.show()
        self.check_button.show()
        self.dur_button.show()
        self.moll_button.show()

        self.restart_button.hide()
        self.menu_button.hide()

        self.next_question()

    def next_question(self):
        if self.question_number >= 10:
            self.show_summary()
            return

        self.question_number += 1

        self.question_label.setText(
            f"Pytanie {self.question_number}/10"
        )

        self.current_chord = random.choice(CHORDS)
        self.selected_quality = None

        self.root_input.clear()
        self.result_label.setText("")

        self.dur_button.setEnabled(True)
        self.moll_button.setEnabled(True)
        self.check_button.setEnabled(True)

        self.dur_button.setStyleSheet("")
        self.moll_button.setStyleSheet("")

        self.play_current_chord()

    def play_current_chord(self):
        if self.current_chord:
            play_chord(self.current_chord)

    def select_quality(self, quality):
        self.selected_quality = quality

        self.dur_button.setStyleSheet("")
        self.moll_button.setStyleSheet("")

        if quality == "dur":
            self.dur_button.setStyleSheet("background-color: #555555;")
        else:
            self.moll_button.setStyleSheet("background-color: #555555;")

    def check_answer(self):
        root = self.root_input.text().strip().upper()

        if root not in ROOT_SEMITONES:
            self.result_label.setText(
                "Wpisz poprawny dźwięk: C, D, E, F, G, A lub H"
            )
            return

        if self.selected_quality is None:
            self.result_label.setText("Wybierz DUR albo MOLL.")
            return

        answer = (root, self.selected_quality)

        self.dur_button.setEnabled(False)
        self.moll_button.setEnabled(False)
        self.check_button.setEnabled(False)

        if answer == self.current_chord:
            self.score += 1
            self.result_label.setText("✓ Dobrze!")
        else:
            correct_root, correct_quality = self.current_chord
            self.result_label.setText(
                f"✗ Źle — poprawna odpowiedź: "
                f"{correct_root} {correct_quality.upper()}"
            )

        QTimer.singleShot(1000, self.next_question)

    def show_summary(self):
        self.root_input.hide()
        self.play_button.hide()
        self.check_button.hide()
        self.dur_button.hide()
        self.moll_button.hide()

        self.question_label.setText("KONIEC ĆWICZENIA")
        self.result_label.setText(f"Wynik: {self.score}/10")

        self.restart_button.show()
        self.menu_button.show()

class ChordTheoryMenu(BaseScreen):
    def __init__(self, main_window):
        super().__init__(
            "TEORIA AKORDÓW",
            "Podaj dźwięki wchodzące w skład akordu"
        )

        self.main_window = main_window

        tiles = QGridLayout()
        tiles.setSpacing(25)

        # Zwykłe akordy
        normal = MenuTile(
            "🎹  ZWYKŁE AKORDY",
            "Akordy bez krzyżyków i bemoli"
        )
        normal.clicked.connect(
            lambda: main_window.show_screen("theory_normal")
        )

        # Akordy z krzyżykami i bemolami
        accidentals = MenuTile(
            "♯♭  KRZYŻYKI I BEMOLE",
            "Akordy z dźwiękami chromatycznymi"
        )
        accidentals.clicked.connect(
            lambda: main_window.show_screen("theory_accidentals")
        )

        tiles.addWidget(normal, 0, 0)
        tiles.addWidget(accidentals, 0, 1)

        self.layout.addLayout(tiles)

        back = QPushButton("←  Wróć do akordów")
        back.setCursor(Qt.PointingHandCursor)
        back.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaaaaa;
                border: none;
                font-size: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        back.clicked.connect(main_window.show_chords)

        self.layout.addWidget(back, alignment=Qt.AlignCenter)

class TheoryNormalScreen(BaseScreen):

    def __init__(self, main_window):
        super().__init__(
            "ZWYKŁE AKORDY",
            "Podaj dźwięki wchodzące w skład akordu"
        )

        self.main_window = main_window

        self.queue = []
        self.question_number = 0
        self.score = 0
        self.current_chord = None
        self.inputs = []

        layout = self.layout

        self.chord_label = QLabel()
        self.chord_label.setAlignment(Qt.AlignCenter)
        self.chord_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("""
            font-size: 16px;
            color: #aaaaaa;
        """)

        inputs_layout = QHBoxLayout()
        inputs_layout.setSpacing(15)

        for i in range(3):
            field = QLineEdit()
            field.setPlaceholderText(f"Dźwięk {i + 1}")
            field.setAlignment(Qt.AlignCenter)
            field.setMinimumHeight(50)
            field.setStyleSheet("""
                QLineEdit {
                    font-size: 20px;
                    font-weight: bold;
                }
            """)
            field.returnPressed.connect(self.check_answer)
            field.installEventFilter(self)          # ← nowa linia

            inputs_layout.addWidget(field)
            self.inputs.append(field)

        self.check_button = QPushButton("✓ SPRAWDŹ")
        self.check_button.setMinimumHeight(55)
        self.check_button.clicked.connect(self.check_answer)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        self.restart_button = QPushButton("🔄 Od nowa")
        self.restart_button.setMinimumHeight(55)
        self.restart_button.clicked.connect(self.start_exercise)

        self.menu_button = QPushButton("← Wybór trudności")
        self.menu_button.setMinimumHeight(55)
        self.menu_button.clicked.connect(
            lambda: self.main_window.show_screen("chord_theory_menu")
        )

        layout.addWidget(self.question_label)
        layout.addWidget(self.chord_label)
        layout.addSpacing(20)
        layout.addLayout(inputs_layout)
        layout.addWidget(self.check_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.restart_button)
        layout.addWidget(self.menu_button)

        self.restart_button.hide()
        self.menu_button.hide()

    # --------------------------------------------------------

    def start_exercise(self):
        self.queue = random.sample(CHORDS, len(CHORDS))
        self.question_number = 0
        self.score = 0

        self.result_label.setText("")

        for field in self.inputs:
            field.show()

        self.check_button.show()
        self.restart_button.hide()
        self.menu_button.hide()

        self.next_question()

    def next_question(self):
        if not self.queue:
            self.show_summary()
            return

        self.question_number += 1
        self.current_chord = self.queue.pop()

        root, quality = self.current_chord

        self.question_label.setText(
            f"Pytanie {self.question_number}/14"
        )
        self.chord_label.setText(f"{root} {quality.upper()}")

        self.result_label.setText("")

        for field in self.inputs:
            field.clear()
            field.setEnabled(True)

        self.check_button.setEnabled(True)
        self.inputs[0].setFocus()

    def check_answer(self):
        given = {
            field.text().strip().lower()
            for field in self.inputs
        }

        if "" in given or len(given) < 3:
            self.result_label.setText(
                "Wypełnij wszystkie 3 pola."
            )
            return

        root, quality = self.current_chord
        expected = set(get_chord_notes(root, quality))

        for field in self.inputs:
            field.setEnabled(False)
        self.check_button.setEnabled(False)

        if given == expected:
            self.score += 1
            self.result_label.setText("✓ Dobrze!")
        else:
            correct_text = ", ".join(sorted(expected))
            self.result_label.setText(
                f"✗ Źle — poprawne dźwięki: {correct_text}"
            )

        QTimer.singleShot(1200, self.next_question)

    def show_summary(self):
        for field in self.inputs:
            field.hide()

        self.check_button.hide()

        self.question_label.setText("KONIEC ĆWICZENIA")
        self.chord_label.setText("")
        self.result_label.setText(f"Wynik: {self.score}/14")

        self.restart_button.show()
        self.menu_button.show()
    
    def eventFilter(self, obj, event):
        if obj in self.inputs and event.type() == QEvent.KeyPress:
            key = event.key()
            index = self.inputs.index(obj)

            if key == Qt.Key_Right and obj.cursorPosition() == len(obj.text()):
                next_index = (index + 1) % len(self.inputs)
                self.inputs[next_index].setFocus()
                self.inputs[next_index].selectAll()
                return True

            if key == Qt.Key_Left and obj.cursorPosition() == 0:
                prev_index = (index - 1) % len(self.inputs)
                self.inputs[prev_index].setFocus()
                self.inputs[prev_index].selectAll()
                return True

        return super().eventFilter(obj, event)


class TheoryAccidentalsScreen(BaseScreen):
    def __init__(self, main_window):
        super().__init__(
            "KRZYŻYKI I BEMOLE",
            "Podaj dźwięki wchodzące w skład akordu"
        )

        info = QLabel("Tutaj później dodamy ćwiczenie z akordami chromatycznymi.")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #aaaaaa; font-size: 16px;")

        self.layout.addWidget(info)

        back = QPushButton("←  Wróć do teorii")
        back.clicked.connect(
            lambda: main_window.show_screen("chord_theory_menu")
        )

        self.layout.addWidget(back, alignment=Qt.AlignCenter)


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

ROOT_SEMITONES = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "H": 11,
}

LETTERS = ['c', 'd', 'e', 'f', 'g', 'a', 'h']

LETTER_SEMITONES = {
    'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'h': 11,
}


def spell_note(letter, diff):
    """Nadaje nazwę literze na podstawie odchylenia od dźwięku czystego."""
    if diff == 0:
        return letter
    if diff == 1:
        return "his" if letter == "h" else letter + "is"
    if diff == -1:
        if letter == "h":
            return "b"
        if letter == "a":
            return "as"
        if letter == "e":
            return "es"
        return letter + "es"
    raise ValueError(f"Nieobsługiwany interwał: {diff}")


def note_by_step(root, steps, semitone_interval):
    """
    Zwraca nazwę dźwięku oddalonego o `steps` liter alfabetu muzycznego
    od `root` i o `semitone_interval` półtonów.
    """
    root = root.lower()
    root_idx = LETTERS.index(root)

    target_letter = LETTERS[(root_idx + steps) % 7]
    natural_semitone = LETTER_SEMITONES[target_letter]

    expected_semitone = (LETTER_SEMITONES[root] + semitone_interval) % 12

    diff = (expected_semitone - natural_semitone) % 12
    if diff > 6:
        diff -= 12

    return spell_note(target_letter, diff)


def get_chord_notes(root, quality):
    """Zwraca listę 3 nazw dźwięków wchodzących w skład akordu."""
    third_interval = 4 if quality == "dur" else 3

    return [
        root.lower(),
        note_by_step(root, 2, third_interval),  # tercja
        note_by_step(root, 4, 7),               # kwinta
    ]

def note_frequency(midi_note):
    """Zwraca częstotliwość nuty dla numeru MIDI."""
    return 440.0 * 2 ** ((midi_note - 69) / 12)


def generate_chord(root, quality, duration=1.2, sample_rate=44100):
    root_midi = 60 + ROOT_SEMITONES[root]

    if quality == "dur":
        intervals = [0, 4, 7]
    else:
        intervals = [0, 3, 7]

    frequencies = [
        note_frequency(root_midi + interval)
        for interval in intervals
    ]

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    audio = np.zeros_like(t)
    for frequency in frequencies:
        audio += np.sin(2 * np.pi * frequency * t)

    audio /= len(frequencies)

    fade_time = 0.05          
    fade_samples = int(sample_rate * fade_time)

    audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
    audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)

    audio *= 0.5

    # cisza na końcu, żeby nie yło pierdzenia
    silence_padding = np.zeros(int(sample_rate * 0.1), dtype=np.float32)
    audio = np.concatenate([audio.astype(np.float32), silence_padding])

    return audio


def play_chord(chord):
    root, quality = chord

    audio = generate_chord(root, quality)

    sd.stop()
    sd.play(audio, 44100, blocking=False)

# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

