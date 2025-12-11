from typing import Literal, Dict, List, Tuple
import unicodedata
from periodictable import Element, ELEMENTS_DATA, ELEMENT_NAME_TO_NUMBER

# Order of filling (Aufbau principle)
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

# Anomalous electron configurations
# Key = Atomic Number. Value = List of transfers: (source_n, source_l, target_n, target_l, amount)
ANOMALY_TRANSFERS = {
    24: [(4, "s", 3, "d", 1)],  # Cr
    29: [(4, "s", 3, "d", 1)],  # Cu
    41: [(5, "s", 4, "d", 1)],  # Nb
    42: [(5, "s", 4, "d", 1)],  # Mo
    44: [(5, "s", 4, "d", 1)],  # Ru
    45: [(5, "s", 4, "d", 1)],  # Rh
    46: [(5, "s", 4, "d", 2)],  # Pd
    47: [(5, "s", 4, "d", 1)],  # Ag
    57: [(4, "f", 5, "d", 1)],  # La
    58: [],                     # Ce
    64: [(4, "f", 5, "d", 1)],  # Gd
    78: [(6, "s", 5, "d", 1)],  # Pt
    79: [(6, "s", 5, "d", 1)],  # Au
    89: [(5, "f", 6, "d", 1)],  # Ac
    90: [(5, "f", 6, "d", 2)],  # Th
    91: [(5, "f", 6, "d", 1)],  # Pa
    92: [(5, "f", 6, "d", 1)],  # U
    93: [(5, "f", 6, "d", 1)],  # Np
    96: [(5, "f", 6, "d", 1)],  # Cm
}


ANOMALY_TRANSFERS[58] = [(4, "f", 5, "d", 1)]


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

def get_electron_configuration(atomic_number: int, charge: int = 0) -> str:
    """
    Calculates the electron configuration for an atom or ion.
    
    Args:
        atomic_number: The proton number (Z).
        charge: The net charge of the species (default 0).
        
    Returns:
        String representation of the configuration.
    """
    
    total_electrons = atomic_number - charge
    
    if total_electrons < 1:
        raise PhysicsError("Resulting electron count must be at least 1.")
    
    # store configuration as a dictionary {(n, l): count}
    config = {}

    electrons_to_distribute = atomic_number
    
    # Neutral Config
    for orbital in ORBITALS:
        config[orbital] = 0
            
    for orbital in ORBITALS:
        capacity = SUBORBITAL_COUNTS[orbital[1]] * 2
        fill = min(electrons_to_distribute, capacity)
        config[orbital] += fill
        electrons_to_distribute -= fill
        if electrons_to_distribute <= 0:
            break
            
    # 2. Apply Anomalies (to Neutral State)
    if atomic_number in ANOMALY_TRANSFERS:
        for transfer in ANOMALY_TRANSFERS[atomic_number]:
            src_n, src_l, dest_n, dest_l, amount = transfer
            
            src_key = (src_n, src_l)
            dest_key = (dest_n, dest_l)
            
            if config.get(src_key, 0) >= amount:
                config[src_key] -= amount
                config[dest_key] = config.get(dest_key, 0) + amount
    
    # 3. Adjust for Ions
    if charge > 0:
        electrons_to_remove = charge
        
        while electrons_to_remove > 0:
            populated = [orb for orb, count in config.items() if count > 0]
            if not populated:
                break
                
            l_val = {"s": 0, "p": 1, "d": 2, "f": 3}
            
            # Sort: largest first
            populated.sort(key=lambda x: (-x[0], -l_val[x[1]]))
            
            target_orbital = populated[0]
            count = config[target_orbital]
            
            remove = min(electrons_to_remove, count)
            config[target_orbital] -= remove
            electrons_to_remove -= remove
            
    elif charge < 0:
        # Anion: Add electrons
        electrons_to_add = abs(charge)
        
        while electrons_to_add > 0:
            # Find first orbital that is not full
            target_orbital = None
            for orbital in ORBITALS:
                capacity = SUBORBITAL_COUNTS[orbital[1]] * 2
                current = config.get(orbital, 0)
                if current < capacity:
                    target_orbital = orbital
                    break
            
            if target_orbital:
                capacity = SUBORBITAL_COUNTS[target_orbital[1]] * 2
                current = config.get(target_orbital, 0)
                space = capacity - current
                add = min(electrons_to_add, space)
                config[target_orbital] = current + add
                electrons_to_add -= add
            else:
                break # Should not happen unless > 118
                
    # 4. Format Output
    formatted_config = []
    
    # Ideally, we display all populated orbitals.
    # Let's sort by energy (index in ORBITALS)
    orbital_to_index = {orb: i for i, orb in enumerate(ORBITALS)}
    
    max_occupied_index = -1
    for i, orbital in enumerate(ORBITALS):
        if config.get(orbital, 0) > 0:
            max_occupied_index = i
            
    for i, orbital in enumerate(ORBITALS):
        if i <= max_occupied_index:
            count = config.get(orbital, 0)
            formatted_config.append(
                f"{orbital[0]}{orbital[1]}{convert_to_script(count)}"
            )
            
    return " ".join(formatted_config)


def get_short_electron_configuration(atomic_number: int, charge: int = 0):
    full_config_str = get_electron_configuration(atomic_number, charge)
    parts = full_config_str.split(" ")
    
    NOBLE_GASES = [
        (86, "₈₆Rn", ["1s"+convert_to_script(2), "2s"+convert_to_script(2), "2p"+convert_to_script(6), "3s"+convert_to_script(2), "3p"+convert_to_script(6), "4s"+convert_to_script(2), "3d"+convert_to_script(10), "4p"+convert_to_script(6), "5s"+convert_to_script(2), "4d"+convert_to_script(10), "5p"+convert_to_script(6), "6s"+convert_to_script(2), "4f"+convert_to_script(14), "5d"+convert_to_script(10), "6p"+convert_to_script(6)]),
        (54, "₅₄Xe", ["1s"+convert_to_script(2), "2s"+convert_to_script(2), "2p"+convert_to_script(6), "3s"+convert_to_script(2), "3p"+convert_to_script(6), "4s"+convert_to_script(2), "3d"+convert_to_script(10), "4p"+convert_to_script(6), "5s"+convert_to_script(2), "4d"+convert_to_script(10), "5p"+convert_to_script(6)]),
        (36, "₃₆Kr", ["1s"+convert_to_script(2), "2s"+convert_to_script(2), "2p"+convert_to_script(6), "3s"+convert_to_script(2), "3p"+convert_to_script(6), "4s"+convert_to_script(2), "3d"+convert_to_script(10), "4p"+convert_to_script(6)]),
        (18, "₁₈Ar", ["1s"+convert_to_script(2), "2s"+convert_to_script(2), "2p"+convert_to_script(6), "3s"+convert_to_script(2), "3p"+convert_to_script(6)]),
        (10, "₁₀Ne", ["1s"+convert_to_script(2), "2s"+convert_to_script(2), "2p"+convert_to_script(6)]),
        (2, "₂He",  ["1s"+convert_to_script(2)]),
    ]
    
    for count, symbol, orbitals in NOBLE_GASES:
        if len(parts) > len(orbitals) and parts[:len(orbitals)] == orbitals:
            remainder = parts[len(orbitals):]
            return f"[{symbol}] " + " ".join(remainder)
             
    return full_config_str


def remove_diacritics(text: str) -> str:
    normalized_text = unicodedata.normalize('NFD', text)
    without_diacritics = normalized_text.encode('ascii', 'ignore').decode('utf-8')
    return without_diacritics


def calculate_configuration():
    try:
        user_input = app.entry.get().strip().split(" ")
        
        # Parse inputs
        if len(user_input) == 0:
            return
        elif len(user_input) > 2:
            raise IndexError()
            
        # 1. Determine Identity
        element_symbol = ""
        atomic_number = 0
        
        first_arg = user_input[0]
        
        if first_arg.isdigit():
            val = int(first_arg)
            if val < 1:
                raise PhysicsError("Atomic number must be at least 1.")
            if val > 118:
                raise PhysicsError("Atomic number exceeds known elements (118).")
            atomic_number = val
            element_symbol = ELEMENTS_DATA[atomic_number]['symbol']
            
        elif len(first_arg) <= 2 and hasattr(Element, first_arg.capitalize()):
             symbol_clean = first_arg.capitalize()
             atomic_number = getattr(Element, symbol_clean)
             element_symbol = symbol_clean
        else:
            # Try name lookup
            found_number = ELEMENT_NAME_TO_NUMBER.get(remove_diacritics(first_arg.lower()))
            if found_number:
                atomic_number = found_number
                element_symbol = ELEMENTS_DATA[atomic_number]['symbol']
            else:
                raise PhysicsError("Element not found.")

        # 2. Determine Charge
        charge = 0
        charge_str = ""
        if len(user_input) > 1:
            raw_charge = user_input[1]
            charge_str = raw_charge # for display
            
            # Formats: "2+", "2-", "+", "-"
            if raw_charge == "+" or raw_charge == "1+":
                charge = 1
            elif raw_charge == "-" or raw_charge == "1-":
                charge = -1
            elif raw_charge[-1] == "+":
                charge = int(raw_charge[:-1])
            elif raw_charge[-1] == "-":
                charge = -int(raw_charge[:-1])
            elif raw_charge[0] == "+":
                charge = int(raw_charge[1:])
            elif raw_charge[0] == "-":
                charge = int(raw_charge)
            else:
                try:
                    charge = int(raw_charge)
                except:
                    raise IndexError("Invalid charge format")

        full_config = get_electron_configuration(atomic_number, charge)
        short_config = get_short_electron_configuration(atomic_number, charge)
        
        # Formatted Element Label: e.g. ₂₆Fe²⁺
        label_part = f"{convert_to_script(atomic_number, 'sub')}{element_symbol}{convert_to_script(charge_str) if charge_str else ''}"
        
        app.output_label.configure(
            text=f"{label_part}: {full_config}\n\n{label_part}: {short_config}"
        )
    except PhysicsError as e:
        app.output_label.configure(text=str(e))
    except ValueError:
        app.output_label.configure(
            text="Please enter a valid element or atomic number."
        )
    except IndexError:
        app.output_label.configure(text="Invalid format. Use '[Element] [Charge]'. E.g. 'Fe 2+'")
        return


if __name__ == "__main__":
    from ui import App
    app = App()
    app.on_button_clicked = calculate_configuration
    app.mainloop()
