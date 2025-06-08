# app.py

from flask import Flask, jsonify, request
import os
import openai
import json
from dotenv import load_dotenv
from datetime import datetime, timezone

from seo_fetcher import fetch_seo_metrics
from ai_generator import generate_blog
from apscheduler.schedulers.background import BackgroundScheduler

# Load environment variables (including OPENAI_API_KEY)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure the API key is available
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not set in .env")

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, AI Blog Generator!"

@app.route('/generate')
def generate():
    """
    GET /generate?keyword=<your_keyword>
    1. Read the “keyword” query parameter. If missing, return a 400 error.
    2. Call fetch_seo_metrics(keyword) to get SEO data.
    3. Call generate_blog(keyword, metrics) to ask OpenAI for a blog draft.
    4. Merge everything (keyword, metrics, blog_data, generated_at) into one JSON dict.
    5. Return that dict as a JSON response.
    """
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "please provide keyword"}), 400

    # Fetch or mock SEO metrics for this keyword
    try:
        seo_metrics = fetch_seo_metrics(keyword)
    except Exception as e:
        return jsonify({"error": f"SEO fetcher failed: {e}"}), 500

    # Generate the actual blog content via ai_generator.generate_blog()
    try:
        blog_data = generate_blog(keyword, seo_metrics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Create a timezone‐aware UTC timestamp
    now_utc = datetime.now(timezone.utc)
    generated_at = now_utc.isoformat().replace("+00:00", "Z")

    # Merge everything into one dict
    result = {
        "keyword": keyword,
        **seo_metrics,
        **blog_data,
        "generated_at": generated_at
    }
    return jsonify(result), 200


# APScheduler daily job configuration
# 1) Predefined keyword 
DAILY_KEYWORD = os.getenv("DAILY_KEYWORD", "wireless earbuds")
# 2) Scheduled time (hour and minute in server’s timezone)
DAILY_HOUR = int(os.getenv("DAILY_HOUR"))
DAILY_MINUTE = int(os.getenv("DAILY_MINUTE"))

def run_daily_task():
    """
    This function runs once per day. It:
    1. Fetches SEO metrics for DAILY_KEYWORD
    2. Calls generate_blog()
    3. Adds a generated_at timestamp
    4. Writes the full JSON payload to a file under daily_posts/
    """
    kw = DAILY_KEYWORD
    try:
        metrics = fetch_seo_metrics(kw)
        blog_data = generate_blog(kw, metrics)
    except Exception as e:
        # Log error with a timezone‐aware timestamp
        now_log = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        print(f"[{now_log}] ERROR in daily task: {e}")
        return

    # Generate a timezone-aware UTC timestamp
    now_utc = datetime.now(timezone.utc)
    generated_at = now_utc.isoformat().replace("+00:00", "Z")

    payload = {
        "keyword": kw,
        **metrics,
        **blog_data,
        "generated_at": generated_at
    }

    # Ensure the folder exists
    os.makedirs("daily_posts", exist_ok=True)
    # File name format: daily_posts/<keyword>_YYYYMMDD.json
    safe_kw = kw.replace(" ", "_")
    date_str = now_utc.strftime("%Y%m%d")
    filename = f"daily_posts/{safe_kw}_{date_str}.json"

    # Write the JSON file with indent=2, ensure_ascii=False for readability
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[{now_utc.isoformat()}] Daily blog generated: {filename}")


if __name__ == '__main__':
    # 1) Start the scheduler
    scheduler = BackgroundScheduler()
    # Schedule at the specified hour/minute every day
    scheduler.add_job(
        run_daily_task,
        trigger="cron",
        hour=DAILY_HOUR,
        minute=DAILY_MINUTE
    )
    scheduler.start()
    print(f"APScheduler started: daily job at {DAILY_HOUR:02d}:{DAILY_MINUTE:02d} for '{DAILY_KEYWORD}'")

    # 2) Run Flask as usual
    app.run(host='0.0.0.0', port=5001, debug=True)
