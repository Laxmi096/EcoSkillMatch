def skill_gap_analysis(user_skills, job_skills):
    user_set = set(user_skills.lower().split())
    job_set = set(job_skills.lower().split())

    matched = list(user_set & job_set)
    missing = list(job_set - user_set)

    advice = []

    if missing:
        advice.append(
            f"To improve your chances, focus on learning: {', '.join(missing)}."
        )
    else:
        advice.append("You already have all the required skills 🎉")

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "advice": advice
    }
