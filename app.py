from flask import Flask, render_template, request, redirect,url_for, session
from flask import Flask, render_template, request, jsonify

import mysql.connector
import hashlib
import os
from werkzeug.utils import secure_filename
from google import genai
import os
client = genai.Client(
    api_key=os.environ.get("AIzaSyC4ajx3cbE1VSlsLbsL-IuYpXRQlh9kjDI"),
    http_options={"api_version": "v1"}

)




# Use environment variable (RECOMMENDED)
client = genai.Client(api_key="AIzaSyC4ajx3cbE1VSlsLbsL-IuYpXRQlh9kjDI")



# ---------------- APP SETUP ----------------
app = Flask(__name__)
app.secret_key = "ecoskillmatch_secret"

# ---------------- DATABASE ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="reegal",
    database="ecoskillmatch"
)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="reegal", # Or "reegal" if you set one
        database="ecoskillmatch"
        
    )

# ---------------- UPLOAD CONFIG ----------------
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- GREEN JOBS DATA ----------------
green_jobs_data = [
    {
        "id": 1,
        "title": "Solar Energy Analyst",
        "company": "Tata Power",
        "location": "Mumbai",
        "type": "Full Time",
        "skills": ["python", "solar", "energy", "excel", "powerbi"],
        "description": "Analyze solar energy systems and sustainability metrics.",
        "link": "https://www.tatapower.com/careers.aspx"
    },
    {
        "id": 2,
        "title": "Environmental Data Analyst",
        "company": "Infosys",
        "location": "Bangalore",
        "type": "Full Time",
        "skills": ["python", "data", "analysis", "climate", "sustainability"],
        "description": "Analyze environmental datasets for sustainability insights.",
        "link": "https://www.infosys.com/careers"
    },
    {
        "id": 3,
        "title": "Solar Energy Data Analyst",
        "company": "Tata Power Renewables",
        "location": "Mumbai",
        "type": "Full Time",
        "skills": ["python", "solar", "energy", "excel"],
        "description": "Solar analytics using Python, Excel and Power BI.",
        "link": "https://www.tatapower.com/renewables"
    }
]

# ---------------- AI JOB MATCHING ----------------
def recommend(user_skills, jobs):
    if isinstance(user_skills, list):
        user_skill_set = set(s.lower().strip() for s in user_skills)
    else:
        user_skill_set = set(user_skills.lower().replace(",", " ").split())

    results = []

    for job in jobs:
        job_skill_set = set(skill.lower() for skill in job["skills"])
        matched = user_skill_set & job_skill_set
        missing = job_skill_set - user_skill_set

        match_percent = int((len(matched) / len(job_skill_set)) * 100)

        if match_percent > 0:
            job_copy = job.copy()
            job_copy["match_percent"] = match_percent
            job_copy["matched_skills"] = list(matched)
            job_copy["missing_skills"] = list(missing)
            job_copy["advice"] = (
                [f"Learn {', '.join(list(missing)[:3])} to improve your chances."]
                if missing else
                ["You're a perfect fit for this role! 🎯"]
            )
            results.append(job_copy)

    return sorted(results, key=lambda x: x["match_percent"], reverse=True)

# ---------------- HOME ----------------
@app.route("/")
def index():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("index.html")
@app.route("/")
def home():
    return render_template("chat.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()
        skills = request.form["skills"]
        location = request.form["location"]

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, skills, location) VALUES (%s,%s,%s,%s,%s)",
            (name, email, password, skills, location)
        )
        db.commit()
        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            session["user"] = user
            return redirect("/dashboard")

        return "Invalid Email"

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=session["user"],
        green_jobs_count=len(green_jobs_data),
        courses_count=4,
        startups_count=4
    )
# ---------------- PROFILE PAGE ----------------
# ---------------- PROFILE ROUTE ----------------
@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if "user" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        new_skills = request.form.get("skills")
        new_location = request.form.get("location")
        user_email = session["user"]["email"]

        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            
            # Check column names: Are they 'skills' and 'location' in your DB?
            query = "UPDATE users SET skills = %s, location = %s WHERE email = %s"
            cursor.execute(query, (new_skills, new_location, user_email))
            db.commit()

            # Refresh session data
            session["user"]["skills"] = new_skills
            session["user"]["location"] = new_location
            session.modified = True 

            cursor.close()
            db.close()
            return redirect(url_for("dashboard"))

        except Exception as e:
            # Look at your CMD/Terminal when you click save!
            print("--- DATABASE ERROR ---")
            print(e) 
            print("-----------------------")
            return f"Update Failed: {str(e)}", 500

    return render_template("edit_profile.html", user=session["user"])
# ---------------- CHANGE PASSWORD ----------------
@app.route("/change-password", methods=["POST"])
def change_password():
    if "user" not in session:
        return redirect("/login")

    old = hashlib.sha256(request.form["old_password"].encode()).hexdigest()
    new = hashlib.sha256(request.form["new_password"].encode()).hexdigest()

    user = session["user"]

    if old != user["password"]:
        return "Wrong old password"

    cursor = db.cursor()
    cursor.execute(
        "UPDATE users SET password=%s WHERE id=%s",
        (new, user["id"])
    )
    db.commit()

    session.clear()
    return redirect("/login")
# ---------------- JOBS ----------------
@app.route("/jobs")
def jobs():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]
    user_skills = session.get("resume_skills") or user.get("skills") or ""

    matched_jobs = recommend(user_skills, green_jobs_data)

    return render_template(
        "jobs.html",
        green_jobs=matched_jobs,
        resume_skills=user_skills
    )

# ---------------- COURSES ----------------
@app.route("/courses")
def courses_page():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]
    courses = [
        {"title": "Sustainable Development", "platform": "Coursera", "provider": "University of Copenhagen", "duration": "6 weeks", "link": "https://www.coursera.org"},
        {"title": "Renewable Energy Systems", "platform": "edX", "provider": "Delft University", "duration": "8 weeks", "link": "https://www.edx.org"},
        {"title": "Climate Change & Environmental Management", "platform": "Udemy", "provider": "Industry Experts", "duration": "Self-paced", "link": "https://www.udemy.com"},
        {"title": "Green Technology & Innovation", "platform": "FutureLearn", "provider": "Imperial College London", "duration": "4 weeks", "link": "https://www.futurelearn.com"}
    ]

    return render_template("courses.html", user=user, courses=courses)

# ---------------- STARTUPS ----------------
@app.route("/startups")
def startups_page():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]
    startups = [
        {"name": "Recykal", "focus": "Plastic Waste Management", "stage": "Growth Stage", "description": "Tech-enabled waste recycling and circular economy startup.", "link": "https://www.recykal.com"},
        {"name": "Ather Energy", "focus": "Electric Vehicles", "stage": "Scale-up", "description": "Electric scooters and EV ecosystem in India.", "link": "https://www.atherenergy.com"},
        {"name": "Ecozen Solutions", "focus": "Clean Energy for Agriculture", "stage": "Startup", "description": "Solar-powered solutions for rural and agricultural use.", "link": "https://www.ecozensolutions.com"},
        {"name": "Oorjan Cleantech", "focus": "Residential Solar", "stage": "Startup", "description": "End-to-end residential solar installation and monitoring.", "link": "https://www.oorjan.com"}
    ]

    return render_template("startups.html", user=user, startups=startups)

# ---------------- RESUME UPLOAD ----------------
@app.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        file = request.files["resume"]
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        with open(path, "r", errors="ignore") as f:
            text = f.read().lower()

        skills_db = [
            "python", "sql", "data", "analysis", "solar",
            "energy", "excel", "powerbi", "climate",
            "sustainability", "renewable"
        ]

        resume_skills = [skill for skill in skills_db if skill in text]
        session["resume_skills"] = resume_skills

        return redirect("/jobs")

    return render_template("upload_resume.html")

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin_dashboard():
    if "user" not in session:
        return redirect("/login")

    if session["user"].get("role") != "admin":
        return "Access Denied", 403

    return render_template(
        "admin_dashboard.html",
        total_users=3,
        total_jobs=len(green_jobs_data),
        total_courses=4,
        total_startups=5,
        skill_labels=["Python", "Solar", "Data", "Sustainability"],
        skill_counts=[4, 3, 5, 2],
        location_labels=["Mumbai", "Pune", "Delhi"],
        location_counts=[3, 5, 7]
    )
@app.route("/interview-prep/<int:job_id>")
def interview_prep(job_id):
    if "user" not in session:
        return redirect(url_for("login"))

    # Find job
    job = next((j for j in green_jobs_data if j["id"] == job_id), None)
    if not job:
        return "Job not found", 404

    # Create AI prompt
    prompt = f"Generate 5 interview questions for a {job['title']} role at {job['company']}. Role info: {job['description']}. List only the questions."

    try:
        # Use the explicit preview ID for the 2026 Gemini 3 models
        response = client.models.generate_content(
            model='gemini-3-flash-preview', 
            contents=prompt
        )

        if not response.text:
            return "AI returned empty response", 500

        # Parse questions (Gemini 3 often adds a 'thought' block, 
        # so we strip potential markdown artifacts)
        questions = [q.strip('* -12345. ') for q in response.text.strip().split('\n') if q.strip()]

        return render_template("interview.html", job=job, questions=questions)

    except Exception as e:
        print(f"AI ERROR DETAILS: {e}")
        return f"AI Error: {str(e)}", 500


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_message
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        print("FULL ERROR:", e)
        return jsonify({"reply": "AI crashed."})


   
    
# ---------------- RUN ----------------
if __name__ == "__main__":
    print("🌱 EcoSkillMatch running successfully")
    app.run(debug=True)
