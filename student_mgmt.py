# Student Management System (Console) with JSON persistence
# Run: python student_mgmt.py

import json, os
from typing import List, Dict, Optional

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
students: List[Dict[str, str]] = []   # in-memory store


# ---------- Persistence ----------
def load_data() -> List[Dict[str, str]]:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            pass
    return []


def save_data() -> None:
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving data: {e}")


# ---------- Helpers ----------
def pause() -> None: input("\nPress Enter to continue...")

def find_by_roll(roll: str) -> Optional[Dict[str, str]]:
    return next((s for s in students if s["roll_no"] == roll), None)

def non_empty(label: str) -> str:
    while True:
        val = input(label).strip()
        if val: return val
        print("Required field. Try again.")


# ---------- CRUD ----------
def add_student() -> None:
    print("\n=== Add Student ===")
    roll = non_empty("Roll no: ")
    if find_by_roll(roll): return print("❌ Roll no exists.")
    students.append({
        "roll_no": roll,
        "name": non_empty("Name: "),
        "grade": non_empty("Grade: "),
        "age": input("Age (optional): ").strip()
    })
    print("✅ Student added.")


def view_students() -> None:
    print("\n=== Students List ===")
    if not students: return print("No records.")
    print(f"{'Roll':<8}{'Name':<20}{'Grade':<8}{'Age':<6}")
    print("-" * 42)
    for s in students:
        print(f"{s['roll_no']:<8}{s['name']:<20}{s['grade']:<8}{s.get('age',''):<6}")


def search_student() -> None:
    print("\n=== Search ===")
    if input("Search by Roll? (y/N): ").lower() == "y":
        s = find_by_roll(input("Roll no: ").strip())
        print(s if s else "Not found.")
    else:
        q = input("Name contains: ").strip().lower()
        results = [s for s in students if q in s["name"].lower()]
        print(*results, sep="\n") if results else print("No matches.")


def update_student() -> None:
    print("\n=== Update ===")
    s = find_by_roll(input("Roll to update: ").strip())
    if not s: return print("Not found.")
    for field in ("name", "grade", "age"):
        val = input(f"{field.capitalize()} [{s.get(field,'')}]: ").strip()
        if val: s[field] = val
    print("✅ Updated.")


def delete_student() -> None:
    print("\n=== Delete ===")
    s = find_by_roll(input("Roll to delete: ").strip())
    if not s: return print("Not found.")
    if input(f"Delete {s['name']} (Roll {s['roll_no']})? (y/N): ").lower() == "y":
        students.remove(s); print("✅ Deleted.")
    else: print("Cancelled.")


# ---------- Main ----------
def main() -> None:
    global students
    students = load_data()
    while True:
        print("\n1) Add  2) View  3) Search  4) Update  5) Delete  6) Exit")
        c = input("Choice: ").strip()
        if c == "1":
            add_student()
            pause()
        elif c == "2":
            view_students()
            pause()
        elif c == "3":
            search_student()
            pause()
        elif c == "4":
            update_student()
            pause()
        elif c == "5":
            delete_student()
            pause()
        elif c == "6":
            save_data()
            print("Goodbye!")
            break
        else: print("Invalid choice.")


if __name__ == "__main__":
    main()
