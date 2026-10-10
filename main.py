
from abc import ABC, abstractmethod
from collections import deque
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# ==========================================
# 1. CLASSES & POLYMORPHISM (From Assignment 1)
# ==========================================


class Researcher(ABC):

  def __init__(self, student_id: int, name: str, base_score: float):
    self.student_id = student_id
    self.name = name
    self.base_score = base_score

  @abstractmethod
  def calculate_performance_metric(self) -> float:
    pass

  def to_file_string(self) -> str:
    return f"{self.__class__.__name__},{self.student_id},{self.name},{self.base_score}"


class ComputerScienceResearcher(Researcher):

  def __init__(
      self,
      student_id: int,
      name: str,
      base_score: float,
      repositories_count: int,
      commits_count: int,
  ):
    super().__init__(student_id, name, base_score)
    self.repositories_count = repositories_count
    self.commits_count = commits_count

  def calculate_performance_metric(self) -> float:
    # Polymorphic variant 1: CS specific metric
    return self.base_score + (self.commits_count * 1.5) + (
        self.repositories_count * 2.0
    )

  def to_file_string(self) -> str:
    base = super().to_file_string()
    return f"{base},{self.repositories_count},{self.commits_count}"


class DataScienceResearcher(Researcher):

  def __init__(
      self,
      student_id: int,
      name: str,
      base_score: float,
      model_accuracy: float,
      model_trained: int,
  ):
    super().__init__(student_id, name, base_score)
    self.model_accuracy = model_accuracy
    self.model_trained = model_trained

  def calculate_performance_metric(self) -> float:
    # Polymorphic variant 2: Data Science specific metric
    return self.base_score + (self.model_accuracy * 50) + (
        self.model_trained * 3.0
    )

  def to_file_string(self) -> str:
    base = super().to_file_string()
    return f"{base},{self.model_accuracy},{self.model_trained}"


class MathematicsResearcher(Researcher):

  def __init__(
      self,
      student_id: int,
      name: str,
      base_score: float,
      proof_verification_count: int,
      theoretical_paper_count: int,
  ):
    super().__init__(student_id, name, base_score)
    self.proof_verification_count = proof_verification_count
    self.theoretical_paper_count = theoretical_paper_count

  def calculate_performance_metric(self) -> float:
    # Polymorphic variant 3: Mathematics specific metric
    return self.base_score + (self.proof_verification_count * 3.0) + (
        self.theoretical_paper_count * 4.0
    )

  def to_file_string(self) -> str:
    base = super().to_file_string()
    return (
        f"{base},{self.proof_verification_count},{self.theoretical_paper_count}"
    )


class ResearchReport:

  def __init__(self, report_title: str, summary: str, status: str = "Draft"):
    self.report_title = report_title
    self.summary = summary
    self.status = status

  def finalize_report(self):
    self.status = "Finalized"


class ResearchProject:

  def __init__(self, project_id: str, title: str):
    self.project_id = project_id
    self.title = title
    self.researchers = []  # Aggregation
    self.reports = []  # Composition
    self.task_queue = deque()  # Abstract Data Type: Queue

  def add_researcher(self, researcher: Researcher):
    self.researchers.append(researcher)

  def count_researchers_by_domain(self, domain_name: str) -> int:
    counts = {
        "CS": ComputerScienceResearcher,
        "DS": DataScienceResearcher,
        "Math": MathematicsResearcher,
    }
    target_class = counts.get(domain_name)
    if not target_class:
      return 0
    return sum(isinstance(r, target_class) for r in self.researchers)

  def calculate_average_performance(self) -> float:
    if not self.researchers:
      return 0.0
    total = sum(r.calculate_performance_metric() for r in self.researchers)
    return total / len(self.researchers)

  def search_researcher_by_id(self, student_id: int) -> Researcher:
    # Linear search algorithm
    for r in self.researchers:
      if r.student_id == student_id:
        return r
    return None

  # ==========================================
  # 2. FILE HANDLING (Save & Read functionality)
  # ==========================================
  def save_to_file(self, filename="nara_data.txt"):
    try:
      with open(filename, "w") as f:
        f.write(f"{self.project_id},{self.title}\n")
        for r in self.researchers:
          f.write(r.to_file_string() + "\n")
      messagebox. Erfolg = "Success"
      messagebox.showinfo("Success", f"Data successfully saved to {filename}")
    except IOError as e:
      messagebox.showerror(
          "File Error", f"An error occurred while saving to file: {e}"
      )

  def load_from_file(self, filename="nara_data.txt"):
    try:
      if not os.path.exists(filename):
        raise FileNotFoundError(f"The file {filename} does not exist.")
      with open(filename, "r") as f:
        lines = f.readlines()
        if not lines:
          return
        proj_info = lines[0].strip().split(",")
        self.project_id = proj_info[0]
        self.title = proj_info[1]
        self.researchers.clear()

        for line in lines[1:]:
          parts = line.strip().split(",")
          if len(parts) < 4:
            continue
          r_type, s_id, name, b_score = (
              parts[0],
              int(parts[1]),
              parts[2],
              float(parts[3]),
          )

          if r_type == "ComputerScienceResearcher":
            self.researchers.append(
                ComputerScienceResearcher(
                    s_id, name, b_score, int(parts[4]), int(parts[5])
                )
            )
          elif r_type == "DataScienceResearcher":
            self.researchers.append(
                DataScienceResearcher(
                    s_id, name, b_score, float(parts[4]), int(parts[5])
                )
            )
          elif r_type == "MathematicsResearcher":
            self.researchers.append(
                MathematicsResearcher(
                    s_id, name, b_score, int(parts[4]), int(parts[5])
                )
            )
      messagebox.showinfo("Success", f"Data successfully loaded from {filename}")
    except Exception as e:
      messagebox.showerror(
          "Error", f"Failed to load data with exception: {e}"
      )


# ==========================================
# 3. GRAPHICAL USER INTERFACE (GUI)
# ==========================================


class NARAGUI:

  def __init__(self, root, project):
    self.root = root
    self.root.title("NARA System - Assignment 2")
    self.root.geometry("600x450")
    self.project = project

    # Menu Bar
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(
        label="Save Data to File", command=self.project.save_to_file
    )
    file_menu.add_command(
        label="Load Data from File", command=self.load_and_refresh
    )
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File Operations", menu=file_menu)
    root.config(menu=menubar)

    # Main UI Layout
    title_label = tk.Label(
        root, text="Namibian Academic Research & Analytics", font=("Arial", 16, "bold")
    )
    title_label.pack(pady=10)

    # Display Box
    self.text_display = tk.Text(root, height=12, width=70)
    self.text_display.pack(pady=5)

    # Buttons Frame
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame,
        text="Add Researcher",
        command=self.add_researcher_dialog,
        width=18,
    ).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(
        btn_frame,
        text="View Analytics",
        command=self.show_analytics,
        width=18,
    ).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(
        btn_frame,
        text="Search by ID",
        command=self.search_researcher,
        width=18,
    ).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(
        btn_frame, text="Refresh View", command=self.refresh_display, width=18
    ).grid(row=1, column=1, padx=5, pady=5)

    self.refresh_display()

  def refresh_display(self):
    self.text_display.delete("1.0", tk.END)
    self.text_display.insert(
        tk.END,
        f"Project ID: {self.project.project_id} | Title: {self.project.title}\n",
    )
    self.text_display.insert(
        tk.END, "-" * 65 + "\n"
    )
    if not self.project.researchers:
      self.text_display.insert(
          tk.END, "No researchers found. Add some using the buttons below.\n"
      )
    for r in self.project.researchers:
      perf = r.calculate_performance_metric()
      info = (
          f"[{r.__class__.__name__}] ID: {r.student_id}, Name: {r.name}, "
          f"Base Score: {r.base_score}, Performance Metric: {perf:.2f}\n"
      )
      self.text_display.insert(tk.END, info)

  def add_researcher_dialog(self):
    try:
      domain = simpledialog.askstring(
          "Domain",
          "Enter domain type (CS, DS, Math):",
      )
      if not domain:
        return
      domain = domain.upper()
      if domain not in ["CS", "DS", "MATH"]:
        raise ValueError("Invalid domain selected! Choose CS, DS, or Math.")

      s_id = simpledialog.askinteger("Input", "Enter Student ID:")
      name = simpledialog.askstring("Input", "Enter Researcher Name:")
      b_score = simpledialog.askfloat("Input", "Enter Base Score:")

      if domain == "CS":
        repos = simpledialog.askinteger("Input", "Enter Repositories Count:")
        commits = simpledialog.askinteger("Input", "Enter Commits Count:")
        res = ComputerScienceResearcher(s_id, name, b_score, repos, commits)
      elif domain == "DS":
        acc = simpledialog.askfloat("Input", "Enter Model Accuracy (0-1):")
        trained = simpledialog.askinteger("Input", "Enter Models Trained Count:")
        res = DataScienceResearcher(s_id, name, b_score, acc, trained)
      elif domain == "MATH":
        proofs = simpledialog.askinteger("Input", "Enter Proofs Verified Count:")
        papers = simpledialog.askinteger(
            "Input", "Enter Theoretical Papers Count:"
        )
        res = MathematicsResearcher(s_id, name, b_score, proofs, papers)

      self.project.add_researcher(res)
      self.refresh_display()
      messagebox.showinfo("Success", "Researcher added successfully!")
    except Exception as e:
      messagebox.showerror(
          "Input Error", f"Invalid input or operation cancelled: {e}"
      )

  def show_analytics(self):
    cs_count = self.project.count_researchers_by_domain("CS")
    ds_count = self.project.count_researchers_by_domain("DS")
    math_count = self.project.count_researchers_by_domain("Math")
    avg_perf = self.project.calculate_average_performance()

    report_text = (
        f"--- Analytics Report ---\n"
        f"Computer Science Researchers: {cs_count}\n"
        f"Data Science Researchers: {ds_count}\n"
        f"Mathematics Researchers: {math_count}\n"
        f"Average Performance Metric: {avg_perf:.2f}\n"
    )
    messagebox.showinfo("Analytics Report", report_text)

  def search_researcher(self):
    try:
      s_id = simpledialog.askinteger(
          "Search", "Enter Student ID to search:"
      )
      if s_id is None:
        return
      res = self.project.search_researcher_by_id(s_id)
      if res:
        messagebox.showinfo(
            "Found",
            f"Found! Name: {res.name}, Domain: {res.__class__.__name__}, Metric:"
            f" {res.calculate_performance_metric():.2f}",
        )
      else:
        messagebox.showwarning("Not Found", f"No researcher found with ID {s_id}")
    except Exception as e:
      messagebox.showerror("Error", f"An error occurred: {e}")

  def load_and_refresh(self):
    self.project.load_from_file()
    self.refresh_display()


# ==========================================
# 4. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
  # Initialize Project
  nara_project = ResearchProject(
      "PRJ-2026-01", "Namibian Academic Research & Analytics"
  )

  # Start Tkinter GUI
  root = tk.Tk()
  app = NARAGUI(root, nara_project)
  root.mainloop()