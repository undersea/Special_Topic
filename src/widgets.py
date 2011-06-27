import gtk
import gobject
import time

class CellRendererButton(gtk.GenericCellRenderer):
    __gproperties__ = {
        "custom": (gobject.TYPE_OBJECT, "Custom",
                   "Custom", gobject.PARAM_READWRITE),
        }

    def __init__(self):
        self.__gobject_init__()
        self.custom = None

    def do_set_property(self, pspec, value):
        setattr(self, pspec.name, value)

    def do_get_property(self, pspec):
        return getattr(self, pspec.name)

    def on_render(self, window, widget, background_area, cell_area, expose_area, flags):
        
        #self.widget.window.draw_rectangle()
        self.custom.draw(cell_area)#window, widget, cell_area.x, cell_area.y)

    def on_get_size(self, widget, cell_area=None):
        return (0, 0, self.custom.window.get_width(), self.custom.window.get_height())
 

gobject.type_register(CellRendererButton)




class CellRendererPixbufXt(gtk.CellRendererPixbuf):
    __gproperties__ = { 'active-state' :                                      
                        (gobject.TYPE_STRING, 'pixmap/active widget state',  
                        'stock-icon name representing active widget state',  
                        None, gobject.PARAM_READWRITE) }                      
    __gsignals__    = { 'clicked' :                                          
                        (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (int,)) ,
                        } 

    def __init__( self ):                                                    
        gtk.CellRendererPixbuf.__init__( self )                              
        self.set_property( 'mode', gtk.CELL_RENDERER_MODE_ACTIVATABLE )      
                                                                              
    def do_get_property( self, property ):                                    
        if property.name == 'active-state':                                  
            return self.active_state                                          
        else:                                                                
            raise AttributeError, 'unknown property %s' % property.name      
                                                                              
    def do_set_property( self, property, value ):                            
        if property.name == 'active-state':                                  
            self.active_state = value                                        
        else:                                                                
            raise AttributeError, 'unknown property %s' % property.name      
                                                                              
    def do_activate( self, event, widget, path,  background_area, cell_area, flags ):    
        if event.type == gtk.gdk.BUTTON_PRESS:
            self.emit('clicked', int(path))

            
                                                  


        
gobject.type_register(CellRendererPixbufXt)


def on_possible_activated(tree, new_path, view_column):
    print 'on_possible_activated:', tree, new_path, view_column


def add_button(pos, column, func):
    cell = CellRendererPixbufXt()
    cell.connect('clicked', func, column)
    #cell.connect('pressed', hello, column)
    #image = gtk.gdk.pixbuf_new_from_file(image_file)#gtk.image_new_from_file(image_file)
    #cell.set_property('pixbuf', image)
    
    column.pack_start(cell)
    column.set_cell_data_func(cell, file_name, pos)

    
def file_name(column, cell, model, iter, pos):
    if model.get_value(iter, pos) != None:
        cell.set_property('pixbuf', gtk.gdk.pixbuf_new_from_file(model.get_value(iter, pos)))
    else:
        cell.set_property('pixbuf', None)
    return
