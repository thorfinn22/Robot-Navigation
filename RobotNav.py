import tkinter as tk
from tkinter import ttk
from map import Map
from Read import InitRes
from algorithom import algorithom

path = "RobotNav-test.txt"
class RobotNavApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Robot Navigation")

        # Load data
        file = InitRes(path)
        file.populateData()
        self.map = Map(file.getMapStructure(), file.getWall())
        self.robot = algorithom(file.getInitialState(), file.getGoalState(), self.map)

        # Setup the GUI layout
        self.label = tk.Label(master, text="Select Search Method:")
        self.label.pack()

        self.method = tk.StringVar()
        self.dropdown = ttk.Combobox(master, textvariable=self.method)
        self.dropdown['values'] = ("DFS", "BFS", "GBFS", "AS", "CUS1", "CUS2", "CUS3")
        self.dropdown.pack()

        self.run_button = tk.Button(master, text="Run Search", command=self.run_search)
        self.run_button.pack()

        self.result_text = tk.Text(master, height=10, width=50)
        self.result_text.pack()

    def run_search(self):
        method = self.method.get()
        result = "Invalid selection. Please select a valid search method."
        if method == "DFS":
            result = self.robot.DfsSearch()
        elif method == "BFS":
            result = self.robot.BfsSearch()
        elif method == "GBFS":
            result = self.robot.GbfsSearch()
        elif method == "AS":
            result = self.robot.AStarSearch()
        elif method == "CUS1":
            result = self.robot.UcsSearch()
        elif method == "CUS2":
            result = self.robot.IdasSearch()
        elif method == "CUS3":
            result = self.robot.VisitAllGoalShortest()

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(result))

def main():
    root = tk.Tk()
    app = RobotNavApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
