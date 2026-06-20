# Vicki Andujar
# CIS261
# WK10 Vibe Coding - Student Grade Calculator

STUDENT_RECORD_FILE = "student_grades.txt"

class Student:
    """Store student data and calculate average and grade."""

    def __init__(self, name, student_id, test1, test2, test3):
        self.name = str(name).strip()
        self.student_id = str(student_id).strip()
        self.test_scores = [float(test1), float(test2), float(test3)]
        self.average = 0.0
        self.grade = ""
        self.calculate_average()
        self.calculate_grade()

    def calculate_average(self):
        self.average = sum(self.test_scores) / len(self.test_scores)
        return self.average

    def calculate_grade(self):
        average = self.average
        if average >= 90:
            self.grade = "A"
        elif average >= 80:
            self.grade = "B"
        elif average >= 70:
            self.grade = "C"
        elif average >= 60:
            self.grade = "D"
        else:
            self.grade = "F"
        return self.grade

    def to_record(self):
        return (
            f"{self.name}|{self.student_id}|"
            f"{self.test_scores[0]:.2f}|{self.test_scores[1]:.2f}|{self.test_scores[2]:.2f}|"
            f"{self.average:.2f}|{self.grade}"
        )

    @classmethod
    def from_record(cls, record_line):
        parts = record_line.strip().split("|")
        if len(parts) != 7:
            raise ValueError("Record does not have exactly 7 fields")

        name, student_id, t1, t2, t3, average_text, grade_text = [part.strip() for part in parts]
        student = cls(name, student_id, float(t1), float(t2), float(t3))

        # Keep values consistent with file contents if possible.
        try:
            loaded_average = float(average_text)
            if abs(loaded_average - student.average) > 0.01:
                print(f"Warning: recomputing average for {name}. File average differs.")
        except ValueError:
            print(f"Warning: invalid average value in file for {name}.")

        if student.grade != grade_text:
            print(f"Warning: recomputing grade for {name}. File grade differs.")

        return student


def load_students(filename):
    students = []
    try:
        with open(filename, "r") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    student = Student.from_record(line)
                    students.append(student)
                except ValueError as err:
                    print(f"Skipping invalid file line {line_number}: {err}")
    except FileNotFoundError:
        print(f"No existing record file found. Starting with an empty student list.")
    except OSError as err:
        print(f"Error loading file '{filename}': {err}")
    else:
        print(f"Loaded {len(students)} student record(s) from '{filename}'.")

    return students


def save_students(filename, students):
    try:
        with open(filename, "w") as file:
            for student in students:
                file.write(student.to_record() + "\n")
    except OSError as err:
        print(f"Error saving file '{filename}': {err}")
        return False

    print(f"Saved {len(students)} student record(s) to '{filename}'.")
    return True


def format_score(value):
    return f"{value:.2f}"


def display_menu():
    print("\n" + "=" * 70)
    print("STUDENT GRADE CALCULATOR")
    print("=" * 70)
    print("1. Add new student record")
    print("2. Display all students")
    print("3. Display class statistics")
    print("4. Search for student by name")
    print("5. Save records to file")
    print("6. Exit")
    print("Type ESC at any menu prompt to exit immediately.")
    print("=" * 70)


def get_nonempty_text(prompt):
    while True:
        value = input(prompt).strip()
        if value.upper() == "ESC":
            return None
        if value:
            return value
        print("Input cannot be blank. Please try again.")


def get_score(prompt):
    while True:
        value = input(prompt).strip()
        if value.upper() == "ESC":
            return None
        try:
            score = float(value)
            if 0 <= score <= 100:
                return score
            print("Please enter a score between 0 and 100.")
        except ValueError:
            print("Invalid score. Enter a numeric value like 87.50.")


def add_student_record(students):
    print("\nEnter new student information. Type ESC at any prompt to cancel.")
    name = get_nonempty_text("Student name: ")
    if name is None:
        print("Student addition cancelled.")
        return

    student_id = get_nonempty_text("Student ID: ")
    if student_id is None:
        print("Student addition cancelled.")
        return

    if any(student.student_id.lower() == student_id.lower() for student in students):
        print(f"A student with ID '{student_id}' already exists.")
        return

    test1 = get_score("Test 1 score: ")
    if test1 is None:
        print("Student addition cancelled.")
        return

    test2 = get_score("Test 2 score: ")
    if test2 is None:
        print("Student addition cancelled.")
        return

    test3 = get_score("Test 3 score: ")
    if test3 is None:
        print("Student addition cancelled.")
        return

    student = Student(name, student_id, test1, test2, test3)
    students.append(student)
    print(f"Added student '{student.name}' with average {student.average:.2f} and grade {student.grade}.")


def display_all_students(students):
    if not students:
        print("No student records available.")
        return

    header = (
        f"{'Name':<20} {'ID':<12} {'Test1':>7} {'Test2':>7} {'Test3':>7} "
        f"{'Average':>9} {'Grade':>7}"
    )
    print("\n" + "=" * 70)
    print(header)
    print("=" * 70)
    for student in students:
        print(
            f"{student.name:<20} {student.student_id:<12} "
            f"{format_score(student.test_scores[0]):>7} {format_score(student.test_scores[1]):>7} "
            f"{format_score(student.test_scores[2]):>7} {format_score(student.average):>9} {student.grade:>7}"
        )
    print("=" * 70)


def display_class_statistics(students):
    complete_students = [student for student in students if len(student.test_scores) == 3]
    if not complete_students:
        print("No complete student records available for statistics.")
        return

    averages = [student.average for student in complete_students]
    print("\n" + "=" * 70)
    print("CLASS STATISTICS")
    print("=" * 70)
    print(f"Total students: {len(complete_students)}")
    print(f"Class average: {sum(averages) / len(averages):.2f}")
    print(f"Highest average: {max(averages):.2f}")
    print(f"Lowest average: {min(averages):.2f}")
    print("=" * 70)


def search_student_by_name(students):
    search_term = get_nonempty_text("Enter student name to search (partial or full): ")
    if search_term is None:
        print("Search cancelled.")
        return

    matches = [student for student in students if search_term.lower() in student.name.lower()]
    if not matches:
        print(f"No students found matching '{search_term}'.")
        return

    print(f"\nFound {len(matches)} student(s) matching '{search_term}':")
    for student in matches:
        print(
            f"- {student.name} (ID: {student.student_id}) | "
            f"Tests: {format_score(student.test_scores[0])}, {format_score(student.test_scores[1])}, "
            f"{format_score(student.test_scores[2])} | Avg: {format_score(student.average)} | Grade: {student.grade}"
        )


def main():
    students = load_students(STUDENT_RECORD_FILE)

    while True:
        display_menu()
        choice = input("Select an option (1-6 or ESC): ").strip()
        if choice.upper() == "ESC":
            print("Exiting program.")
            break

        if choice == "1":
            add_student_record(students)
        elif choice == "2":
            display_all_students(students)
        elif choice == "3":
            display_class_statistics(students)
        elif choice == "4":
            search_student_by_name(students)
        elif choice == "5":
            save_students(STUDENT_RECORD_FILE, students)
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6, or ESC to exit.")

    if students:
        save_students(STUDENT_RECORD_FILE, students)
    else:
        print("No records to save.")


if __name__ == "__main__":
    main()


