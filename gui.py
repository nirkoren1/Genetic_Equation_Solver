import solver
import tkinter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# plot variables
iteration = 0
plot_best = 20
pause = True


# tkinter and plt init
root = tkinter.Tk()
root.geometry('1200x700+200+100')
root.title('Evolution equation solver')
root.state('zoomed')
background = '#fafafa'
root.config(background=background)
plt.style.use('fivethirtyeight')


# Buttons
solve_btn = tkinter.Button(root, text='SOLVE!', command=lambda: solve_ani(), font=("Helvetica", 16)).place(x=920, y=40)
zoom_btn = tkinter.Button(root, text='Zoom(min/max)', command=lambda: zoom_func(), font=("Helvetica", 16)).place(x=900, y=850)
pause_btn = tkinter.Button(root, text='Pause', command=lambda: pause_func(), font=("Helvetica", 16)).place(x=850, y=250)
resume_btn = tkinter.Button(root, text='Resume', command=lambda: resume_func(), font=("Helvetica", 16)).place(x=980, y=250)


# Labels
dashboard_text = tkinter.StringVar()
dashboard = tkinter.Label(root, textvariable=dashboard_text, bg=background, font=("Helvetica", 16))
dashboard.place(x=1300, y=30)
target_lb = tkinter.Label(root, text="Target/Equation", bg=background, font=("Helvetica", 25))
cross_over_rate_lb = tkinter.Label(root, text="Cross Over Rate", bg=background, font=("Helvetica", 16))
mutation_rate_lb = tkinter.Label(root, text="Mutation Rate", bg=background, font=("Helvetica", 16))
elitism_lb = tkinter.Label(root, text="Elitism(True/False)", bg=background, font=("Helvetica", 16))
elitism_group_lb = tkinter.Label(root, text="Elitism Group(must be even number)", bg=background, font=("Helvetica", 16))
population_lb = tkinter.Label(root, text="Population(must be even number)", bg=background, font=("Helvetica", 16))
generations_lb = tkinter.Label(root, text="Generations", bg=background, font=("Helvetica", 16))
plot_best_lb = tkinter.Label(root, text="Plot Best", bg=background, font=("Helvetica", 16))
tournament_group_lb = tkinter.Label(root, text="Tournament Group", bg=background, font=("Helvetica", 16))
labels_lst = [population_lb, cross_over_rate_lb, mutation_rate_lb, elitism_lb, elitism_group_lb, generations_lb, tournament_group_lb, plot_best_lb]


# Entries
bd_en = 2
width_en = 10
target_en = tkinter.Entry(root, bd=bd_en, width=37, font=("Helvetica", 16))
cross_over_rate_en = tkinter.Entry(root, bd=bd_en, font=("Helvetica", 16), width=width_en)
mutation_rate_en = tkinter.Entry(root, bd=bd_en, font=("Helvetica", 16), width=width_en)
elitism_en = tkinter.Entry(root, bd=bd_en, font=("Helvetica", 16), width=width_en)
elitism_group_en = tkinter.Entry(root, bd=bd_en, font=("Helvetica", 16), width=width_en)
population_en = tkinter.Entry(root, bd=bd_en, font=("Helvetica", 16), width=width_en)
generations_en = tkinter.Entry(root, bd=bd_en, font=("Helvetica", 16), width=width_en)
plot_best_en = tkinter.Entry(root, bd=bd_en, font=("Helvetica", 16), width=width_en)
tournament_group_en = tkinter.Entry(root, bd=bd_en, font=("Helvetica", 16), width=width_en)
zoom_en = tkinter.Entry(root, bd=bd_en, font=("Helvetica", 16), width=13)
entries_lst = [population_en, cross_over_rate_en, mutation_rate_en, elitism_en, elitism_group_en, generations_en, tournament_group_en, plot_best_en]
target_en.insert(0, solver.target)
cross_over_rate_en.insert(0, solver.cross_over_rate)
mutation_rate_en.insert(0, solver.mutation_rate)
elitism_en.insert(0, str(solver.elitism))
elitism_group_en.insert(0, solver.elitism_group)
population_en.insert(0, solver.population)
generations_en.insert(0, solver.iterations)
plot_best_en.insert(0, plot_best)
tournament_group_en.insert(0, solver.tournament_group)
zoom_en.insert(0, '-5000/5000')


# Placing entries and labels
target_en.place(x=900-150, y=190)
target_lb.place(x=850, y=120)
zoom_en.place(x=900, y=900)
x_labels = 900
y_labels = 350
y = 0
for lb in range(len(labels_lst)):
    labels_lst[lb].place(x=x_labels, y=y+y_labels)
    entries_lst[lb].place(x=x_labels-150, y=y+y_labels)
    y += 60

# fig 1
xar = []
yar = []
fig1 = plt.figure(figsize=(6, 4.5), dpi=100)
ax1 = fig1.add_subplot(1, 1, 1)
ax1.set_ylim(0, 110)
ax1.set_title('Accuracy/Fitness')
line, = ax1.plot(xar, yar, 'r', marker='o')


# fig 2
xar2 = []
yar2 = []
color_map = []
fig2 = plt.figure(figsize=(6, 4.5), dpi=100)
ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_xlim(-5000, 5000)
ax2.set_ylim(0, solver.iterations)
ax2.set_title('Offsprings')
scatter = ax2.scatter(xar2, yar2, c=color_map, cmap='viridis', vmin=98.2, vmax=100)


# solve function
def solve_ani():
    global pause, plot_best, xar2, xar, yar, yar2, iteration, color_map
    pause = True
    iteration = 0
    xar = []
    xar2 = []
    yar = []
    yar2 = []
    color_map = []
    solver.current_gen = []
    solver.next_gen = []
    solver.fitness_lst = []
    solver.target = target_en.get()
    solver.iterations = int(generations_en.get())
    solver.population = int(population_en.get())
    solver.mutation_rate = float(mutation_rate_en.get())
    solver.cross_over_rate = float(cross_over_rate_en.get())
    solver.elitism_group = int(elitism_group_en.get())
    solver.tournament_group = int(tournament_group_en.get())
    plot_best = int(plot_best_en.get())
    if elitism_en.get() == 'True':
        solver.elitism = True
    else:
        solver.elitism = False
    if not check_errors():
        ax2.set_ylim(0, solver.iterations)
        init_solver()
        pause = False


# checking the input parameter for errors
def check_errors():
    if solver.population < solver.tournament_group:
        popupmsg("population must be bigger than tournament group")
        return True
    if solver.population < plot_best:
        popupmsg("population must be bigger than plot best")
        return True
    if solver.population < solver.elitism_group:
        popupmsg("population must be bigger than elitism group")
        return True
    if solver.population < 1:
        popupmsg("population must be bigger than 1")
        return True
    if solver.population % 2 == 1:
        popupmsg("population must be an even number")
        return True
    if solver.elitism is True and solver.elitism_group < 2:
        popupmsg("elitism group must be bigger than 1")
        return True
    if solver.elitism_group % 2 == 1 and solver.elitism is True:
        popupmsg("elitism group must be an even number")
        return True
    if len(solver.target) < 3:
        popupmsg("target length must br bigger than 2")
        return True
    if '=' not in solver.target:
        popupmsg("'=' must be in target")
        return True
    if 'x' not in solver.target:
        popupmsg("'x' must be in target")
        return True
    if solver.iterations < 3:
        popupmsg("generations must be bigger than 2")
        return True
    return False


# pop up msg if error is raised
def popupmsg(msg):
    popup = tkinter.Tk()
    popup.wm_title("!")
    label = tkinter.Label(popup, text=msg, font=("Helvetica", 16))
    label.pack(side="top", fill="x", pady=10)
    b1 = tkinter.Button(popup, text="Okay", command=popup.destroy)
    b1.pack()
    popup.mainloop()


# zooming by Min/Max values
def zoom_func():
    values = zoom_en.get().split('/')
    min_val, max_val = int(values[0]), int(values[1])
    ax2.set_xlim(min_val, max_val)


def pause_func():
    global pause
    pause = True


def resume_func():
    global pause
    pause = False


# initiating the solver
def init_solver():
    global yar2, xar2, color_map
    solver.init_gen_0()
    solver.fitness_update()
    yar.append(max(solver.fitness_lst))
    xar.append(iteration)
    yar2 += [0] + [0 for i in range(plot_best)]
    xar2 += [-1] + list(map(solver.binary32bit_to_float, [solver.current_gen[g] for g in np.argsort(solver.fitness_lst)]))[-plot_best:]
    color_map += [0] + sorted(solver.fitness_lst)[-1*plot_best:]


# animation of accuracy fig
def animate1(i):
    global iteration, yar2, xar2, color_map, dashboard_text, pause
    if not pause and iteration < solver.iterations:
        iteration += 1
        solver.create_new_gen()
        solver.fitness_update()
        yar.append(max(solver.fitness_lst))
        xar.append(iteration + 1)
        yar2 += [iteration for i in range(plot_best)]
        xar2 += list(map(solver.binary32bit_to_float, [solver.current_gen[g] for g in np.argsort(solver.fitness_lst)]))[-plot_best:]
        color_map += sorted(solver.fitness_lst)[-1*plot_best:]
        txt = ''
        for i in range(plot_best):
            txt += str(color_map[-(i+1)])[:6] + "  " + str(xar2[-(i+1)])[:10] + "  " + str(solver.current_gen[np.argsort(solver.fitness_lst)[-(i+1)]]) + '\n' + '\n'
        dashboard_text.set(txt)
        line.set_data(xar, yar)
        ax1.set_xlim(-10, iteration + 10)
        if iteration >= solver.iterations:
            pause = True


# animation of offsprings fig
def animate2(i):
    global iteration, yar2, xar2, color_map
    if not pause and iteration < solver.iterations:
        try:
            scatter.set_offsets(np.c_[xar2, yar2])
            scatter.set_array(np.array(color_map))
        except OverflowError:
            xar2 = xar2[:-plot_best]
            yar2 = yar2[:-plot_best]
            color_map = color_map[:-plot_best]


# closing the program function
def on_close():
    root.destroy()
    exit(0)


root.protocol("WM_DELETE_WINDOW", on_close)


plotcanvas = FigureCanvasTkAgg(fig1, root)
plotcanvas2 = FigureCanvasTkAgg(fig2, root)
plotcanvas.get_tk_widget().place(x=50, y=30)
plotcanvas2.get_tk_widget().place(x=50, y=530)
ani = animation.FuncAnimation(fig1, animate1, interval=10, blit=False)
ani2 = animation.FuncAnimation(fig2, animate2, interval=10, blit=False, repeat=True, frames=2)

root.mainloop()
