from flask import render_template, request
from manage import app, db, mongo, GIS_institute, EC_institute, DVLA_institute


def add_citizens():
    citizen_1 = EC_institute(
        first_name="Sabrina",
        middle_name="Lamie",
        last_name="Awuni",
        age=22
    )
    citizen_2 = GIS_institute(
        first_name="Sabrina",
        middle_name="Lamie",
        last_name="Awuni",
        age=22
    )
    citizen_3 = DVLA_institute(
        first_name="Sabrina",
        middle_name="Lamie",
        last_name="Awuni",
        age=22
    )
    citizen_4 = {
        "first_name": "Sabrina",
        "middle_name": "Lamie",
        "last_name": "Awuni",
        "age": "25",
    }
    #
    db.session.add(citizen_1)  # Adds new User record to database
    db.session.add(citizen_2)  # Adds new User record to database
    db.session.add(citizen_3)  # Adds new User record to database
    db.session.commit()
    mongo.db.individual_NHIS.insert(citizen_4)

@app.route('/', methods=['GET', 'POST'])
def index():
    #add_citizens()
    errors = []

    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if first_name and last_name:
            results_EC = EC_institute.query.filter_by(first_name=first_name, last_name=last_name).all()
            results_GIS = GIS_institute.query.filter_by(first_name=first_name, last_name=last_name).all()
            results_DVLA = DVLA_institute.query.filter_by(first_name=first_name, last_name=last_name).all()

            citizens = mongo.db.individual_NHIS
            results_NHIS_1 = []
            for c in citizens.find():
                results_NHIS_1.append(
                    {'first_name': c['first_name'], 'middle_name': c['middle_name'], 'last_name': c['last_name'],
                     'age': c['age']})

            results_NHIS = []
            for citizen in results_NHIS_1:
                if citizen['first_name'] == first_name and citizen['last_name'] == last_name:
                    results_NHIS.append(
                        {'first_name': citizen['first_name'], 'middle_name': citizen['middle_name'],
                         'last_name': citizen['last_name'],
                         'age': citizen['age']})





            return render_template('results.html', results_EC=results_EC, results_GIS=results_GIS,
                                   results_DVLA=results_DVLA, results_NHIS=results_NHIS)
        else:
            errors = {"error": "The request payload is not in JSON format"}

    return render_template('index.html', errors=errors)


@app.route('/results', methods=['GET', ])
def results():
    return render_template('results.html')


if __name__ == "__main__":


    app.run()
