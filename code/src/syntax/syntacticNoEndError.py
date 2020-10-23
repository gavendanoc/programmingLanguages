class SyntacticNoEndError(Exception):
    def __init__(self, data):
        row = len(data) + 1  # end va en siguiente linea
        self.message = f"<{row}:1> Error sintactico: se encontro final de archivo; se esperaba 'end'."
        super().__init__(self.message)
