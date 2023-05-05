import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

win = tk.Tk()
win.title("FCFS Visualiser")
win.config(bg="skyblue")

def calculate():
    arrival_times = []
    burst_times = []
    process_ids = []
    completion_times = []
    turn_around_times = []
    waiting_times = []
    for i in range(5):
        arrival_times.append(int(arrival_entries[i].get()))
        burst_times.append(int(burst_entries[i].get()))
        process_ids.append(int(processid_entries[i].get()))

    # Sorting arrays
    for i in range(len(arrival_times)):
      for j in range(0, len(arrival_times) - i - 1):
          if arrival_times[j] > arrival_times[j + 1]:
              temp = arrival_times[j]
              arrival_times[j] = arrival_times[j+1]
              arrival_times[j+1] = temp

              temp1 = burst_times[j]
              burst_times[j] = burst_times[j+1]
              burst_times[j+1] = temp1

              temp2 = process_ids[j]
              process_ids[j] = process_ids[j+1]
              process_ids[j+1] = temp2
    # Calculate completion time and waiting time for each process
    for i in range(5):
        if i == 0:
            completion_times.append(burst_times[i])
        else:
            completion_times.append(completion_times[i-1] + burst_times[i])
    
    # Calculate turnaround time and waiting time for each process
    for i in range(5):
        turn_around_times.append(completion_times[i] - arrival_times[i])
        waiting_times.append(turn_around_times[i] - burst_times[i])

    # Create Gantt Chart
    fig, gnt = plt.subplots()

    # Set chart properties
    gnt.set_title('FCFS Gantt Chart')
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.grid(True)

    # Set x-axis limits
    gnt.set_xlim(0, completion_times[-1]+3)

    # Set y-axis limits
    gnt.set_ylim(0, len(process_ids))

    # Create bars for each process
    c=burst_times[0]
    colors=["red","green","yellow","purple","blue"]
    for i in range(len(process_ids)):
        
        if(i==0):
          gnt.broken_barh([(arrival_times[i], burst_times[i])], (i, 1),color=colors[i])
        else:
          gnt.broken_barh([(c, burst_times[i])], (i,1),color=colors[i])
          c+=burst_times[i]

        # Add process labels
        gnt.text(completion_times[i], i+0.5, f'P{process_ids[i]} & WT: {waiting_times[i]}')
    ax = plt.gca()
    ax.axes.yaxis.set_ticklabels([])
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start, end, 1))
    
    # Calculate average waiting time and turnaround time
    awt = sum(waiting_times)/5
    att = sum(turn_around_times)/5

    textbox = tk.Text(result_frame, height=5, width=30, font=("Helvetica", 12))
    textbox.grid(column=0, row=1)
    textbox.insert(tk.END, "Average Waiting Time: " + str(awt) + "\nAverage Turnaround Time: " + str(att))
                

    #Display Gantt Chart
    gantt_frame = tk.Frame(result_frame,padx=10, pady=10)
    gantt_frame.grid(column=0, row=0)

    canvas = FigureCanvasTkAgg(fig,master = gantt_frame)  
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(column=0, row=0)



result_frame2 = tk.Frame(win)
result_frame2.grid(column=0, row=0)

labeltitle = tk.Label(result_frame2, text="FCFS Visualiser", font=("Helvetica Bold", 20))
labeltitle.grid(column=1, row=0)

inputframe = tk.Frame(result_frame2)
inputframe.grid(column=1, row=1)


arrival_entries = []
burst_entries = []
processid_entries = []

names = ["Process ID", "Arrival Time", "Burst Time"]
for i in range(3):
    label = tk.Label(inputframe, text=names[i], font=("Helvetica Bold", 12))
    label.grid(row=1, column=i)

for i in range(5):
    arrival_entry = tk.Entry(inputframe, width=10, font=("Helvetica", 12))
    arrival_entry.grid(row=i+2, column=1)
    arrival_entries.append(arrival_entry)
    
    burst_entry = tk.Entry(inputframe, width=10, font=("Helvetica", 12))
    burst_entry.grid(row=i+2, column=2)
    burst_entries.append(burst_entry)

    processid_entry = tk.Entry(inputframe, width=10, font=("Helvetica", 12))
    processid_entry.grid(row=i+2, column=0)
    processid_entries.append(processid_entry)

inputbtn = tk.Button(result_frame2, text="Input", font=("Helvetica Bold", 12),width=10,bg="purple",fg="white",command=calculate)
inputbtn.grid(column=1, row=2)

result_frame = tk.Frame(win)
result_frame.grid(column=1, row=0)

win.mainloop()

