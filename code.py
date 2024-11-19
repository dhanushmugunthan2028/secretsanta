import csv
import random


class SecretSanta:
    def __init__(self, input_csv='parti.csv', output_csv='secret_santas.csv'):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.participants = []  # List of dictionaries with 'name' and 'email'

    def load_participants(self):
        """Load participants from the input CSV file."""
        try:
            with open(self.input_csv, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                self.participants = [row for row in reader]
                print(f"Loaded participants: {self.participants}")
        except FileNotFoundError:
            print(f"No file found: {self.input_csv}. Ensure the input file exists.")
            self.participants = []

    def assign_secret_santas(self):
        """Assign Secret Santas and return assignments."""
        if len(self.participants) < 2:
            print("Not enough participants to assign Secret Santas.")
            return []

        givers = self.participants[:]
        receivers = self.participants[:]
        random.shuffle(receivers)

        # Ensure no one is their own Secret Santa
        for _ in range(100):  # Retry mechanism
            if all(giver != receiver for giver, receiver in zip(givers, receivers)):
                break
            random.shuffle(receivers)
        else:
            print("Failed to assign Secret Santas without conflicts.")
            return []

        # Generate assignments
        assignments = []
        for giver, receiver in zip(givers, receivers):
            assignments.append({
                'employee_name': giver['Name'],
                'employee_email': giver['Email'],
                'secret_santa_name': receiver['Name'],
                'secret_santa_email': receiver['Email']
            })
        return assignments

    def save_assignments(self, assignments):
        """Save the Secret Santa assignments to the output CSV file."""
        if not assignments:
            print("No assignments to save.")
            return

        with open(self.output_csv, mode='w', newline='') as file:
            fieldnames = ['employee_name', 'employee_email', 'secret_santa_name', 'secret_santa_email']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(assignments)
            print(f"Assignments saved to {self.output_csv}.")

    def display_assignments(self, assignments):
        """Display Secret Santa assignments."""
        if not assignments:
            print("No assignments to display.")
            return
        print("\nSecret Santa Assignments:")
        for assignment in assignments:
            print(f"{assignment['employee_name']} ({assignment['employee_email']}) -> "
                  f"{assignment['secret_santa_name']} ({assignment['secret_santa_email']})")


# Main Functionality
def main():
    santa_game = SecretSanta()
    santa_game.load_participants()

    if not santa_game.participants:
        print("No participants loaded. Exiting program.")
        return

    assignments = santa_game.assign_secret_santas()
    santa_game.display_assignments(assignments)
    santa_game.save_assignments(assignments)


if __name__ == "__main__":
    main()
