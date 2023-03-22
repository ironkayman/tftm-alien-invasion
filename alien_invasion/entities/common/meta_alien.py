import arcade as arc

class MetaAlien(arc.Particle):


    def __init__(self, spawner: arc.Emitter, **particle_kwargs) -> None:
        super().__init__(**particle_kwargs)

        self._loadout: 

        self.hp = property(doc="""
        """)
        self.speed = property(doc="""
        """)

        self.primary = property(doc="""
            Object representation of primary weapon
        """)
        self.secondary = property(doc="""
            Object containing array of secondary weapons
        """)

        self.energy = property(doc="""
            Abstraction above Engine loadout object
        """)
        self.cosmic_alignments = property(doc="""
            Dict of cosmic alignmets with high-concept elements based on loadout
        """)

        # Emmiters sprite list
        self._spawner = spawner
        self._spawner_sprite_list: arc.SpriteList = spawner._particles