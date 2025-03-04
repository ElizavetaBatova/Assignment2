from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

user_preferences = {}
recipes = [
    {'name': 'Cheese Sandwich', 'ingredients': 'Bread, Cheese, Babys Blood', 'cuisine': 'Irish', 'author': 'Irish Witch from the tenth century'},
    {'name': 'Spaghetti Carbonara', 'ingredients': 'Spaghetti, Eggs, Pancetta, Parmesan Cheese, Black Pepper', 'cuisine': 'Italian'},
    {'name': 'Chicken Curry', 'ingredients': 'Chicken, Curry Powder, Coconut Milk, Onion, Garlic, Ginger, Tomatoes', 'cuisine': 'Japanese'},
    {'name': 'Vegetable Stir Fry', 'ingredients': 'Broccoli, Carrots, Bell Peppers, Soy Sauce, Ginger, Garlic, Sesame Oil', 'cuisine': 'International'}]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        user_preferences['dietary_restrictions'] = request.form['dietary_restrictions'].lower()
        user_preferences['favorite_cuisine'] = request.form['favorite_cuisine'].lower()
        user_preferences['meals_per_week'] = int(request.form['meals_per_week'])
        return redirect(url_for('recipe_plan'))
    else:
        name = request.args.get('name', '')
        return render_template('preferences.html', name=name)

@app.route('/recipe_input', methods=['GET', 'POST'])
def recipe_input():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        ingredients = request.form['ingredients']
        cuisine = request.form.get('cuisine', 'Unknown').capitalize()
        recipes.append({'name': recipe_name, 'ingredients': ingredients, 'cuisine': cuisine})
        return redirect(url_for('recipe_plan'))
    else:
        return render_template('recipe_input.html')

@app.route('/recipe_plan')
def recipe_plan():
    if not recipes:
        return render_template('no_recipes.html')

    # Ensure case-insensitive filtering
    dietary_restrictions = user_preferences.get('dietary_restrictions', '').lower()
    favorite_cuisine = user_preferences.get('favorite_cuisine', '').lower()

    # Filter recipes based on dietary restrictions and favorite cuisine
    filtered_recipes = [
        recipe for recipe in recipes
        if dietary_restrictions not in recipe['ingredients'].lower() and  # Block restricted ingredients
        (favorite_cuisine in recipe['name'].lower() or favorite_cuisine in recipe['cuisine'].lower())
    ]

    return render_template('recipe_plan.html', filtered_recipes=filtered_recipes, user_preferences=user_preferences)

if __name__ == '__main__':
    app.run(debug=True)