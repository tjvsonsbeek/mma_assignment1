# Multimedia Analytics: PyQT6 Demo

This is a demo for the usage of PyQT6 for making interactive data analytics dashboards. It should give you an idea of the options and capabilities of PyQT6. It also shows the general workflow that should be used to get an effective workflow and flow of information between the widgets. 


## Demo

This dashboard is designed to provide data analysis of UMAP embeddings of the birds dataset. The main components of the dashboard are as follows:

1. **(left) UMAP Scatterplot**: On the left side of the dashboard, there is a scatterplot that displays a UMAP embedding of a portion of the birds dataset. UMAP is a dimensionality reduction technique used to visualize high-dimensional data in lower dimensions. The scatterplot allows you to explore the relationships and clusters within the dataset.

1. **(left) Selection with Mouse**: By using left and right mouse clicks, the user can select a rectangular area within the UMAP scatterplot. This selection defines a subset of points in the dataset. 

2. **(right) Wordcloud Generation**: Once a selection is made, a word cloud is dynamically generated based on the selected subset. The word cloud visually represents the frequency of words associated with the selected data points. The size of each word in the cloud indicates its occurrence frequency.

3. **(middle) Buttons**: In the middle of the dashboard, there are buttons displaying the top occurring associated tags. These tags are derived from the dataset and represent common attributes or labels associated with the data points. By selecting a button, the points corresponding to that specific tag will change color in the scatterplot, allowing for a visual differentiation of different categories or groups within the dataset.

5. **(bottom )Image Sample**: At the bottom of the plot, a sample of images is displayed. This sample consists of a random selection of images from the subset of points that were selected in the UMAP scatterplot and/or the button selection. It provides a visual representation of the data points associated with the selected area.

Overall, this dashboard provides an interactive and informative interface for exploring the UMAP embeddings of the birds dataset. Users can visually analyze the clusters, generate word clouds based on selections, highlight specific tag categories, and view corresponding images to gain insights and understanding of the dataset.


## Instructions 

1. Create a python environment using the 'requirements.txt' file
2. Prepare one of the datasets through the dataloading scripts/adapt it for your own dataset/download it from here: https://amsuni-my.sharepoint.com/:f:/g/personal/t_j_vansonsbeek_uva_nl/EutCd4e9a9hEpEFZUzU7tiAB1be1dou-bRA2gl_dSFhvsQ
4. Define the locations of the dataset, the .pkl file and the .h5 file in config.ini
5. Run the dashboard with the following command: "python main_window.py"
6. Tip: if you get the following output and images don't show: 'pixmap is a null pixmap', the path to the images of you dataset is incorrect. 

**Note** In case you get the following error while installing on ubuntu ```qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
Available platform plugins are: minimalegl, offscreen, eglfs, vnc, wayland, wayland-egl, minimal, vkkhrdisplay, linuxfb, xcb.``` 

then run ```sudo apt install libxcb-cursor0```

## PyQt Basics

The following sources are usefull to get acquanted with pyqt 

https://www.pythonguis.com/pyqt6-tutorial/ 
https://www.riverbankcomputing.com/static/Docs/PyQt6/

When designing a PyQt6 dashboard, the general approach consists of three steps: defining widgets, connecting widgets, and setting the dashboard layout. 

### Define Widgets

In PyQt6, widgets are the building blocks of the GUI. They are the elements that users interact with, such as buttons, text boxes, labels, plots, wordclouds, etc. To define widgets in PyQt, you typically create instances of a specific widget class provided by the PyQt. 

For example, to create a button widget, you can use the `QPushButton` class:

`button = QPushButton("Click me")`

Here, we create a button widget with the label "Click me."

### Connect Widgets

Signals and slots are used to enable communication between widgets in a PyQt dashboard. A signal is an event or a piece of data emitted by a widget, and a slot is a function that receives and processes the signal.

To connect widgets, you typically define custom slots and connect them to the appropriate signals using the `connect` method. PyQt provides a wide range of predefined signals and slots for common interactions.

For example, to connect a button's clicked signal to a custom slot called `handle_button_click`, you can do the following:

pythonCopy code

`button.clicked.connect(handle_button_click)`

Here, `handle_button_click` is a function defined in another widget that prompts the desired action. 
Signals and slots allow widgets to communicate and respond to user actions or changes in data. They form the foundation for interactivity in PyQt applications.

### Set Dashboard Layout

Once you have defined the widgets and connected them appropriately, you need to arrange them in a layout that determines their position and sizing within the dashboard. 

To set the dashboard layout, you typically create an instance of a layout class, add your widgets to it, and then set the layout on the main window or container widget.

For example, to create a vertical layout and add a button and a text box to it:

`layout = QVBoxLayout()`
`layout.addWidget(button)`
`layout.addWidget(textbox)`

Here, we create a vertical layout, add the button and textbox widgets to it, and stack them vertically.

Finally, you set the layout on the main window or container widget using the `setLayout` method:

`window.setLayout(layout)`

This assigns the layout to the window, ensuring that the widgets are displayed according to the specified layout.
