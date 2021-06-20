from flask import Flask, request, render_template, send_from_directory
from hashlib import md5
from tinydb import TinyDB, Query
from requests import post
app = Flask(__name__, static_folder='static')
hashes = {
  "user": "26ed49287e3bbe890bd58ae3b174a91a",
  "pass": "17b525ce8f0f7ecab8e9672152b666c8"
}
db = TinyDB('db.json')
candidates = db.table('candidates')

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/', methods=["GET", "POST"])
def main():
  return render_template('index.html')

@app.route('/admin', methods=["GET", "POST"])
def admin():
  if request.method == "POST":
    form = request.form.to_dict()
    if 'user' in form and 'pass' in form:
      form_type = "login"
    elif 'name' in form and 'experience' in form:
      form_type = "screening"
    if form_type == "login":
      if md5(form["user"].encode()).hexdigest() == hashes["user"] and md5(form["pass"].encode()).hexdigest() == hashes["pass"]:
        return render_template('screening.html')
      else:
        return render_template('admin.html', errors = "Username or password incorrect.")
    elif form_type == "screening":
      
      name = form["name"]
      experience = form["experience"]
      points = form["points"]
      equipment = form["equipment"]
      medical = form["medical"]
      manual = form["manual"]
      soon = form["soon"]
      notes = form["notes"]
      if 'nights' in form:
        nights = 'yes'
      else:
        nights = 'no'
      if 'saturdays' in form:
        saturdays = 'yes'
      else:
        saturdays = 'no'
      if 'sundays' in form:
        sundays = 'yes'
      else:
        sundays = 'no'
      if 'local' in form:
        local = 'yes'
      else:
        local = 'no'
      if 'regional' in form:
        regional = 'yes'
      else:
        regional = 'no'

      candidates.insert({'name': name, 'experience': experience, 'points': points, 'equipment': equipment, 'medical': medical, 'manual': manual, 'nights': nights, 'saturdays': saturdays, 'sundays': sundays, 'local': local, 'regional': regional, 'soon': soon, 'notes': notes})
      print(candidates.all())
      print(type(candidates.all()))

      msg = f'Name:  {name}\nYears Driving:  {experience}\nPoints in the last 3 years:  {points}\nEquipment Driven:  {equipment}\nValid medical card:  {medical}\nManual transmission:  {manual}\nAvailability:  {nights}, {saturdays}, {sundays}, {local}, {regional}\nHow soon can start:  {soon}\nNotes:  {notes}'
      post('https://discord.com/api/webhooks/855181200834560010/cQfZZFKek-bL6X4zmX38ecmVQilQglzgO2W0s0b_eDWslx8Cdqwh_X16pywdOWODVyYO', data={'content': msg})
      return render_template('screening.html')


  return render_template('admin.html')
