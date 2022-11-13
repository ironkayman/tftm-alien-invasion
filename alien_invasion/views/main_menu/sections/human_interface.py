from enum import IntEnum, auto

import arcade as arc
# why simple import?
import arcade.gui

from alien_invasion.constants import DISPLAY
from alien_invasion.settings import KEYMAP
from alien_invasion.views import Invasion


class EnumButton(IntEnum):
    """Custom Button IDs (.bid) for custom button widgets."""
    START = auto()
    QUIT = auto()


class QuitButton(arc.gui.UIFlatButton):
    bid = EnumButton.QUIT

    def on_click(self, event: arc.gui.UIOnClickEvent):
        print('Exiting ...')
        arc.exit()


class StartButton(arc.gui.UIFlatButton):
    bid = EnumButton.START

    def on_click(self, event: arc.gui.UIOnClickEvent):
        print("Starting ...", event)
        invasion_view = Invasion()
        invasion_view.setup()
        # TODO: call prototype parent until window attr? functools.reduce?
        root = self.parent.parent.parent
        root.window.show_view(invasion_view)


class HumanInterface(arc.Section):
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
        super().__init__(
            left,
            bottom,
            width,
            height,
            **kwargs
        )

        # a UIManager to handle the UI
        self.manager = arc.gui.UIManager(self.view)
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.menu = arc.gui.UIBoxLayout()

        start_button = StartButton(text="Start Game", width=200)
        self.menu.add(start_button)#.with_space_around(bottom=20))

        quit_button = QuitButton(text="Quit", width=200)
        self.menu.add(quit_button)

        # Create a widget to hold the menu widget, that will center the buttons
        self.manager.add(
            arc.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.menu,
            )
        )

        start_button.hovered = True
        print('children:', self.menu.children)
        print(self.selected_widget)

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

    def on_draw(self) -> None:
        self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Process standard keyboard input."""
        if symbol == arc.key.DOWN:
            self.selected_widget = self.selected_widget_id() + 1
            # self.view.background.center_y -= 12
        elif symbol == arc.key.UP:
            self.selected_widget = self.selected_widget_id() - 1
            # self.view.background.center_y += 12
        elif symbol == arc.key.ENTER:
            self.selected_widget.on_click(arc.gui.UIOnClickEvent)