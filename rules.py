"""Access rules for Rayman"""

from rule_builder.rules import Has, True_

none = True_()

# Powers
has_fist = Has("Telescopic Fist")
has_hang = Has("Hanging")
has_grappling_fist = Has("Grappling Fist")
has_helicopter = Has("Helicopter")

# Special items
has_magic_seed = Has("Magic Seed")

# Level access

### Combine thoses rules with the one above when
### the time comes to add the unlock items
# can_access_pink_plant_wood = True_()
# can_access_anguish_lagoon = Has("Anguish Lagoon Unlock")
# can_access_swamps_of_forgetfulness = Has("The Swamps of Forgetfulness Unlock")
# can_acess_moskito_nest = Has("Moskito's Nest Unlock")

can_access_pink_plant_wood = True_()
can_access_anguish_lagoon = Has("Pink Plant Woods finished event item")
can_access_swamps_of_forgetfulness = Has("Anguish Lagoon finished event item")
can_acess_moskito_nest = Has("The Swamps of Forgetfulness finished event item")
