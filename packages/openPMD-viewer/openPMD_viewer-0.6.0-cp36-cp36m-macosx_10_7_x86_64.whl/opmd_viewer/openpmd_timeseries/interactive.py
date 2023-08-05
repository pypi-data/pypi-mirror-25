"""
This file is part of the openPMD-viewer.

It defines an interactive interface for the viewer,
based on the IPython notebook functionalities

Copyright 2015-2016, openPMD-viewer contributors
Authors: Remi Lehe, Axel Huebl
License: 3-Clause-BSD-LBNL
"""

from ipywidgets import widgets, __version__
from IPython.core.display import display, clear_output
import math
import matplotlib
import matplotlib.pyplot as plt
from functools import partial
ipywidgets_version = int(__version__[0])


class InteractiveViewer(object):

    def __init__(self):
        pass

    def slider(self, figsize=(6, 5),
               exclude_particle_records=['charge', 'mass'], **kw):
        """
        Navigate the simulation using a slider

        Parameters:
        -----------
        figsize: tuple
            Size of the figures

        exclude_particle_records: list of strings
            List of particle quantities that should not be displayed
            in the slider (typically because they are less interesting)

        kw: dict
            Extra arguments to pass to matplotlib's imshow
        """
        # -----------------------
        # Define useful functions
        # -----------------------

        def refresh_field(change=None, force=False):
            """
            Refresh the current field figure

            Parameters :
            ------------
            change: dictionary
                Dictionary passed by the widget to a callback functions
                whenever a change of a widget happens
                (see docstring of ipywidgets.Widget.observe)
                This is mainline a place holder ; not used in this function

            force: bool
                Whether to force the update
            """
            # Determine whether to do the refresh
            do_refresh = False
            if (self.avail_fields is not None):
                if force or fld_refresh_toggle.value:
                    do_refresh = True
            # Do the refresh
            if do_refresh:
                plt.figure(fld_figure_button.value, figsize=figsize)
                plt.clf()

                # When working in inline mode, in an ipython notebook,
                # clear the output (prevents the images from stacking
                # in the notebook)
                if 'inline' in matplotlib.get_backend():
                    clear_output()

                # Colorscale range
                vmin, vmax = fld_color_button.get_range()
                # Determine range of the plot from widgets
                plot_range = [ fld_hrange_button.get_range(),
                                fld_vrange_button.get_range() ]

                # Call the method get_field
                self.get_field( iteration=self.current_iteration,
                    output=False, plot=True,
                    field=fieldtype_button.value, coord=coord_button.value,
                    m=convert_to_int(mode_button.value),
                    slicing=slicing_button.value, theta=theta_button.value,
                    slicing_dir=slicing_dir_button.value,
                    plot_range=plot_range, vmin=vmin, vmax=vmax,
                    cmap=fld_color_button.cmap.value)

        def refresh_ptcl(change=None, force=False):
            """
            Refresh the current particle figure

            Parameters :
            ------------
            change: dictionary
                Dictionary passed by the widget to a callback functions
                whenever a change of a widget happens
                (see docstring of ipywidgets.Widget.observe)
                This is mainline a place holder ; not used in this function

            force: bool
                Whether to force the update
            """
            # Determine whether to do the refresh
            do_refresh = False
            if self.avail_species is not None:
                if force or ptcl_refresh_toggle.value:
                    do_refresh = True
            # Do the refresh
            if do_refresh:
                plt.figure(ptcl_figure_button.value, figsize=figsize)
                plt.clf()

                # When working in inline mode, in an ipython notebook,
                # clear the output (prevents the images from stacking
                # in the notebook)
                if 'inline' in matplotlib.get_backend():
                    clear_output()

                # Colorscale range
                vmin, vmax = ptcl_color_button.get_range()
                # Determine range of the plot from widgets
                plot_range = [ ptcl_hrange_button.get_range(),
                                ptcl_vrange_button.get_range() ]

                if ptcl_yaxis_button.value == 'None':
                    # 1D histogram
                    self.get_particle( iteration=self.current_iteration,
                        output=False, var_list=[ptcl_xaxis_button.value],
                        select=ptcl_select_widget.to_dict(),
                        species=ptcl_species_button.value, plot=True,
                        vmin=vmin, vmax=vmax,
                        cmap=ptcl_color_button.cmap.value,
                        nbins=ptcl_bins_button.value,
                        plot_range=plot_range,
                        use_field_mesh=ptcl_use_field_button.value )
                else:
                    # 2D histogram
                    self.get_particle( iteration=self.current_iteration,
                        output=False, var_list=[ptcl_xaxis_button.value,
                                                ptcl_yaxis_button.value],
                        select=ptcl_select_widget.to_dict(),
                        species=ptcl_species_button.value, plot=True,
                        vmin=vmin, vmax=vmax,
                        cmap=ptcl_color_button.cmap.value,
                        nbins=ptcl_bins_button.value,
                        plot_range=plot_range,
                        use_field_mesh=ptcl_use_field_button.value )

        def refresh_field_type(change):
            """
            Refresh the field type and disable the coordinates buttons
            if the field is scalar.

            Parameter
            ---------
            change: dictionary
                Dictionary passed by the widget to a callback functions
                whenever a change of a widget happens
                (see docstring of ipywidgets.Widget.observe)
            """
            if self.avail_fields[change['new']] == 'scalar':
                coord_button.disabled = True
            elif self.avail_fields[change['new']] == 'vector':
                coord_button.disabled = False
            refresh_field()

        def refresh_species(change=None):
            """
            Refresh the particle species buttons by populating them
            with the available records for the current species

            Parameter
            ---------
            change: dictionary
                Dictionary passed by the widget to a callback functions
                whenever a change of a widget happens
                (see docstring of ipywidgets.Widget.observe)
            """
            # Deactivate the particle refreshing to avoid callback
            # while modifying the widgets
            saved_refresh_value = ptcl_refresh_toggle.value
            ptcl_refresh_toggle.value = False

            # Get available records for this species
            avail_records = [q for q in self.avail_record_components[
                             ptcl_species_button.value]
                             if q not in exclude_particle_records]
            # Update the plotting buttons
            ptcl_xaxis_button.options = avail_records
            ptcl_yaxis_button.options = avail_records + ['None']
            if ptcl_xaxis_button.value not in ptcl_xaxis_button.options:
                ptcl_xaxis_button.value = avail_records[0]
            if ptcl_yaxis_button.value not in ptcl_yaxis_button.options:
                ptcl_yaxis_button.value = 'None'

            # Update the selection widgets
            for dropdown_button in ptcl_select_widget.quantity:
                dropdown_button.options = avail_records

            # Put back the previous value of the refreshing button
            ptcl_refresh_toggle.value = saved_refresh_value

        def change_iteration(change):
            "Plot the result at the required iteration"
            # Find the closest iteration
            self._current_i = abs(self.iterations - change['new']).argmin()
            self.current_iteration = self.iterations[ self._current_i ]
            refresh_field()
            refresh_ptcl()

        def step_fw(b):
            "Plot the result one iteration further"
            if self._current_i < len(self.t) - 1:
                self.current_iteration = self.iterations[self._current_i + 1]
            else:
                self.current_iteration = self.iterations[self._current_i]
            slider.value = self.current_iteration

        def step_bw(b):
            "Plot the result one iteration before"
            if self._current_i > 0:
                self.current_iteration = self.iterations[self._current_i - 1]
            else:
                self.current_iteration = self.iterations[self._current_i]
            slider.value = self.current_iteration

        # ---------------
        # Define widgets
        # ---------------

        # Slider
        iteration_min = self.iterations.min()
        iteration_max = self.iterations.max()
        step = max( int( (iteration_max - iteration_min) / 20. ), 1 )
        slider = widgets.IntSlider( description="iteration",
            min=iteration_min, max=iteration_max + step, step=step )
        slider.observe( change_iteration, names='value', type='change' )
        set_widget_dimensions( slider, width=500 )

        # Forward button
        button_p = widgets.Button(description="+")
        set_widget_dimensions( button_p, width=40 )
        button_p.on_click(step_fw)

        # Backward button
        button_m = widgets.Button(description="-")
        set_widget_dimensions( button_m, width=40 )
        button_m.on_click(step_bw)

        # Display the time widgets
        container = widgets.HBox(children=[button_m, button_p, slider])
        display(container)

        # Field widgets
        # -------------
        if (self.avail_fields is not None):

            # Field type
            # ----------
            # Field button
            fieldtype_button = widgets.ToggleButtons(
                description='Field:',
                options=sorted(self.avail_fields.keys()))
            fieldtype_button.observe( refresh_field_type, 'value', 'change' )

            # Coord button
            if self.geometry == "thetaMode":
                coord_button = widgets.ToggleButtons(
                    description='Coord:', options=['x', 'y', 'z', 'r', 't'])
            elif self.geometry in \
                    ["1dcartesian", "2dcartesian", "3dcartesian"]:
                coord_button = widgets.ToggleButtons(
                    description='Coord:', options=['x', 'y', 'z'])
            coord_button.observe( refresh_field, 'value', 'change')
            # Mode and theta button (for thetaMode)
            mode_button = widgets.ToggleButtons(description='Mode:',
                                                options=self.avail_circ_modes)
            mode_button.observe( refresh_field, 'value', 'change')
            theta_button = widgets.FloatSlider( value=0.,
                    min=-math.pi / 2, max=math.pi / 2)
            set_widget_dimensions( theta_button, width=190 )
            theta_button.observe( refresh_field, 'value', 'change')
            # Slicing buttons (for 3D)
            slicing_dir_button = widgets.ToggleButtons(
                value=self.axis_labels[0], options=self.axis_labels,
                description='Slice normal:')
            slicing_dir_button.observe( refresh_field, 'value', 'change' )
            slicing_button = widgets.FloatSlider( min=-1., max=1., value=0.)
            set_widget_dimensions( slicing_button, width=180 )
            slicing_button.observe( refresh_field, 'value', 'change')

            # Plotting options
            # ----------------
            # Figure number
            fld_figure_button = widgets.IntText( value=0 )
            set_widget_dimensions( fld_figure_button, width=50 )
            # Colormap button
            fld_color_button = ColorBarSelector(
                refresh_field, default_cmap='viridis' )
            # Range buttons
            fld_hrange_button = RangeSelector( refresh_field,
                default_value=10., title='Horizontal axis:')
            fld_vrange_button = RangeSelector( refresh_field,
                default_value=10., title='Vertical axis:')
            # Refresh buttons
            fld_refresh_toggle = widgets.ToggleButton(
                description='Always refresh', value=True)
            fld_refresh_button = widgets.Button(
                description='Refresh now!')
            fld_refresh_button.on_click( partial(refresh_field, force=True) )

            # Containers
            # ----------
            # Field type container
            if self.geometry == "thetaMode":
                container_fields = widgets.VBox( children=[
                    fieldtype_button, coord_button, mode_button,
                    add_description('Theta:', theta_button) ])
            elif self.geometry in ["1dcartesian", "2dcartesian"]:
                container_fields = widgets.VBox(
                    children=[fieldtype_button, coord_button])
            elif self.geometry == "3dcartesian":
                container_fields = widgets.VBox( children=[
                    fieldtype_button, coord_button, slicing_dir_button,
                    add_description("Slicing:", slicing_button) ])
            set_widget_dimensions( container_fields, width=330 )
            # Plotting options container
            container_fld_cbar = fld_color_button.to_container()
            container_fld_hrange = fld_hrange_button.to_container()
            container_fld_vrange = fld_vrange_button.to_container()
            if self.geometry == "1dcartesian":
                container_fld_plots = widgets.VBox( children=[
                    add_description("<b>Figure:</b>", fld_figure_button),
                    container_fld_vrange, container_fld_hrange ])
            else:
                container_fld_plots = widgets.VBox( children=[
                    add_description("<b>Figure:</b>", fld_figure_button),
                    container_fld_cbar, container_fld_vrange,
                    container_fld_hrange ])
            set_widget_dimensions( container_fld_plots, width=330 )
            # Accordion for the field widgets
            accord1 = widgets.Accordion(
                children=[container_fields, container_fld_plots])
            accord1.set_title(0, 'Field type')
            accord1.set_title(1, 'Plotting options')
            # Complete field container
            container_fld = widgets.VBox( children=[accord1, widgets.HBox(
                children=[fld_refresh_toggle, fld_refresh_button])])
            set_widget_dimensions( container_fld, width=370 )

        # Particle widgets
        # ----------------
        if (self.avail_species is not None):

            # Particle quantities
            # -------------------
            # Species selection
            ptcl_species_button = widgets.Dropdown(options=self.avail_species)
            set_widget_dimensions( ptcl_species_button, width=250 )
            ptcl_species_button.observe( refresh_species, 'value', 'change')
            # Get available records for this species
            avail_records = [q for q in
                             self.avail_record_components[
                                 ptcl_species_button.value]
                             if q not in exclude_particle_records]
            # Particle quantity on the x axis
            ptcl_xaxis_button = widgets.ToggleButtons(options=avail_records)
            ptcl_xaxis_button.observe( refresh_ptcl, 'value', 'change')
            # Particle quantity on the y axis
            ptcl_yaxis_button = widgets.ToggleButtons(
                options=avail_records + ['None'], value='None')
            ptcl_yaxis_button.observe( refresh_ptcl, 'value', 'change')

            # Particle selection
            # ------------------
            # 3 selection rules at maximum
            ptcl_select_widget = ParticleSelectWidget(3,
                                 avail_records, refresh_ptcl)

            # Plotting options
            # ----------------
            # Figure number
            ptcl_figure_button = widgets.IntText( value=1 )
            set_widget_dimensions( ptcl_figure_button, width=50 )
            # Number of bins
            ptcl_bins_button = widgets.IntText( value=100 )
            set_widget_dimensions( ptcl_bins_button, width=60 )
            ptcl_bins_button.observe( refresh_ptcl, 'value', 'change')
            # Colormap button
            ptcl_color_button = ColorBarSelector(
                refresh_ptcl, default_cmap='Blues' )
            # Range buttons
            ptcl_hrange_button = RangeSelector( refresh_ptcl,
                default_value=10., title='Horizontal axis:')
            ptcl_vrange_button = RangeSelector( refresh_ptcl,
                default_value=10., title='Vertical axis:')
            # Use field mesh buttons
            ptcl_use_field_button = widgets.ToggleButton(
                description=' Use field mesh', value=True )
            ptcl_use_field_button.observe( refresh_ptcl, 'value', 'change')
            # Resfresh buttons
            ptcl_refresh_toggle = widgets.ToggleButton(
                description='Always refresh', value=True)
            ptcl_refresh_button = widgets.Button(
                description='Refresh now!')
            ptcl_refresh_button.on_click( partial(refresh_ptcl, force=True) )

            # Containers
            # ----------
            # Particle quantity container
            container_ptcl_quantities = widgets.VBox( children=[
                ptcl_species_button, ptcl_xaxis_button, ptcl_yaxis_button])
            set_widget_dimensions( container_ptcl_quantities, width=310 )
            # Particle selection container
            container_ptcl_select = ptcl_select_widget.to_container()
            # Plotting options container
            container_ptcl_fig = widgets.HBox( children=[
                add_description("<b>Figure:</b>", ptcl_figure_button),
                add_description( "Bins:", ptcl_bins_button ) ] )
            container_ptcl_cbar = ptcl_color_button.to_container()
            container_ptcl_hrange = ptcl_hrange_button.to_container()
            container_ptcl_vrange = ptcl_vrange_button.to_container()
            container_ptcl_plots = widgets.VBox( children=[ container_ptcl_fig,
                container_ptcl_cbar, container_ptcl_vrange,
                container_ptcl_hrange, ptcl_use_field_button ])
            set_widget_dimensions( container_ptcl_plots, width=310 )
            # Accordion for the field widgets
            accord2 = widgets.Accordion(
                children=[container_ptcl_quantities, container_ptcl_select,
                          container_ptcl_plots])
            accord2.set_title(0, 'Particle quantities')
            accord2.set_title(1, 'Particle selection')
            accord2.set_title(2, 'Plotting options')
            # Complete particle container
            container_ptcl = widgets.VBox( children=[accord2, widgets.HBox(
                children=[ptcl_refresh_toggle, ptcl_refresh_button])])
            set_widget_dimensions( container_ptcl, width=370 )

        # Global container
        if (self.avail_fields is not None) and \
                (self.avail_species is not None):
            global_container = widgets.HBox(
                children=[container_fld, container_ptcl])
            display(global_container)
        elif self.avail_species is None:
            display(container_fld)
        elif self.avail_fields is None:
            display(container_ptcl)


def convert_to_int(m):
    """
    Convert the string m to an int, except if m is 'all' or None
    """
    if (m == 'all') or (m is None):
        return(m)
    else:
        return(int(m))


class ColorBarSelector(object):
    """
    Class that allows to select a colorbar and the corresponding range.
    It features a widget for the exponent, in order to rapidly change
    the order of magnitude of the colorbar.
    """

    def __init__( self, callback_function, default_cmap ):
        """
        Initialize a set of widgets that select a colorbar.

        Parameters:
        -----------
        callback_function: callable
            The function to call when activating/deactivating the range,
            or when changing the colormap
        default_cmap: string
            The name of the colormap that will be used when the widget is
            initialized
        """
        # Create the colormap widget
        available_cmaps = sorted( plt.colormaps() )
        if default_cmap not in available_cmaps:
            default_cmap = 'jet'
        self.cmap = widgets.Select(options=available_cmaps, value=default_cmap)

        # Create the widgets for the range
        self.active = widgets.Checkbox( value=False )
        self.low_bound = widgets.FloatText( value=-5. )
        self.up_bound = widgets.FloatText( value=5. )
        self.exponent = widgets.FloatText( value=9. )

        # Add the callback function
        self.active.observe( callback_function, 'value', 'change' )
        self.exponent.observe( callback_function, 'value', 'change' )
        self.cmap.observe( callback_function, 'value', 'change' )

    def to_container( self ):
        """
        Return a widget container, where all the widgets
        are placed properly, with respect to each other.
        """
        # Set the widget dimensions
        set_widget_dimensions( self.active, width=20 )
        set_widget_dimensions( self.low_bound, width=60 )
        set_widget_dimensions( self.up_bound, width=60 )
        set_widget_dimensions( self.exponent, width=45 )
        set_widget_dimensions( self.cmap, width=200 )
        # Gather the different widgets on two lines
        cmap_container = widgets.HBox( children=[
            widgets.HTML( "<b>Colorbar:</b>"), self.cmap ])
        if ipywidgets_version > 4:
            # For newer version of ipywidgets: add the "x10^" on same line
            range_container = widgets.HBox( children=[ self.active,
                add_description("from", self.low_bound, width=30 ),
                add_description("to", self.up_bound, width=20 ),
                add_description("x 10^", self.exponent, width=45 ) ] )
            final_container = widgets.VBox(
                children=[ cmap_container, range_container ])
        else:
            # For older version of ipywidgets: add the "x10^" on new line
            range_container = widgets.HBox( children=[ self.active,
                add_description("from", self.low_bound, width=30 ),
                add_description("to", self.up_bound, width=20 ) ] )
            final_container = widgets.VBox(
                children=[ cmap_container, range_container,
                add_description("x 10^", self.exponent, width=45 ) ])
        set_widget_dimensions( final_container, width=310 )
        return( final_container )

    def get_range( self ):
        """
        Return a list of 2 elements: the current lower bound and upper bound.
        When the widget is not active, None is returned instead of the bounds.
        """
        if self.active.value is True:
            return( [ self.low_bound.value * 10.**self.exponent.value,
                      self.up_bound.value * 10.**self.exponent.value ] )
        else:
            return( [ None, None ] )


class RangeSelector(object):
    """
    Class that allows to select a range of (float) values.
    """

    def __init__( self, callback_function, default_value, title ):
        """
        Initialize a set of widgets that select a range of (float) values

        Parameters:
        -----------
        callback_function: callable
            The function to call when activating/deactivating the range
        default_value:
            The default value of the upper bound of the range at initialization
            (The default lower bound is the opposite of this value.)
        title:
            The title that is displayed on top of the widgets
        """
        # Register title
        self.title = title

        # Create the widgets
        self.active = widgets.Checkbox( value=False )
        self.low_bound = widgets.FloatText( value=-default_value )
        self.up_bound = widgets.FloatText( value=default_value )

        # Add the callback function
        self.active.observe( callback_function, 'value', 'change' )

    def to_container( self ):
        """
        Return a widget container, where all the range widgets
        are placed properly, with respect to each other.
        """
        # Set the widget dimensions
        set_widget_dimensions( self.active, width=20 )
        set_widget_dimensions( self.low_bound, width=60 )
        set_widget_dimensions( self.up_bound, width=60 )
        # Gather the different widgets on one line
        container = widgets.HBox( children=[ self.active,
            add_description("from", self.low_bound, width=30 ),
            add_description("to", self.up_bound, width=20 ) ] )
        set_widget_dimensions( container, width=310 )
        # Add the title
        final_container = widgets.VBox( children=[
            widgets.HTML( "<b>%s</b>" % self.title ), container ] )
        return( final_container )

    def get_range( self ):
        """
        Return a list of 2 elements: the current lower bound and upper bound.
        When the widget is not active, None is returned instead of the bounds.
        """
        if self.active.value is True:
            return( [ self.low_bound.value, self.up_bound.value ] )
        else:
            return( [ None, None ] )


class ParticleSelectWidget(object):

    """
    Class that groups the particle selection widgets.
    """

    def __init__(self, n_rules, avail_records, refresh_ptcl):
        """
        Initialize a set of particle selection widgets

        Parameters:
        -----------
        n_rules: int
            The number of selection rules to display

        avail_records: list of strings
            The list of available records for the current species

        refresh_ptcl: callable
            The callback function to execute when the widget is changed
        """
        self.n_rules = n_rules

        # Create widgets that determines whether the rule is used
        self.active = [widgets.Checkbox(value=False)
                       for i in range(n_rules)]
        # Create widgets that determines the quantity on which to select
        # (The Dropdown menu is empty, but is later populated by the
        # function refresh_species)
        self.quantity = [widgets.Dropdown(options=avail_records,
            description='Select ') for i in range(n_rules)]
        # Create widgets that determines the lower bound and upper bound
        self.low_bound = [widgets.FloatText( value=-1.e-1 )
            for i in range(n_rules)]
        self.up_bound = [widgets.FloatText( value=1.e-1 )
            for i in range(n_rules)]

        # Add the callback function refresh_ptcl to each widget
        for i in range(n_rules):
            self.active[i].observe( refresh_ptcl, 'value', 'change' )
            self.quantity[i].observe( refresh_ptcl, 'value', 'change' )
            self.low_bound[i].observe( refresh_ptcl, 'value', 'change' )
            self.up_bound[i].observe( refresh_ptcl, 'value', 'change' )

    def to_container(self):
        """
        Return a widget container, where all the particle selection
        widgets are placed properly, with respect to each other.
        """
        containers = []
        for i in range(self.n_rules):
            set_widget_dimensions( self.active[i], width=20 )
            set_widget_dimensions( self.low_bound[i], width=90 )
            set_widget_dimensions( self.up_bound[i], width=90 )
            containers.append(widgets.HBox(
                children=[self.active[i], self.quantity[i]]))
            containers.append( widgets.HBox( children=[
                add_description("from", self.low_bound[i], width=30 ),
                add_description("to", self.up_bound[i], width=20 )] ) )

        final_container = widgets.VBox(children=containers)
        set_widget_dimensions( final_container, width=310 )
        return( final_container )

    def to_dict(self):
        """
        Return a selection dictionary of the form
        {'uz': [-0.1, 2.], 'x':[-10., 10.]}
        depending on the values of the widgets.
        """
        rule_dict = {}
        # Go through the selection rules and add the active rules
        for i in range(self.n_rules):
            if self.active[i].value is True:
                rule_dict[ self.quantity[i].value ] = \
                    [self.low_bound[i].value, self.up_bound[i].value]

        # If any rule is active, return a dictionary
        if len(rule_dict) != 0:
            return(rule_dict)
        # If no rule is active, return None
        else:
            return(None)


def set_widget_dimensions( widget, height=None, width=None, left_margin=None ):
    """
    Set the dimensions of the widget, using the proper API
    (which depends on the version of ipywidgets)

    Parameters
    ----------
    widget: an ipywidget object

    height, width: integer, optional
        The height and width in number of points

    left_margin: integer, optional
        Only used for ipywidgets version > 5
        The left margin of a widget (avoids collisions with other widgets)
    """
    if ipywidgets_version >= 5:
        if height is not None:
            widget.layout.height = str(height) + 'px'
        if width is not None:
            widget.layout.width = str(width) + 'px'
        if left_margin is not None:
            widget.layout.margin = "0px 0px 0px " + str(left_margin) + "px"
    else:
        if height is not None:
            widget.height = height
        if width is not None:
            widget.width = width


def add_description( text, annotated_widget, width=50 ):
    """
    Add a description (as an HTML widget) to the left of `annotated_widget`

    Parameters
    ----------
    text: string
        The text to be added
    annotated_widget: an ipywidgets widget
        The widget to which the description will be added
    width: int
        The width of the description
    """
    html_widget = widgets.HTML(text)
    set_widget_dimensions( html_widget, width=width )
    return( widgets.HBox( children=[ html_widget, annotated_widget] ) )
