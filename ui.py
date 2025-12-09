import customtkinter as ctk
from config import load_settings

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.settings = load_settings()
        self.on_button_clicked = lambda: print("hi")
        button_hover = "#%02x%02x%02x" % tuple(
            int(int(c, 16) * 0.8)
            for c in [self.settings["button_color"][1:3], self.settings["button_color"][3:5], self.settings["button_color"][5:7]]
        )

        ctk.set_appearance_mode("Light")
        self.configure(fg_color=self.settings["background_color"])
        self.geometry("600x400")
        self.title("Electron Configuration")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        title_label = ctk.CTkLabel(
            self,
            text="Electron Configuration Calculator",
            text_color=self.settings["text_color"],
            anchor="center",
            font=ctk.CTkFont(family="trebuchet ms", size=35, weight="bold"),
        )
        title_label.grid(row=0, column=0, padx=20, pady=20)

        entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        entry_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        entry_frame.columnconfigure(0, weight=3)
        entry_frame.columnconfigure(1, weight=1)
        entry_frame.rowconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            entry_frame,
            text_color=self.settings["text_color"],
            fg_color=self.settings["entry_and_label_color"],
            font=ctk.CTkFont(family="trebuchet ms", size=25),
            placeholder_text="Enter amount of electrons",
        )
        self.entry.grid(row=0, column=0, padx=10, sticky="nsew")

        calculate_button = ctk.CTkButton(
            entry_frame,
            fg_color=self.settings["button_color"],
            hover_color=button_hover,
            font=ctk.CTkFont(family="trebuchet ms", size=25),
            command=self._button_clicked,
            text_color=self.settings["text_color"],
            text="Calculate",
        )
        calculate_button.grid(row=0, column=1, padx=10, sticky="nsew")

        self.output_label = ctk.CTkLabel(
            self,
            text="",
            text_color=self.settings["text_color"],
            corner_radius=15,
            fg_color=self.settings["entry_and_label_color"],
            font=ctk.CTkFont(family="trebuchet ms", size=25),
            wraplength=630,
        )
        self.output_label.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")


        self.bind("<Return>", self._button_clicked)
            
    def _button_clicked(self, event=None):
        self.on_button_clicked()

if __name__ == "__main__":
    App()