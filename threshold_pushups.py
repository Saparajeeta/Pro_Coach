# Get thresholds for beginner mode
def get_thresholds_beginner():

    # Angle of the elbow (Shoulder -> Elbow -> Wrist)
    # NORMAL: arms extended (up position)
    # TRANS: going down
    # PASS: deep pushup (down position)
    _ANGLE_ELBOW = {
                    'NORMAL' : (180, 140),
                    'TRANS'  : (139, 90),
                    'PASS'   : (89, 45)
                   }    
        
    thresholds = {
                    'ELBOW_ANGLE': _ANGLE_ELBOW,

                    # Straight back tracking (Shoulder -> Hip -> Knee)
                    'HIP_ANGLE_THRESH' : 150, # If angle is < 150, back is sagging/raised

                    'OFFSET_THRESH'    : 35.0,
                    'INACTIVE_THRESH'  : 15.0,

                    'CNT_FRAME_THRESH' : 50
                            
                }

    return thresholds
