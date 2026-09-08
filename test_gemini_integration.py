"""Unit and integration tests for Gemini Flash Model Integration."""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.config.settings import DEFAULT_GEMINI_MODEL
from src.ml.gemini_client import (
    get_gemini_api_key,
    is_gemini_available,
    _build_system_instruction,
    _format_ai_response_card,
    query_gemini_flash,
)
from src.data_access.loader import load_data
from src.ui.pipeline import generate_response

class TestGeminiIntegration(unittest.TestCase):
    def setUp(self):
        self.df = load_data()

    def test_system_instruction_languages(self):
        """Verify clinical system instruction customizes by language."""
        instr_en = _build_system_instruction("en")
        self.assertIn("English", instr_en)
        self.assertIn("MJPJAY", instr_en)

        instr_hi = _build_system_instruction("hi")
        self.assertIn("हिंदी", instr_hi)

        instr_mr = _build_system_instruction("mr")
        self.assertIn("मराठी", instr_mr)

    def test_response_card_formatting(self):
        """Verify markdown parsing and clinical card styling."""
        raw_text = "### Immediate Assessment\nPatient has mild viral symptoms.\n\n* Take rest\n* Drink ORS"
        card_html = _format_ai_response_card(raw_text, DEFAULT_GEMINI_MODEL, "en")
        self.assertIn("th-dx-card", card_html)
        self.assertIn("GEMINI 2.5 FLASH CLINICAL AI TRIAGE", card_html)
        self.assertIn("Immediate Assessment", card_html)
        self.assertIn("Disclaimer", card_html)

    def test_fallback_when_no_key(self):
        """Verify is_gemini_available is False when no key is set."""
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(is_gemini_available())
            resp = query_gemini_flash("I have fever", "en")
            self.assertEqual(resp, "")

    @patch("src.ml.gemini_client.get_gemini_api_key", return_value="mock-test-key")
    def test_query_gemini_mocked_success(self, mock_key):
        """Verify query_gemini_flash produces styled output when mocked."""
        mock_response = MagicMock()
        mock_response.text = "### Assessment: Mild\nRecommendation: Rest and hydration."

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch("google.genai.Client", return_value=mock_client):
            output = query_gemini_flash(
                query="I have a slight headache and tiredness",
                response_lang="en",
                entities={"age": 25, "district": "Nandurbar"},
                matched_disease_row={"disease": "Viral Fever", "recommended_facility": "PHC"},
            )
            self.assertTrue(len(output) > 0)
            self.assertIn("MahaArogya AI Clinical Consultant", output)
            self.assertIn("Assessment: Mild", output)

    def test_end_to_end_emergency_preserves_deterministic_safety(self):
        """Verify emergency queries NEVER bypass the 108 Emergency Banner."""
        resp = generate_response(
            query="Patient is unconscious and having severe chest pain in Nandurbar",
            language="English",
            df=self.df,
            symptom_embeddings=None,
            name_embeddings=None,
            model=None,
        )
        self.assertIn("108", resp)
        self.assertIn("EMERGENCY", resp.upper())

    def test_end_to_end_fallback_pipeline(self):
        """Verify pipeline handles queries gracefully when Gemini is offline."""
        with patch("src.ml.gemini_client.is_gemini_available", return_value=False):
            resp = generate_response(
                query="I have high fever and body ache",
                language="English",
                df=self.df,
                symptom_embeddings=None,
                name_embeddings=None,
                model=None,
            )
            self.assertTrue(len(resp) > 0)
            # Standard local embedding or keyword response
            self.assertTrue("fever" in resp.lower() or "care" in resp.lower() or "triage" in resp.lower())


    def test_penetrating_trauma_knife_in_stomach(self):
        """Verify knife in stomach immediately triggers critical surgical trauma emergency."""
        resp = generate_response(
            query="knife in stomach",
            language="English",
            df=self.df,
            symptom_embeddings=None,
            name_embeddings=None,
            model=None,
        )
        self.assertIn("108", resp)
        self.assertIn("CRITICAL SURGICAL EMERGENCY", resp)
        self.assertIn("DO NOT REMOVE", resp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
