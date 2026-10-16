"""Access rules for Rayman"""

from rule_builder.rules import Has, True_

none = True_()

# Powers
has_fist = Has("Fist")
has_hang = Has("Hanging")
has_grappling_fist = Has("Grappling Fist")

# Special items
has_magic_seed = Has("Magic Seed")

# Level access
can_access_pink_plant_wood = True_()
can_access_anguish_lagoon = Has("Anguish Lagoon Unlock")
can_access_swamps_of_forgetfulness = Has("The Swamps of Forgetfulness Unlock")
can_acess_moskito_nest = Has("Moskito's Nest Unlock")
