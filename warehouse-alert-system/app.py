from flask import Flask, render_template, request, redirect, session, url_for, flash
from config import Config
from services import auth_service
from services.dynamodb_service import add_item, get_items, update_stock, delete_item
from services.sns_service import send_alert

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY


# -----------------------------
# 🔐 AUTH ROUTES
# -----------------------------

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if auth_service.login(username, password):
            session['user'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid Credentials")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if auth_service.signup(username, password):
            flash('Account created successfully! Please login.', 'success')
            return redirect('/login')
        else:
            return render_template('signup.html', error="User already exists")

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/login')


# -----------------------------
# 🛡️ AUTH CHECK
# -----------------------------

def is_logged_in():
    return 'user' in session


# -----------------------------
# 📊 DASHBOARD
# -----------------------------

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect('/login')

    items = get_items()

    low_stock_count = sum(
        1 for item in items if int(item['quantity']) <= int(item['threshold'])
    )

    total_items = len(items)

    return render_template(
        'dashboard.html',
        items=items,
        low_stock_count=low_stock_count,
        total_items=total_items
    )


# -----------------------------
# ➕ ADD ITEM
# -----------------------------

@app.route('/add_item', methods=['GET', 'POST'])
def add_item_page():
    if not is_logged_in():
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        threshold = request.form['threshold']

        success = add_item(name, quantity, threshold)

        if success:
            flash(f'"{name}" added successfully!', 'success')
        else:
            flash('Error adding item.', 'error')

        return redirect('/dashboard')

    return render_template('add_item.html')


# -----------------------------
# 🔄 UPDATE ITEM
# -----------------------------

@app.route('/update_item/<item_id>', methods=['GET', 'POST'])
def update_item_page(item_id):
    if not is_logged_in():
        return redirect('/login')

    items = get_items()
    item = next((i for i in items if i['item_id'] == item_id), None)

    if not item:
        flash('Item not found.', 'error')
        return redirect('/dashboard')

    if request.method == 'POST':
        quantity = int(request.form['quantity'])

        success = update_stock(item_id, quantity)

        if not success:
            flash('Error updating stock.', 'error')
            return redirect('/dashboard')

        # 🚨 Low Stock Alert
        if quantity <= int(item['threshold']):
            message = f"⚠ Low stock alert!\nItem: {item['name']}\nQuantity: {quantity}"

            try:
                send_alert(message)
                flash(f'Low stock alert sent for "{item["name"]}"!', 'error')
            except Exception:
                flash(f'Stock updated for "{item["name"]}" (Alert failed)', 'warning')
        else:
            flash(f'Stock updated for "{item["name"]}"', 'success')

        return redirect('/dashboard')

    return render_template('update_item.html', item=item)


# -----------------------------
# 🔍 SEARCH FEATURE
# -----------------------------

@app.route('/search', methods=['GET'])
def search():
    if not is_logged_in():
        return redirect('/login')

    query = request.args.get('q', '').lower()
    items = get_items()

    filtered_items = [
        item for item in items
        if query in item['name'].lower()
    ]

    low_stock_count = sum(
        1 for item in filtered_items if int(item['quantity']) <= int(item['threshold'])
    )

    total_items = len(filtered_items)

    return render_template(
        'dashboard.html',
        items=filtered_items,
        low_stock_count=low_stock_count,
        total_items=total_items
    )


# -----------------------------
# 🗑 DELETE ITEM (FIXED)
# -----------------------------

@app.route('/delete/<item_id>')
def delete_item_route(item_id):
    if not is_logged_in():
        return redirect('/login')

    items = get_items()
    item = next((i for i in items if i['item_id'] == item_id), None)

    if item:
        success = delete_item(item_id)

        if success:
            flash(f'"{item["name"]}" deleted successfully.', 'info')
        else:
            flash('Error deleting item.', 'error')
    else:
        flash('Item not found.', 'error')

    return redirect('/dashboard')


# -----------------------------
# ▶️ RUN APP
# -----------------------------

if __name__ == '__main__':
    app.run(debug=True)