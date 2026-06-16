from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from datetime import datetime
import openai
from app import db
from app.models import AIChatHistory
from app.forms import AIQueryForm
from flask import current_app

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    form = AIQueryForm()
    chat_history = AIChatHistory.query.filter_by(user_id=current_user.id).order_by(
        AIChatHistory.timestamp.desc()
    ).all()
    
    if form.validate_on_submit():
        return get_ai_response()
    
    return render_template("ai/chat.html", form=form, chat_history=chat_history)


@ai_bp.route("/api/chat", methods=["POST"])
@login_required
def get_ai_response():
    data = request.get_json()
    question = data.get("question", "").strip()
    
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400
    
    if not current_app.config.get("OPENAI_API_KEY"):
        return jsonify({"error": "OpenAI API key not configured"}), 500
    
    try:
        openai.api_key = current_app.config.get("OPENAI_API_KEY")
        
        system_prompt = """You are a helpful financial advisor for college students. 
        Provide practical, actionable advice about budgeting, saving, expense tracking, 
        and financial planning. Keep responses concise and student-friendly. 
        Focus on helping them manage limited budgets and plan for future purchases."""
        
        response = openai.ChatCompletion.create(
            model=current_app.config.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        chat_entry = AIChatHistory(
            user_id=current_user.id,
            question=question,
            response=ai_response,
            timestamp=datetime.utcnow()
        )
        db.session.add(chat_entry)
        db.session.commit()
        
        return jsonify({
            "response": ai_response,
            "timestamp": chat_entry.timestamp.isoformat()
        })
    
    except openai.error.AuthenticationError:
        return jsonify({"error": "Invalid OpenAI API key"}), 500
    except openai.error.APIError as e:
        print(f"OpenAI API Error: {e}")
        return jsonify({"error": "Failed to get response from AI. Please try again."}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred. Please try again."}), 500


@ai_bp.route("/api/chat-history")
@login_required
def get_chat_history():
    chat_history = AIChatHistory.query.filter_by(user_id=current_user.id).order_by(
        AIChatHistory.timestamp.desc()
    ).limit(50).all()
    
    return jsonify([{
        "id": ch.id,
        "question": ch.question,
        "response": ch.response,
        "timestamp": ch.timestamp.isoformat()
    } for ch in chat_history])


@ai_bp.route("/api/delete-chat/<int:chat_id>", methods=["DELETE"])
@login_required
def delete_chat(chat_id):
    chat = AIChatHistory.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    try:
        db.session.delete(chat)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"error": "Failed to delete chat"}), 500

