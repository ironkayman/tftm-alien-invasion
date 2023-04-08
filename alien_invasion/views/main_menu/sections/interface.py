from abc import ABC
from enum import IntEnum, auto

import arcade as arc
# why simple import?
import arcade.gui

from alien_invasion.constants import DISPLAY
from alien_invasion.settings import KEYMAP
from alien_invasion.views import Invasion


class EnumButton(IntEnum):
    """Custom Button IDs (.bid) for custom button widgets."""
    SELECT_MISSION = auto()
    QUIT = auto()
    LAUNCH_MISSION = auto()
    BACK = auto()


class CallbackButton(arc.gui.UIFlatButton, ABC):
    """Abstract class for buttons with callback"""
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.click_callback = kwargs['click_callback']

    def on_click(self, event: arc.gui.UIOnClickEvent):
        self.click_callback()


class QuitButton(CallbackButton):
    """Exit."""
    bid = EnumButton.QUIT


class SelectMissionButton(CallbackButton):
    """Start gameplay loop."""
    bid = EnumButton.SELECT_MISSION

class LaunchMissionButton(CallbackButton):
    """Start gameplay loop."""
    bid = EnumButton.LAUNCH_MISSION


class Interface(arc.Section, arc.Scene):
    """Logic and interface for main menu buttons"""

    def __init__(
        self,
        left: int,
        bottom: int,
        width: int,
        height: int,
        **kwargs,
    ) -> None:
        """Initialise UIManager and register custom buttons."""
        # Manual MRO resolution
        arc.Section.__init__(self,
            left,
            bottom,
            width,
            height,
            **kwargs
        )
        arc.Scene.__init__(self)

        self.manager = arc.gui.UIManager(self.view)
        # enabling moved to parent View

        # Create a vertical BoxGroup to align buttons
        self.menu = arc.gui.UIBoxLayout()

        start_button = LaunchMissionButton(text="Start Game", width=200,
            click_callback=self.__deploy_view_invasion)
        self.menu.add(start_button.with_space_around(bottom=20))

        quit_button = QuitButton(text="Quit", width=200,
            click_callback=self.__deploy_exit)
        self.menu.add(quit_button)

        # Create a widget to hold the menu widget, that will center the buttons
        self.manager.add(arc.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.menu,
        ))

        start_button.hovered = True

    def __deploy_view_invasion(self) -> None:
        """Callback funct for starting Invasion view."""
        invasion_view = Invasion(self.view)
        invasion_view.setup()
        self.window.show_view(invasion_view)

    def __deploy_exit(self) -> None:
        """Callback func for Exiting Arcade."""
        arc.exit()

    @property
    def selected_widget(self) -> arc.gui.UIWidget|None:
        """Get selected/first `hovered` widget.
        
        Selected widget is defined by `hovered=True` state.
        This condition and built upon it logic
        requires no more than 1 `hovered` widget.
        Also checks that its custom widget with `bid`
        attribute from `EnumButton`.

        Returns
        -------
        UIWidget
            Returns first found `hovered=True` state widget
            from iteration over `IUManager.walk_widgets()`.
        """
        # filter all, since its an iterator, turn it into list,
        # if none, make a failsafe list from 1 element: [None]
        # then select [0]'th element -> None or UIWidget
        return (
            [*filter(
                lambda wdg: getattr(wdg, 'hovered', False) and hasattr(wdg, 'bid'),
                self.manager.walk_widgets()
            )] or
            [None]
        )[0]

    @selected_widget.setter
    def selected_widget(self, widget: arc.gui.UIWidget|int) -> None:
        """Select new widget as active.
        
        Selected widget is defined by `hovered=True` state.
        This condition and built upon it logic
        requires no more than 1 `hovered` widget.

        Paramters
        ---------
        widget: arc.gui.UIWidget|int
            `UIWidget` instance or its `bid` from `EnumButton`.
        """
        found = None
        for widget_from_tree in self.manager.walk_widgets():
            # UIFlatButton untested
            if (
                isinstance(widget, arc.gui.UIFlatButton)
                and widget_from_tree == widget
            ):
                found = widget_from_tree
            # or search by .bid
            elif (
                isinstance(widget, int)
                and (bid := getattr(widget_from_tree, 'bid', False))
                and bid == widget
            ):
                found = widget_from_tree

            if found:
                # clean previous selection
                if (selected:= self.selected_widget) is not None:
                    selected.hovered = False
                # activate new selection
                found.hovered = True
                break

    def selected_widget_id(self) -> int:
        """Get selected widget `bid`.

        Returns
        -------
        int
            Interractable widget with `bid`.
            If no selected widget found return `-1`.
        """
        return self.selected_widget.bid if self.selected_widget else -1

    def draw(self) -> None:
        self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Process standard keyboard input."""
        if symbol == arc.key.DOWN:
            self.selected_widget = self.selected_widget_id() + 1 if self.selected_widget_id() >= 0 else len(EnumButton)
            # self.view.background.center_y -= 12
        elif symbol == arc.key.UP:
            self.selected_widget = self.selected_widget_id() - 1 if self.selected_widget_id() >= 0 else 1
            # self.view.background.center_y += 12
        elif symbol == arc.key.ENTER:
            self.selected_widget.on_click(arc.gui.UIOnClickEvent)