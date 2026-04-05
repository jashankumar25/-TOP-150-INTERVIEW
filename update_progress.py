import os
import re

# Configuration
README_PATH = "README.md"
SOLUTIONS_DIR = "solutions"
SOURCE_EXTENSIONS = {".cpp", ".java", ".py", ".js", ".ts", ".go", ".rs"}

def get_solution_files():
    """Returns a list of all source files in the SOLUTIONS_DIR."""
    files = []
    if not os.path.exists(SOLUTIONS_DIR):
        # Fallback to root if solutions dir doesn't exist
        search_dir = "."
    else:
        search_dir = SOLUTIONS_DIR

    for root, _, filenames in os.walk(search_dir):
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in SOURCE_EXTENSIONS and "update_progress" not in f:
                files.append(f)
    return files

def update_readme():
    if not os.path.exists(README_PATH):
        print(f"Error: {README_PATH} not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    solution_files = get_solution_files()
    print(f"Found {len(solution_files)} solution files.")

    # Update Table Rows
    lines = content.split("\n")
    updated_lines = []
    completed_count = 0
    total_problems = 0
    
    # Counts by difficulty
    diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    solved_diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    
    # Regex to capture table rows: | Status | # | Title | Difficulty | Topic | Solution |
    # Enhanced to capture Difficulty: | (❌|✅) | ID | Title | Icons Difficulty | Topic | ...
    row_pattern = re.compile(r"\| (❌|✅) \| (\d+) \| (.*?) \| (.*?) \|")
    
    for line in lines:
        match = row_pattern.search(line)
        if match:
            total_problems += 1
            status, prob_id, prob_title, prob_diff_raw = match.groups()
            
            # Extract difficulty (ignoring emojis)
            prob_diff = "Easy" if "Easy" in prob_diff_raw else "Medium" if "Medium" in prob_diff_raw else "Hard"
            diff_counts[prob_diff] += 1
            
            # Check if this problem is solved
            is_solved = False
            
            # Normalizing search terms
            clean_title = re.sub(r'[^a-zA-Z0-9 ]', '', prob_title.lower()).replace(' ', '')
            
            for f in solution_files:
                f_clean = re.sub(r'[^a-zA-Z0-9]', '', f.lower())
                if f.startswith(f"{prob_id} ") or f.startswith(f"{prob_id}.") or f.startswith(f"{prob_id}_") or f.split('.')[0] == str(prob_id) or clean_title in f_clean:
                    is_solved = True
                    break

            if is_solved:
                completed_count += 1
                solved_diff_counts[prob_diff] += 1
                line = line.replace("❌", "✅")
            
            updated_lines.append(line)
        else:
            updated_lines.append(line)

    new_content = "\n".join(updated_lines)

    # Update Stats
    remaining_count = total_problems - completed_count
    accuracy = int((completed_count / total_problems * 100)) if total_problems > 0 else 0

    # Update HTML comments
    new_content = re.sub(r"<!-- completed_count -->.*?<!-- /completed_count -->", f"<!-- completed_count -->{completed_count}<!-- /completed_count -->", new_content)
    new_content = re.sub(r"<!-- remaining_count -->.*?<!-- /remaining_count -->", f"<!-- remaining_count -->{remaining_count}<!-- /remaining_count -->", new_content)
    new_content = re.sub(r"<!-- accuracy -->.*?<!-- /accuracy -->", f"<!-- accuracy -->{accuracy}%<!-- /accuracy -->", new_content)

    # Update Visual Progress Bar: `[▓░░░]`
    bar_width = 40
    filled = int(accuracy / 100 * bar_width)
    bar = "▓" * filled + "░" * (bar_width - filled)
    new_content = re.sub(r"`\[[▓░]+\]`", f"`[{bar}]`", new_content)

    # Update Difficulty Table
    # Pattern: | **0** | **1** | **0** |
    diff_table_pattern = r"\| \*\*Easy\*\* \| \*\*Medium\*\* \| \*\*Hard\*\* \|\n\| :---: \| :---: \| :---: \|\n\| \*\*\d+\*\* \| \*\*\d+\*\* \| \*\*\d+\*\* \|"
    # Actually my new README has:
    # | 🏆 Overall Progress | 🟢 Easy | 🟡 Medium | 🔴 Hard |
    # | :---: | :---: | :---: | :---: |
    # | **1%** | **0** | **1** | **0** |
    # | (1 / 150) | / 50 | / 80 | / 20 |
    
    # Update Difficulty Table
    # Pattern: | **1%** | **0** | **1** | **0** |
    new_content = re.sub(r"\|\s\*\*<!-- accuracy -->.*?<!-- /accuracy -->\*\*\s\|\s\*\*\d+\*\*\s\|\s\*\*\d+\*\*\s\|\s\*\*\d+\*\*\s\|", 
                         f"| **<!-- accuracy -->{accuracy}%<!-- /accuracy -->** | **{solved_diff_counts['Easy']}** | **{solved_diff_counts['Medium']}** | **{solved_diff_counts['Hard']}** |", new_content)
    
    # Update total counts row
    # Pattern: | (1 / 150) | / 50 | / 80 | / 20 |
    new_content = re.sub(r"\|\s\(<!-- completed_count -->.*?<!-- /completed_count -->\s/\s\d+\)\s\|\s/\s\d+\s\|\s/\s\d+\s\|\s/\s\d+\s\|",
                         f"| (<!-- completed_count -->{completed_count}<!-- /completed_count --> / {total_problems}) | / {diff_counts['Easy']} | / {diff_counts['Medium']} | / {diff_counts['Hard']} |", new_content)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Successfully updated README.md: {completed_count}/{total_problems} completed.")

if __name__ == "__main__":
    update_readme()
