"""GUI smoke tests — Tk 위젯 생성·도메인 연동 검증 (이벤트 루프 없음)."""

import pytest

pytest.importorskip("tkinter")

import tkinter as tk
from unittest.mock import patch

from unit_converter.gui import UnitConverterApp


@pytest.fixture(scope="module")
def tk_root():
    try:
        root = tk.Tk()
        root.withdraw()
    except tk.TclError as exc:
        pytest.skip(f"tkinter unavailable: {exc}")
    yield root
    root.destroy()


@pytest.fixture
def gui_app(tk_root, registry):
    return UnitConverterApp(tk_root, registry=registry)


class TestGuiSmoke:
    """unit_converter/gui.py — 수동 Mom Test 보조 자동 검증"""

    def test_gui_convert_shows_results(self, gui_app):
        gui_app.unit_var.set("meter")
        gui_app.value_var.set("2.5")
        gui_app._on_convert()

        rows = gui_app.tree.get_children()
        assert len(rows) == 2
        values = {gui_app.tree.item(r)["values"][0] for r in rows}
        assert values == {"feet", "yard"}

    def test_gui_rejects_negative_value(self, gui_app):
        gui_app.unit_var.set("meter")
        gui_app.value_var.set("-1")
        gui_app._on_convert()

        assert gui_app.tree.get_children() == ()
        assert "Negative values are not allowed." in gui_app.status_var.get()

    def test_gui_register_invalid_format(self, gui_app):
        gui_app.register_var.set("cubit = 1 meter")
        with patch("unit_converter.gui.messagebox.showerror") as show_error:
            gui_app._on_register()
        show_error.assert_called_once()
        assert "Invalid registration format" in show_error.call_args[0][1]

    def test_gui_register_and_convert(self, gui_app):
        gui_app.register_var.set("1 cubit = 0.4572 meter")
        gui_app._on_register()

        names = list(gui_app.unit_combo["values"])
        assert "cubit" in names

        gui_app.unit_var.set("cubit")
        gui_app.value_var.set("1")
        gui_app._on_convert()
        rows = gui_app.tree.get_children()
        assert len(rows) == 3
