import csv
import json

def export_to_csv(notes, filename="notes.csv"):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Title", "Content"])
        for note in notes:
            writer.writerow([note.id, note.title, note.content])

def export_to_json(notes, filename="notes.json"):
    data = [{"id": n.id, "title": n.title, "content": n.content} for n in notes]
    with open(filename, 'w') as f:
        json.dump(data, f)