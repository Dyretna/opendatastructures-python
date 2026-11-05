class Validator:
    @staticmethod
    def validate_index_access(i: int, size: int):
        if not (0 <= i <= size - 1):
            raise IndexError(f"index {i} not in range 0 - {size - 1}")

    @staticmethod
    def validate_index_insert(i: int, size: int):
        if not (0 <= i <= size):
            raise IndexError(f"index {i} not in range 0 - {size}")
