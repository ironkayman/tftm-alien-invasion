from abc import ABC
from enum import IntEnum, auto

import arcade as arc
# why simple import?
import arcade.gui
from arcade.gui.events import (
    UIEvent,
    UIKeyEvent,
    UIKeyPressEvent,
    UIKeyReleaseEvent,
    UIMouseEvent,
)
from pyglet.event import (
    EVENT_HANDLED,
    EVENT_UNHANDLED,
)


from alien_invasion import CONSTANTS

from alien_invasion.constants import DISPLAY
from alien_invasion.settings import KEYMAP
from alien_invasion.views import Invasion


class EnumButton(IntEnum):
    """Custom Button IDs (.sid) for custom button widgets."""
    SELECT_MISSION = auto()
    QUIT = auto()

    LAUNCH_MISSION = auto()
    BACK = auto()


class EnumButtonGroup(IntEnum):
    menu = auto()


class CallbackButton(arc.gui.UIFlatButton, ABC):
    """Abstract class for buttons with callback"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.click_callback = kwargs['click_callback']

    def on_event(self, event: UIEvent) -> bool|None:
        """Override method of event processing since we dont need Mouse control
        """
        if isinstance(event, UIMouseEvent):
            return EVENT_HANDLED

        # if isinstance(event, UIMouseMovementEvent):
        #     self.hovered = self.rect.collide_with_point(event.x, event.y)

        if self.hovered and isinstance(event, UIKeyPressEvent) and event.symbol == KEYMAP['confirm']:
            self.pressed = True
            return EVENT_HANDLED

        if self.pressed and self.hovered and isinstance(event, UIKeyReleaseEvent) and event.symbol == KEYMAP['confirm']:
            self.pressed = False
            # Dispatch new on_click event, source is this widget itself
            self.dispatch_event("on_event", UIKeyPressEvent(self, KEYMAP['confirm'], 0))  # type: ignore
            self.click_callback()
            return EVENT_HANDLED

        if self.hovered and isinstance(event, UIKeyPressEvent) and event.symbol == KEYMAP['confirm']:
            return self.dispatch_event("on_click", event)

        if super().on_event(event):
            return EVENT_HANDLED

        return EVENT_UNHANDLED


class QuitButton(CallbackButton):
    """Exit."""
    sid = EnumButton.QUIT


class SelectMissionButton(CallbackButton):
    """Start gameplay loop."""
    sid = EnumButton.SELECT_MISSION

class LaunchMissionButton(CallbackButton):
    """Start gameplay loop."""
    sid = EnumButton.LAUNCH_MISSION


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

        start_button = LaunchMissionButton(
            text="Start Game",
            width=150 * CONSTANTS.DISPLAY.SCALE_RELATION,
            height=40 * CONSTANTS.DISPLAY.SCALE_RELATION,
            click_callback=self.__deploy_view_invasion)
        self.menu.add(start_button.with_space_around(
            bottom=20 * CONSTANTS.DISPLAY.SCALE_RELATION
        ))

        quit_button = QuitButton(
            text="Quit",
            width=150 * CONSTANTS.DISPLAY.SCALE_RELATION,
            height=40 * CONSTANTS.DISPLAY.SCALE_RELATION,
            click_callback=self.__deploy_exit)
        self.menu.add(quit_button)

        # Create a widget to hold the menu widget, that will center the buttons
        self.manager.add(arc.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=-20 * CONSTANTS.DISPLAY.SCALE_RELATION,
            child=self.menu,
        ))


    def __deploy_view_invasion(self) -> None:
        """Callback funct for starting Invasion view."""
        invasion_view = Invasion(self.view)
        invasion_view.setup()
        self.window.show_view(invasion_view)

    def __deploy_exit(self) -> None:
        """Callback func for Exiting Arcade."""
        arc.exit()

    def get_widget(self) -> CallbackButton:
        for index, widget_from_tree in enumerate(filter(lambda w: isinstance(w, CallbackButton), self.manager.walk_widgets())):
            if index == self.selected_index:
                return widget_from_tree

    def reset_widget_selection(self) -> None:
        for widget_from_tree in self.manager.walk_widgets():
            if getattr(widget_from_tree, 'pressed', None):
                widget_from_tree.pressed = False
            widget_from_tree.hovered = False

    def widget_next(self) -> None:
        for index, widget_from_tree in enumerate(filter(lambda w: isinstance(w, CallbackButton), self.manager.walk_widgets())):
            if index + 1 == self.selected_index and isinstance(widget_from_tree, CallbackButton):
                self.selected_index = index
                return widget_from_tree

    def widget_prev(self) -> None:
        for index, widget_from_tree in enumerate(filter(lambda w: isinstance(w, CallbackButton), self.manager.walk_widgets())):
            if index - 1 == self.selected_index:
                self.selected_index = index
                return widget_from_tree

    def draw(self) -> None:
        self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Process standard keyboard input."""
        # event = UIKeyEvent(self, symbol, 0)
        widget = self.get_widget()

        if symbol == arc.key.DOWN:
            widget = self.widget_next()
        elif symbol == arc.key.UP:
            widget = self.widget_prev()

        if widget:
            self.reset_widget_selection()
            widget.hovered = True
            # firther interactions are passed directrly to CallbackButtons
