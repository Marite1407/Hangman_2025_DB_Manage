from controllers.Controller import Controller
from models.Model import Model
from views.View import View

if __name__ == '__main__':
    model = Model()
    view = View(model, None)  # Alguses paneme None, sest controllerit pole veel loodud
    controller = Controller(model, view)  # Loome kontrolleri

    # Seome kontrolleri View klassi sisse
    view.controller = controller

    view.mainloop()  # Käivitame GUI
