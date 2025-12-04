import unittest
from unittest.mock import patch
from src.generate_counter_value import generate_counter_value, VALIDITY_DURATION


class TestGenerateCounterValue(unittest.TestCase):
    """Tests unitaires pour la fonction generate_counter_value"""

    def test_custom_timestamp_returns_correct_counter(self):
        """Test avec un timestamp personnalisé"""
        # Timestamp de 60 secondes -> counter = 60 / 30 = 2
        result = generate_counter_value(custom_timestamp=60.0)
        self.assertEqual(result, 2)

    def test_custom_timestamp_with_decimal(self):
        """Test avec un timestamp décimal (doit être arrondi vers le bas)"""
        # Timestamp de 65.9 secondes -> floor(65) / 30 = 2
        result = generate_counter_value(custom_timestamp=65.9)
        self.assertEqual(result, 2)

    def test_custom_timestamp_zero(self):
        """Test avec un timestamp de zéro (epoch)"""
        result = generate_counter_value(custom_timestamp=0.0)
        self.assertEqual(result, 0)

    def test_custom_timestamp_boundary(self):
        """Test aux limites de la fenêtre de 30 secondes"""
        # 29 secondes -> counter = 0
        self.assertEqual(generate_counter_value(custom_timestamp=29.0), 0)
        # 30 secondes -> counter = 1
        self.assertEqual(generate_counter_value(custom_timestamp=30.0), 1)
        # 59 secondes -> counter = 1
        self.assertEqual(generate_counter_value(custom_timestamp=59.0), 1)
        # 60 secondes -> counter = 2
        self.assertEqual(generate_counter_value(custom_timestamp=60.0), 2)

    def test_large_timestamp(self):
        """Test avec un timestamp réaliste (date actuelle approximative)"""
        # Timestamp du 4 décembre 2025 00:00:00 UTC = 1764806400
        timestamp = 1764806400.0
        expected_counter = 1764806400 // VALIDITY_DURATION
        result = generate_counter_value(custom_timestamp=timestamp)
        self.assertEqual(result, expected_counter)

    @patch('src.generate_counter_value.time.time')
    def test_no_timestamp_uses_current_time(self, mock_time):
        """Test que l'heure actuelle est utilisée si aucun timestamp n'est fourni"""
        mock_time.return_value = 90.0  # 90 secondes -> counter = 3
        result = generate_counter_value()
        self.assertEqual(result, 3)
        mock_time.assert_called_once()

    def test_validity_duration_constant(self):
        """Test que la constante VALIDITY_DURATION est bien définie à 30"""
        self.assertEqual(VALIDITY_DURATION, 30)


if __name__ == '__main__':
    unittest.main()
