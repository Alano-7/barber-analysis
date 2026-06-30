import subprocess

print("Starting extraction...")
subprocess.run(["python", r"C:\Users\alano\OneDrive\Documents\barber_analysis\Scripts\extract_google.py"])

print("Starting transformation...")
subprocess.run(["python", r"C:\Users\alano\OneDrive\Documents\barber_analysis\Scripts\clean.py"])

print("Starting loading...")
subprocess.run(["python", r"C:\Users\alano\OneDrive\Documents\barber_analysis\Scripts\load.py"])

print("Pipeline complete!")

print("Presenting dashboard...")
subprocess.run(["python", r"C:\Users\alano\OneDrive\Documents\barber_analysis\Scripts\dash.py"])
