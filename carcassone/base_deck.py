import os
from .game.connection import Connection
from .game.farmer_connection import FarmerConnection
from .game.side import Side
from .game.tile import Tile
from .game.farmer_side import FarmerSide

base_tiles = {
    "chapel_with_road": Tile(
        description="chapel_with_road",
        road=[Connection(Side.BOTTOM, Side.CENTER)],
        grass=[Side.LEFT, Side.TOP, Side.RIGHT],
        chapel=True,
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT,
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL, FarmerSide.TLT,
                    FarmerSide.TRT, FarmerSide.TRR,
                    FarmerSide.BRR, FarmerSide.BRB,
                    FarmerSide.BLB, FarmerSide.BLL
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_A.png")
    ),
    "chapel": Tile(
        description="chapel",
        grass=[Side.TOP, Side.RIGHT, Side.BOTTOM, Side.LEFT],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT,
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL, FarmerSide.TLT,
                    FarmerSide.TRT, FarmerSide.TRR,
                    FarmerSide.BRR, FarmerSide.BRB,
                    FarmerSide.BLB, FarmerSide.BLL
                ]
            )
        ],
        chapel=True,
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_B.png")
    ),
    "full_city_with_shield": Tile(
        description="full_city_with_shield",
        city=[[Side.TOP, Side.RIGHT, Side.BOTTOM, Side.LEFT]],
        shield=True,
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_C.png")
    ),
    "city_top_straight_road": Tile(
        description="city_top_straight_road",
        road=[Connection(Side.LEFT, Side.RIGHT)],
        city=[[Side.TOP]],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL, FarmerSide.TLT,
                    FarmerSide.TRT, FarmerSide.TRR
                ],
                city_sides=[
                    Side.TOP
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRR, FarmerSide.BRB,
                    FarmerSide.BLB, FarmerSide.BLL
                ]
            )
        ],
        grass=[Side.BOTTOM],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_D.png")
    ),
    "city_top": Tile(
        description="city_top",
        city=[[Side.TOP]],
        grass=[Side.RIGHT, Side.BOTTOM, Side.LEFT],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT,
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL,
                    FarmerSide.TRR,
                    FarmerSide.BRR, FarmerSide.BRB,
                    FarmerSide.BLB, FarmerSide.BLL
                ],
                city_sides=[
                    Side.TOP
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_E.png")
    ),
    "city_narrow_shield": Tile(
        description="city_narrow_shield",
        city=[[Side.LEFT, Side.RIGHT]],
        grass=[Side.TOP, Side.BOTTOM],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLT,
                    FarmerSide.TRT
                ],
                city_sides=[
                    Side.LEFT, Side.RIGHT
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRB,
                    FarmerSide.BLB
                ],
                city_sides=[
                    Side.LEFT, Side.RIGHT
                ]
            )
        ],
        shield=True,
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_F.png")
    ),
    "city_narrow": Tile(
        description="city_narrow",
        city=[[Side.LEFT, Side.RIGHT]],
        grass=[Side.TOP, Side.BOTTOM],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLT,
                    FarmerSide.TRT
                ],
                city_sides=[
                    Side.LEFT, Side.RIGHT
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRB,
                    FarmerSide.BLB
                ],
                city_sides=[
                    Side.LEFT, Side.RIGHT
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_G.png")
    ),
    "city_left_right": Tile(
        description="city_left_right",
        city=[[Side.LEFT], [Side.RIGHT]],
        grass=[Side.TOP, Side.BOTTOM, Side.CENTER],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT,
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLT,
                    FarmerSide.TRT,
                    FarmerSide.BRB,
                    FarmerSide.BLB,
                ],
                city_sides=[
                    Side.LEFT,
                    Side.RIGHT
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_H.png")
    ),
    "city_top_right": Tile(
        description="city_top_right",
        city=[[Side.TOP], [Side.RIGHT]],
        grass=[Side.LEFT, Side.BOTTOM, Side.CENTER],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT,
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL,
                    FarmerSide.BRB,
                    FarmerSide.BLB, FarmerSide.BLL
                ],
                city_sides=[
                    Side.TOP,
                    Side.RIGHT
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_I.png")
    ),
    "city_top_road_bend_right": Tile(
        description="city_top_road_bend_right",
        city=[[Side.TOP]],
        road=[Connection(Side.BOTTOM, Side.RIGHT)],
        grass=[Side.LEFT],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT,
                    Side.BOTTOM_LEFT
                ],
                tile_connections=[
                    FarmerSide.TLL,
                    FarmerSide.TRR,
                    FarmerSide.BLB, FarmerSide.BLL
                ],
                city_sides=[
                    Side.TOP
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRR,
                    FarmerSide.BRB
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_J.png")
    ),
    "city_top_road_bend_left": Tile(
        description="city_top_road_bend_left",
        city=[[Side.TOP]],
        road=[Connection(Side.BOTTOM, Side.LEFT)],
        grass=[Side.RIGHT],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL,
                    FarmerSide.TRR,
                    FarmerSide.BRB, FarmerSide.BRR
                ],
                city_sides=[
                    Side.TOP
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT
                ],
                tile_connections=[
                    FarmerSide.BLL,
                    FarmerSide.BLB
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_K.png")
    ),
    "city_top_crossroads": Tile(
        description="city_top_crossroads",
        city=[[Side.TOP]],
        road=[
            Connection(Side.BOTTOM, Side.CENTER),
            Connection(Side.LEFT, Side.CENTER),
            Connection(Side.RIGHT, Side.CENTER)
        ],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL,
                    FarmerSide.TRR,
                ],
                city_sides=[
                    Side.TOP
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT
                ],
                tile_connections=[
                    FarmerSide.BLL,
                    FarmerSide.BLB
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRB,
                    FarmerSide.BRR
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_L.png")
    ),
    "city_diagonal_top_right_shield": Tile(
        description="city_diagonal_top_right_shield",
        city=[[Side.TOP, Side.RIGHT]],
        grass=[Side.LEFT, Side.BOTTOM],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL,
                    FarmerSide.BLB, FarmerSide.BLL,
                    FarmerSide.BRB
                ],
                city_sides=[
                    Side.TOP,
                    Side.RIGHT
                ]
            )
        ],
        shield=True,
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_M.png")
    ),
    "city_diagonal_top_right": Tile(
        description="city_diagonal_top_right",
        city=[[Side.TOP, Side.RIGHT]],
        grass=[Side.LEFT, Side.BOTTOM],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL,
                    FarmerSide.BLB, FarmerSide.BLL,
                    FarmerSide.BRB
                ],
                city_sides=[
                    Side.TOP,
                    Side.RIGHT
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_N.png")
    ),
    "city_diagonal_top_left_shield_road": Tile(
        description="city_diagonal_top_left_shield_road",
        road=[Connection(Side.BOTTOM, Side.RIGHT)],
        city=[[Side.TOP, Side.LEFT]],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT,
                    Side.TOP_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BLB,
                    FarmerSide.TRR
                ],
                city_sides=[
                    Side.TOP,
                    Side.LEFT
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRR,
                    FarmerSide.BRB
                ]
            )
        ],
        shield=True,
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_O.png")
    ),
    "city_diagonal_top_left_road": Tile(
        description="city_diagonal_top_left_shield_road",
        road=[Connection(Side.BOTTOM, Side.RIGHT)],
        city=[[Side.TOP, Side.LEFT]],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT,
                    Side.TOP_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BLB,
                    FarmerSide.TRR
                ],
                city_sides=[
                    Side.TOP,
                    Side.LEFT
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRR,
                    FarmerSide.BRB
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_P.png")
    ),
    "city_bottom_grass_shield": Tile(
        description="city_bottom_grass_shield",
        city=[[Side.TOP, Side.LEFT, Side.RIGHT]],
        grass=[Side.BOTTOM],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BLB,
                    FarmerSide.BRB
                ],
                city_sides=[
                    Side.TOP,
                    Side.LEFT,
                    Side.RIGHT
                ]
            )
        ],
        shield=True,
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_Q.png")
    ),
    "city_bottom_grass": Tile(
        description="city_bottom_grass",
        city=[[Side.TOP, Side.LEFT, Side.RIGHT]],
        grass=[Side.BOTTOM],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BLB,
                    FarmerSide.BRB
                ],
                city_sides=[
                    Side.TOP,
                    Side.LEFT,
                    Side.RIGHT
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_R.png")
    ),
    "city_bottom_road_shield": Tile(
        description="city_bottom_road_shield",
        city=[[Side.TOP, Side.LEFT, Side.RIGHT]],
        road=[Connection(Side.BOTTOM, Side.CENTER)],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT
                ],
                tile_connections=[
                    FarmerSide.BLB
                ],
                city_sides=[
                    Side.TOP,
                    Side.LEFT,
                    Side.RIGHT
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRB
                ],
                city_sides=[
                    Side.TOP,
                    Side.LEFT,
                    Side.RIGHT
                ]
            )
        ],
        shield=True,
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_S.png")
    ),
    "city_bottom_road": Tile(
        description="city_bottom_road",
        city=[[Side.TOP, Side.LEFT, Side.RIGHT]],
        road=[Connection(Side.BOTTOM, Side.CENTER)],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT
                ],
                tile_connections=[
                    FarmerSide.BLB
                ],
                city_sides=[
                    Side.TOP,
                    Side.LEFT,
                    Side.RIGHT
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRB
                ],
                city_sides=[
                    Side.TOP,
                    Side.LEFT,
                    Side.RIGHT
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_T.png")
    ),
    "straight_road": Tile(
        description="straight_road",
        road=[Connection(Side.BOTTOM, Side.TOP)],
        grass=[Side.LEFT, Side.RIGHT],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.BOTTOM_LEFT
                ],
                tile_connections=[
                    FarmerSide.TLL, FarmerSide.TLT,
                    FarmerSide.BLB, FarmerSide.BLL
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_RIGHT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TRR, FarmerSide.TRT,
                    FarmerSide.BRR, FarmerSide.BRB
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_U.png")
    ),
    "bent_road": Tile(
        description="bent_road",
        road=[Connection(Side.LEFT, Side.BOTTOM)],
        grass=[Side.TOP, Side.RIGHT],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT
                ],
                tile_connections=[
                    FarmerSide.BLB, FarmerSide.BLL
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT,
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL, FarmerSide.TLT,
                    FarmerSide.TRR, FarmerSide.TRT,
                    FarmerSide.BRB, FarmerSide.BRR
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_V.png")
    ),
    "three_split_road": Tile(
        description="three_split_road",
        road=[
            Connection(Side.BOTTOM, Side.CENTER),
            Connection(Side.LEFT, Side.CENTER),
            Connection(Side.RIGHT, Side.CENTER)
        ],
        grass=[Side.TOP],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT
                ],
                tile_connections=[
                    FarmerSide.BLB, FarmerSide.BLL
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRB, FarmerSide.BRR
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT,
                    Side.TOP_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TLL, FarmerSide.TLT,
                    FarmerSide.TRR, FarmerSide.TRT
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_W.png")
    ),
    "crossroads": Tile(
        description="crossroads",
        road=[
            Connection(Side.BOTTOM, Side.CENTER),
            Connection(Side.LEFT, Side.CENTER),
            Connection(Side.RIGHT, Side.CENTER),
            Connection(Side.TOP, Side.CENTER)
        ],
        farms=[
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_LEFT
                ],
                tile_connections=[
                    FarmerSide.BLB, FarmerSide.BLL
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.BOTTOM_RIGHT
                ],
                tile_connections=[
                    FarmerSide.BRB, FarmerSide.BRR
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_LEFT
                ],
                tile_connections=[
                    FarmerSide.TLL, FarmerSide.TLT
                ]
            ),
            FarmerConnection(
                farmer_positions=[
                    Side.TOP_RIGHT
                ],
                tile_connections=[
                    FarmerSide.TRR, FarmerSide.TRT
                ]
            )
        ],
        image=os.path.join("default_tiles", "Base_Game_C2_Tile_X.png")
    )
}

base_tile_counts = {
    "chapel_with_road": 2,
    "chapel": 4,
    "full_city_with_shield": 1,
    "city_top_straight_road": 4,
    "city_top": 5,
    "city_narrow_shield": 2,
    "city_narrow": 1,
    "city_left_right": 3,
    "city_top_right": 2,
    "city_top_road_bend_right": 3,
    "city_top_road_bend_left": 3,
    "city_top_crossroads": 3,
    "city_diagonal_top_right_shield": 2,
    "city_diagonal_top_right": 3,
    "city_diagonal_top_left_shield_road": 2,
    "city_diagonal_top_left_road": 3,
    "city_bottom_grass_shield": 1,
    "city_bottom_grass": 3,
    "city_bottom_road_shield": 2,
    "city_bottom_road": 1,
    "straight_road": 8,
    "bent_road": 9,
    "three_split_road": 4,
    "crossroads": 1
}