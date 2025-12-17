"""Interface graphique minimale sans dépendances externes."""

from __future__ import annotations

import logging
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from listedetenus.workflow import convert_pdf_to_csv

LOG_FORMAT = "%(levelname)s | %(message)s"
WINDOW_TITLE = "Liste des détenus - Conversion PDF vers CSV"
WINDOW_SIZE = "520x220"
PADDING = 8

LOGGER = logging.getLogger(__name__)


class ConversionApp:
    """Gère l'interface Tkinter et les interactions utilisateur."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.pdf_path_var = tk.StringVar()
        self.csv_path_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Prêt à convertir.")
        self._configure_root()
        self._build_widgets()

    def run(self) -> None:
        """Démarre la boucle principale Tkinter."""

        self.root.mainloop()

    def _configure_root(self) -> None:
        """Initialise la fenêtre principale."""

        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)

    def _build_widgets(self) -> None:
        """Construit les champs et boutons de l'interface."""

        frame = tk.Frame(self.root, padx=PADDING, pady=PADDING)
        frame.pack(fill=tk.BOTH, expand=True)

        self._build_path_row(
            frame, "Fichier PDF :", self.pdf_path_var, self._on_browse_pdf
        )
        self._build_path_row(
            frame, "CSV de sortie :", self.csv_path_var, self._on_browse_csv
        )

        convert_button = tk.Button(
            frame,
            text="Convertir",
            command=self._on_convert,
            padx=12,
            pady=6,
        )
        convert_button.grid(row=2, column=0, columnspan=3, pady=(12, 0))

        status_label = tk.Label(
            frame,
            textvariable=self.status_var,
            anchor="w",
            fg="gray30",
        )
        status_label.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="we",
            pady=(12, 0),
        )

    def _build_path_row(
        self,
        frame: tk.Frame,
        label_text: str,
        path_var: tk.StringVar,
        browse_callback: tk.Callable[[], None],
    ) -> None:
        """Crée une ligne avec libellé, champ et bouton Parcourir."""

        row_index = frame.grid_size()[1]
        label = tk.Label(frame, text=label_text, anchor="w")
        label.grid(row=row_index, column=0, sticky="w", pady=(0, 4))

        entry = tk.Entry(frame, textvariable=path_var, width=48)
        entry.grid(row=row_index, column=1, padx=(8, 8), pady=(0, 4))

        button = tk.Button(frame, text="Parcourir", command=browse_callback)
        button.grid(row=row_index, column=2, pady=(0, 4))

    def _on_browse_pdf(self) -> None:
        """Demande à l'utilisateur de choisir un PDF."""

        selected = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if selected:
            self.pdf_path_var.set(selected)

    def _on_browse_csv(self) -> None:
        """Demande à l'utilisateur de choisir un CSV de sortie."""

        selected = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")]
        )
        if selected:
            self.csv_path_var.set(selected)

    def _on_convert(self) -> None:
        """Lance la conversion et affiche le résultat."""

        pdf_value = self.pdf_path_var.get().strip()
        csv_value = self.csv_path_var.get().strip()
        if not self._paths_provided(pdf_value, csv_value):
            return

        pdf_path = Path(pdf_value).expanduser()
        csv_path = Path(csv_value).expanduser()

        self._set_status("Conversion en cours...")
        try:
            result_path = convert_pdf_to_csv(pdf_path, csv_path)
        except Exception as error:  # noqa: BLE001
            LOGGER.error("Échec GUI: %s", error)
            self._show_error(str(error))
            self._set_status("Échec de la conversion.")
            return

        messagebox.showinfo(
            "Succès",
            f"Fichier CSV généré :\n{result_path.as_posix()}",
        )
        self._set_status("Conversion terminée.")

    def _paths_provided(self, pdf_value: str, csv_value: str) -> bool:
        """Vérifie que les champs PDF et CSV sont remplis."""

        if not pdf_value:
            self._show_error("Veuillez sélectionner un fichier PDF.")
            return False
        if not csv_value:
            self._show_error("Veuillez sélectionner un fichier CSV.")
            return False
        return True

    def _show_error(self, message: str) -> None:
        """Affiche une boîte de dialogue d'erreur."""

        messagebox.showerror("Erreur", message)

    def _set_status(self, message: str) -> None:
        """Met à jour la zone de statut."""

        self.status_var.set(message)


def main() -> None:
    """Point d'entrée de l'interface graphique."""

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    root = tk.Tk()
    app = ConversionApp(root)
    app.run()


if __name__ == "__main__":
    main()
