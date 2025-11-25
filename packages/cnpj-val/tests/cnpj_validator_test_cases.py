from abc import ABC, abstractmethod


class CnpjValidatorTestCases(ABC):
    @abstractmethod
    def is_valid(self, _cnpj_string: str) -> bool:
        pass

    def test_cnpj_string_with_dots_and_dash_is_valid(self):
        result = self.is_valid("22.250.620/0001-11")

        assert result is True

    def test_cnpj_string_with_dots_and_dot_is_valid(self):
        result = self.is_valid("53.975.985/0001.37")

        assert result is True

    def test_cnpj_string_with_underscores_and_pipe_is_valid(self):
        result = self.is_valid("31_592_118|0001_80")

        assert result is True

    def test_cnpj_string_with_dash_is_valid(self):
        result = self.is_valid("188549330001-01")

        assert result is True

    def test_cnpj_string_only_numbers_is_valid(self):
        result = self.is_valid("19593887000105")

        assert result is True

    def test_cnpj_string_99042801000187_is_valid(self):
        result = self.is_valid("99042801000187")

        assert result is True

    def test_cnpj_string_27728000000169_is_valid(self):
        result = self.is_valid("27728000000169")

        assert result is True

    def test_cnpj_string_72199088000123_is_valid(self):
        result = self.is_valid("72199088000123")

        assert result is True

    def test_cnpj_string_00113719000139_is_valid(self):
        result = self.is_valid("00113719000139")

        assert result is True

    def test_cnpj_string_50096743000185_is_valid(self):
        result = self.is_valid("50096743000185")

        assert result is True

    def test_cnpj_string_with_dots_and_dash_is_not_valid(self):
        result = self.is_valid("68.224.994/0001-62")

        assert result is False

    def test_cnpj_string_with_dots_and_pipe_is_not_valid(self):
        result = self.is_valid("41.406.219|0001.73")

        assert result is False

    def test_cnpj_string_with_underscores_and_hash_is_not_valid(self):
        result = self.is_valid("46_063_859#0001_41")

        assert result is False

    def test_cnpj_string_with_slash_is_not_valid(self):
        result = self.is_valid("54964126/000106")

        assert result is False

    def test_cnpj_string_03783943000127_is_not_valid(self):
        result = self.is_valid("03783943000127")

        assert result is False

    def test_value_123_is_not_valid(self):
        result = self.is_valid("123")

        assert result is False

    def test_value_123456_is_not_valid(self):
        result = self.is_valid("123456")

        assert result is False

    def test_value_123456789_is_not_valid(self):
        result = self.is_valid("123456789")

        assert result is False

    def test_value_abc_is_not_valid(self):
        result = self.is_valid("abc")

        assert result is False

    def test_value_abc123_is_not_valid(self):
        result = self.is_valid("abc123")

        assert result is False

    def test_value_true_is_not_valid(self):
        result = self.is_valid("true")

        assert result is False

    def test_value_false_is_not_valid(self):
        result = self.is_valid("false")

        assert result is False

    def test_value_undefined_is_not_valid(self):
        result = self.is_valid("undefined")

        assert result is False

    def test_value_infinity_is_not_valid(self):
        result = self.is_valid("Infinity")

        assert result is False

    def test_value_null_is_not_valid(self):
        result = self.is_valid("null")

        assert result is False

    def test_empty_string_is_not_valid(self):
        result = self.is_valid("")

        assert result is False
