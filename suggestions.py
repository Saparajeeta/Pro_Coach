FOLLOW_UPS = {
    "Squats": [
        {"page": "pages/Lunges AI Trainer.py", "label": "Lunges", "reason": "works the same muscle group from a different angle"},
        {"page": "pages/12_Romanian_Deadlifts.py", "label": "Romanian Deadlifts", "reason": "extends the posterior chain with a different loading pattern"},
    ],
    "Push-ups": [
        {"page": "pages/Tricep KickBack.py", "label": "Tricep KickBack", "reason": "works the same upper-body pushing pattern from a different angle"},
        {"page": "pages/10_Overhead_Dumbbell_Shoulder_Press.py", "label": "Shoulder Press", "reason": "targets the front-deltoid and triceps with a different pressing angle"},
    ],
    "Bicep Curls": [
        {"page": "pages/Tricep KickBack.py", "label": "Tricep KickBack", "reason": "works the same upper arm from a different angle"},
        {"page": "pages/11_Standing_Lateral_Dumbbell_Raises.py", "label": "Lateral Raises", "reason": "adds shoulder work with a different arm path"},
    ],
    "Tree Pose": [
        {"page": "pages/14_Warrior_II_Pose.py", "label": "Warrior II Pose", "reason": "builds balance and lower-body control with a different stance"},
    ],
    "Warrior II Pose": [
        {"page": "pages/13_Tree_Pose.py", "label": "Tree Pose", "reason": "builds balance and lower-body control with a different stance"},
    ],
    "Lunges": [
        {"page": "pages/Squat AI Trainer.py", "label": "Squats", "reason": "works the same lower-body pattern in a different range of motion"},
        {"page": "pages/12_Romanian_Deadlifts.py", "label": "Romanian Deadlifts", "reason": "strengthens the posterior chain with a different movement pattern"},
    ],
    "Shoulder Press": [
        {"page": "pages/11_Standing_Lateral_Dumbbell_Raises.py", "label": "Lateral Raises", "reason": "offers another shoulder movement pattern"},
    ],
    "Lateral Raises": [
        {"page": "pages/10_Overhead_Dumbbell_Shoulder_Press.py", "label": "Shoulder Press", "reason": "offers another shoulder movement pattern"},
    ],
    "Romanian Deadlifts": [
        {"page": "pages/Squat AI Trainer.py", "label": "Squats", "reason": "offers another lower-body movement pattern"},
    ],
    "Cricket Bowling": [
        {"page": "pages/16_Football_Kick.py", "label": "Football Kick", "reason": "offers a different sports movement to practice"},
    ],
    "Football Kick": [
        {"page": "pages/15_Cricket_Bowling_Action.py", "label": "Cricket Bowling", "reason": "offers a different sports movement to practice"},
    ],
}

MISTAKE_TIPS = {
    "Sagging Back in Pushups": "Keep your torso rigid and brace your core before lowering into the push-up.",
    "Asymmetrical Squat Load": "Keep your hips level and distribute your weight evenly through both feet.",
    "KNEE FALLING OVER TOE": "Keep the knee tracking over the midfoot and avoid collapsing inward.",
    "MOVE HAND FORWARD": "Keep the movement path controlled and move the hand in a straight line.",
    "STRAIGHTEN YOUR BACK": "Stand tall and keep your spine neutral while your arm moves.",
    "BEND BACKWARDS": "Keep your torso stacked over your hips and avoid leaning backward.",
    "BEND FORWARD": "Stay tall through the chest and keep your torso more upright.",
    "SQUAT TOO DEEP": "Stop the descent before your hips drop below a stable, controlled depth.",
    "LOWER YOUR HIPS": "Lower the hips smoothly and keep the knees aligned with the toes.",
    "KEEP YOUR BACK STRAIGHT": "Brace your core and keep the back neutral throughout the rep.",
    "GO LOWER": "Lower with control and keep the body aligned while descending.",
    "HOLD TIME": "Keep your balance steady and focus on smooth alignment instead of rushing the pose.",
}


def build_suggestions(exercise, correct, incorrect, mistakes):
    follow_ups = FOLLOW_UPS.get(exercise, FOLLOW_UPS.get("Squats", []))
    tips = []
    if mistakes:
        for item in mistakes:
            if item in MISTAKE_TIPS:
                tips.append(MISTAKE_TIPS[item])
    return {
        "follow_ups": follow_ups,
        "tips": tips,
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    }
