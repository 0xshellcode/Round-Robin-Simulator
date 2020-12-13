import matplotlib.pyplot as plt
from tkinter import messagebox
import tkinter as tk
from tkinter import *
import random
import time

# For Testing
# queue = [16, 10, 12, 8]
# processIDs = [1, 2, 3, 4]
# quantum = 7


# For Testing 2
# queue = [10, 5, 8]
# quantum = 2
# processIDs = [1, 2, 3]
# burstTime = []

# Real
queue = []
burstTime = []
processIDs = []
quantum = 0
noProcesses = 0


# Function to find the waiting time
# for all processIDs
def findWaitingTime(processIDs, noProcesses, burstTime,
                    waitingTime, quantum):
    remainingBurstTime = [0] * noProcesses

    # Copy the burst time into remaining burst time[]
    for i in range(noProcesses):
        remainingBurstTime[i] = burstTime[i]
    time = 0  # Current time

    while(1):
        done = True

        # Traverse all processIDs one by
        # one repeatedly
        for i in range(noProcesses):

            # If remaining burst time of a process is greater
            # than 0 then only need to process further
            if (remainingBurstTime[i] > 0):
                done = False  # This process is not over

                if (remainingBurstTime[i] > quantum):

                    time += quantum

                    # Decrease the burst_time of current
                    # process by quantum
                    remainingBurstTime[i] -= quantum

                else:


                    time += remainingBurstTime[i]

                    # Waiting time is current time minus
                    # time used by this process
                    waitingTime[i] = time - burstTime[i]

                    # As the process gets fully executed
                    # make its remaining burst time = 0
                    remainingBurstTime[i] = 0

        # If all processIDs are done
        if (done == True):
            break

# Function to calculate turn around time


def findTurnAroundTime(processIDs, noProcesses, burstTime, waitingTime, turnaroundTime):

    # Calculating turnaround time
    for i in range(noProcesses):
        turnaroundTime[i] = burstTime[i] + waitingTime[i]


# Function to calculate average waiting
# and turn-around times.
def findavgTime(processIDs, noProcesses, burstTime, quantum):

    # Here we declare the size of these lists based on the value in the number of processes

    waitingTime = [0] * noProcesses
    turnaroundTime = [0] * noProcesses

    # Function to find waiting time
    # of all processIDs
    findWaitingTime(processIDs, noProcesses, burstTime,
                    waitingTime, quantum)

    # Function to find turn around time
    # for all processIDs
    findTurnAroundTime(processIDs, noProcesses, burstTime,
                       waitingTime, turnaroundTime)
    totalWaitingTime = 0
    totalTurnaroundTime = 0
    for i in range(noProcesses):

        totalWaitingTime = totalWaitingTime + waitingTime[i]
        totalTurnaroundTime = totalTurnaroundTime + turnaroundTime[i]

    data = [processIDs, burstTime, waitingTime, turnaroundTime]
    fig, axs = plt.subplots()
    rowLabels = ("Process ID", "Burst Time", "Waiting Time", "Turn-Around Time")
    fig.patch.set_visible(False)
    axs.axis('off')
    axs.axis('tight')
    axs.table(cellText=data, rowLabels=rowLabels,
              rowLoc='center', loc='center')
    plt.title("\nRound Robin\n")
    avgWaTime = "\nAverage waiting time = %.2f " % (
        totalWaitingTime / noProcesses)
    plt.gcf().text(0.02, 0.7, avgWaTime, fontsize=12)
    avgTurTime = "Average turn around time = %.2f " % (
        totalTurnaroundTime / noProcesses)
    plt.gcf().text(0.02, 0.65, avgTurTime, fontsize=12)
    fig.tight_layout()
    plt.show()


# Input Validation
def onlyNumbers(input):
    return input.isdigit()

# Quantum
def setQuantum():
    window = tk.Tk()
    window.title('Set Time Quantum')
    window.geometry('350x50')
    window.resizable(0, 0)
    validation = window.register(onlyNumbers)

    myEntry = Entry(window, show=None, font=('Arial', 14),  justify=tk.CENTER)
    myEntry.config(validate="key", validatecommand=(validation, '%P'))
    myEntry.pack()

    def getEntry():
        entry = myEntry.get()
        global quantum
        quantum = int(entry)
        messagebox.showinfo("Information", "Quatum Saved")
        quantumLabel = Label(frame, justify=CENTER, text=f"Quantum is: {quantum}", bg="#020202", foreground="red").pack(side=TOP, anchor=NW)
        window.destroy()

    # Buttons
    setQuatumScheduler = tk.Button(
        window, text="Ok", padx=10, pady=5, fg="white", bg="#263D42", command=getEntry)
    setQuatumScheduler.pack()

def schedulerAnimation():

    if (quantum <= 0):
        messagebox.showerror(
            "Error", "You must enter the quantum for the processes")
        pass
    else:
        counter = 0
        counterText = StringVar()
        counterText.set(counter)
        labelRunning = Label(frame, justify=CENTER, text="Running Please Wait", bg="#020202", foreground="red").pack(side=BOTTOM, anchor=NW)
        programcounterLabel = Label(frame, justify=CENTER, text="PC: ", bg="#020202", foreground="red").pack(side=TOP, anchor=NW)
        programCounter = Label(frame, justify=CENTER, textvariable=counterText, bg="#020202", foreground="red").pack(side=TOP, anchor=NW)
        global burstTime
        for i in queue:
            burstTime.append(i)
        global noProcesses
        noProcesses = len(burstTime)
        while len(queue) != 0: # Check if the queue is empty or not
            takenProcess = queue.pop(0) # Take out the first process of the queue based on the data strucuture FIFO
            burstCPU = takenProcess - quantum # The subtraction is made between the burst time of the current process and the quantum
            if burstCPU > 0: # Check if he still has burst time left in the process that has just been executed
                queue.append(burstCPU) # The condition is met, then the process returns to the queue
                label = Label(frame, justify=CENTER, text=queue,
                              bg="#020202", foreground="green").pack(side="top")
            elif burstCPU <= 0:
                print("Process completed") # Otherwise the process will not be added to the queue
                label = Label(frame, justify=CENTER, text=queue,
                        bg="#020202", foreground="green").pack(side="top")
            counter += 1
            frame.update()
            time.sleep(1)
            #print(counter)
            counterText.set(counter)
        label = Label(frame, justify=CENTER,
                      text="All processes have been completed", bg="#020202", foreground="red").pack(side=TOP)

def randomProcess(queueText, processText):
    global queue
    global processIDs
    if (len(queue) <= 0):
        processLabel = Label(frame, justify=CENTER, text="Processes IDs", bg="#020202", foreground="green").pack(side=TOP)
        label = Label(frame, justify=CENTER, textvariable=processText,
                      bg="#020202", foreground="green").pack(side=TOP)
        burstTimeLabel = Label(frame, justify=CENTER, text="Burts Time", bg="#020202", foreground="green").pack(side=TOP)
        label = Label(frame, justify=CENTER, textvariable=queueText,
                      bg="#020202", foreground="green").pack(side=TOP)
        queue.append(random.randint(1, 15))
        if len(processIDs) <= 0:
            processIDs.append(1)
        else:
            processIDs.append(processIDs[-1] + 1)
        queueText.set(queue)
        processText.set(processIDs)
        messagebox.showinfo("Information", "Process Saved")
    else:
        queue.append(random.randint(1, 26))
        if len(processIDs) <= 0:
            processIDs.append(1)
        else:
            processIDs.append(processIDs[-1] + 1)
        queueText.set(queue)
        processText.set(processIDs)
        messagebox.showinfo("Information", "Process Saved")

root = tk.Tk()

queueText = StringVar()
processText = StringVar()

# Custom Size
canvas = tk.Canvas(root, height=700, width=700, bg="#000000")
canvas.pack()

# Framw inside root
frame = LabelFrame(root, text="Main", bg="#020202", foreground="green")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

root.title('Round Robin Simulator')
root.geometry("700x700")
root.resizable(0, 0)

# Main Menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Set Quantum", command=setQuantum)
filemenu.add_command(label="Generate Process", command=lambda: randomProcess(queueText, processText))
filemenu.add_command(label="Run Scheduler", command=schedulerAnimation)
filemenu.add_command(label="Turnaround Time & Waiting Time", command=lambda: findavgTime(
    processIDs, noProcesses, burstTime, quantum))

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Actions", menu=filemenu)


root.config(menu=menubar)
root.mainloop()
