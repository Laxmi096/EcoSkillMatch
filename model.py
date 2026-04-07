# model.py

def recommend_green_paths(skills, location=None):
    skills = skills.lower().split(",")

    # REALISTIC job links (as examples from popular job boards)
    GREEN_JOBS = [
        {
            "title": "Renewable Energy Analyst",
            "company": "Green Power Corp",
            "location": "Remote",
            "link": "https://www.indeed.com/viewjob?jk=renewable-energy-analyst-001",
            "skills": ["solar", "energy", "sustainability", "analysis"]
        },
        {
            "title": "Environmental Consultant",
            "company": "EcoConsult",
            "location": "Bangalore",
            "link": "https://in.linkedin.com/jobs/view/environmental-consultant-bangalore-002",
            "skills": ["environment", "policy", "sustainability"]
        },
        {
            "title": "Sustainability Manager",
            "company": "Future Earth",
            "location": "Mumbai",
            "link": "https://www.naukri.com/sustainability-manager-jobs",
            "skills": ["management", "esg", "reporting"]
        }
    ]

    COURSES = [
        {
            "name": "Renewable Energy Specialization",
            "platform": "Coursera",
            "link": "https://www.coursera.org/specializations/renewable-energy",
            "skills": ["renewable", "energy"]
        },
        {
            "name": "Sustainable Development Goals (SDGs)",
            "platform": "edX",
            "link": "https://www.edx.org/professional-certificate/sustainable-development",
            "skills": ["policy", "sustainability"]
        },
        {
            "name": "Climate Change & Environment",
            "platform": "Udemy",
            "link": "https://www.udemy.com/course/climate-change-environment",
            "skills": ["climate", "environment"]
        }
    ]

    STARTUPS = [
        {
            "name": "SolarNest",
            "idea": "Affordable rooftop solar solutions",
            "link": "https://angel.co/company/solarnest",
            "skills": ["solar", "energy"]
        },
        {
            "name": "EcoRecycle",
            "idea": "Plastic recycling & circular economy",
            "link": "https://angel.co/company/ecorecycle",
            "skills": ["recycling", "sustainability"]
        },
        {
            "name": "GreenFarm",
            "idea": "Organic farming & agri-tech",
            "link": "https://angel.co/company/greenfarm",
            "skills": ["agriculture", "organic"]
        }
    ]

    jobs, courses, startups = [], [], []

    for job in GREEN_JOBS:
        if any(skill in job["skills"] for skill in skills):
            jobs.append(job)

    for course in COURSES:
        if any(skill in course["skills"] for skill in skills):
            courses.append(course)

    for st in STARTUPS:
        if any(skill in st["skills"] for skill in skills):
            startups.append(st)

    # If no matches, still show a few
    if not jobs:
        jobs = GREEN_JOBS
    if not courses:
        courses = COURSES
    if not startups:
        startups = STARTUPS

    return {
        "green_jobs": jobs,
        "courses": courses,
        "startups": startups
    }
