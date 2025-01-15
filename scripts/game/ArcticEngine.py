from scripts.utility.logger import Logger
from scripts.game.Tile import StaticTile, DynamicTile
from pygame import Surface, transform
from math import gcd, ceil, floor


class ArcticEngine:
    
    __TUPLE_NOT_IN_RANGE = "{topic} not in range '{value}'. Ensure values are >= 1."
    __GAME_SURF_DIM = "Specified game surface dimensions"
    __MAP_DIM = "Specified map dimensions"
    __NEW_MAP = "Map created of size: '{map_dim}'."
    
    def __init__(self):
        
        self.__game_scale: float = 1.0
        self.__game_scale_updated: bool = False
        self.unscaled_game_surf: Surface = None
        self.unscaled_game_surf_dim: tuple[int, int] = None
        self.game_surf: Surface = None
        self.game_surf_dim: tuple[int, int] = None
        self.game_surf_pos: tuple[int, int] = (0, 0)
        
        self.map_surf: Surface = None
        self.map_surf_dim: tuple[int, int] = None
        self.map_array: list[list[StaticTile | DynamicTile]] = None
        self.map_dim: tuple[int, int] = None
        self.map_tile_dim: int = None
    
    
    def new_map(self,
                dim: tuple[int,int], 
                texture_img_name: str):
        """
        Creates a new map with the specified dimensions and texture image name. 
        The map_tile_dim is set based on the first tiles texture in the map
        array.
        
        Args:
            dim (tuple[int,int]): A tuple representing the dimensions of the map.
            texture_img_name (str): The name of the texture image to be used for the map.
        """
        
        if all(i >= 1 for i in dim):
            
            self.map_array = []
            
            self.map_dim = dim
            
            for y in range(dim[1]):
                
                self.map_array.append([])
                for x in range(dim[0]):
                    
                    new_map_tile = StaticTile(texture_img_name)
                    
                    if y == 0 and x == 0:
                        self.map_tile_dim = new_map_tile.dim
                    
                    self.map_array[y].append(new_map_tile)
                    
            self.__set_map_surf()
                    
            Logger.log_info(
                ArcticEngine.__NEW_MAP.format(map_dim = dim))
                    
        else:
            Logger.log_error(
                ArcticEngine.__TUPLE_NOT_IN_RANGE.format(
                    topic = ArcticEngine.__MAP_DIM, valeu = dim))
            
            
    def __set_map_surf(self):
        
        self.map_surf_dim = (
            self.map_dim[0] * self.map_tile_dim[0],
            self.map_dim[1] * self.map_tile_dim[1])
        
        self.map_surf = Surface(self.map_surf_dim)
        
        for y in range(len(self.map_array)):
            for x in range(len(self.map_array[y])):
                self.map_surf.blit(self.map_array[y][x].get_texture_surf(), (self.map_tile_dim[0] * x, self.map_tile_dim[1] * y))
    
    
    def get_game_scale(self):
        return self.__game_scale
    
    
    def set_game_scale(self, value):
        
        if value != self.__game_scale:
            if value >= 1:
                self.__game_scale = value
            else:
                self.__game_scale = 1
            
            self.__game_scale_updated = True

            
    def __set_unscaled_game_surf(self, surf_resized: bool, surf_dim: tuple[int, int]):
        
        if self.unscaled_game_surf == None or surf_resized  or self.__game_scale_updated:
            
            if all(i >= 1 for i in surf_dim):
                
                self.unscaled_game_surf_dim = (
                    (surf_dim[0] / self.__game_scale)+1, 
                    (surf_dim[1] / self.__game_scale)+1)
                
                self.unscaled_game_surf = Surface(self.unscaled_game_surf_dim)
                
                self.x_centered = self.unscaled_game_surf.get_width() % 2 == 0
                self.y_centered = self.unscaled_game_surf.get_height() % 2 == 0
            
            else:
                Logger.log_error(
                    ArcticEngine.__TUPLE_NOT_IN_RANGE.format(
                        topic = ArcticEngine.__GAME_SURF_DIM, valeu = surf_dim))
    
        
    def __set_game_surf_pos(self) -> tuple[int, int]:
        
        x = -(self.__game_scale / 2)
        if not self.x_centered:
            x += self.__game_scale / 2
            
        y = -(self.__game_scale / 2)
        if not self.y_centered:
            y += self.__game_scale / 2
            
        self.game_surf_pos = (round(x), round(y))
        
    
    def __set_scaled_game_surf(self, surf_resized: bool, surf_dim: tuple[int, int]):
        
        if self.game_surf == None or surf_resized or self.__game_scale_updated:
                
                self.game_surf = transform.scale(self.unscaled_game_surf, (
                    round(self.unscaled_game_surf_dim[0] * self.__game_scale),
                    round(self.unscaled_game_surf_dim[1] * self.__game_scale)))
                
                self.game_surf_dim = surf_dim
                                
                self.__game_scale_updated = False
                
                self.__set_game_surf_pos()


    def set_game_surf(self, surf_resized: bool, surf_dim: tuple[int, int]) -> Surface:
        
        ## Setting the game window
        self.__set_unscaled_game_surf(surf_resized, surf_dim)
        
        ## Drawing the map onto the game window
        self.unscaled_game_surf.blit(self.map_surf, (
            (self.unscaled_game_surf_dim[0] / 2),
            (self.unscaled_game_surf_dim[1] / 2),
        ))
        
        ## Scaleding the game window to match the size of the surface being drawn on
        self.__set_scaled_game_surf(surf_resized, surf_dim)
        
        