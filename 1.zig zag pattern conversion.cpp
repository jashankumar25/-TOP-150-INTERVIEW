#include <bits/stdc++.h>
using namespace std;

/*
============================================================
LEETCODE 6: ZIGZAG CONVERSION
============================================================

PROBLEM:
Write string in zigzag form and read row-wise.

Example:
s = "ABCDEF", numRows = 3

Zigzag:
A   E
B D F
C

Output: "AEBDFC"

============================================================
APPROACH 1: SIMULATION (BEST & EASY)
============================================================

IDEA:
- Move like a wave:
  row: 0 → 1 → 2 → 1 → 0 → ...
- Store characters in rows

TIME COMPLEXITY: O(n)
SPACE COMPLEXITY: O(n)

WHY USE:
- Easy to understand
- Best for interviews
*/

string convert_simulation(string s, int numRows)
{
    if (numRows == 1 || s.length() <= (size_t)numRows)
        return s;

    vector<string> row_strings(numRows);
    int current_row = 0;
    bool goingDown = false;

    for (char c : s)
    {
        row_strings[current_row] += c;

        // Change direction when at top or bottom
        if (current_row == 0 || current_row == numRows - 1)
            goingDown = !goingDown;

        // Move to the next row
        current_row += goingDown ? 1 : -1;
    }

    // Combine all rows into a single string
    string ans = "";
    for (const string& row_str : row_strings)
        ans += row_str;

    return ans;
}


/*
============================================================
APPROACH 2: MATHEMATICAL (OPTIMIZED)
============================================================

IDEA:
- Zigzag follows a repeating cycle

cycle = 2 * (numRows - 1)

- First & last rows:
  jump by cycle

- Middle rows:
  alternate jumps:
  step1 = cycle - 2*row
  step2 = 2*row

TIME COMPLEXITY: O(n)
SPACE COMPLEXITY: O(1)  (no extra storage)

WHY USE:
- More optimized
- Harder to understand
*/

string convert_math(string s, int numRows)
{

    if (numRows == 1)
        return s;

    string ans = "";
    int n = s.length();
    int cycle = 2 * (numRows - 1);

    for (int row = 0; row < numRows; row++)
    {

        for (int j = row; j < n; j += cycle)
        {

            ans += s[j];

            // middle rows
            if (row != 0 && row != numRows - 1)
            {
                int extra = j + cycle - 2 * row;
                if (extra < n)
                    ans += s[extra];
            }
        }
    }

    return ans;
}

/*
============================================================
APPROACH 3: BRUTE FORCE (NOT RECOMMENDED)
============================================================

IDEA:
- Create 2D matrix
- Fill zigzag manually
- Read row-wise

TIME COMPLEXITY: O(n)
SPACE COMPLEXITY: O(n * numRows)  ❌ HIGH

WHY NOT USE:
- Waste of space
- Complex logic
*/

string convert_bruteforce(string s, int numRows)
{

    if (numRows == 1)
        return s;

    int n = s.length();

    // create matrix (rows x n)
    vector<vector<char>> mat(numRows, vector<char>(n, ' '));

    int row = 0, col = 0;
    bool goingDown = true;

    for (char c : s)
    {

        mat[row][col] = c;

        if (goingDown)
        {
            if (row == numRows - 1)
            {
                goingDown = false;
                row--;
                col++;
            }
            else
            {
                row++;
            }
        }
        else
        {
            if (row == 0)
            {
                goingDown = true;
                row++;
            }
            else
            {
                row--;
                col++;
            }
        }
    }

    // read row-wise
    string ans = "";
    for (int i = 0; i < numRows; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (mat[i][j] != ' ')
                ans += mat[i][j];
        }
    }

    return ans;
}

/*
============================================================
MAIN FUNCTION (TEST ALL APPROACHES)
============================================================
*/

int main()
{

    string s = "PAYPALISHIRING";
    int numRows = 3;

    cout << "Simulation: " << convert_simulation(s, numRows) << endl;
    cout << "Math:       " << convert_math(s, numRows) << endl;
    cout << "BruteForce: " << convert_bruteforce(s, numRows) << endl;

    return 0;
}

/*
============================================================
FINAL SUMMARY
============================================================

Approach 1 (Simulation):
- Time: O(n)
- Space: O(n)
- BEST for interview

Approach 2 (Math):
- Time: O(n)
- Space: O(1)
- Optimized

Approach 3 (Brute Force):
- Time: O(n)
- Space: O(n * numRows)
- NOT recommended

============================================================
MEMORY TRICK:
"Move up-down like wave OR use cycle formula"
============================================================
*/