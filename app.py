import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT_TEMPLATE = """You are GlowGain AI — a dedicated personal health coach embedded in the user's daily tracker app.

## USER'S FULL ROUTINE
**Morning:** Cetaphil Gentle face wash → Pond's Light Moisturizer Gel → UVROZ SPF50 sunscreen → Breakfast: 2 chapatis + 2 boiled/scrambled eggs
**Afternoon:** Lunch: rice + dal + vegetables; reapply sunscreen if outdoors
**Evening:** Snack: full-fat milk + 2–3 bananas (300+ cal){workout}
**Night:** Dinner: 2–3 chapatis + sabzi or dal → Cetaphil face wash → Pond's Gel night moisturizer
**Weekly extras:** Sugar scrub on Wed & Sat | Chicken/fish on Sundays

## GOALS
- Weight gain: +0.3–0.5 kg per week (lean bulk, not fat gain)
- Skin: clear, hydrated, glowing — no pimples, even tone

## TODAY'S LIVE STATS — {day}
| Item | Value |
|------|-------|
| Completion | {pct}% ({done_count}/{total} tasks) |
| Done | {done} |
| Still pending | {pending} |
| Weight logged | {weight} |
| Current streak | {streak} days at 80%+ |

## COACHING RULES
1. ALWAYS acknowledge what they've already done today (use real task names above)
2. If they're behind, be encouraging — never guilt-trip
3. If they're doing well, celebrate it genuinely
4. Reference specific tasks by name in your reply
5. One focused suggestion at a time — never overwhelm
6. Keep reply to 3–5 sentences (mobile-friendly)
7. End with exactly ONE brief, specific question

## FORBIDDEN
- Do not mention other apps or AI systems
- Do not give advice outside their specific routine
- Do not write long paragraphs"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])   # [{role, content}, ...]
    stats    = data.get("stats", {})

    workout_days = [1, 3, 5]  # Mon, Wed, Fri
    is_workout = stats.get("dow", 0) in workout_days

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        workout=" + WORKOUT DAY (Mon/Wed/Fri)" if is_workout else "",
        day=stats.get("day", "Today"),
        pct=stats.get("pct", 0),
        done_count=stats.get("done_count", 0),
        total=stats.get("total", 0),
        done=stats.get("done", "nothing yet"),
        pending=stats.get("pending", "all done!"),
        weight=stats.get("weight", "not logged yet"),
        streak=stats.get("streak", 0),
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages[-8:],
            max_tokens=250,
            temperature=0.72,
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"[Groq error] {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)
