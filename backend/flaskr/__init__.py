from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    # CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,PATCH,DELETE,OPTIONS'
        )
        response.headers.add(
            'Access-Control-Allow-Origin',
            '*'
        )
        return response

    # Error Handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    # Create database tables
    with app.app_context():
        db.create_all()

    # CATEGORIES

    @app.route('/categories')
    def get_categories():

        categories = Category.query.order_by(Category.id).all()

        found_categories = {}

        for category in categories:
            found_categories[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': found_categories
        })

    # PAGINATION

    def paginate_questions(request, selection):

        page = request.args.get('page', 1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [
            question.format()
            for question in selection
        ]

        return questions[start:end]

    # GET ALL QUESTIONS

    @app.route('/questions')
    def get_questions():

        selected_questions = Question.query.order_by(
            Question.id
        ).all()

        show_all_questions = paginate_questions(
            request,
            selected_questions
        )

        categories = Category.query.order_by(
            Category.id
        ).all()

        format_categories = {
            category.id: category.type
            for category in categories
        }

        return jsonify({
            'success': True,
            'questions': show_all_questions,
            'total_questions': len(selected_questions),
            'categories': format_categories,
            'current_category': None
        })

    # DELETE QUESTION

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question_to_delete = Question.query.get(question_id)

        if question_to_delete is None:
            abort(404)

        try:
            db.session.delete(question_to_delete)
            db.session.commit()

        except Exception:
            db.session.rollback()
            abort(422)

        selection = Question.query.order_by(
            Question.id
        ).all()

        refreshed_questions = paginate_questions(
            request,
            selection
        )

        return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': refreshed_questions,
            'total_questions': len(selection)
        })

    # CREATE QUESTION

    @app.route('/questions', methods=['POST'])
    def create_question():

        body = request.get_json()

        if not body:
            abort(422)

        question_text = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        if (
            not question_text
            or not answer
            or category is None
            or difficulty is None
        ):
            abort(422)

        try:

            new_question = Question(
                question=question_text,
                answer=answer,
                category=str(category),
                difficulty=difficulty
            )

            db.session.add(new_question)
            db.session.commit()

            return jsonify({
                'success': True,
                'created': new_question.id
            }), 201

        except Exception:

            db.session.rollback()
            abort(422)

    # SEARCH QUESTIONS

    @app.route('/questions/search', methods=['POST'])
    def search_questions():

        body = request.get_json()

        if not body or 'searchTerm' not in body:
            abort(422)

        search_term = body['searchTerm']

        questions = Question.query.filter(
            Question.question.ilike(
                f'%{search_term}%'
            )
        ).all()

        categories = Category.query.order_by(
            Category.id
        ).all()

        format_categories = {
            category.id: category.type
            for category in categories
        }

        return jsonify({
            'success': True,
            'questions': [
                question.format()
                for question in questions
            ],
            'total_questions': len(questions),
            'current_category': None,
            'categories': format_categories
        })

    # GET QUESTIONS BY CATEGORY

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        category = Category.query.get(category_id)

        if category is None:
            abort(404)

        selected_questions = Question.query.filter(
            Question.category == str(category_id)
        ).order_by(
            Question.id
        ).all()

        show_questions = paginate_questions(
            request,
            selected_questions
        )

        categories = Category.query.order_by(
            Category.id
        ).all()

        format_categories = {
            category.id: category.type
            for category in categories
        }

        return jsonify({
            'success': True,
            'questions': show_questions,
            'total_questions': len(selected_questions),
            'current_category': category_id,
            'categories': format_categories
        })

    # QUIZ

    @app.route('/quizzes', methods=['POST'])
    def quiz():

        body = request.get_json()

        if not body:
            abort(422)

        previous_questions = body.get(
            'previous_questions',
            []
        )

        quiz_category = body.get(
            'quiz_category'
        )

        # Get questions for selected category
        if quiz_category:

            category_id = quiz_category.get('id')

            if category_id:
                questions = Question.query.filter(
                    Question.category == str(category_id)
                ).all()
            else:
                questions = Question.query.all()

        else:
            questions = Question.query.all()

        # Remove questions already asked
        available_questions = [
            question
            for question in questions
            if question.id not in previous_questions
        ]

        # No questions left
        if not available_questions:
            return jsonify({
                'success': True,
                'question': None
            })

        # Select a random question
        random_question = random.choice(
            available_questions
        )

        return jsonify({
            'success': True,
            'question': random_question.format()
        })

    return app