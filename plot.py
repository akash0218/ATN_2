import matplotlib.pyplot as plt


class Plot:
    def plot(self, x, y):
        plt.plot(x, y, marker='o')
        plt.xlabel('p-values')
        plt.ylabel('Reliability-values')
        plt.title('p vs Reliability plot')
        plt.show()

