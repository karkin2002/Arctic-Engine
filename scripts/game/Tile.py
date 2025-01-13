from pygame import Surface
import scripts.utility.glob as glob
glob.init()

class Tile:
    def __init__(self, 
                 dim: tuple[int, int]):
        
        self.dim = dim


class DynamicTile(Tile):
    
    
    def __init__(self):
        super().__init__((100,100))
    
    
    
class StaticTile(Tile):
    
    
    def __init__(self, 
                 texture_img_name: str):
        
        self.texture_img_name = texture_img_name
        
        super().__init__(
            glob.get_img_dim(self.texture_img_name)
        )
        
    def get_texture_surf(self):
        return glob.get_img_surf(self.texture_img_name)