import sys
import os
import subprocess

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QRadioButton
)

from backend.run_multiwfn import run_qtaim, run_nci


# =========================================================
# FILE TAB
# =========================================================
class FileTab(QWidget):
    def __init__(self):
        super().__init__()

        self.wfn_file = None

        layout = QVBoxLayout()

        self.label = QLabel("No wavefunction file selected")
        self.button = QPushButton("Load Wavefunction File")
        self.button.clicked.connect(self.load_file)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select wavefunction file",
            "",
            "Wavefunction Files (*.wfn *.wfx *.fchk *.molden)"
        )
        if file_path:
            self.wfn_file = file_path
            self.label.setText(f"Loaded: {file_path}")



# SIMPLE PLACEHOLDER TAB

class SimpleTab(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(text))
        self.setLayout(layout)



# NCI TAB

class NCITab(QWidget):
    def __init__(self, file_tab):
        super().__init__()

        self.file_tab = file_tab

        layout = QVBoxLayout()

        layout.addWidget(QLabel("NCI Type:"))

        self.classic_radio = QRadioButton("Classic NCI (RDG-based)")
        self.fragment_radio = QRadioButton("Fragment-based NCI (IGM / IGMH)")
        self.classic_radio.setChecked(True)

        layout.addWidget(self.classic_radio)
        layout.addWidget(self.fragment_radio)

        self.run_nci_button = QPushButton("Run NCI Analysis")
        self.run_nci_button.clicked.connect(self.run_nci)
        layout.addWidget(self.run_nci_button)

        self.status_label = QLabel("NCI analysis not run yet.")
        layout.addWidget(self.status_label)

        self.launch_vmd_button = QPushButton("Launch VMD (NCI)")
        self.launch_vmd_button.clicked.connect(self.launch_vmd)
        layout.addWidget(self.launch_vmd_button)

        self.setLayout(layout)

   
    # RUN NCI
   
    def run_nci(self):
        wfn_file = self.file_tab.wfn_file

        if not wfn_file:
            self.status_label.setText("Please load a wavefunction file first.")
            return

        if not self.classic_radio.isChecked():
            self.status_label.setText(
                "Fragment-based NCI is not implemented yet."
            )
            return

        try:
            self.status_label.setText("Running NCI analysis...")
            output_dir = run_nci(wfn_file)

            self.status_label.setText(
                "NCI analysis completed successfully.\n"
                f"Output directory:\n{output_dir}"
            )

        except Exception as e:
            self.status_label.setText(
                f"NCI analysis failed:\n{e}"
            )


    # LAUNCH VMD (NCI)
  
    def launch_vmd(self):
        vmd_path = r"C:\Users\hp\OneDrive\Desktop\Multiwfn_3.7_bin_Win64\VMD\vmd.exe"

        wfn_file = self.file_tab.wfn_file
        if not wfn_file:
            self.status_label.setText("Run NCI first, then launch VMD.")
            return

        workdir = os.path.join(os.path.dirname(wfn_file), "NCI_Output")
        tcl_file = os.path.join(workdir, "nci_vmd.tcl")

        if not os.path.exists(tcl_file):
            self.status_label.setText("nci_vmd.tcl not found in NCI_Output!")
            return

        try:
            subprocess.Popen(
                [vmd_path, "-e", tcl_file],
                cwd=workdir
            )
            self.status_label.setText("VMD launched for NCI visualization.")

        except Exception as e:
            self.status_label.setText(
                f"Failed to launch VMD:\n{e}"
            )



# MAIN WINDOW

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTAIM + NCI + IGI GUI (Prototype)")
        self.setGeometry(300, 200, 720, 500)

        self.tabs = QTabWidget()
        self.file_tab = FileTab()

        self.tabs.addTab(self.file_tab, "File")
        self.tabs.addTab(SimpleTab("QTAIM options will appear here"), "QTAIM")

        self.nci_tab = NCITab(self.file_tab)
        self.tabs.addTab(self.nci_tab, "NCI")

        self.tabs.addTab(SimpleTab("IGI options will appear here"), "IGI")

        self.run_button = QPushButton("Run QTAIM Analysis")
        self.run_button.clicked.connect(self.run_qtaim)

        self.vmd_button = QPushButton("Launch VMD (Full QTAIM)")
        self.vmd_button.clicked.connect(self.launch_vmd)

        central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.run_button)
        layout.addWidget(self.vmd_button)
        central.setLayout(layout)

        self.setCentralWidget(central)

    
    # RUN QTAIM
    
    def run_qtaim(self):
        wfn_file = self.file_tab.wfn_file

        if not wfn_file:
            self.file_tab.label.setText("Please load a wavefunction file first!")
            return

        output_dir = run_qtaim(wfn_file)
        self.file_tab.label.setText(
            f"QTAIM completed.\nOutput directory:\n{output_dir}"
        )

  
    # LAUNCH VMD (QTAIM)
  
    def launch_vmd(self):
        vmd_path = r"C:\Users\hp\OneDrive\Desktop\Multiwfn_3.7_bin_Win64\VMD\vmd.exe"

        wfn_file = self.file_tab.wfn_file
        if not wfn_file:
            self.file_tab.label.setText("Run QTAIM first, then launch VMD.")
            return

        workdir = os.path.join(os.path.dirname(wfn_file), "QTAIM_Output")
        tcl_file = os.path.join(workdir, "qtaim_vmd.tcl")

        if not os.path.exists(tcl_file):
            self.file_tab.label.setText("qtaim_vmd.tcl not found in QTAIM_Output!")
            return

        subprocess.Popen(
            [vmd_path, "-e", tcl_file],
            cwd=workdir
        )

# PROGRAM ENTRY POINT
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
