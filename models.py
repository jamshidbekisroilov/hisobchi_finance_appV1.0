from db import get_connection

def add_income(date, amount, category, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO income (date, amount, category, note)
        VALUES (?, ?, ?, ?)
    """, (date, amount, category, note))
    conn.commit()
    conn.close()

def get_income_by_date(start, end):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM income
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
    """, (start, end))
    results = cursor.fetchall()
    conn.close()
    return results
def add_expense(date, amount, category, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expense (date, amount, category, note)
        VALUES (?, ?, ?, ?)
    """, (date, amount, category, note))
    conn.commit()
    conn.close()

def get_expense_by_date(start, end):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, amount, category, note
        FROM expense
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
    """, (start, end))
    results = cursor.fetchall()
    conn.close()
    return results
def add_kreditor(name, phone, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO person (name, phone, note)
        VALUES (?, ?, ?)
    """, (name, phone, note))
    conn.commit()
    conn.close()
def get_kreditor_list():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM person ORDER BY name ASC")
    results = cursor.fetchall()
    conn.close()
    return results
def add_kreditor_debt(person_id, amount, date, due_date, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kreditor_debt (person_id, amount, date, due_date, note)
        VALUES (?, ?, ?, ?, ?)
    """, (person_id, amount, date, due_date, note))
    conn.commit()
    conn.close()
def add_kreditor_payment(person_id, amount, date, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kreditor_payment (person_id, amount, date, note)
        VALUES (?, ?, ?, ?)
    """, (person_id, amount, date, note))
    conn.commit()
    conn.close()
def get_kreditor_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT d.date, p.name, d.amount, d.note, d.due_date, 'debt', d.id
        FROM kreditor_debt d
        JOIN person p ON d.person_id = p.id
        UNION ALL
        SELECT pay.date, p.name, pay.amount, pay.note, NULL, 'payment', pay.id
        FROM kreditor_payment pay
        JOIN person p ON pay.person_id = p.id
        ORDER BY date DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results
def get_kreditor_balances():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.name,
               IFNULL(SUM(d.amount), 0) AS total_debt,
               IFNULL((SELECT SUM(amount) FROM kreditor_payment WHERE person_id = p.id), 0) AS total_paid,
               IFNULL(SUM(d.amount), 0) - IFNULL((SELECT SUM(amount) FROM kreditor_payment WHERE person_id = p.id), 0) AS remaining
        FROM person p
        LEFT JOIN kreditor_debt d ON p.id = d.person_id
        GROUP BY p.id
        ORDER BY remaining DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results
def add_debitor_debt(person_id, amount, date, due_date, note):
    """Debitorga qarz berish"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO debitor_debt (person_id, amount, date, due_date, note)
        VALUES (?, ?, ?, ?, ?)
    """, (person_id, amount, date, due_date, note))
    conn.commit()
    conn.close()


def add_debitor_payment(person_id, amount, date, note):
    """Debitordan qarz undirish"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO debitor_payment (person_id, amount, date, note)
        VALUES (?, ?, ?, ?)
    """, (person_id, amount, date, note))
    conn.commit()
    conn.close()


def get_debitor_transactions():
    """Debitor harakatlari jadvali: qarz berish + undirish"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.date, p.name, d.amount, d.note, d.due_date, 'debt', d.id
        FROM debitor_debt d
        JOIN person p ON d.person_id = p.id
        UNION ALL
        SELECT pay.date, p.name, pay.amount, pay.note, NULL, 'payment', pay.id
        FROM debitor_payment pay
        JOIN person p ON pay.person_id = p.id
        ORDER BY date DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results


def get_debitor_balances():
    """Debitorlar bo‘yicha qolgan haqlar jadvali"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name,
               IFNULL(SUM(d.amount), 0) AS total_debt,
               IFNULL((SELECT SUM(amount) FROM debitor_payment WHERE person_id = p.id), 0) AS total_paid,
               IFNULL(SUM(d.amount), 0) - IFNULL((SELECT SUM(amount) FROM debitor_payment WHERE person_id = p.id), 0) AS remaining
        FROM person p
        LEFT JOIN debitor_debt d ON p.id = d.person_id
        GROUP BY p.id
        ORDER BY remaining DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results
def get_all_persons():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, phone, note
        FROM person
        ORDER BY name ASC
    """)
    results = cursor.fetchall()
    conn.close()
    return results
from datetime import datetime, timedelta

def get_daily_debitor_kreditor_balances():
    conn = get_connection()
    cursor = conn.cursor()

    # Oxirgi 30 kun
    today = datetime.today().date()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in reversed(range(30))]

    debitor_values = []
    kreditor_values = []

    for date in dates:
        # Debitorlar: qarz berilgan - undirilgan
        cursor.execute("""
            SELECT IFNULL(SUM(amount), 0) FROM debitor_debt WHERE date <= ?
        """, (date,))
        total_debt = cursor.fetchone()[0]

        cursor.execute("""
            SELECT IFNULL(SUM(amount), 0) FROM debitor_payment WHERE date <= ?
        """, (date,))
        total_paid = cursor.fetchone()[0]

        debitor_qoldiq = total_debt - total_paid
        debitor_values.append(debitor_qoldiq)

        # Kreditorlar: qarz olingan - to‘langan
        cursor.execute("""
            SELECT IFNULL(SUM(amount), 0) FROM kreditor_debt WHERE date <= ?
        """, (date,))
        kreditor_debt = cursor.fetchone()[0]

        cursor.execute("""
            SELECT IFNULL(SUM(amount), 0) FROM kreditor_payment WHERE date <= ?
        """, (date,))
        kreditor_paid = cursor.fetchone()[0]

        kreditor_qoldiq = kreditor_debt - kreditor_paid
        kreditor_values.append(kreditor_qoldiq)

    conn.close()
    return dates, debitor_values, kreditor_values
def get_monthly_income_expense():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount)
        FROM income
        GROUP BY month
        ORDER BY month ASC
    """)
    income_data = dict(cursor.fetchall())

    cursor.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount)
        FROM expense
        GROUP BY month
        ORDER BY month ASC
    """)
    expense_data = dict(cursor.fetchall())

    # Barcha oylarni birlashtiramiz
    all_months = sorted(set(income_data.keys()) | set(expense_data.keys()))
    monthly_income = [income_data.get(m, 0) for m in all_months]
    monthly_expense = [expense_data.get(m, 0) for m in all_months]

    conn.close()
    return all_months, monthly_income, monthly_expense
def get_active_persons_summary():
    conn = get_connection()
    cursor = conn.cursor()

    # Oxirgi 30 kun
    cursor.execute("""
        SELECT p.name,
               COUNT(*) AS count,
               SUM(d.amount) AS total
        FROM debitor_debt d
        JOIN person p ON d.person_id = p.id
        WHERE d.date >= date('now', '-30 days')
        GROUP BY p.id
        UNION ALL
        SELECT p.name,
               COUNT(*) AS count,
               SUM(k.amount) AS total
        FROM kreditor_debt k
        JOIN person p ON k.person_id = p.id
        WHERE k.date >= date('now', '-30 days')
        GROUP BY p.id
    """)
    rows = cursor.fetchall()

    # Birlashtirish
    summary = {}
    for name, count, total in rows:
        if name not in summary:
            summary[name] = [0, 0.0]
        summary[name][0] += count
        summary[name][1] += total

    conn.close()
    # Saralash: eng faol yuqorida
    sorted_summary = sorted(summary.items(), key=lambda x: x[1][0], reverse=True)
    return sorted_summary

def get_expense_by_category():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expense
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def get_monthly_savings():
    conn = get_connection()
    cursor = conn.cursor()

    # Daromad
    cursor.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount)
        FROM income
        GROUP BY month
    """)
    income = dict(cursor.fetchall())

    # Xarajat
    cursor.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount)
        FROM expense
        GROUP BY month
    """)
    expense = dict(cursor.fetchall())

    # To‘lovlar (kreditor to‘lash)
    cursor.execute("""
        SELECT strftime('%Y-%m', date) AS month, SUM(amount)
        FROM kreditor_payment
        GROUP BY month
    """)
    payments = dict(cursor.fetchall())

    # Barcha oylar
    all_months = sorted(set(income.keys()) | set(expense.keys()) | set(payments.keys()))
    savings = []
    for m in all_months:
        i = income.get(m, 0)
        e = expense.get(m, 0)
        p = payments.get(m, 0)
        savings.append(i - e - p)

    conn.close()
    return all_months, savings
