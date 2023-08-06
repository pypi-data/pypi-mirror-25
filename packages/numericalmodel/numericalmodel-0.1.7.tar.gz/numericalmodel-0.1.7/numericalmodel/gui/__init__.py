#!/usr/bin/env python3
# system modules
import os, sys, time, re
import hashlib
import logging
import signal
import textwrap
from pkg_resources import resource_filename

# internal modules
from .. import utils
from ..numericalmodel import NumericalModel

# external modules
import numpy as np


instructions = textwrap.dedent("""
To install the prerequisites, use your system's package manager and install
``python3-gi`` (might also be called ``pygobject3``) and ``libffi``.

On Debian/Ubuntu:

.. code:: sh

    sudo apt-get install python3-gi libcffi6 libffi-dev

.. note:: If you don't have system privileges, there is also the (experimental)
    :mod:`pgi` module on `PyPi <https://pypi.python.org/pypi/pgi/>`_ that you
    can install via::

        pip3 install --user pgi

    Theoretically, the :any:`NumericalModelGui` might work with this package as
    well, but no guarantees...

.. warning::

    If you are using `Anaconda <https://conda.io/docs/index.html>`_ you will
    **NOT** have fun trying to install Gtk. It seems to be pretty impossible
    unfortunately...

Then, install :mod:`numericalmodel` with the ``gui`` feature:

.. code:: sh

    pip3 install --user 'numericalmodel[gui]'

""")

__doc__ = \
"""
Graphical user interface for a NumericalModel. This module is only useful
if the system package ``python3-gi`` is installed to provide the :mod:`gi`
module.

""" + instructions

PGI = False
GTK_INSTALLED = False
try: # try real gi module
    import gi
    gi.require_version('Gtk','3.0')
    from gi.repository import Gtk,Gdk,GLib
    GTK_INSTALLED = True # importing real gi worked
except: # importing real gi didn't work
    logging.info("no 'gi' module found")
    try: # try pgi package
        import pgi
        pgi.install_as_gi()
        import gi
        gi.require_version('Gtk','3.0')
        from gi.repository import Gtk
        from gi.repository import GLib
        PGI = True
        GTK_INSTALLED = True # importing pgi worked
        logging.warning("using 'pgi' module instead of 'gi'")
    except:
        logging.error("Neither 'pgi' nor 'gi' module found!"
            "The GUI will not work.")

from matplotlib.figure import Figure
try:
    from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg \
        as FigureCanvas
except:
    logging.error("matplotlib seems to not have a working Gtk3 backend. "
        "The GUI will not work.")


MODEL_CONTENT = ["variables","forcing","parameters","observations"]

def string2color(string):
    """
    Convert a string to a hex HTML color string

    Args:
        string (str): the string to use

    Returns:
        string : an HTML color string (e.g. #34df12)
    """
    return "#" + hashlib.md5(string.encode("utf-8")).hexdigest()[:6]

# only if gtk is installed
class NumericalModelGui(utils.LoggerObject):
    """
    class for a GTK gui to run a :any:`NumericalModel` interactively

    Args:
        numericalmodel (NumericalModel): the NumericalModel to run
    """
    def __init__(self, numericalmodel):
        # check for GTK
        if not GTK_INSTALLED:
            logging.error("Gtk3.0 bindings seem not installed.\n"+instructions)
            sys.exit()

        self.setup_signals(
            signals = [signal.SIGINT, signal.SIGTERM, signal.SIGHUP],
            handler = self.quit
        )

        self.DRAGTARGETS = Gtk.TargetList.new([])
        self.DRAGTARGETS.add_text_targets(80)

        self.model = numericalmodel

    ##################
    ### Properties ###
    ##################
    @property
    def model(self):
        """
        The :any:`NumericalModel` behind the gui

        :type: :any:`NumericalModel`
        """
        try:
            return self._model
        except AttributeError:
            self._model = NumericalModel()
        return self._model

    @model.setter
    def model(self, newmodel):
        assert isinstance(newmodel,NumericalModel)
        self._model = newmodel

    @property
    def builder(self):
        """
        The gui's :code:`GtkBuilder`. This is a read-only property.

        :getter: Return the :class:`GtkBuilder`, load the :any:`gladefile` if
            necessary.
        :type: :class:`GtkBuilder`
        """
        try:
            self._builder
        except AttributeError:
            self._builder = Gtk.Builder() # new builder
            # load the gladefile
            self._builder.add_from_file( self.gladefile )
        return self._builder

    @property
    def gladefile(self):
        """
        The gui's Glade file. This is a read-only property.

        :type: :any:`str`
        """
        return resource_filename(__name__, "gui.glade")

    @property
    def figures(self):
        """
        The gui's :any:`matplotlib.figure.Figure` for plotting

        :type: :any:`dict` of :any:`matplotlib.figure.Figure`
        :getter: returns the gui's :any:`matplotlib.figure.Figure`, create one
            if necessary
        """
        try:
            self._figures
        except AttributeError:
            self._figures = {}
            for n in MODEL_CONTENT:
                self._figures[n] = Figure(tight_layout=True)
        return self._figures

    @property
    def figures_content(self):
        """
        The :any:`figures` ' content as abstract dict

        :type: :any:`dict` of :any:`str`
        :getter: returns the :any:`figures` ' current content template, create
            new template if none was set yet
        :setter: sets the :any:`figures` ' content template and reloads the
            current plot. Resets the content template if set to ``None``.
        """
        try:
            self._figures_content
        except AttributeError:
            # default figure content
            self._figures_content = {}
            for tab in MODEL_CONTENT:
                self._figures_content[tab] = {}
                self._figures_content[tab][tab]= \
                    {k:v for k,v in getattr(self.model,tab).items()}
        return self._figures_content

    @figures_content.setter
    def figures_content(self, newcontent):
        if newcontent is None:
            del self._figures_content
        else:
            assert hasattr(newcontent,"items")
            self._figures_content = newcontent
        # changing the figures' content means replotting
        self.update_current_plot()

    @property
    def scales(self):
        """
        The :class:`GtkScale` used to manipulate model data

        :type: :any:`dict` of :class:`GtkScale`
        :getter: return the gui's :class:`GtkScale`, create new if necessary
        """
        try:
            self._scales
        except AttributeError:
            self._scales = {}
            for attr in MODEL_CONTENT:
                self._scales[attr] = {}
                grid = Gtk.Grid()
                grid.props.hexpand = True
                grid.props.column_spacing = 10
                grid.props.row_spacing = 5
                i = 0
                for ivid,iv in sorted(getattr(self.model,attr).items()):
                    self._scales[attr][ivid] = {}
                    self._scales[attr][ivid]["initial"] = iv.value
                    bounds = iv.bounds
                    if np.isfinite(bounds).all():
                        pass
                    elif np.isfinite(bounds[0]):
                        bounds[1] = max(max(bounds[0],iv.value),1) * 2
                    elif np.isfinite(bounds[1]):
                        bounds[0] = - max(max(bounds[1],iv.value),1) * 2
                    else:
                        bounds = [-2*abs(min(iv.values)),2*abs(max(iv.values))]
                    DIGITS = 3
                    adj = Gtk.Adjustment(
                        value = iv.value,lower = bounds[0], upper = bounds[1],
                        step_increment = 10**(-DIGITS))
                    scale = Gtk.Scale(
                        orientation=Gtk.Orientation.HORIZONTAL,adjustment=adj)
                    scale.get_adjustment().set_value(iv.value)
                    scale.props.draw_value = False
                    scale.props.digits = 3
                    scale.props.hexpand = True
                    scale.add_mark(self._scales[attr][ivid]["initial"],
                        Gtk.PositionType.TOP,None)
                    spinbutton = Gtk.SpinButton.new(
                        scale.get_adjustment(),
                        climb_rate=scale.get_adjustment().get_step_increment(),
                        digits = scale.props.digits
                        )
                    eventbox = Gtk.EventBox()
                    namelabel = Gtk.Label(ivid)
                    namelabel.set_alignment(1,0.5)

                    eventbox.drag_source_set(
                        Gdk.ModifierType.BUTTON1_MASK,
                        [],
                        Gdk.DragAction.COPY
                        )
                    eventbox.drag_source_set_target_list(self.DRAGTARGETS)
                    def on_drag_get(widget, context, data,info,time,*args):
                        modelpart, ivid = args
                        string = "{}:::{}".format(modelpart,ivid)
                        data.set_text(string,len(string))
                    eventbox.connect("drag-data-get",on_drag_get,attr,ivid)
                    eventbox.add(namelabel)
                    unitlabel = Gtk.Label(iv.unit)
                    unitlabel.set_alignment(0,0.5)
                    for w in [unitlabel,scale]:
                        w.set_tooltip_markup("<b>{}</b>\nDrag'n'Drop the name "
                            "<b>{}</b> onto the plot area to add it".format(
                            iv.name,ivid))
                    for w in [namelabel]:
                        w.set_tooltip_markup("<b>{}</b>\nDrag'n'Drop this "
                            "onto the plot area to add it".format(iv.name))

                    grid.attach(scale,1,i,1,1)
                    grid.attach_next_to(
                        eventbox,scale,Gtk.PositionType.LEFT,1,1)
                    grid.attach_next_to(
                        spinbutton,scale,Gtk.PositionType.RIGHT,1,1)
                    grid.attach_next_to(
                        unitlabel,spinbutton,Gtk.PositionType.RIGHT,1,1)
                    self._scales[attr][ivid]["scale"] = scale
                    i += 1
                self._scales[attr]["grid"] = grid
        return self._scales

    ###############
    ### Methods ###
    ###############
    def setup_signals(self, signals, handler):
        """
        This is a workaround to signal.signal(signal, handler)
        which does not work with a ``GLib.MainLoop`` for some reason.
        Thanks to: http://stackoverflow.com/a/26457317/5433146

        Args:
            signals (list): the signals (see :any:`signal` module) to
                connect to
            handler (callable): function to be executed on these signals
        """
        def install_glib_handler(sig): # add a unix signal handler
            GLib.unix_signal_add( GLib.PRIORITY_HIGH,
                sig, # for the given signal
                handler, # on this signal, run this function
                sig # with this argument
                )

        for sig in signals: # loop over all signals
            GLib.idle_add( # 'execute'
                install_glib_handler, sig, # add a handler for this signal
                priority = GLib.PRIORITY_HIGH  )

    def plot_interfacevalues(self, interfacevalues, figure, times = None):
        """
        Plot an :any:`InterfaceValue` onto a given Figure

        Args:
            interfacevalues (list): the :any:`InterfaceValue` s to plot
            figure (matplotlib.figure.Figure): the
                :any:`matplotlib.figure.Figure` to plot onto
            times (numpy.ndarray, optional): Times to plot. If left unspecified,
                plot the times that are available.
        """
        # delete all old axes
        for ax in figure.axes:
            figure.delaxes(ax)
        units = {}
        for interfacevalue in interfacevalues:
            try:
                units[interfacevalue.unit].append(interfacevalue)
            except KeyError:
                units[interfacevalue.unit] = [interfacevalue]

        interp2drawstyle = {}
        if times is None:
            interp2drawstyle = {'linear':'default','nearest':'steps-mid',
                'zero':'steps-post',}
        i = 1
        axes = {}
        timeunit = "s"
        for unit,ivlist in sorted(units.items()):
            try:
                axes[unit]
            except KeyError:
                try:
                    axes[unit] = figure.add_subplot(len(units),1,len(units)-i+1,
                        sharex=xaxis_shared)
                except NameError:
                    axes[unit] = figure.add_subplot(len(units),1,len(units)-i+1)
                    xaxis_shared = axes[unit]
            ax = axes[unit]
            for iv in ivlist:
                if times is None:
                    x = iv.times
                    y = iv.values
                else:
                    oneday = 24 * 60 * 60
                    onehour = 60 * 60
                    oneminute = 60
                    if max(times) > oneday:
                        x = times / oneday
                        timeunit = "d"
                    elif max(times) > onehour:
                        x = times / onehour
                        timeunit = "h"
                    elif max(times) > oneminute:
                        x = times / oneminute
                        timeunit = "min"
                    else:
                        x = times
                    y = iv(times)

                plot_kwargs = {
                    "label":"{} ({})".format(iv.name,iv.id),
                    "linewidth":2,
                    "zorder":5
                    }
                if self["settings_plot_consistent_colors_checkbutton"]\
                    .get_active():
                    plot_kwargs.update({"color":string2color(iv.name+iv.id)})
                if np.array(x).size > 1:
                    plot_kwargs.update({ "drawstyle":interp2drawstyle.get(
                            iv.interpolation,"steps-post"),})
                    ax.plot( x,y, **plot_kwargs)
                else:
                    ax.scatter( x,y, **plot_kwargs)
            ax.set_ylabel("[{}]".format(unit))
            ax.tick_params(direction="in")
            ax.grid(zorder=0)
            ax.legend(fontsize="small")
            i += 1

        for unit,ax in axes.items():
            if ax == xaxis_shared:
                ax.set_xlabel("time [{}]".format(timeunit))
            else:
                ax.tick_params(bottom=True,left=True,top=True,
                    right=True,labelbottom=False,)
        figure.canvas.draw()

    def apply_data_from_settings(self,*args,**kwargs):
        """
        Read the data from the settings and feed it into the model
        """
        self.add_status("settings","Applying new data settings...")
        for what,d in self.scales.items():
            for ivid,widgets in sorted(d.items()):
                if ivid == "grid": continue
                iv = getattr(self.model,what)[ivid]
                value = widgets["scale"].get_adjustment().get_value()
                if iv.value != value:
                    try:
                        iv.next_time = iv.time + \
                            0.99 * (iv.time_function()-iv.time)
                        iv.value = iv.value
                        iv.next_time = None
                        iv.value = value
                    except Exception as e:
                        problem = "Could not update {} from {} to {}"\
                            .format(iv.id,iv.value,value)
                        self.error(main=problem,secondary="<i>{}</i>".format(e))
                        self.add_status("settings",problem,important = True)
                        logging.warning(problem)
                        value = widgets["scale"].get_adjustment().set_value(
                            iv.value)

        self.add_status("settings","New data fed into model!")

    def apply_model_data_to_settings(self,*args,**kwargs):
        """
        Read the data from the model and feed it into the settings
        """
        self.add_status("settings","Applying model data to settings...")
        for what,d in self.scales.items():
            for ivid,widgets in sorted(d.items()):
                if ivid == "grid": continue
                iv = getattr(self.model,what)[ivid]
                value = widgets["scale"].get_adjustment().set_value(iv.value)
        self.add_status("settings","Model data fed into settings!")

    def reset_scales(self, what=None):
        """
        Reset scales

        Args:
            what (list, optional): Reset what scales? Sublist of
                ``"variables"``,``"forcing"``, ``"parameters"`` or
                ``"observations"``. Reset all if left unspecified.
        """
        if what is None:
            what = self.scales.keys()
        for whatscale in what:
            for ivid,widgets in self.scales[what].items():
                if ivid == "grid": continue
                widgets["scale"].set_value( widgets["initial"] )

    def update_current_plot(self, *args, **kwargs):
        """
        Update the current plot
        """
        plot_interfacevalues_kwargs = {}
        if self["settings_plot_usevariabletime_checkbutton"].get_active():
            all_times = np.array([])
            for v in self.model.variables.elements:
                all_times = np.union1d(all_times,v.times)
            plot_interfacevalues_kwargs["times"] = all_times

        for tab,content in self.figures_content.items():
            current_tab = self["plot_notebook"].get_current_page()
            current_box = self["plot_notebook"].get_nth_page(current_tab)
            if self["plot_{}_box".format(tab)] == current_box:
                self.add_status("plot","Plotting...",important=True)
                interfacevalues = []
                for modelpart,ivs in content.items():
                    interfacevalues.extend(ivs.values())
                self.plot_interfacevalues(
                    interfacevalues,
                    self.figures.get(tab), # onto this figure
                    **plot_interfacevalues_kwargs
                    )
        self.add_status("plot","Plot updated!",important=True)


    ###################
    ### Gui methods ###
    ###################
    def setup_gui(self):
        """
        Set up the GTK gui elements
        """
        def reset_variables(action,*args,**kwargs):
            self.reset_scales("variables")
        def reset_forcing(action,*args,**kwargs):
            self.reset_scales("forcing")
        def reset_params(action,*args,**kwargs):
            self.reset_scales("parameters")
        def reset_observations(action,*args,**kwargs):
            self.reset_scales("observations")
        def feedmodel(action,*args,**kwargs):
            self.apply_data_from_settings()
            self.update_current_plot()
        def reset_plots(action,*args,**kwargs):
            for attr in MODEL_CONTENT:
                label = self["plot_{}_notebook_label".format(attr)]
                italictext = re.sub(
                    string=label.get_text(),
                    pattern=r"^(?:<b><i>)?([^<]+)(?:</i></b>)?$",
                    repl=r"\1")
                label.set_markup(italictext)
            self.figures_content = None
        # connect signals
        self.handlers = {
            "CloseApplication": self.quit,
            "Integrate": self.integrate,
            "UpdatePlot": self.update_current_plot,
            "ResetParams": reset_params,
            "ResetForcing": reset_forcing,
            "ResetVariables": reset_variables,
            "ResetObservations": reset_observations,
            "ResetPlots": reset_plots,
            "FeedModel": feedmodel,
            }
        self.builder.connect_signals(self.handlers)

        ### Plot ###
        # add the Figure to the plot box in the gui
        def on_drag_motion(widgt, context, x, y, time, *args):
            Gdk.drag_status(context, Gdk.DragAction.COPY, time)
            return True
        def on_drag_drop(widget, context, x, y, time, *args):
            widget.drag_get_data(context, context.list_targets()[-1], time)
            return True
        def on_drag_data_received(widget, context, x, y, data, info, time,
            user_data):
            try:
                attr,ivid = data.get_text().split(":::")
            except ValueError:
                self.error(main="Strange dropped content!",
                    secondary="Whatever you dropped into here doesn't work :-)")
                Gtk.drag_finish(context,False,False,time)
                return False

            figures_content = self.figures_content.copy()
            newdict = {ivid:getattr(self.model,attr)[ivid]}
            try:
                figures_content[user_data]
            except KeyError:
                figures_content[user_data] = {}
            try:
                figures_content[user_data][attr].update(newdict)
            except KeyError:
                figures_content[user_data][attr] = newdict
            nb = self["plot_notebook"]
            label = nb.get_tab_label(nb.get_nth_page(nb.get_current_page()))
            italictext = re.sub(
                string=label.get_text(),
                pattern=r"^(?:<b><i>)?([^<]+)(?:</i></b>)?$",
                repl=r"<b><i>\1</i></b>")
            label.set_markup(italictext)
            self.figures_content = figures_content
            Gtk.drag_finish(context,True,False,time)

        for n,fig in self.figures.items():
            box = self["plot_{}_box".format(n)]
            canvas = FigureCanvas(fig)
            canvas.drag_dest_set(
                0,
                [],
                Gdk.DragAction.COPY
                )
            canvas.drag_dest_set_target_list(self.DRAGTARGETS)
            canvas.connect("drag-motion",on_drag_motion)
            canvas.connect("drag-drop",on_drag_drop)
            canvas.connect("drag-data-received",on_drag_data_received,n)
            box.pack_start(canvas,True,True,0)

        ### Fill the settings dialog ###
        for what,d in sorted(self.scales.items()):
            expander_box = self["{}_slider_box".format(what)]
            expander_box.pack_start(d["grid"],True,True,3)

        for value,text in zip(
            [60,10*60,30*60,60*60],
            ["1 min","10 min","30 min","1 hour"]
            ):
            self["time_scale"].add_mark(value,Gtk.PositionType.TOP,text)

        self.update_current_plot()

        self.add_status("general","Running a NumericalModel interactively")

        # show everything
        self["main_applicationwindow"].set_title(self.model.name)
        self["main_applicationwindow"].show_all()

    def error(self, main, secondary = None):
        """
        Display a error dialog

        Args:
            main (str): the main text to display
            secondary (str, optional): the secondary text to display
        """
        dialog = Gtk.MessageDialog(
            self["main_applicationwindow"],
            0,
            Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK,
            main
            )
        if not secondary is None:
            dialog.format_secondary_markup(secondary)
        dialog.run()
        dialog.destroy()

    def wait_for_gui(self):
        """
        Wait for the gui to process all pending events
        """
        while Gtk.events_pending():
            Gtk.main_iteration()

    def integrate(self, *args, **kwags):
        """
        Integrate the underlying model by the step defined in the
        ``time_adjustment``.
        """
        self.apply_data_from_settings()
        step = self["time_adjustment"].get_value()
        self.add_status("model","Integrating...",important=True)
        try:
            self.model.integrate(final_time = self.model.model_time + step)
            self.add_status("model","Integration was successful!",
                important=True)
        except Exception as e:
            self.add_status("model","Integration FAILED!",important=True)
            self.error(main="Integration failed!",
                secondary="<i>{}</i>".format(e))
        self.apply_model_data_to_settings()
        self.update_current_plot()


    def add_status(self, context, text, important = False):
        """
        Add a status to the statusbar

        Args:
            context (str): the context in which to display the text
            text (str): the text to display
            important (bool, optional): Make sure the text is **really**
                displayed by calling :any:`wait_for_gui`. Defaults to ``False``.
                Enabling this can slow down the gui.
        """
        context_id = self["statusbar"].get_context_id(context)
        self["statusbar"].push(context_id,text)
        if important:
            self.wait_for_gui()

    def run(self):
        """
        Run the gui
        """
        # set up the gui
        self.setup_gui()
        # run the gui
        self.logger.debug("starting mainloop")
        Gtk.main()
        self.logger.debug("mainloop is over")

    def quit(self, *args):
        """
        Stop the gui
        """
        self.logger.debug("received quitting signal")
        self.logger.debug("stopping mainloop...")
        Gtk.main_quit()
        self.logger.debug("mainloop stopped")


    #######################
    ### Special methods ###
    #######################
    def __getitem__(self, key):
        """
        When indexed, return the corresponding Glade gui element

        Args:
            key (str): the Glade gui element name
        """
        return self.builder.get_object( key )
