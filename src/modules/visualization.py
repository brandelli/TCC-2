import matplotlib.pyplot as plt
import numpy as np
class Visualization:

    def teste(self):
        columns = ('Last', 'High', 'Low', 'Chg.', 'Chg. %', 'Time', 'T?')
        rows = ['Gold', 'Silver', 'Copper', 'Aluminum']

        data_list = np.random.randint(10,90, size=(len(rows), len(columns)))
        scatter_x = (1, 2, 3)
        scatter_y = (1224.53, 1231.76, 1228.70)

        fig = plt.figure(1)
        fig.subplots_adjust(left=0.2,top=0.8, wspace=1)

        #Table - Main table
        ax = plt.subplot2grid((4,3), (0,0), colspan=2, rowspan=2)
        ax.table(cellText=data_list,
                rowLabels=rows,
                colLabels=columns, loc="upper center")

        ax.axis("off")

        #Gold Scatter - Small scatter to the right
        plt.subplot2grid((4,3), (0,2))
        plt.scatter(scatter_x, scatter_y)
        plt.ylabel('Gold Last')

        fig.set_size_inches(w=6, h=5)
        plt.show()