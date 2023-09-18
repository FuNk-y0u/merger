from inc import *
from flask import current_app

def watch():
    response = request.get_json()
    try:
        HostClass = current_app.config[response["token"]] 
        hostTime = HostClass.hostTime
        paused = HostClass.paused
        playing = HostClass.playing
        speed = HostClass.speed
        return jsonify(
            {
                "hostTime": hostTime,
                "paused": paused,
                "playing": playing,
                "speed" : speed
            }
        )
    except Exception as e:
        return Response("Bad request",status=404)

def video():
    return redirect(url_for('static',filename=f'videos/{request.args.get("id")}.webm'))