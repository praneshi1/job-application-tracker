import sqlite3

DB_FILE = "jobs.db"


def connect():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Applied',
            deadline TEXT
        )
    """)
    conn.commit()
    return conn


def add_job(conn):
    company = input("Company: ").strip()
    role = input("Role: ").strip()
    deadline = input("Deadline (e.g. 2026-11-22, or leave blank): ").strip()

    if not company or not role:
        print("Company and role are required.")
        return

    conn.execute(
        "INSERT INTO jobs (company, role, deadline) VALUES (?, ?, ?)",
        (company, role, deadline or None),
    )
    conn.commit()
    print("Job added.")


def list_jobs(conn):
    rows = conn.execute(
        "SELECT id, company, role, status, deadline FROM jobs ORDER BY id"
    ).fetchall()

    if not rows:
        print("No jobs saved yet.")
        return

    print("\n{:<4} {:<15} {:<22} {:<11} {}".format("ID", "Company", "Role", "Status", "Deadline"))
    print("-" * 70)
    for job_id, company, role, status, deadline in rows:
        print("{:<4} {:<15} {:<22} {:<11} {}".format(
            job_id, company, role, status, deadline or "-"))


def update_status(conn):
    list_jobs(conn)
    try:
        job_id = int(input("Enter job ID to update: "))
    except ValueError:
        print("Please enter a number.")
        return

    status = input("New status (Applied / Interview / Selected / Rejected): ").strip()
    cursor = conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()

    print("Status updated." if cursor.rowcount else "No job with that ID.")


def main():
    conn = connect()
    while True:
        print("\n1. Add job   2. List jobs   3. Update status   4. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_job(conn)
        elif choice == "2":
            list_jobs(conn)
        elif choice == "3":
            update_status(conn)
        elif choice == "4":
            break
        else:
            print("Invalid choice, try again.")

    conn.close()
    print("Goodbye!")


if __name__ == "__main__":
    main()
