import streamlit as st


GUIDES = {
    "Squats": {
        "goal": "Practice a controlled squat while keeping your torso and knees aligned.",
        "camera": "Use a front or side view and stand far enough away to keep your full body in frame.",
        "steps": [
            "Stand with your feet in a comfortable stance.",
            "Brace gently and begin bending your hips and knees.",
            "Lower while keeping your feet planted and torso steady.",
            "Return to standing with control.",
        ],
        "checks": ["BEND BACKWARDS", "BEND FORWARD", "KNEE FALLING OVER TOE", "SQUAT TOO DEEP", "WEIGHT SHIFT DETECTED"],
        "mistakes": ["Letting the knees drift inward", "Shifting weight unevenly", "Rushing the descent"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Push-ups": {
        "goal": "Practice a steady push-up while keeping your body aligned.",
        "camera": "Use a side view and position the camera far enough away to show your full body on the floor.",
        "steps": [
            "Place your hands beneath your shoulders and extend your legs.",
            "Keep your body in a steady line from shoulders to heels.",
            "Bend your elbows and lower with control.",
            "Press through your hands to return to the start.",
        ],
        "checks": ["KEEP BACK STRAIGHT", "GO LOWER"],
        "mistakes": ["Letting the hips sag", "Flaring the elbows", "Moving too quickly"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Bicep Curls": {
        "goal": "Practice a controlled curl while keeping your upper arm steady.",
        "camera": "Use a front or side view and stand far enough away to keep your arms and torso in frame.",
        "steps": [
            "Stand tall with your arms relaxed by your sides.",
            "Keep your elbows close to your torso.",
            "Bend your elbows to bring your hands upward.",
            "Lower your hands slowly to the start.",
        ],
        "checks": ["STRAIGHTEN YOUR BACK", "MOVE HAND FORWARD", "MOVE HAND BACKWARD"],
        "mistakes": ["Swinging the torso", "Moving the elbows forward", "Dropping the hands quickly"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Lunges": {
        "goal": "Practice a controlled lunge while keeping your balance and alignment.",
        "camera": "Use a front or side view and stand far enough away to keep your full body in frame.",
        "steps": [
            "Stand tall with your feet comfortably apart.",
            "Step one foot forward and keep your torso steady.",
            "Bend both knees as you lower with control.",
            "Push through the front foot to return to standing.",
        ],
        "checks": ["BEND BACKWARDS", "BEND FORWARD", "KNEE FALLING OVER TOE", "SQUAT TOO DEEP"],
        "mistakes": ["Leaning the torso", "Letting the front knee drift inward", "Losing balance during the step"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Tricep Kickback": {
        "goal": "Practice a controlled arm extension while keeping your upper arm steady.",
        "camera": "Use a side view and stand far enough away to keep your torso and moving arm in frame.",
        "steps": [
            "Hinge forward comfortably and keep your back steady.",
            "Keep your upper arm close to your torso.",
            "Extend your forearm behind you with control.",
            "Bend your elbow to return to the start.",
        ],
        "checks": ["STRAIGHTEN YOUR BACK", "MOVE HAND FORWARD", "MOVE HAND BACKWARD"],
        "mistakes": ["Rounding the back", "Moving the upper arm", "Swinging through the extension"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Dumbbell Fly": {
        "goal": "Practice a controlled arm movement while keeping your shoulders steady.",
        "camera": "Use a front or side view and position the camera far enough away to show your full upper body.",
        "steps": [
            "Stand in a stable position and soften your elbows.",
            "Move your arms outward without changing your posture.",
            "Bring your arms back toward the center with control.",
            "Keep the movement comfortable and steady.",
        ],
        "checks": ["STRAIGHTEN YOUR BACK", "MOVE HAND FORWARD", "MOVE HAND BACKWARD", "Experimental: this page uses elbow-angle repetition counting. Form feedback is not calibrated for dumbbell fly."],
        "mistakes": ["Bending or locking the elbows abruptly", "Swinging the arms", "Leaning the torso"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Shoulder Press": {
        "goal": "Practice a steady overhead press while keeping your torso upright.",
        "camera": "Use a front or side view and stand far enough away to keep your full body and raised arms in frame.",
        "steps": [
            "Stand comfortably with your arms bent near shoulder level.",
            "Keep your torso steady as you press upward.",
            "Extend your arms without leaning backward.",
            "Lower your arms smoothly to the start.",
        ],
        "checks": [],
        "mistakes": ["Leaning backward", "Moving unevenly", "Rushing the lowering phase"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Lateral Raises": {
        "goal": "Practice a controlled side raise while keeping your torso steady.",
        "camera": "Use a front view and stand far enough away to keep your full body and arms in frame.",
        "steps": [
            "Stand tall with your arms relaxed at your sides.",
            "Raise your arms out to the sides with control.",
            "Keep your shoulders relaxed and torso steady.",
            "Lower your arms slowly to the start.",
        ],
        "checks": ["WARNING: Arms too high!"],
        "mistakes": ["Shrugging the shoulders", "Swinging the torso", "Raising the arms too high"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Romanian Deadlifts": {
        "goal": "Practice a controlled hip hinge while keeping your back steady.",
        "camera": "Use a side view and stand far enough away to keep your full body in frame.",
        "steps": [
            "Stand tall with a soft bend in your knees.",
            "Send your hips back while keeping your back steady.",
            "Lower your hands along your legs with control.",
            "Drive your hips forward to return to standing.",
        ],
        "checks": ["Keep legs straight, hinge at hips!"],
        "mistakes": ["Rounding the back", "Bending the knees too much", "Moving the hips forward too soon"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Tree Pose": {
        "goal": "Practice holding a balanced standing pose with steady posture.",
        "camera": "Use a front view and position the camera far enough away to show your full body and feet.",
        "steps": [
            "Stand tall and focus your gaze on a steady point.",
            "Shift your weight onto one foot.",
            "Bring the other foot to a comfortable position on the standing leg.",
            "Keep your hips level and breathe steadily while holding.",
        ],
        "checks": ["GET INTO POSE", "Keep your hips level!"],
        "mistakes": ["Rushing into the balance", "Letting the hips tilt", "Looking around while balancing"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Warrior II": {
        "goal": "Practice a steady wide stance with your arms extended.",
        "camera": "Use a front or side view and stand far enough away to keep your full body and arms in frame.",
        "steps": [
            "Take a wide, comfortable stance and turn one foot outward.",
            "Bend the front knee while keeping your torso upright.",
            "Extend both arms out to the sides.",
            "Hold steadily, then change sides comfortably.",
        ],
        "checks": ["GET INTO POSE", "Keep your arms parallel to the ground!", "Bend your front knee more!"],
        "mistakes": ["Leaning the torso", "Letting the arms drop", "Letting the front knee drift inward"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Cricket Bowling": {
        "goal": "Practice a controlled bowling action while keeping your body balanced.",
        "camera": "Use a side-on view and stand far enough away to keep your whole body and bowling path in frame.",
        "steps": [
            "Begin in a balanced stance with your full body visible.",
            "Move through your approach with control.",
            "Keep your trunk steady as your bowling arm moves.",
            "Complete the action while maintaining balance.",
        ],
        "checks": ["FRONT KNEE TOO STRAIGHT", "KEEP TRUNK TALL", "SMOOTHER ELBOW EXTENSION", "LOAD THE BACK LEG"],
        "mistakes": ["Losing balance through the action", "Letting the trunk lean", "Rushing the arm movement"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
    "Football Kick": {
        "goal": "Practice a controlled kick while keeping your trunk and plant foot steady.",
        "camera": "Use a side-on view and stand far enough away to keep your full body and kicking path in frame.",
        "steps": [
            "Stand in a balanced position with your full body visible.",
            "Set your plant foot beside the ball area.",
            "Swing your kicking leg through with control.",
            "Finish in balance and reset comfortably.",
        ],
        "checks": ["WIDE PLANT FOOT", "KEEP TRUNK OVER BALL", "LOAD KICKING LEG", "SNAP KNEE THROUGH"],
        "mistakes": ["Placing the plant foot too far away", "Leaning the trunk excessively", "Losing balance after contact"],
        "safety": "If you feel pain, stop and consult a qualified trainer or doctor.",
    },
}


def render_guide(name):
    guide = GUIDES.get(name)
    if guide is None:
        return

    seen_key = f"guide_seen_{name}"
    with st.expander(
        "How to do this exercise (new here? start here)",
        expanded=not st.session_state.get(seen_key, False),
    ):
        st.markdown("**Goal**")
        st.write(guide["goal"])
        st.markdown("**Camera**")
        st.write(guide["camera"])
        st.markdown("**Steps**")
        for step in guide["steps"]:
            st.write(f"- {step}")
        st.markdown("**Checks**")
        if guide["checks"]:
            for check in guide["checks"]:
                st.write(f"- {check}")
        else:
            st.write("No separate form-check banners are defined for this page.")
        st.markdown("**Mistakes**")
        for mistake in guide["mistakes"]:
            st.write(f"- {mistake}")
        st.markdown("**Safety**")
        st.write(guide["safety"])

    st.session_state[seen_key] = True