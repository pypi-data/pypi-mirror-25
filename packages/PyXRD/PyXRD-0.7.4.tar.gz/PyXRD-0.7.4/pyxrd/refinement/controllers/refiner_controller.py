# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

from pyxrd.generic.controllers.dialog_controller import DialogController
from pyxrd.refinement.parspace import ParameterSpaceGenerator

class RefinerController(DialogController):
    """
        A controller for a Refiner object that keeps track
        of the solutions and residuals generated by the refinement
        algorithm. This allows to show a nice dialog with the end
        results and some graphs about the parameter space.
    """

    auto_adapt_excluded = [
        "refine_method_index",
        "refinables",
        "make_psp_plots",
    ]

    register_lazy = False
    samples = None

    def __init__(self, refiner, *args, **kwargs):
        super(RefinerController, self).__init__(*args, **kwargs)
        self.refiner = refiner

    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_cancel(self):
        self.view.hide()
        self.parent.parent.view.parent.show()

    def on_btn_initial_clicked(self, event):
        self.refiner.apply_initial_solution()
        del self.refiner
        self.on_cancel()
        return True

    def on_btn_best_clicked(self, event):
        self.refiner.apply_best_solution()
        del self.refiner
        self.on_cancel()
        return True

    def on_btn_last_clicked(self, event):
        self.refiner.apply_last_solution()
        del self.refiner
        self.on_cancel()
        return True

    # ------------------------------------------------------------
    #      Methods & Functions
    # ------------------------------------------------------------
    def update_labels(self):
        self.view.update_labels(
            self.refiner.history.initial_residual,
            self.refiner.history.best_residual,
            self.refiner.history.last_residual,
        )
    
    def generate_images(self, output_dir="", density=200):
        """
            Generate the parameter space plots
        """
        samples = self.refiner.get_plot_samples()
        labels = self.refiner.get_plot_labels()
        truths = self.refiner.history.best_solution
       
        psg = ParameterSpaceGenerator()
        psg.initialize(self.refiner.ranges, 199)
        for sample in samples:
            psg.record(sample[:-1], sample[-1])
        psg.plot_images(self.view.figure, truths, labels[:-1])

    def clear_images(self):
        self.view.figure.clear()
        self.view.figure.text(0.5, 0.5, "no plots to show", va="center", ha="center")

    pass # end of class