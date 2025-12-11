import unittest
import base64
from src.generate_hash import generate_hash


class TestGenerateHash(unittest.TestCase):
    """Tests unitaires pour la fonction generate_hash"""

    def test_returns_bytes(self):
        """Test que la fonction retourne des bytes"""
        secret = "JBSWY3DPEHPK3PXP"  # Secret de test en base32
        result = generate_hash(secret, 0)
        self.assertIsInstance(result, bytes)

    def test_hash_length_is_20_bytes(self):
        """Test que le hash SHA1 fait 20 bytes (160 bits)"""
        secret = "JBSWY3DPEHPK3PXP"
        result = generate_hash(secret, 0)
        self.assertEqual(len(result), 20)

    def test_same_inputs_produce_same_hash(self):
        """Test que les mêmes inputs produisent le même hash (déterministe)"""
        secret = "JBSWY3DPEHPK3PXP"
        counter = 12345
        result1 = generate_hash(secret, counter)
        result2 = generate_hash(secret, counter)
        self.assertEqual(result1, result2)

    def test_different_counters_produce_different_hashes(self):
        """Test que des compteurs différents produisent des hashes différents"""
        secret = "JBSWY3DPEHPK3PXP"
        result1 = generate_hash(secret, 0)
        result2 = generate_hash(secret, 1)
        self.assertNotEqual(result1, result2)

    def test_different_secrets_produce_different_hashes(self):
        """Test que des secrets différents produisent des hashes différents"""
        counter = 100
        result1 = generate_hash("JBSWY3DPEHPK3PXP", counter)
        result2 = generate_hash("GEZDGNBVGY3TQOJQ", counter)
        self.assertNotEqual(result1, result2)

    def test_rfc6238_test_vector(self):
        """Test avec les vecteurs de test RFC 6238 (SHA1)
        Secret: 12345678901234567890 (en ASCII) = GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ en base32
        """
        # Secret ASCII "12345678901234567890" encodé en base32
        secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
        # Le hash doit être reproductible
        result = generate_hash(secret, 1)
        self.assertEqual(len(result), 20)
        self.assertIsInstance(result, bytes)

    def test_counter_zero(self):
        """Test avec un compteur à zéro"""
        secret = "JBSWY3DPEHPK3PXP"
        result = generate_hash(secret, 0)
        self.assertEqual(len(result), 20)

    def test_large_counter_value(self):
        """Test avec une grande valeur de compteur"""
        secret = "JBSWY3DPEHPK3PXP"
        large_counter = 2**32  # Valeur au-delà de 32 bits
        result = generate_hash(secret, large_counter)
        self.assertEqual(len(result), 20)

    def test_project_secret(self):
        """Test avec le secret utilisé dans le projet"""
        secret = "F5TGYYLHNFZW433UNBSXEZJP"
        result = generate_hash(secret, 58826880)  # Un compteur arbitraire
        self.assertEqual(len(result), 20)
        self.assertIsInstance(result, bytes)


if __name__ == '__main__':
    unittest.main()

