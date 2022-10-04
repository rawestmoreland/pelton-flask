from flask import Flask, jsonify, request
from peloton import PelotonWorkout
import requests

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return "<p>The fake Peloton API</p>"


@app.route("/workouts", methods=['GET'])
def workouts():
    if (request.method == 'GET'):
        data = []
        workouts = PelotonWorkout.list()
        print(f"Workouts: {len(workouts)}")
        for workout in workouts:
            data.append(
                {"start_time": workout.start_time, "personal_record": workout.personal_record, "fitness_discipline": workout.fitness_discipline})
        return jsonify(data)


@app.route("/instructors", methods=['GET'])
def instructors():
    if (request.method == 'GET'):
        response = requests.get('https://api.onepeloton.com/api/instructor')
        return response.json()


@app.route("/latest", methods=['GET'])
def latest():
    if (request.method == 'GET'):
        workout = PelotonWorkout.latest()
        data = {
            "start_time": workout.start_time,
            "personal_record": workout.personal_record,
            "fitness_discipline": workout.fitness_discipline,
            "title": workout.ride.title,
            "instructor": {
                "first_name": workout.ride.instructor.first_name,
                "last_name": workout.ride.instructor.last_name,
                "bio": workout.ride.instructor.bio,
                "short_bio": workout.ride.instructor.short_bio
            },
            "description": workout.ride.description,
            "heart_rate": {
                "average": workout.metrics.heart_rate.average,
                "max": workout.metrics.heart_rate.max,
                "values": workout.metrics.heart_rate.values
            }
        }
        return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
