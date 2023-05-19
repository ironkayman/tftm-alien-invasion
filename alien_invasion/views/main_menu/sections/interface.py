from abc import ABC
from functools import partial
from pathlib import Path

import arcade as arc

# why simple import?
import arcade.gui
from arcade.gui.events import UIEvent, UIKeyPressEvent, UIKeyReleaseEvent, UIMouseEvent
from pyglet.event import EVENT_HANDLED, EVENT_UNHANDLED

from alien_invasion import CONSTANTS
from alien_invasion.constants import DISPLAY
from alien_invasion.settings import KEYMAP
from alien_invasion.utils.loaders.level import loader as load_level_configs
from alien_invasion.views import Invasion


class CallbackButton(arc.gui.UIFlatButton, ABC):
    """Abstract class for buttons with callback"""

    SOUND = arc.Sound(CONSTANTS.DIR_MUSIC / "menu_button_press.opus", streaming=False)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.click_callback = kwargs["click_callback"]
        self.ui_state = "main_menu"
        self.scale(CONSTANTS.DISPLAY.SCALE_RELATION)

    def on_event(self, event: UIEvent) -> bool | None:
        """Override method of event processing since we dont need Mouse control"""
        if isinstance(event, UIMouseEvent):
            return EVENT_HANDLED

        if (
            self.hovered
            and isinstance(event, UIKeyPressEvent)
            and event.symbol == KEYMAP["confirm"]
        ):
            self.pressed = True
            return EVENT_HANDLED

        if (
            self.pressed
            and self.hovered
            and isinstance(event, UIKeyReleaseEvent)
            and event.symbol == KEYMAP["confirm"]
        ):
            self.pressed = False
            # Dispatch new on_click event, source is this widget itself
            self.dispatch_event("on_event", UIKeyPressEvent(self, KEYMAP["confirm"], 0))  # type: ignore
            self.SOUND.play(volume=0.4)
            self.click_callback()
            return EVENT_HANDLED

        if (
            self.hovered
            and isinstance(event, UIKeyPressEvent)
            and event.symbol == KEYMAP["confirm"]
        ):
            return self.dispatch_event("on_click", event)

        if super().on_event(event):
            return EVENT_HANDLED

        return EVENT_UNHANDLED


class KeyTextArea(arc.gui.UITextArea, ABC):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # self.click_callback = kwargs['click_callback']
        self.hovered = False

    def on_event(self, event: UIEvent) -> bool:
        if not self.hovered:
            return EVENT_HANDLED
        if isinstance(event, UIKeyPressEvent):
            if event.symbol == arc.key.UP:
                self.layout.view_y += 3 * self.scroll_speed
            elif event.symbol == arc.key.DOWN:
                self.layout.view_y += -3 * self.scroll_speed
            else:
                return EVENT_HANDLED
            self.trigger_full_render()
            return EVENT_HANDLED
        # elif isinstance(event, UIKeyReleaseEvent):
        #     self.layout.view_y += event.scroll_y * self.scroll_speed
        #     self.trigger_full_render()

        # if super().on_event(event):
        #     return EVENT_HANDLED

        return EVENT_UNHANDLED


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
        arc.Section.__init__(self, left, bottom, width, height, **kwargs)
        arc.Scene.__init__(self)

        self.manager = arc.gui.UIManager(self.view)

        self._create_start_menu()

    def _create_start_menu(self) -> None:
        self.manager.clear()
        self.ui_state = "start_menu"
        # Create a vertical BoxGroup to align buttons
        start_menu = arc.gui.UIBoxLayout()

        start_button = CallbackButton(
            text="Mission Select",
            width=150,
            height=40,
            click_callback=self._create_level_select_menu,
        )
        start_menu.add(
            start_button.with_space_around(
                bottom=20 * CONSTANTS.DISPLAY.SCALE_RELATION,
            )
        )

        quit_button = CallbackButton(
            text="Quit", width=150, height=40, click_callback=self.__deploy_exit
        )
        start_menu.add(quit_button)

        # Create a widget to hold the menu widget, that will center the buttons
        self.manager.add(
            arc.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-20 * CONSTANTS.DISPLAY.SCALE_RELATION,
                child=start_menu,
            )
        )

    def _create_level_select_menu(self) -> None:
        self.manager.clear()
        self.ui_state = "level_selection"

        level_select = arc.gui.UIBoxLayout()
        for level in load_level_configs():
            level_button = CallbackButton(
                width=150,
                height=40,
                text=level[0]["display_name"],
                # partial fixes 2 problems:
                # 1. pointer for level variable changes
                # for previos oteration to the last one
                # 2. we had to pass level dict object
                # into a deployed view
                click_callback=partial(
                    self.__deploy_view_invasion_with_level, level_config=level
                ),
            ).with_space_around(10 * CONSTANTS.DISPLAY.SCALE_RELATION)
            level_select.add(
                level_button,
            )

        self.manager.add(
            arc.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=level_select,
            )
        )

    def __deploy_view_invasion_with_level(
        self, level_config: tuple[dict, Path]
    ) -> None:
        """Callback funct for starting Invasion view."""
        invasion_view = Invasion(self.view, mission_config=level_config)
        self.window.show_view(invasion_view)

    def __deploy_exit(self) -> None:
        """Callback func for Exiting Arcade."""
        self.view.on_hide_view()
        arc.exit()

    def get_widget(self) -> CallbackButton:
        for index, widget_from_tree in enumerate(
            filter(lambda w: isinstance(w, CallbackButton), self.manager.walk_widgets())
        ):
            if index == self.selected_index:
                return widget_from_tree

    def reset_widget_selection(self) -> None:
        for widget_from_tree in self.manager.walk_widgets():
            if getattr(widget_from_tree, "pressed", None):
                widget_from_tree.pressed = False
            widget_from_tree.hovered = False

    def widget_next(self) -> None:
        for index, widget_from_tree in enumerate(
            filter(lambda w: isinstance(w, CallbackButton), self.manager.walk_widgets())
        ):
            if index + 1 == self.selected_index and isinstance(
                widget_from_tree, CallbackButton
            ):
                self.selected_index = index
                return widget_from_tree

    def widget_prev(self) -> None:
        for index, widget_from_tree in enumerate(
            filter(lambda w: isinstance(w, CallbackButton), self.manager.walk_widgets())
        ):
            if index - 1 == self.selected_index:
                self.selected_index = index
                return widget_from_tree

    def draw(self) -> None:
        self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Process standard keyboard input."""
        # event = UIKeyEvent(self, symbol, 0)
        if symbol == KEYMAP["back"]:
            CallbackButton.SOUND.play(volume=0.4)
            if self.ui_state == "level_selection":
                self._create_start_menu()

        widget = self.get_widget()

        if symbol == arc.key.DOWN:
            widget = self.widget_next()
        elif symbol == arc.key.UP:
            widget = self.widget_prev()

        if widget:
            self.reset_widget_selection()
            widget.hovered = True
            # firther interactions are passed directrly to CallbackButtons
