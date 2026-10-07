from BaseClasses import Region
from .locations import LOCATIONS, RaymanLocation

def create_regions(world) -> None:
        #Overworld creation (Not in locations)
        world.multiworld.regions.append(Region("Overworld",world.player,world.multiworld))
        
        region_names = sorted({loc.region for loc in LOCATIONS})
        #Gathering regions from LOCATIONS
        for name in region_names:
            world.multiworld.regions.append(Region(name,world.player,world.multiworld))
            
        #Creating locations
        for loc in LOCATIONS:
            region = world.get_region(loc.region)
            location = RaymanLocation(world.player,loc.name,loc.id,region)
            region.locations.append(location)
            
        #Connection
        hub = world.get_region("Overworld")
        hub.connect(world.get_region("Pink Plant Woods"))
        #...