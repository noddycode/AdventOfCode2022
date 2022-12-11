use std::env;
use std::fs::read_to_string;

fn get_calorie_set() -> Vec<i32>{
    let mut cwd = env::current_dir().unwrap();  // Get the current working directory
    cwd.push("input");  // Add the "input" directory to the path
    cwd.push("bigInput.txt");  // Now add the file path
    let input_path = cwd.as_path();  // Convert from PathBuf to String

    let mut input = read_to_string(input_path)  // Open and read the file
        .expect("Should have read input");  // If opening the path fails, this error message will be printed

    input.push_str("\r\n");  // Add an empty line to ensure our last calorie group is counted

    let lines = input.split("\r\n");  // Split the file input into individual lines
    // Making it use the right platform line split is difficult... so I won't do it
    let mut calorie_sum: i32 = 0;  // Create a new 32-bit integer
    let mut sums= vec![];  // New vec to store calorie counts
    for line in lines{
        match line  { // match is kind of like switch, we can use this instead of if statements
            "" => {  // Match an empty string
                sums.push(calorie_sum);
                calorie_sum = 0;
            }
            _ => {  // This is a catch-all that will match any value not previously matched
                let calorie_count: i32 = line.parse().unwrap();
                calorie_sum += calorie_count;
            }
        }
    }

    sums  // The "return" keyword isn't necessary, Rust will return the value of the last statement
    // You can, however, include it for clarity
}

fn part_one() -> i32 {

    let sums = get_calorie_set();
    let result =  *sums.iter().max().unwrap();  // Copy result value into a new i32
    // This allows us to return the result without keeping the source vector in memory
    return result;
}

fn part_two() -> i32{
    let mut sums = get_calorie_set();
    println!("{:?}", sums);  // Use debug print to print the elements of the vector
    sums.sort();  // Sorts vector in place. This is okay since we don't need it to stay in original order
    sums.reverse();  // Reverse order so it goes from big to small
    let top_three = sums.get(..3).unwrap().iter().sum();  // Note that this does not own the vector
    return top_three;
}

fn main() {
    let max_calories = part_one();
    println!("{}", max_calories);

    let top_three_sum = part_two();
    println!("{}", top_three_sum)
}
