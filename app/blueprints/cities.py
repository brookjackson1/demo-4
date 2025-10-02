from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.db_connect import get_db

cities = Blueprint('cities', __name__)

@cities.route('/', methods=['GET', 'POST'])
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
        return redirect(url_for('cities.show_cities'))

    # Handle GET request with optional filtering
    capital_filter = request.args.get('capital')
    region_filter = request.args.get('region')

    # Base query
    base_query = '''
        SELECT c.city_id, c.city_name, c.population, c.is_capital,
               co.country_name, co.country_id, co.continent
        FROM cities c
        JOIN countries co ON c.country_id = co.country_id
    '''

    # Apply filters
    where_conditions = []
    params = []

    if capital_filter == 'true':
        where_conditions.append('c.is_capital = 1')
        flash('Showing capital cities only', 'info')
    elif capital_filter == 'false':
        where_conditions.append('c.is_capital = 0')
        flash('Showing major cities (non-capitals)', 'info')

    if region_filter:
        if region_filter == 'Americas':
            where_conditions.append('(co.continent = %s OR co.continent = %s)')
            params.extend(['North America', 'South America'])
            flash('Showing cities in the Americas', 'info')
        elif region_filter == 'Europe':
            where_conditions.append('co.continent = %s')
            params.append('Europe')
            flash('Showing cities in Europe', 'info')
        elif region_filter == 'Asia':
            where_conditions.append('(co.continent = %s OR co.continent = %s)')
            params.extend(['Asia', 'Oceania'])
            flash('Showing cities in Asia & Oceania', 'info')

    # Construct final query
    if where_conditions:
        query = base_query + ' WHERE ' + ' AND '.join(where_conditions)
    else:
        query = base_query

    query += ' ORDER BY co.country_name, c.city_name'

    cursor.execute(query, params)
    all_cities = cursor.fetchall()

    # Get countries for dropdown
    cursor.execute('SELECT country_id, country_name FROM countries ORDER BY country_name')
    countries_list = cursor.fetchall()

    return render_template('cities_simple.html', all_cities=all_cities, countries_list=countries_list)

@cities.route('/update_city/<int:city_id>', methods=['POST'])
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
    return redirect(url_for('cities.show_cities'))

@cities.route('/delete_city/<int:city_id>', methods=['POST'])
def delete_city(city_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the city
    cursor.execute('DELETE FROM cities WHERE city_id = %s', (city_id,))
    db.commit()

    flash('City deleted successfully!', 'danger')
    return redirect(url_for('cities.show_cities'))

@cities.route('/by_country/<int:country_id>')
def cities_by_country(country_id):
    """Show cities filtered by country"""
    db = get_db()
    cursor = db.cursor()

    # Get country info
    cursor.execute('SELECT country_name FROM countries WHERE country_id = %s', (country_id,))
    country = cursor.fetchone()

    if not country:
        flash('Country not found!', 'danger')
        return redirect(url_for('cities.show_cities'))

    # Get cities for this country
    cursor.execute('''
        SELECT c.city_id, c.city_name, c.population, c.is_capital,
               co.country_name, co.country_id
        FROM cities c
        JOIN countries co ON c.country_id = co.country_id
        WHERE c.country_id = %s
        ORDER BY c.city_name
    ''', (country_id,))
    filtered_cities = cursor.fetchall()

    # Get all countries for dropdown
    cursor.execute('SELECT country_id, country_name FROM countries ORDER BY country_name')
    countries_list = cursor.fetchall()

    return render_template('cities_standalone.html',
                         all_cities=filtered_cities,
                         countries_list=countries_list,
                         selected_country=country['country_name'])

@cities.route('/api/cities', methods=['GET'])
def api_cities():
    """API endpoint to get all cities"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT c.city_id, c.city_name, c.population, c.is_capital,
               co.country_name, co.country_id
        FROM cities c
        JOIN countries co ON c.country_id = co.country_id
        ORDER BY co.country_name, c.city_name
    ''')
    cities_list = cursor.fetchall()

    return jsonify(cities_list)

@cities.route('/api/cities/<int:country_id>', methods=['GET'])
def api_cities_by_country(country_id):
    """API endpoint to get cities for a specific country"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT city_id, city_name FROM cities WHERE country_id = %s ORDER BY city_name', (country_id,))
    cities_list = cursor.fetchall()

    return jsonify(cities_list)

@cities.route('/search')
def search_cities():
    """Search cities by name"""
    search_term = request.args.get('q', '')

    if not search_term:
        return redirect(url_for('cities.show_cities'))

    db = get_db()
    cursor = db.cursor()

    # Search cities by name (case-insensitive)
    cursor.execute('''
        SELECT c.city_id, c.city_name, c.population, c.is_capital,
               co.country_name, co.country_id
        FROM cities c
        JOIN countries co ON c.country_id = co.country_id
        WHERE c.city_name LIKE %s
        ORDER BY c.city_name
    ''', (f'%{search_term}%',))
    search_results = cursor.fetchall()

    # Get all countries for dropdown
    cursor.execute('SELECT country_id, country_name FROM countries ORDER BY country_name')
    countries_list = cursor.fetchall()

    return render_template('cities_standalone.html',
                         all_cities=search_results,
                         countries_list=countries_list,
                         search_term=search_term)