pub mod game_data {
    use crate::final_board::final_board::RustBoard;
    use chrono::DateTime;
    use chrono::Local;

    // the struct Game below follows the PGN notation as many as possible
    // white represents player 1 and black represents player 2
    pub struct Game {
        date: DateTime<Local>,
        round: i16,
        white: String,
        black: String,
        result: String,
        actions_taken: Vec<i16>,
        turn: i16,
    }

    impl Game {
        pub fn new(round: i16, white: &str, black: &str) -> Game {
            let mut white_mode: String;
            let mut black_mode: String;
            for mode in [white_mode, black_mode] {
                match mode.as_str() {
                    "GBFS" => white_mode = String::from("GBFS"),
                    _ => white_mode = String::from("Test"),
                }
            }

            Game {
                date: Local::now(),
                round,
                white: white_mode,
                black: black_mode,
                result: String::from("0-0"),
                actions_taken: vec![],
                turn: 1,
            }
        }
    }
}
