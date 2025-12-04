import unittest
from src.truncate_dynamically import truncate_dynamically


class TestTruncateDynamically(unittest.TestCase):
    """Tests unitaires pour la fonction truncate_dynamically"""

    def test_returns_integer(self):
        """Test que la fonction retourne un entier"""
        # Hash de 20 bytes pour SHA1
        test_hash = bytes([0] * 19 + [0x0F])
        result = truncate_dynamically(test_hash)
        self.assertIsInstance(result, int)

    def test_result_is_31_bits_max(self):
        """Test que le résultat est au maximum 31 bits (masque 0x7FFFFFFF)"""
        # Créer un hash qui produirait une grande valeur
        test_hash = bytes([0xFF] * 20)
        result = truncate_dynamically(test_hash)
        self.assertLessEqual(result, 0x7FFFFFFF)
        self.assertGreaterEqual(result, 0)

    def test_offset_extraction(self):
        """Test que l'offset est correctement extrait du dernier byte"""
        # Dernier byte = 0x05, donc offset = 5
        test_hash = bytes([0] * 19 + [0x05])
        # Les bytes à l'offset 5-8 sont tous 0, donc résultat = 0
        result = truncate_dynamically(test_hash)
        self.assertEqual(result, 0)

    def test_known_value(self):
        """Test avec une valeur connue"""
        # Hash où offset = 0 (dernier byte & 0x0F = 0)
        # Les 4 premiers bytes = 0x01020304
        test_hash = bytes([0x01, 0x02, 0x03, 0x04] + [0] * 16)
        result = truncate_dynamically(test_hash)
        expected = 0x01020304 & 0x7FFFFFFF
        self.assertEqual(result, expected)

    def test_offset_at_max(self):
        """Test avec l'offset maximum (15)"""
        # Dernier byte = 0x0F, donc offset = 15
        # Les bytes 15-18 seront utilisés
        test_hash = bytes([0] * 15 + [0x12, 0x34, 0x56, 0x78, 0x0F])
        result = truncate_dynamically(test_hash)
        expected = 0x12345678 & 0x7FFFFFFF
        self.assertEqual(result, expected)

    def test_msb_cleared(self):
        """Test que le bit le plus significatif est toujours effacé"""
        # Créer un hash qui produirait un nombre avec MSB = 1
        test_hash = bytes([0x80, 0x00, 0x00, 0x00] + [0] * 16)
        result = truncate_dynamically(test_hash)
        # Le MSB doit être effacé par le masque 0x7FFFFFFF
        self.assertEqual(result, 0x00000000)

    def test_deterministic(self):
        """Test que la fonction est déterministe"""
        test_hash = bytes(range(20))
        result1 = truncate_dynamically(test_hash)
        result2 = truncate_dynamically(test_hash)
        self.assertEqual(result1, result2)

    def test_different_hashes_can_produce_different_results(self):
        """Test que des hashes différents peuvent produire des résultats différents"""
        hash1 = bytes([0x01] * 20)
        hash2 = bytes([0x02] * 20)
        result1 = truncate_dynamically(hash1)
        result2 = truncate_dynamically(hash2)
        # Ces hashes spécifiques devraient produire des résultats différents
        self.assertNotEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()

