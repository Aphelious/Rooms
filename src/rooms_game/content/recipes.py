# Recipes describe what happens when items are brought together via 'use' or 'combine'.
# They are intentionally kept SEPARATE from item definitions because an interaction is
# inherently BETWEEN items and belongs to no single one.
#
# RECIPE SCHEMA
#   requires   set of item ids that must ALL be active for the recipe to fire.
#   consumes   subset of `requires` that is deactivated on success. Anything in
#              `requires` but NOT in `consumes` is a reusable catalyst (e.g. the lighter).
#   produces   {item id: "activate"} - items created/revealed on success.
#   message    success narration shown to the player.
#   hint       (optional) near-miss narration shown when the player's combined set
#              matches ALL BUT ONE of `requires`. Encourages discovery.
#
# Order does not matter: `requires` is a set, so "use A on B" and "use B on A"
# resolve to the same recipe.

recipes = [
    # Reassemble the torn note from its two halves.
    {
        'requires': {'Torn Paper 1', 'Torn Paper 2'},
        'consumes': {'Torn Paper 1', 'Torn Paper 2'},
        'produces': {'Full Paper': 'activate'},
        'message': 'You align the torn edges and the two halves fit together perfectly, '
                   'forming a single, whole parchment.',
        'hint': 'You get the feeling this fragment is only part of something larger.',
    },

    # Burning paper: each is consumed and leaves ash. The lighter survives (catalyst).
    {
        'requires': {'Lighter', 'Torn Paper 1'},
        'consumes': {'Torn Paper 1'},
        'produces': {'Ash': 'activate'},
        'message': 'The flame catches the parchment and devours it until nothing remains but ash.',
    },
    {
        'requires': {'Lighter', 'Torn Paper 2'},
        'consumes': {'Torn Paper 2'},
        'produces': {'Ash': 'activate'},
        'message': 'The flame catches the parchment and devours it until nothing remains but ash.',
    },
    {
        'requires': {'Lighter', 'Full Paper'},
        'consumes': {'Full Paper'},
        'produces': {'Ash': 'activate'},
        'message': 'The flame catches the parchment and devours it until nothing remains but ash. '
                   'Whatever it said is gone now.',
    },

    # Fuse the broken key: needs both fragments, wire (consumed as solder),
    # and the lighter (reusable heat source, NOT consumed).
    {
        'requires': {'Metal Key Fragment 1', 'Metal Key Fragment 2', 'Metal Wire', 'Lighter'},
        'consumes': {'Metal Key Fragment 1', 'Metal Key Fragment 2', 'Metal Wire'},
        'produces': {'Metal Key': 'activate'},
        'message': 'You hold the fragments together and play the flame over the wire until it '
                   'melts into the seam. As it cools, the pieces are one: a whole key.',
        'hint': 'The fragments line up, but the join won\'t hold without heat and something to fuse it with.',
    },

    # Open the lock with the repaired key. The lock is deactivated (opened).
    {
        'requires': {'Metal Key', 'Metal Lock'},
        'consumes': {'Metal Lock'},
        'produces': {},
        'message': 'The key turns three times and the lock springs open with a satisfying clunk.',
    },
]
