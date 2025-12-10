from typing import Literal

import unicodedata
from periodictable import Element, ELEMENTS_DATA, ELEMENT_NAME_TO_NUMBER


ORBITALS = [
    (1, "s"), (2, "s"), (2, "p"),
    (3, "s"), (3, "p"), (4, "s"), 
    (3, "d"), (4, "p"), (5, "s"),
    (4, "d"), (5, "p"), (6, "s"),
    (4, "f"), (5, "d"), (6, "p"),
    (7, "s"), (5, "f"), (6, "d"),
    (7, "p"),
]
SUBORBITAL_COUNTS = {"s": 1, "p": 3, "d": 5, "f": 7}


class PhysicsError(ValueError):
    pass


def convert_to_script(x: str | int, mode: Literal["super", "sub"] = "super") -> str:
    SUPER = str.maketrans("0123456789+-()", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁽⁾")
    SUB = str.maketrans("0123456789+-()", "₀₁₂₃₄₅₆₇₈₉₊₋₍₎")
    x = str(x)
    if mode == "super":
        return x.translate(SUPER)
    else:
        return x.translate(SUB)


def get_electron_configuration(electron_count: int, skip_orbitals: int = 0) -> str:
    configuration = []
    for orbital in ORBITALS[skip_orbitals:]:
        configuration.append(
            f"{orbital[0]}{orbital[1]}{convert_to_script(min(electron_count, SUBORBITAL_COUNTS[orbital[1]] * 2))}"
        )
        electron_count -= min(electron_count, SUBORBITAL_COUNTS[orbital[1]] * 2)
        if electron_count <= 0:
            break
    return " ".join(configuration)


def get_short_electron_configuration(electron_count: int):
    noble_gases = [
        (2, "₂He", 1),
        (10, "₁₀Ne", 3),
        (18, "₁₈Ar", 5),
        (36, "₃₆Kr", 8),
        (54, "₅₄Xe", 11),
        (86, "₈₆Rn", 15),
    ]
    for noble_gas in reversed(noble_gases):
        if electron_count > noble_gas[0]:
            return f"[{noble_gas[1]}] " + get_electron_configuration(
                electron_count - noble_gas[0], skip_orbitals=noble_gas[2]
            )
    return get_electron_configuration(electron_count)


def remove_diacritics(text: str) -> str:
    normalized_text = unicodedata.normalize('NFD', text)
    without_diacritics = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return without_diacritics


def calculate_configuration():
    try:
        user_input = app.entry.get().strip().split(" ")
        electron_count = None
        if len(user_input) == 0:
            return
        elif len(user_input) > 2:
            raise IndexError()
        if user_input[0].isdigit():
            electron_count = int(user_input[0])
            if electron_count < 1:
                raise PhysicsError("Number of electrons must be at least 1.")
            if electron_count > 118:
                raise PhysicsError("Number of electrons exceeds known elements (118).")
        elif len(user_input[0]) == 2 and hasattr(Element, user_input[0][0].upper() + user_input[0][1].lower()):
            electron_count = getattr(Element, user_input[0][0].upper() + user_input[0][1].lower())
        else:
            found_electron_count = ELEMENT_NAME_TO_NUMBER.get(remove_diacritics(user_input[0].lower()))
            if found_electron_count:
                electron_count = found_electron_count
            else:
                raise PhysicsError("Element not found in the periodic table.")
            
        electron_count = int(electron_count)
        atomic_number = electron_count
        if len(user_input) > 1:
            if user_input[1][-1] == "+":
                electron_count -= int(user_input[1][:-1])
            elif user_input[1][-1] == "-":
                electron_count += int(user_input[1][:-1])
            else:
                raise IndexError()

        full_config = get_electron_configuration(electron_count)
        short_config = get_short_electron_configuration(electron_count)
        element_symbol = ELEMENTS_DATA[atomic_number]['symbol']
        app.output_label.configure(
            text=f"{convert_to_script(atomic_number, 'sub') + element_symbol + (convert_to_script(user_input[1]) if len(user_input) > 1 else '')}: {full_config}\n\n{convert_to_script(atomic_number, 'sub') + element_symbol + (convert_to_script(user_input[1]) if len(user_input) > 1 else '')}: {short_config}"
        )
    except PhysicsError as e:
        app.output_label.configure(text=str(e))
    except ValueError:
        app.output_label.configure(
            text="Please enter a valid integer for the number of electrons."
        )
    except IndexError:
        app.output_label.configure(text="Invalid format for ion charge. Use + or - followed by a number.")
        return


if __name__ == "__main__":
    from ui import App
    app = App()
    app.on_button_clicked = calculate_configuration
    app.mainloop()