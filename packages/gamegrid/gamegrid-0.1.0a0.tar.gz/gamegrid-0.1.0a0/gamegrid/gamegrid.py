import ipywidgets as widgets
from traitlets import Unicode, validate, List, Tuple, Int, All

class GameGrid(widgets.DOMWidget):
    _view_name = Unicode('GameGridView').tag(sync=True)
    _view_module = Unicode('gamegrid').tag(sync=True)
    _view_module_version = Unicode('0.1.0').tag(sync=True)
    _model_name = Unicode('GameGridModel').tag(sync=True)
    _model_module = Unicode('gamegrid').tag(sync=True)
    _model_module_version = Unicode('0.1.0').tag(sync=True)
    _grid = List([[]]).tag(sync=True)
    _images = List([
        "https://brifly.github.io/python-lessons-images/diamond.png",
        "https://brifly.github.io/python-lessons-images/wdiamond.png",
        "https://brifly.github.io/python-lessons-images/precious-stone.png",
        "https://brifly.github.io/python-lessons-images/jewels.png",
        "https://brifly.github.io/python-lessons-images/gem.png"   
    ]).tag(sync=True)
    _selected = List(Tuple().tag(sync=True), []).tag(sync=True)
    
    def __init__(self, **kwargs):
        super(GameGrid, self).__init__(**kwargs)
        self._click_handlers = widgets.CallbackDispatcher()
        self.on_msg(self._handle_click_msg)        
    
    def on_click(self, callback, remove=False):
        self._click_handlers.register_callback(lambda s, a: callback(self, a['row'],a['col']), remove=remove)
    
    def update(self, arr):
        self._grid = arr.tolist()
     
    def get_images(self, images):
        self._images = images;
    
    def set_images(self, images):
        self._images = images;
      
    def toggle_select(self, row, col):
        t = (row, col)
        
        # Copy the list so that it forces an update
        newList = self._selected[:]
        if(t in newList):
            newList.remove(t)
        else:
            newList.append((row, col))
            
        self._selected = newList
                
    def get_selected(self):
        return self.selected
            
    def _handle_click_msg(self, _, content, buffers):
        if content.get('event', '') == 'click':
            self._click_handlers(self, content)