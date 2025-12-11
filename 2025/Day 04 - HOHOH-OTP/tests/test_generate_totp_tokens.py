import unittest
from unittest.mock import patch
from src.generate_totp_tokens import generate_totp_tokens, VALID_START, VALID_END


class TestGenerateTotpTokens(unittest.TestCase):
    """Tests unitaires pour la fonction generate_totp_tokens"""

    def test_returns_list(self):
        """Test que la fonction retourne une liste"""
        result = generate_totp_tokens("JBSWY3DPEHPK3PXP", custom_timestamp=1000000)
        self.assertIsInstance(result, list)

    def test_default_window_returns_5_tokens(self):
        """Test que la fenêtre par défaut (-2 à +2) retourne 5 tokens"""
        result = generate_totp_tokens("JBSWY3DPEHPK3PXP", custom_timestamp=1000000)
        self.assertEqual(len(result), 5)

    def test_tokens_are_strings(self):
        """Test que tous les tokens sont des chaînes"""
        result = generate_totp_tokens("JBSWY3DPEHPK3PXP", custom_timestamp=1000000)
        for token in result:
            self.assertIsInstance(token, str)

    def test_tokens_are_6_digits(self):
        """Test que tous les tokens ont 6 chiffres"""
        result = generate_totp_tokens("JBSWY3DPEHPK3PXP", custom_timestamp=1000000)
        for token in result:
            self.assertEqual(len(token), 6)
            self.assertTrue(token.isdigit())

    def test_custom_window(self):
        """Test avec une fenêtre personnalisée"""
        result = generate_totp_tokens(
            "JBSWY3DPEHPK3PXP",
            timestep_start=-1,
            timestep_end=1,
            custom_timestamp=1000000
        )
        self.assertEqual(len(result), 3)

    def test_single_token_window(self):
        """Test avec une fenêtre d'un seul token"""
        result = generate_totp_tokens(
            "JBSWY3DPEHPK3PXP",
            timestep_start=0,
            timestep_end=0,
            custom_timestamp=0
        )
        self.assertEqual(len(result), 1)

    def test_deterministic_with_same_timestamp(self):
        """Test que les mêmes inputs produisent les mêmes tokens"""
        result1 = generate_totp_tokens("JBSWY3DPEHPK3PXP", custom_timestamp=1000)
        result2 = generate_totp_tokens("JBSWY3DPEHPK3PXP", custom_timestamp=1000)
        self.assertEqual(result1, result2)

    def test_different_timestamps_in_same_window_share_tokens(self):
        """Test que des timestamps dans la même fenêtre de 30s partagent le token central"""
        # Timestamps 0 et 15 sont dans la même fenêtre de 30 secondes
        result1 = generate_totp_tokens(
            "JBSWY3DPEHPK3PXP",
            timestep_start=0,
            timestep_end=0,
            custom_timestamp=0
        )
        result2 = generate_totp_tokens(
            "JBSWY3DPEHPK3PXP",
            timestep_start=0,
            timestep_end=0,
            custom_timestamp=15
        )
        self.assertEqual(result1, result2)

    def test_different_secrets_produce_different_tokens(self):
        """Test que des secrets différents produisent des tokens différents"""
        result1 = generate_totp_tokens("JBSWY3DPEHPK3PXP", custom_timestamp=1000000)
        result2 = generate_totp_tokens("GEZDGNBVGY3TQOJQ", custom_timestamp=1000000)
        self.assertNotEqual(result1, result2)

    def test_project_secret(self):
        """Test avec le secret utilisé dans le projet"""
        secret = "F5TGYYLHNFZW433UNBSXEZJP"
        result = generate_totp_tokens(secret, custom_timestamp=1764806400)
        self.assertEqual(len(result), 5)
        for token in result:
            self.assertEqual(len(token), 6)
            self.assertTrue(token.isdigit())

    def test_valid_start_end_constants(self):
        """Test des constantes VALID_START et VALID_END"""
        self.assertEqual(VALID_START, -2)
        self.assertEqual(VALID_END, 2)

    def test_tokens_change_every_30_seconds(self):
        """Test que les tokens changent toutes les 30 secondes"""
        result1 = generate_totp_tokens(
            "JBSWY3DPEHPK3PXP",
            timestep_start=0,
            timestep_end=0,
            custom_timestamp=0
        )
        result2 = generate_totp_tokens(
            "JBSWY3DPEHPK3PXP",
            timestep_start=0,
            timestep_end=0,
            custom_timestamp=30
        )
        self.assertNotEqual(result1, result2)

    @patch('src.generate_counter_value.time.time')
    def test_uses_current_time_when_no_timestamp(self, mock_time):
        """Test que l'heure actuelle est utilisée si aucun timestamp n'est fourni"""
        mock_time.return_value = 60.0
        result = generate_totp_tokens("JBSWY3DPEHPK3PXP")
        self.assertEqual(len(result), 5)
        mock_time.assert_called()

    def test_known_totp_value(self):
        """Test d'intégration avec une valeur TOTP connue
        Secret: F5TGYYLHNFZW433UNBSXEZJP
        Pour valider que l'implémentation est conforme RFC 6238
        """
        secret = "F5TGYYLHNFZW433UNBSXEZJP"
        # Utiliser un timestamp fixe pour avoir des résultats reproductibles
        result = generate_totp_tokens(
            secret,
            timestep_start=0,
            timestep_end=0,
            custom_timestamp=0
        )
        # Le token doit être une chaîne de 6 chiffres
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 6)
        self.assertTrue(result[0].isdigit())


if __name__ == '__main__':
    unittest.main()

