## Player / Starship
Consists of 5 componsnts:
- __hull__

    Base for a ship, defines armor and secondary weapons' mount slots

- __engine__

    Managers produstion of energy to sustain the ship. Every active component by default
    drains energy, engine restores it.
    If energy reaches `0`, the ship fallbacks in **free fall** state. 

- __thrusters__

    Control ship's movement.

    Normally allows moving left or right. When reaching a border allow going insiode of it at `1/3` thrusters speed stopping when `1/3` of ship's width is iinside the boundry. Exiting the boundary also is made under `1/3` of thrusters' speed. 

- __armor__

    Maximum amount is defined by selected hull

- __primary weapon__

    Only single primary weapon mount allowed.

    Pressing both L/R and firing cuases primary weapon to **rapid fire** an `2/3` of its usual cooldown timing for a same energy per shot.

- __secondary weapons__

    Maximum amount is defined by selected hull.

    During **rapid fire** cooldowns of all secondary weapons are `4/3` of their usual timeouts.

### **Free Fall** state/power outage
If engine's energy reaches `o` all components are shut down (firing not possible),
requiring manual reactivation once enough energy is restoread and `0.5 sec` passed. Free falling makes ship float in a last thruster move drection and bouncing of the borders (without slowing down or going inside the border) at `1/3` thrusters speed.

If there's energy, free wall will continue since it requires manually moving left or right. Firing during free fall is possible if there's enought energy but it won't stop ship itself from continuesly floating.