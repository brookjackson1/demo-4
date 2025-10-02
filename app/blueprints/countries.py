from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db

countries = Blueprint('countries', __name__)

@countries.route('/', methods=['GET', 'POST'])
def show_countries():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new country
    if request.method == 'POST':
        country_name = request.form['country_name']
        country_code = request.form['country_code']
        continent = request.form['continent']
        population = request.form['population']

        # Insert the new country into the database
        cursor.execute('INSERT INTO countries (country_name, country_code, continent, population) VALUES (%s, %s, %s, %s)',
                       (country_name, country_code, continent, population))
        db.commit()

        flash('New country added successfully!', 'success')
        return redirect(url_for('countries.show_countries'))

    # Handle GET request with optional filtering
    continent_filter = request.args.get('continent')

    if continent_filter:
        cursor.execute('SELECT * FROM countries WHERE continent = %s ORDER BY country_name', (continent_filter,))
        flash(f'Showing countries in {continent_filter}', 'info')
    else:
        cursor.execute('SELECT * FROM countries ORDER BY country_name')

    all_countries = cursor.fetchall()
    return render_template('countries.html', all_countries=all_countries, selected_continent=continent_filter)

@countries.route('/update_country/<int:country_id>', methods=['POST'])
def update_country(country_id):
    db = get_db()
    cursor = db.cursor()

    # Update the country's details
    country_name = request.form['country_name']
    country_code = request.form['country_code']
    continent = request.form['continent']
    population = request.form['population']

    cursor.execute('UPDATE countries SET country_name = %s, country_code = %s, continent = %s, population = %s WHERE country_id = %s',
                   (country_name, country_code, continent, population, country_id))
    db.commit()

    flash('Country updated successfully!', 'success')
    return redirect(url_for('countries.show_countries'))

@countries.route('/delete_country/<int:country_id>', methods=['POST'])
def delete_country(country_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the country (cities will be deleted automatically due to CASCADE)
    cursor.execute('DELETE FROM countries WHERE country_id = %s', (country_id,))
    db.commit()

    flash('Country deleted successfully!', 'danger')
    return redirect(url_for('countries.show_countries'))

@countries.route('/cities', methods=['GET', 'POST'])
def show_cities():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new city
    if request.method == 'POST':
        city_name = request.form['city_name']
        country_id = request.form['country_id']
        population = request.form['population']
        is_capital = 'is_capital' in request.form

        # Insert the new city into the database
        cursor.execute('INSERT INTO cities (city_name, country_id, population, is_capital) VALUES (%s, %s, %s, %s)',
                       (city_name, country_id, population, is_capital))
        db.commit()

        flash('New city added successfully!', 'success')
        return redirect(url_for('countries.show_cities'))

    # Handle GET request to display all cities with country names
    cursor.execute('''
        SELECT c.city_id, c.city_name, c.population, c.is_capital,
               co.country_name, co.country_id
        FROM cities c
        JOIN countries co ON c.country_id = co.country_id
        ORDER BY co.country_name, c.city_name
    ''')
    all_cities = cursor.fetchall()

    # Get countries for dropdown
    cursor.execute('SELECT country_id, country_name FROM countries ORDER BY country_name')
    countries_list = cursor.fetchall()

    return render_template('cities.html', all_cities=all_cities, countries_list=countries_list)

@countries.route('/update_city/<int:city_id>', methods=['POST'])
def update_city(city_id):
    db = get_db()
    cursor = db.cursor()

    # Update the city's details
    city_name = request.form['city_name']
    country_id = request.form['country_id']
    population = request.form['population']
    is_capital = 'is_capital' in request.form

    cursor.execute('UPDATE cities SET city_name = %s, country_id = %s, population = %s, is_capital = %s WHERE city_id = %s',
                   (city_name, country_id, population, is_capital, city_id))
    db.commit()

    flash('City updated successfully!', 'success')
    return redirect(url_for('countries.show_cities'))

@countries.route('/delete_city/<int:city_id>', methods=['POST'])
def delete_city(city_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the city
    cursor.execute('DELETE FROM cities WHERE city_id = %s', (city_id,))
    db.commit()

    flash('City deleted successfully!', 'danger')
    return redirect(url_for('countries.show_cities'))

@countries.route('/api/countries', methods=['GET'])
def api_countries():
    """API endpoint to get countries for dropdown"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT country_id, country_name FROM countries ORDER BY country_name')
    countries_list = cursor.fetchall()

    return jsonify(countries_list)

@countries.route('/api/cities/<int:country_id>', methods=['GET'])
def api_cities_by_country(country_id):
    """API endpoint to get cities for a specific country"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT city_id, city_name FROM cities WHERE country_id = %s ORDER BY city_name', (country_id,))
    cities_list = cursor.fetchall()

    return jsonify(cities_list)