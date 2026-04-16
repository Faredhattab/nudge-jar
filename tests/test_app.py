#test push
import unittest

from app import app, reset_nudges


class NudgeJarAppTests(unittest.TestCase):
    def setUp(self):
        reset_nudges()
        self.client = app.test_client()

    def test_index_page_renders(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Nudge Jar", response.get_data(as_text=True))
        self.assertIn("Save short nudges to your future self", response.get_data(as_text=True))

    def test_get_nudges_returns_empty_list_by_default(self):
        response = self.client.get("/api/nudges")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"nudges": []})

    def test_add_nudge_rejects_empty_text(self):
        response = self.client.post("/api/nudges", json={"text": "   "})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Nudge cannot be empty."})

    def test_add_nudge_strips_whitespace_and_returns_updated_list(self):
        response = self.client.post("/api/nudges", json={"text": "  Send the email  "})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {"ok": True, "nudges": ["Send the email"]},
        )

    def test_random_nudge_requires_at_least_one_saved_item(self):
        response = self.client.get("/api/nudges/random")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Add a nudge first."})

    def test_random_nudge_returns_saved_item(self):
        self.client.post("/api/nudges", json={"text": "Drink water"})
        response = self.client.get("/api/nudges/random")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"nudge": "Drink water"})


if __name__ == "__main__":
    unittest.main()
