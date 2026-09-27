import json
import unittest
import os

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):

    # Set up the test database
    def setUp(self):
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_password = os.environ.get('DATABASE_PASSWORD')
        self.database_host = "localhost:5432"

        self.database_path = (
            f"postgresql://{self.database_user}:"
            f"{self.database_password}@"
            f"{self.database_host}/"
            f"{self.database_name}"
        )

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Remove existing questions first because they depend on categories
            db.session.query(Question).delete()
            db.session.query(Category).delete()
            db.session.commit()

            # Create test categories
            categories = [
                Category(type="Science"),
                Category(type="Literature"),
                Category(type="Geography")
            ]

            db.session.add_all(categories)
            db.session.commit()

            # Use the actual category IDs assigned by the database
            self.science_id = categories[0].id
            self.literature_id = categories[1].id
            self.geography_id = categories[2].id

            # Create test questions
            questions = [
                Question(
                    question="What is the largest planet in our solar system?",
                    answer="Jupiter",
                    category=str(self.science_id),
                    difficulty=1
                ),
                Question(
                    question="What is the process by which plants make food?",
                    answer="Photosynthesis",
                    category=str(self.science_id),
                    difficulty=2
                ),
                Question(
                    question="Who wrote the novel 1984?",
                    answer="George Orwell",
                    category=str(self.literature_id),
                    difficulty=2
                ),
                Question(
                    question="Who painted The Starry Night?",
                    answer="Vincent van Gogh",
                    category=str(self.literature_id),
                    difficulty=2
                ),
                Question(
                    question="What is the capital city of Japan?",
                    answer="Tokyo",
                    category=str(self.geography_id),
                    difficulty=1
                ),
                Question(
                    question="Which continent is the Sahara Desert located on?",
                    answer="Africa",
                    category=str(self.geography_id),
                    difficulty=1
                )
            ]

            db.session.add_all(questions)
            db.session.commit()

    # Clean up after each test
    def tearDown(self):
        with self.app.app_context():
            db.session.query(Question).delete()
            db.session.query(Category).delete()
            db.session.commit()
            db.session.remove()

    # Test getting categories
    def test_get_categories(self):
        res = self.client.get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['categories']), 3)

    # Test getting all questions
    def test_get_questions(self):
        res = self.client.get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 6)
        self.assertEqual(data['total_questions'], 6)
        self.assertIsNone(data['current_category'])

    # Test requesting page two
    def test_get_questions_page_two(self):
        res = self.client.get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['questions'], [])

    # Test requesting page zero
    def test_get_questions_page_zero(self):
        res = self.client.get('/questions?page=0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['questions'], [])

    # Test requesting a page beyond available questions
    def test_get_questions_invalid_page(self):
        res = self.client.get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['questions'], [])
        self.assertEqual(data['total_questions'], 6)

    # Test creating a question
    def test_create_question(self):
        new_question = {
            'question': 'What is the fastest land animal?',
            'answer': 'Cheetah',
            'category': str(self.science_id),
            'difficulty': 2
        }

        res = self.client.post(
            '/questions',
            json=new_question
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIn('created', data)

    # Test creating question without question
    def test_create_question_missing_question(self):
        new_question = {
            'answer': 'Cheetah',
            'category': str(self.science_id),
            'difficulty': 2
        }

        res = self.client.post(
            '/questions',
            json=new_question
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)

    # Test creating question without answer
    def test_create_question_missing_answer(self):
        new_question = {
            'question': 'What is the fastest land animal?',
            'category': str(self.science_id),
            'difficulty': 2
        }

        res = self.client.post(
            '/questions',
            json=new_question
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)

    # Test creating question without category
    def test_create_question_missing_category(self):
        new_question = {
            'question': 'What is the fastest land animal?',
            'answer': 'Cheetah',
            'difficulty': 2
        }

        res = self.client.post(
            '/questions',
            json=new_question
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)

    # Test creating question without difficulty
    def test_create_question_missing_difficulty(self):
        new_question = {
            'question': 'What is the fastest land animal?',
            'answer': 'Cheetah',
            'category': str(self.science_id)
        }

        res = self.client.post(
            '/questions',
            json=new_question
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)

    # Test creating question with empty body
    def test_create_question_empty_body(self):
        res = self.client.post(
            '/questions',
            json={}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)

    # Test deleting a question
    def test_delete_question(self):
        with self.app.app_context():
            question = Question.query.first()
            question_id = question.id

        res = self.client.delete(
            f'/questions/{question_id}'
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)

    # Test deleting a nonexistent question
    def test_delete_question_not_found(self):
        res = self.client.delete(
            '/questions/999999'
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    # Test searching questions
    def test_search_questions(self):
        res = self.client.post(
            '/questions/search',
            json={
                'searchTerm': 'planet'
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)

    # Test case-insensitive search
    def test_search_questions_case_insensitive(self):
        res = self.client.post(
            '/questions/search',
            json={
                'searchTerm': 'PLANET'
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 1)

    # Test search with no results
    def test_search_questions_no_results(self):
        res = self.client.post(
            '/questions/search',
            json={
                'searchTerm': 'zzzzzz'
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['questions'], [])
        self.assertEqual(data['total_questions'], 0)

    # Test search without search term
    def test_search_questions_missing_search_term(self):
        res = self.client.post(
            '/questions/search',
            json={}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)

    # Test getting questions by category
    def test_get_questions_by_category(self):
        res = self.client.get(
            f'/categories/{self.science_id}/questions'
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['current_category'], self.science_id)

        for question in data['questions']:
            self.assertEqual(
                question['category'],
                self.science_id
            )

    # Test invalid category
    def test_get_questions_by_category_invalid(self):
        res = self.client.get(
            '/categories/999999/questions'
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    # Test quiz by category
    def test_quiz_category(self):
        res = self.client.post(
            '/quizzes',
            json={
                'previous_questions': [],
                'quiz_category': {
                    'id': self.science_id,
                    'type': 'Science'
                }
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])
        self.assertEqual(
            data['question']['category'],
            self.science_id
        )

    # Test quiz using all categories
    def test_quiz_all_categories(self):
        res = self.client.post(
            '/quizzes',
            json={
                'previous_questions': [],
                'quiz_category': {
                    'id': None,
                    'type': 'All'
                }
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])

    # Test excluding previous questions
    def test_quiz_excludes_previous_questions(self):
        with self.app.app_context():
            questions = Question.query.order_by(
                Question.id
            ).all()

            previous_questions = [
                question.id
                for question in questions[:-1]
            ]

            remaining_question_id = questions[-1].id

        res = self.client.post(
            '/quizzes',
            json={
                'previous_questions': previous_questions,
                'quiz_category': {
                    'id': None,
                    'type': 'All'
                }
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])
        self.assertEqual(
            data['question']['id'],
            remaining_question_id
        )

    # Test quiz when all questions have been used
    def test_quiz_no_questions_remaining(self):
        with self.app.app_context():
            questions = Question.query.all()

            previous_questions = [
                question.id
                for question in questions
            ]

        res = self.client.post(
            '/quizzes',
            json={
                'previous_questions': previous_questions,
                'quiz_category': {
                    'id': None,
                    'type': 'All'
                }
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNone(data['question'])

    # Test category quiz when all category questions have been used
    def test_quiz_no_questions_remaining_in_category(self):
        with self.app.app_context():
            questions = Question.query.filter(
                Question.category == str(self.science_id)
            ).all()

            previous_questions = [
                question.id
                for question in questions
            ]

        res = self.client.post(
            '/quizzes',
            json={
                'previous_questions': previous_questions,
                'quiz_category': {
                    'id': self.science_id,
                    'type': 'Science'
                }
            }
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNone(data['question'])

    # Test invalid quiz request
    def test_quiz_invalid_body(self):
        res = self.client.post(
            '/quizzes',
            json={}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)

    # Test 404 error handler
    def test_404_error(self):
        res = self.client.get(
            '/this-route-does-not-exist'
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(
            data['message'],
            'resource not found'
        )

    # Test 422 error handler
    def test_422_error(self):
        res = self.client.post(
            '/questions/search',
            json={}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(
            data['message'],
            'unprocessable'
        )


if __name__ == '__main__':
    unittest.main()