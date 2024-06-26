#!/usr/bin/python3

import gi
import os
import subprocess
import sys
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk

# designate the scripts directory
home = os.environ['HOME']
launcher_dir = os.path.join(home, 'script-handler/scripts')

class CarouselApp(Adw.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="com.example.CarouselApp", **kwargs)
        self.window = None
        self.scripts_dir = launcher_dir
        self.current_dir = launcher_dir

    def do_activate(self):
        if not self.window:
            self.window = Adw.ApplicationWindow(application=self)
            
            display = Gdk.Display.get_default()
            monitor = display.get_monitors().get_item(0)  # Get the first monitor
            geometry = monitor.get_geometry()
            screen_width = geometry.width
            screen_height = geometry.height
            self.window.set_default_size(screen_width, screen_height)
            
            self.create_carousel(self.current_dir)
        self.window.present()

    def create_carousel(self, directory):
        carousel = Adw.Carousel()
        carousel.set_hexpand(True)
        carousel.set_vexpand(True)
        carousel.set_allow_scroll_wheel(True)
        carousel.set_orientation(Gtk.Orientation.HORIZONTAL)  # Horizontal scrolling

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
                window {
                    background-color: rgba(0, 0, 0, 0.8);  /* 80% transparent black background */
                }
                box {
                    border-radius: 20px;  /* Rounded corners */ 
                }
                button {
                    min-width: 150px; 
                    min-height: 50px; 
                    padding: 5px 20px;
                    border-radius: 30px;
                    font-size: 14px;
                    margin: 10px;
                    background: #1a5fb4;
                }
                button:hover {
                    background: #1c71d8;
                }
            """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), 
            css_provider, 
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        items = sorted(os.listdir(directory))
        bash_scripts = [f for f in items if f.endswith('.sh')]
        directories = [d for d in items if os.path.isdir(os.path.join(directory, d))]

        num_items = len(bash_scripts) + len(directories)
        num_pages = (num_items + 11) // 12

        for i in range(num_pages):
            grid = Gtk.Grid()
            grid.set_row_spacing(15)
            grid.set_column_spacing(15)
            grid.set_margin_top(15)
            grid.set_margin_bottom(15)
            grid.set_margin_start(15)
            grid.set_margin_end(15)
            grid.set_halign(Gtk.Align.CENTER)
            grid.set_valign(Gtk.Align.CENTER)

            # Each page will have 3 columns and up to 4 rows
            for j in range(12*i, min(12*(i+1), num_items)):
                if j < len(directories):
                    dir_name = directories[j]
                    button = Gtk.Button(label=f"{dir_name}")
                    button.connect("clicked", self.on_directory_clicked, os.path.join(directory, dir_name))
                else:
                    script_name = bash_scripts[j - len(directories)]
                    button_label = script_name.replace('.sh', '')
                    button = Gtk.Button(label=button_label)
                    button.connect("clicked", self.on_button_clicked, os.path.join(directory, script_name))
                
                # Attach buttons left to right before moving to the next row
                grid.attach(button, j % 3, (j // 3) % 4, 1, 1)  # Modify attachment for horizontal order

            carousel.append(grid)

        dots = Adw.CarouselIndicatorDots()
        dots.set_carousel(carousel)
        dots.set_orientation(Gtk.Orientation.HORIZONTAL)  # Horizontal dots
        dots.set_halign(Gtk.Align.CENTER)  # Dots centered horizontally
        dots.set_valign(Gtk.Align.END)  # Dots at the bottom

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.append(carousel)
        vbox.append(dots)
        vbox.set_homogeneous(False)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)

        self.window.set_content(vbox)

    def on_button_clicked(self, button, script_path):
        subprocess.Popen(['bash', script_path], start_new_session=True)
        sys.exit(0)

    def on_directory_clicked(self, button, dir_path):
        self.create_carousel(dir_path)

app = CarouselApp()
app.run()

