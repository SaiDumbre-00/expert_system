import tkinter as tk
from tkinter import messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Main Window
root = tk.Tk()
root.title("Medical Expert System")
root.geometry("520x700")
root.configure(bg="#f5f7fa")

# Title
tk.Label(root, text="Medical Expert System",
         font=("Arial", 18, "bold"), bg="#f5f7fa").pack(pady=10)

# Patient Name
tk.Label(root, text="Enter Patient Name:",
         font=("Arial", 12), bg="#f5f7fa").pack()

patient_name = tk.Entry(root, font=("Arial", 12))
patient_name.pack(pady=5)

# Rules (Knowledge Base)
rules = [
    {"disease": "Fever", "symptoms": ["fever", "weakness"], "advice": "Take rest and drink water"},
    {"disease": "Cold", "symptoms": ["cough", "cold", "throat pain"], "advice": "Drink warm water and take steam"},
    {"disease": "Flu", "symptoms": ["fever", "cough", "weakness"], "advice": "Take rest and proper medicine"},
    {"disease": "Headache", "symptoms": ["headache"], "advice": "Take rest and avoid screen"},
    {"disease": "Food Poisoning", "symptoms": ["feeling like vomiting", "vomiting"], "advice": "Drink ORS and stay hydrated"},
    {"disease": "Stomach Pain", "symptoms": ["feeling like vomiting", "weakness"], "advice": "Eat light food and rest"},
]

# Symptoms List
symptoms_list = [
    "fever", "cough", "weakness", "headache",
    "feeling like vomiting", "vomiting", "throat pain", "cold"
]

# Selected symptoms
selected = set()
buttons = []
result_text = ""

# Toggle button selection
def toggle(symptom, btn):
    if symptom in selected:
        selected.remove(symptom)
        btn.config(bg="#e0e0e0", fg="black")
    else:
        selected.add(symptom)
        btn.config(bg="#4CAF50", fg="white")

# Symptoms Label
tk.Label(root, text="Select Symptoms",
         font=("Arial", 14, "bold"), bg="#f5f7fa").pack(pady=10)

# Symptoms Buttons Frame
frame = tk.Frame(root, bg="#f5f7fa")
frame.pack()

# Create buttons
for symptom in symptoms_list:
    btn = tk.Button(frame, text=symptom, width=20, bg="#e0e0e0")
    btn.pack(pady=5)

    btn.config(command=lambda s=symptom, b=btn: toggle(s, b))
    buttons.append(btn)

# Diagnose Function
def diagnose():
    global result_text

    if not selected:
        messagebox.showwarning("Warning", "Please select symptoms")
        return

    results = []

    for rule in rules:
        match = len(set(rule["symptoms"]) & selected)
        confidence = (match / len(rule["symptoms"])) * 100

        if match > 0:
            results.append((rule["disease"], confidence, rule["advice"]))

    results.sort(key=lambda x: x[1], reverse=True)

    output.delete("1.0", tk.END)
    result_text = ""

    name = patient_name.get() if patient_name.get() else "Unknown"

    header = f"Patient Name: {name}\n\nDiagnosis Report:\n\n"
    output.insert(tk.END, header)
    result_text += header

    if results:
        for disease, confidence, advice in results:
            text = f"Disease: {disease}\nConfidence: {confidence:.2f}%\nAdvice: {advice}\n\n"
            output.insert(tk.END, text)
            result_text += text
    else:
        output.insert(tk.END, "No disease matched")

# Export PDF Function
def export_pdf():
    global result_text

    if not result_text:
        messagebox.showerror("Error", "No result to export")
        return

    doc = SimpleDocTemplate("Diagnosis_Report.pdf")
    styles = getSampleStyleSheet()

    content = []
    for line in result_text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 5))

    doc.build(content)
    messagebox.showinfo("Success", "PDF saved successfully")

# Buttons
tk.Button(root, text="Diagnose", command=diagnose,
          bg="#4CAF50", fg="white", width=20, height=2).pack(pady=10)

tk.Button(root, text="Export PDF", command=export_pdf,
          bg="#2196F3", fg="white", width=20, height=2).pack()

# Output Box
output = tk.Text(root, height=15, width=60)
output.pack(pady=10)

# Warning Label
tk.Label(root, text="⚠️ Not a real medical system",
         fg="red", bg="#f5f7fa").pack()

# Run App
root.mainloop()