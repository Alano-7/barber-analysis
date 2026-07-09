import subprocess
import sys

CREATE_NO_WINDOW = 0x08000000

scripts = [
    r"C:\Users\alano\OneDrive\Documents\barber_analysis\Scripts\extract_google.py",
    r"C:\Users\alano\OneDrive\Documents\barber_analysis\Scripts\clean.py",
    r"C:\Users\alano\OneDrive\Documents\barber_analysis\Scripts\load.py"
]

for script in scripts:
    subprocess.run(
        [sys.executable, script],
        creationflags=CREATE_NO_WINDOW,
        check=True
    )
#print("Presenting dashboard...")
#subprocess.run(["python", r"C:\Users\alano\OneDrive\Documents\barber_analysis\Scripts\dash.py"])
