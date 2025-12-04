import unittest
from src.truncated_hash_to_token import truncated_hash_to_token, TOKEN_LENGTH


class TestTruncatedHashToToken(unittest.TestCase):
    """Tests unitaires pour la fonction truncated_hash_to_token"""

    def test_returns_string(self):
        """Test que la fonction retourne une chaîne"""
        result = truncated_hash_to_token(123456)
        self.assertIsInstance(result, str)

    def test_default_length_is_6(self):
        """Test que la longueur par défaut est 6 chiffres"""
        result = truncated_hash_to_token(123456)
        self.assertEqual(len(result), 6)

    def test_token_length_constant(self):
        """Test que la constante TOKEN_LENGTH vaut 6"""
        self.assertEqual(TOKEN_LENGTH, 6)

    def test_modulo_operation(self):
        """Test que le modulo est correctement appliqué"""
        # 1234567 % 10^6 = 234567
        result = truncated_hash_to_token(1234567)
        self.assertEqual(result, "234567")

    def test_left_padding_with_zeros(self):
        """Test que les tokens courts sont complétés avec des zéros à gauche"""
        result = truncated_hash_to_token(123)
        self.assertEqual(result, "000123")

    def test_zero_value(self):
        """Test avec une valeur de zéro"""
        result = truncated_hash_to_token(0)
        self.assertEqual(result, "000000")

    def test_max_6_digit_value(self):
        """Test avec la valeur maximum pour 6 chiffres"""
        result = truncated_hash_to_token(999999)
        self.assertEqual(result, "999999")

    def test_custom_digit_count(self):
        """Test avec un nombre de chiffres personnalisé"""
        result = truncated_hash_to_token(12345, digits=4)
        self.assertEqual(result, "2345")  # 12345 % 10000 = 2345
        self.assertEqual(len(result), 4)

    def test_custom_digit_count_with_padding(self):
        """Test avec un nombre de chiffres personnalisé nécessitant du padding"""
        result = truncated_hash_to_token(5, digits=8)
        self.assertEqual(result, "00000005")
        self.assertEqual(len(result), 8)

    def test_large_input_value(self):
        """Test avec une grande valeur d'entrée"""
        large_value = 2147483647  # Max 31-bit integer
        result = truncated_hash_to_token(large_value)
        self.assertEqual(len(result), 6)
        # 2147483647 % 1000000 = 483647
        self.assertEqual(result, "483647")

    def test_deterministic(self):
        """Test que la fonction est déterministe"""
        result1 = truncated_hash_to_token(987654)
        result2 = truncated_hash_to_token(987654)
        self.assertEqual(result1, result2)

    def test_single_digit_input(self):
        """Test avec un seul chiffre"""
        result = truncated_hash_to_token(7)
        self.assertEqual(result, "000007")

    def test_exactly_6_digits(self):
        """Test avec exactement 6 chiffres, pas de modulo nécessaire"""
        result = truncated_hash_to_token(123456)
        self.assertEqual(result, "123456")


if __name__ == '__main__':
    unittest.main()

