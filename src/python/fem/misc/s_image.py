# TODO

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import serialize
from PIL import Image

filename = 'my_plot'

fig = Figure()
FigureCanvas(fig)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3])
ax.set_title('TODO')
ax.grid(True)
ax.set_xlabel('TODO')
ax.set_ylabel('TODO')
fig.savefig(filename)


im = Image.open('/Users/ashraov/projects/study/diploma/src/python/fem/misc/my_plot.png')
tmp = serialize(im)

#new_im = deserialize(im)


#file = open('data.pkl', 'rb')


#print image
#file.close()
