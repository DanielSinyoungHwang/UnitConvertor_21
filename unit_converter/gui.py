"""Tkinter 기반 단위 변환 GUI."""

import tkinter as tk
from tkinter import messagebox, ttk

from unit_converter.app.input_parser import (
    InputFormatError,
    InvalidNumberError,
    NegativeValueError,
    parse_and_validate,
)
from unit_converter.app.registration_parser import (
    RegistrationFormatError,
    parse_registration,
)
from unit_converter.domain.converter import Converter
from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.unit_registry import UnitRegistry
from unit_converter.infrastructure.config_loader import load_registry


class UnitConverterApp:
    """단위 변환·등록·결과 표시를 담당하는 메인 GUI 애플리케이션."""

    def __init__(self, root: tk.Tk, registry: UnitRegistry | None = None) -> None:
        """Tk 루트 윈도우와 레지스트리를 받아 UI와 Converter를 초기화한다."""
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("520x480")
        self.root.minsize(420, 400)

        self.registry = registry or load_registry()
        self.converter = Converter(self.registry)

        self._build_ui()
        self._refresh_unit_list()

    def _build_ui(self) -> None:
        """변환·등록·결과 패널과 위젯을 구성한다."""
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        convert_frame = ttk.LabelFrame(main, text="변환", padding=10)
        convert_frame.pack(fill=tk.X, pady=(0, 10))

        row = ttk.Frame(convert_frame)
        row.pack(fill=tk.X)

        ttk.Label(row, text="값:").pack(side=tk.LEFT)
        self.value_var = tk.StringVar(value="2.5")
        ttk.Entry(row, textvariable=self.value_var, width=12).pack(side=tk.LEFT, padx=(6, 16))

        ttk.Label(row, text="단위:").pack(side=tk.LEFT)
        self.unit_var = tk.StringVar()
        self.unit_combo = ttk.Combobox(row, textvariable=self.unit_var, width=14, state="readonly")
        self.unit_combo.pack(side=tk.LEFT, padx=(6, 16))

        ttk.Button(row, text="변환", command=self._on_convert).pack(side=tk.LEFT)

        raw_row = ttk.Frame(convert_frame)
        raw_row.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(raw_row, text="또는 unit:value:").pack(side=tk.LEFT)
        self.raw_var = tk.StringVar(value="meter:2.5")
        ttk.Entry(raw_row, textvariable=self.raw_var, width=24).pack(side=tk.LEFT, padx=6)
        ttk.Button(raw_row, text="입력 변환", command=self._on_convert_raw).pack(side=tk.LEFT)

        register_frame = ttk.LabelFrame(main, text="단위 등록", padding=10)
        register_frame.pack(fill=tk.X, pady=(0, 10))

        reg_row = ttk.Frame(register_frame)
        reg_row.pack(fill=tk.X)

        ttk.Label(reg_row, text="예: 1 cubit = 0.4572 meter").pack(side=tk.LEFT)
        self.register_var = tk.StringVar()
        ttk.Entry(reg_row, textvariable=self.register_var, width=28).pack(side=tk.LEFT, padx=6)
        ttk.Button(reg_row, text="등록", command=self._on_register).pack(side=tk.LEFT)

        result_frame = ttk.LabelFrame(main, text="결과", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("target", "value")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)
        self.tree.heading("target", text="단위")
        self.tree.heading("value", text="변환값")
        self.tree.column("target", width=120, anchor=tk.W)
        self.tree.column("value", width=120, anchor=tk.E)

        scroll = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.status_var = tk.StringVar(value="값과 단위를 입력한 뒤 변환을 누르세요.")
        ttk.Label(main, textvariable=self.status_var, foreground="#555").pack(anchor=tk.W, pady=(8, 0))

    def _refresh_unit_list(self) -> None:
        """콤보박스 단위 목록을 레지스트리 기준으로 갱신한다."""
        names = sorted(unit.name for unit in self.registry.all_units())
        self.unit_combo["values"] = names
        if names and not self.unit_var.get():
            self.unit_var.set(names[0])

    def _clear_results(self) -> None:
        """결과 Treeview의 모든 행을 제거한다."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _show_results(self, source_unit: str, value: float) -> None:
        """변환을 실행하고 결과를 Treeview와 상태바에 표시한다."""
        self._clear_results()
        results = self.converter.convert(source_unit, value)
        for unit, converted in results.items():
            self.tree.insert("", tk.END, values=(unit, converted))
        self.status_var.set(f"{value} {source_unit} → {len(results)}개 단위로 변환됨")

    def _handle_user_error(self, exc: Exception) -> None:
        """입력 오류 시 결과를 비우고 상태바에 오류 메시지를 표시한다."""
        self._clear_results()
        self.status_var.set(str(exc))

    def _on_convert(self) -> None:
        """값·단위 콤보박스 입력으로 변환 버튼 클릭을 처리한다."""
        unit = self.unit_var.get().strip()
        value_str = self.value_var.get().strip()
        input_str = f"{unit}:{value_str}"

        try:
            parsed_unit, value = parse_and_validate(input_str, self.registry)
        except NegativeValueError:
            self._handle_user_error(Exception("Negative values are not allowed."))
            return
        except (InputFormatError, InvalidNumberError, UnknownUnitError) as exc:
            self._handle_user_error(exc)
            return

        self._show_results(parsed_unit, value)

    def _on_convert_raw(self) -> None:
        """unit:value 원문 입력으로 변환 버튼 클릭을 처리한다."""
        input_str = self.raw_var.get().strip()
        try:
            unit, value = parse_and_validate(input_str, self.registry)
        except NegativeValueError:
            self._handle_user_error(Exception("Negative values are not allowed."))
            return
        except (InputFormatError, InvalidNumberError, UnknownUnitError) as exc:
            self._handle_user_error(exc)
            return

        self.unit_var.set(unit)
        self.value_var.set(str(value))
        self._show_results(unit, value)

    def _on_register(self) -> None:
        """단위 등록 입력을 파싱·등록하고 단위 목록을 갱신한다."""
        text = self.register_var.get().strip()
        if not text:
            messagebox.showwarning("등록", "등록할 단위 식을 입력하세요.")
            return

        try:
            self.registry.register(parse_registration(text))
        except RegistrationFormatError as exc:
            messagebox.showerror("등록 오류", str(exc))
            return

        self.register_var.set("")
        self._refresh_unit_list()
        self.status_var.set(f"단위가 등록되었습니다. (총 {len(self.registry.all_units())}개)")


def main() -> None:
    """GUI 애플리케이션을 생성하고 이벤트 루프를 시작한다."""
    root = tk.Tk()
    UnitConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
