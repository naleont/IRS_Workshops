from flask import Flask
from flask import render_template, request, redirect, url_for
from models import *

app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
db.create_all()


@app.route('/workshop/<wsh_id>/', defaults={'saved': None})
@app.route('/workshop/<wsh_id>/<saved>')
def main(wsh_id, saved):
    name = Workshops.query.filter(Workshops.wsh_id == wsh_id).first().wsh_name
    return render_template('workshops.html', workshop=wsh_id, name=name, saved=saved)


@app.route('/evaluate/<workshop>/<grade>')
def evaluate(workshop, grade):
    ip = request.remote_addr
    if ip not in [g.ip for g in Grades.query.filter(Grades.wsh_id == workshop).all()]:
        grade = Grades(workshop, ip, grade)
        db.session.add(grade)
    else:
        db.session.query(Grades).filter(Grades.wsh_id == workshop
                                        ).filter(Grades.ip == ip).update({Grades.grade: grade})
    db.session.commit()
    return redirect(url_for('.main', wsh_id=workshop, saved=True))


@app.route('/add_wshs', defaults={'success': None, 'no': None})
@app.route('/add_wshs/<success>/<no>')
def add_wshs(success, no):
    return render_template('add_wshs.html', success=success, no=no)


@app.route('/accept_wshs', methods=['POST'])
def accept_wshs():
    data = request.form['data']
    wshs = data.split('\n')
    print(wshs)
    try:
        for wsh in wshs:
            if wsh not in [w.wsh_name for w in Workshops.query.all()] and wsh != '':
                w = Workshops(wsh.strip('\r'))
                db.session.add(w)
                db.session.commit()
        success = True
    except Exception:
        success = False
    no = len(wshs)
    return redirect(url_for('.add_wshs', success=success, no=no))


@app.route('/results')
def results():
    res = []
    for w in Workshops.query.all():
        w_id = w.wsh_id
        grades = {'name': w.wsh_name, 'no': 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 'avg':0}
        if w_id in [g.wsh_id for g in Grades.query.all()]:
            for g in Grades.query.filter(Grades.wsh_id == w_id):
                grades['no'] += 1
                if g.grade == 1:
                    grades[1] += 1
                elif g.grade == 2:
                    grades[2] += 1
                elif g.grade == 3:
                    grades[3] += 1
                elif g.grade == 4:
                    grades[4] += 1
                elif g.grade == 5:
                    grades[5] += 1
                total = 0
                for o in range(1, 6):
                    this_grade = o * grades[o]
                    total += this_grade
                grades['avg'] = total / grades['no']
        res.append(grades)
    res_sorted = sorted(res, key=lambda d: d['avg'], reverse=True)
    return render_template('results.html', res=res_sorted)


if __name__ == '__main__':
    app.run(debug=False)
