import unittest
from unittest.mock import patch

import main


class TestTaskManager(unittest.TestCase):
    @patch("main.save_tasks")
    @patch("builtins.input", side_effect=["Finish assignment", "3"])
    def test_add_task(self, mock_input, mock_save):
        tasks = []

        task = main.add_task(tasks)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Finish assignment")
        self.assertFalse(task["completed"])
        self.assertEqual(task["priority"], "High")
        mock_save.assert_called_once_with(tasks)

    @patch("main.save_tasks")
    @patch("builtins.input", return_value="1")
    def test_complete_task(self, mock_input, mock_save):
        tasks = [
            {"id": 1, "title": "Study", "completed": False, "priority": "Medium"}
        ]

        result = main.complete_task(tasks)

        self.assertTrue(result)
        self.assertTrue(tasks[0]["completed"])
        mock_save.assert_called_once_with(tasks)

    @patch("main.save_tasks")
    @patch("builtins.input", return_value="2")
    def test_delete_task(self, mock_input, mock_save):
        tasks = [
            {"id": 1, "title": "Study", "completed": False, "priority": "Medium"},
            {"id": 2, "title": "Shop", "completed": False, "priority": "Low"},
        ]

        result = main.delete_task(tasks)

        self.assertTrue(result)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], 1)
        mock_save.assert_called_once_with(tasks)

    @patch("builtins.input", return_value="ASSIGNMENT")
    def test_search_tasks_is_case_insensitive(self, mock_input):
        tasks = [
            {
                "id": 1,
                "title": "Finish assignment",
                "completed": False,
                "priority": "High",
            },
            {"id": 2, "title": "Buy groceries", "completed": False, "priority": "Low"},
        ]

        matches = main.search_tasks(tasks)

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["id"], 1)


if __name__ == "__main__":
    unittest.main()
