from malleablec2 import Profile
from lark import Visitor, Tree
from typing import Union

class ProfileRandomizer(Visitor):
    def visit(self, profile_or_tree: Union[Profile, Tree]):
        if isinstance(profile_or_tree, Profile) and hasattr(profile_or_tree, "ast"):
            return super().visit(profile_or_tree.ast)

        return super().visit(profile_or_tree)

    def randomize(self, profile: Profile):
        return self.visit(profile)