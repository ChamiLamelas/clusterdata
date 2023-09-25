import plot
import metrics
import data
import timing

def main():
    t = timing.MyTimer()
    t.start("compute and plot availability")
    availability = metrics.get_availability(data.load_tasks())
    plot.plot_availability(availability)
    t.stop()

if __name__ == '__main__':
    main()