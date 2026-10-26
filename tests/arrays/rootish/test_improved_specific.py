"""Balance and structure tests specific to ImprovedRAS implementation."""

import pytest

from ods.arrays import ImprovedRAS

# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------


def contents(seq):
    """Logical contents via public API."""
    return [seq.get(i) for i in range(seq.size)]


def assert_balanced(seq):
    """Check that ImprovedRAS maintains front/back balance invariant."""
    if seq.size <= 4:
        return  # No balancing required for small stacks
    ratio_front = 3 * seq.front_n
    ratio_back = 3 * seq.back_n
    assert not (ratio_front < seq.back_n or ratio_back < seq.front_n), (
        f"Imbalanced: front_n={seq.front_n}, back_n={seq.back_n}, total={seq.size}"
    )


def assert_structure_valid(seq):
    """Check basic structural invariants."""
    assert seq.front_n + seq.back_n == seq.size, (
        f"Element count mismatch: front={seq.front_n} + back={seq.back_n} != {seq.size}"
    )
    assert_balanced(seq)


# -------------------------------------------------------------------------
# Test Class: Core Balance Invariants
# -------------------------------------------------------------------------


class TestBalanceInvariant:
    """Verify that balancing maintains the 3:1 ratio constraint."""

    @pytest.mark.parametrize(
        "operation_count, build_direction",
        [
            pytest.param(50, "front", id="50_front"),
            pytest.param(100, "front", id="100_front"),
            pytest.param(100, "back", id="100_back"),
            pytest.param(200, "front", id="200_front"),
            pytest.param(200, "back", id="200_back"),
        ],
    )
    def test_balance_after_bulk_insert(self, operation_count, build_direction):
        """Large inserts from either direction should trigger and maintain balance."""
        seq = ImprovedRAS()

        if build_direction == "front":
            for i in range(operation_count):
                seq.add(0, i)
        else:
            for i in range(operation_count):
                seq.add(seq.size, i)

        assert seq.size == operation_count
        assert_structure_valid(seq)

    def test_balance_engages_at_size_five(self):
        """Balance is NOT triggered until size > 4."""
        seq = ImprovedRAS()

        # Build to exactly 4 elements — no balancing yet
        for i in range(4):
            seq.add(0, i)

        # At size=4, balancing shortcut returns early
        assert seq.size == 4

        # Adding one more triggers balancing
        seq.add(0, 4)
        assert seq.size == 5
        assert_balanced(seq)  # Now must be balanced

    @pytest.mark.parametrize(
        "i, expected_block",
        [
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (5, 2),
            (6, 3),
            (9, 3),
            (10, 4),
            (14, 4),
            (15, 5),
        ],
    )
    def test_i2b_at_block_boundaries(self, i, expected_block):
        """Index-to-block conversion at triangular number boundaries."""
        seq = ImprovedRAS()
        result = seq._i2b(i)
        assert result == expected_block, (
            f"_i2b({i}) = {result}, expected {expected_block}"
        )


# -------------------------------------------------------------------------
# Test Class: Balance Preserves Semantics
# -------------------------------------------------------------------------


class TestBalancePreservesSemantics:
    """Ensure balancing never loses or corrupts data."""

    @pytest.mark.parametrize(
        "insert_count, pattern",
        [
            pytest.param(50, "front_only", id="50_front_only"),
            pytest.param(50, "back_only", id="50_back_only"),
            pytest.param(100, "mixed", id="100_mixed"),
        ],
    )
    def test_contents_preserved_after_balance(self, insert_count, pattern):
        """Reference list tracks what we expect; contents must match."""
        seq = ImprovedRAS()
        ref = []

        if pattern == "front_only":
            for i in range(insert_count):
                seq.add(0, i)
                ref.insert(0, i)
        elif pattern == "back_only":
            for i in range(insert_count):
                seq.add(seq.size, i)
                ref.append(i)
        else:  # mixed
            for i in range(insert_count):
                seq.add(0, i)
                ref.insert(0, i)
                seq.add(seq.size, i * -1)
                ref.append(i * -1)

        assert contents(seq) == ref, "Contents diverged from reference after operations"
        assert_structure_valid(seq)

    def test_all_elements_reachable_after_many_front_adds(self):
        """Every element inserted at front must be retrievable by index."""
        seq = ImprovedRAS()
        insert_count = 250

        for i in range(insert_count):
            seq.add(0, i)

        result = [seq.get(j) for j in range(seq.size)]
        expected = list(reversed(range(insert_count)))

        assert result == expected, "Not all elements reachable via get()"

    def test_round_trip_add_remove_restores_state(self):
        """Add then remove at same index should restore original contents."""
        seq = ImprovedRAS()
        initial = [1, 2, 3, 4, 5]

        for v in initial:
            seq.add(seq.size, v)

        for i in range(len(initial) + 1):
            seq.add(i, 999)
            removed = seq.remove(i)
            assert removed == 999, f"Expected 999 at index {i}, got {removed}"
            assert contents(seq) == initial, f"State corrupted after index {i}"


# -------------------------------------------------------------------------
# Test Class: Edge Cases and Boundary Conditions
# -------------------------------------------------------------------------


class TestBalanceEdgeCases:
    """Test critical boundary conditions for balancing logic."""

    @pytest.mark.parametrize(
        "initial_size, remove_count, expected_remaining",
        [
            pytest.param(100, 80, 20, id="100_minus_80"),
            pytest.param(50, 45, 5, id="50_minus_45"),
            pytest.param(20, 18, 2, id="20_minus_18"),
        ],
    )
    def test_balance_after_front_removes(
        self, initial_size, remove_count, expected_remaining
    ):
        """Many removes from front should shrink and rebalance."""
        seq = ImprovedRAS()
        for i in range(initial_size):
            seq.add(seq.size, i)

        for _ in range(remove_count):
            seq.remove(0)

        assert seq.size == expected_remaining
        assert_structure_valid(seq)
        assert contents(seq) == list(range(remove_count, initial_size))

    @pytest.mark.parametrize(
        "initial_size, remove_count, expected_remaining",
        [
            pytest.param(100, 80, 20, id="100_back_remove"),
            pytest.param(50, 45, 5, id="50_back_remove"),
        ],
    )
    def test_balance_after_back_removes(
        self, initial_size, remove_count, expected_remaining
    ):
        """Many removes from back should shrink and rebalance."""
        seq = ImprovedRAS()
        for i in range(initial_size):
            seq.add(seq.size, i)

        for _ in range(remove_count):
            seq.remove(seq.size - 1)

        assert seq.size == expected_remaining
        assert_structure_valid(seq)
        assert contents(seq) == list(range(expected_remaining))

    def test_switch_between_front_and_back_operations(self):
        """Switching between front and back ops shouldn't break balance."""
        seq = ImprovedRAS()
        ref = []

        # Heavy front load
        for i in range(200):
            seq.add(0, i)
            ref.insert(0, i)

        # Then some removes from front
        for _ in range(75):
            seq.remove(0)
            ref.pop(0)

        # Then adds to back
        for i in range(50):
            seq.add(seq.size, i)
            ref.append(i)

        assert contents(seq) == ref
        assert_structure_valid(seq)

    def test_balanced_stack_has_correct_element_count(self):
        """front_n + back_n must always equal total size."""
        seq = ImprovedRAS()

        # Mix of operations
        for i in range(50):
            seq.add(0, i)
            seq.add(seq.size, i)

        for _ in range(25):
            seq.remove(0)
            seq.remove(seq.size - 1)

        assert seq.front_n + seq.back_n == seq.size


# -------------------------------------------------------------------------
# Test Class: Stress Tests
# -------------------------------------------------------------------------


class TestBalanceStress:
    """Heavy stress tests for balancing under extreme conditions."""

    @pytest.mark.parametrize("cycle_count", [3, 5, 10])
    def test_repeated_growth_and_shrink_cycles(self, cycle_count):
        """Repeatedly grow to large size and shrink back to zero."""
        seq = ImprovedRAS()
        max_size = 150

        for _ in range(cycle_count):
            # Grow
            for i in range(max_size):
                seq.add(seq.size, i)
            assert seq.size == max_size
            assert_structure_valid(seq)

            # Shrink from front
            for _ in range(max_size):
                seq.remove(0)

            assert seq.is_empty()
            assert seq.size == 0
            assert contents(seq) == []
