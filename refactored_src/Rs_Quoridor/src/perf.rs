pub mod peformance_tests {
    use crate::final_board;
    use crate::final_mcts::final_mcts::MctsTree;
    use crate::rand_chacha;
    pub use final_board::final_board::RustBoard;
    pub use rand_chacha::ChaCha8Rng;
    use rayon::prelude::*;
    use std::io;

    use chrono::Utc;

    use std::collections::VecDeque;

    use chrono::DateTime;
    use chrono::Local;
    use std::error::Error;
    use std::fs;
    use std::fs::File;
    use std::io::Write;
    use std::time::Instant;

    use std::io::prelude::*;
    use std::path::Path;

    #[derive(Clone, Copy, Debug, serde::Serialize)]
    pub struct GameDataBasic {
        num_walls: i16,
        num_moves: i16,
        num_actions: i16,
        time_taken: f64,
        mode: i16,
    }
    pub fn generate_data(n: usize) -> Result<(), Box<dyn Error>> {
        let mut data: Vec<GameDataBasic> = vec![];

        let file_string: String = fs::read_to_string("benchmark_actions.txt")
            .expect("Should have been able to read the file");

        let contents: Vec<&str> = file_string.split(", ").collect();
        let mut actions: VecDeque<i16> = VecDeque::new();
        for a in contents {
            if a.trim().parse::<i16>().is_err() {
                continue;
            } else {
                actions.push_back(a.trim().parse::<i16>().unwrap());
            }
        }

        let (mut board1, mut board2, mut board3, mut board4): (
            RustBoard,
            RustBoard,
            RustBoard,
            RustBoard,
        );
        let (mut times1, mut times2, mut times3, mut times4): (f64, f64, f64, f64);
        let mut start: Instant;
        let (mut num_walls, mut num_moves): (i16, i16);
        'main: for _ in 0..n {
            (num_walls, num_moves) = (0, 0);

            board1 = RustBoard::new(1);
            board2 = RustBoard::new(2);
            board3 = RustBoard::new(3);
            board4 = RustBoard::new(4);
            'game: loop {
                (times1, times2, times3, times4) = (0.0, 0.0, 0.0, 0.0);
                for _ in 0..10 {
                    start = Instant::now();
                    board1.get_available_actions_fast();
                    times1 += start.elapsed().as_secs_f64();
                    start = Instant::now();
                    board2.get_available_actions_fast();
                    times2 += start.elapsed().as_secs_f64();
                    start = Instant::now();
                    board3.get_available_actions_fast();
                    times3 += start.elapsed().as_secs_f64();
                    start = Instant::now();
                    board4.get_available_actions_fast();
                    times4 += start.elapsed().as_secs_f64();
                }
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times1 / 10.0,
                    mode: 1,
                });
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times2 / 10.0,
                    mode: 2,
                });
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times3 / 10.0,
                    mode: 3,
                });
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times4 / 10.0,
                    mode: 4,
                });

                match actions.pop_front() {
                    Some(action) => {
                        if action == -1 {
                            break 'game;
                        }
                        board1.take_action(action);
                        board2.take_action(action);
                        board3.take_action(action);
                        board4.take_action(action);

                        if action < 128 {
                            num_walls += 1;
                        } else {
                            num_moves += 1;
                        }
                    }
                    None => break 'main,
                }
            }
        }

        let now: String = format!("{}", Utc::now().format("%Y-%m-%d_%H-%M-%S"));
        let mut wtr = csv::Writer::from_path(format!("./data/{}-{}.csv", now, n))?;
        for record in data {
            wtr.serialize(record)?;
        }
        wtr.flush()?;
        Ok(())
    }

    pub fn generate_actions(n: usize) {
        let mut board: RustBoard;
        let mut actions: Vec<i16> = vec![];
        let mut random_action: i16;
        for _ in 0..n {
            board = RustBoard::new(1);
            loop {
                random_action = board.get_random_action();
                actions.push(random_action);
                board.take_action(random_action);
                if board.is_over() {
                    actions.push(-1);
                    break;
                }
            }
        }
        let mut output_string: String = String::with_capacity(1000);
        let mut action_string: String;
        for action in actions {
            action_string = action.to_string();
            output_string.push_str(&action_string);
            output_string.push_str(", ");
        }
        output_string.pop();
        output_string.pop();

        println!("{}", output_string);
    }

    // the struct Game below follows the PGN notation as many as possible
    // white represents player 1 and black represents player 2
    #[derive(Clone, Debug)]
    pub struct GameData {
        date: DateTime<Local>,
        round: i16,
        white: i16,
        black: i16,
        result: String,
        actions_taken: Vec<i16>,
        rollouts_count: Vec<i32>,
    }

    impl GameData {
        pub fn new(round: i16, white: i16, black: i16) -> GameData {
            GameData {
                date: Local::now(),
                round,
                white,
                black,
                result: String::from("0-0"),
                actions_taken: vec![],
                rollouts_count: vec![],
            }
        }
        pub fn playout(&mut self) {
            let mut board_white: RustBoard;
            let mut board_black: RustBoard;

            match self.white {
                mode if mode / 10 == 1 => board_white = RustBoard::new(1), // BFS
                mode if mode / 10 == 2 => board_white = RustBoard::new(2), // DFS
                mode if mode / 10 == 3 => board_white = RustBoard::new(3), // GBFS
                mode if mode / 10 == 4 => board_white = RustBoard::new(4), // A*
                mode if mode / 10 == 5 => board_white = RustBoard::new(1), // only for Random

                _ => panic!("WHITE IS INVALID MODE"),
            }
            match self.white {
                mode if mode / 10 == 1 => board_black = RustBoard::new(1), // BFS
                mode if mode / 10 == 2 => board_black = RustBoard::new(2), // DFS
                mode if mode / 10 == 3 => board_black = RustBoard::new(3), // GBFS
                mode if mode / 10 == 4 => board_black = RustBoard::new(4), // A*
                mode if mode / 10 == 5 => board_black = RustBoard::new(1), // only for Random
                _ => panic!("WHITE IS INVALID MODE"),
            }

            let mut tree_white: MctsTree = MctsTree::new(board_white);
            let mut tree_black: MctsTree = MctsTree::new(board_black);

            let (mut action, mut rollout): (i16, i32);
            loop {
                tree_white.reset_tree(board_white);
                tree_black.reset_tree(board_black);
                rollout = 0;
                if self.white % 10 == 0 {
                    // random choose
                    action = tree_white.random_choose();
                } else if self.white % 10 == 1 {
                    // 1 second MCTS
                    (action, rollout) = tree_white.rollout_choose_timed(0.1);
                } else if self.white % 10 == 2 {
                    // 2 second MCTS
                    (action, rollout) = tree_white.rollout_choose_timed(0.2);
                } else if self.white % 10 == 3 {
                    // 5 second MCTS
                    (action, rollout) = tree_white.rollout_choose_timed(1.0);
                } else if self.white % 10 == 4 {
                    // 10 second MCTS
                    (action, rollout) = tree_white.rollout_choose_timed(5.0);
                } else {
                    panic!("INVALID MOVE GEN MODE");
                }
                board_white.take_action(action);
                board_black.take_action(action);
                self.actions_taken.push(action);
                self.rollouts_count.push(rollout);

                if board_white.is_over() | board_black.is_over() {
                    if board_white.is_over() != board_black.is_over() {
                        panic!("DIFFERENT OVER");
                    } else {
                        self.result = String::from("1-0");
                        break;
                    }
                }

                tree_white.reset_tree(board_white);
                tree_black.reset_tree(board_black);
                rollout = 0;
                if self.black % 10 == 0 {
                    // random choose
                    action = tree_black.random_choose();
                } else if self.black % 10 == 1 {
                    // 1 second MCTS
                    (action, rollout) = tree_black.rollout_choose_timed(0.1);
                } else if self.black % 10 == 2 {
                    // 2 second MCTS
                    (action, rollout) = tree_black.rollout_choose_timed(0.2);
                } else if self.black % 10 == 3 {
                    // 5 second MCTS
                    (action, rollout) = tree_black.rollout_choose_timed(1.0);
                } else if self.black % 10 == 4 {
                    // 10 second MCTS
                    (action, rollout) = tree_black.rollout_choose_timed(5.0);
                } else {
                    panic!("INVALID MOVE GEN MODE");
                }

                board_white.take_action(action);
                board_black.take_action(action);
                self.actions_taken.push(action);
                self.rollouts_count.push(rollout);
                if board_white.is_over() | board_black.is_over() {
                    if board_white.is_over() != board_black.is_over() {
                        board_white.display();
                        board_black.display();
                        panic!("DIFFERENT OVER");
                    } else {
                        self.result = String::from("0-1");
                        break;
                    }
                }
                // board_white.display();
            }
        }
        pub fn playout_write(&mut self, mut file: &File) {
            println!("Round {} start", self.round);

            let mut action_rollout: String;
            let mut white_str: String;
            let mut black_str: String;

            let mut enumerated_actions_rollouts: String;

            // let mut vec_data: Vec<GameData> = vec![];
            self.playout();
            action_rollout = String::with_capacity(180);
            for a in 0..self.actions_taken.len() {
                action_rollout.push_str(
                    format!(
                        "{}. {}({}) ",
                        a + 1,
                        self.actions_taken[a],
                        self.rollouts_count[a]
                    )
                    .as_str(),
                )
            }
            match self.white {
                50 => white_str = String::from("random"),
                11 => white_str = String::from("BFS 0.1s vanilla MCTS"),
                12 => white_str = String::from("BFS 0.2s vanilla MCTS"),
                13 => white_str = String::from("BFS 1.0s vanilla MCTS"),
                14 => white_str = String::from("BFS 5.0s vanilla MCTS"),
                21 => white_str = String::from("DFS 0.1s vanilla MCTS"),
                22 => white_str = String::from("DFS 0.2s vanilla MCTS"),
                23 => white_str = String::from("DFS 1.0s vanilla MCTS"),
                24 => white_str = String::from("DFS 5.0s vanilla MCTS"),
                41 => white_str = String::from("A* 0.1s vanilla MCTS"),
                42 => white_str = String::from("A* 0.2s vanilla MCTS"),
                43 => white_str = String::from("A* 1.0s vanilla MCTS"),
                44 => white_str = String::from("A* 5.0s vanilla MCTS"),
                _ => panic!("INVALID SEARCH"),
            }
            match self.black {
                50 => black_str = String::from("random"),
                11 => black_str = String::from("BFS 0.1s vanilla MCTS"),
                12 => black_str = String::from("BFS 0.2s vanilla MCTS"),
                13 => black_str = String::from("BFS 1.0s vanilla MCTS"),
                14 => black_str = String::from("BFS 5.0s vanilla MCTS"),
                21 => black_str = String::from("DFS 0.1s vanilla MCTS"),
                22 => black_str = String::from("DFS 0.2s vanilla MCTS"),
                23 => black_str = String::from("DFS 1.0s vanilla MCTS"),
                24 => black_str = String::from("DFS 5.0s vanilla MCTS"),
                41 => black_str = String::from("A* 0.1s vanilla MCTS"),
                42 => black_str = String::from("A* 0.2s vanilla MCTS"),
                43 => black_str = String::from("A* 1.0s vanilla MCTS"),
                44 => black_str = String::from("A* 5.0s vanilla MCTS"),
                _ => panic!("INVALID SEARCH"),
            }
            enumerated_actions_rollouts = String::new();
            for x in (0..self.actions_taken.len() - 1).step_by(2) {
                enumerated_actions_rollouts.push_str(
                    format!(
                        "{}. {}({}) {}({}) ",
                        (x + 2) / 2,
                        self.actions_taken[x],
                        self.rollouts_count[x],
                        self.actions_taken[x + 1],
                        self.rollouts_count[x + 1]
                    )
                    .as_str(),
                )
            }
            if self.actions_taken.len() % 2 == 1 {
                enumerated_actions_rollouts.push_str(
                    format!(
                        "{}. {}({}) {}\n",
                        self.actions_taken.len() / 2 + 1,
                        self.actions_taken[self.actions_taken.len() / 2 + 1],
                        self.rollouts_count[self.actions_taken.len() / 2 + 1],
                        self.result
                    )
                    .as_str(),
                )
            } else {
                enumerated_actions_rollouts.push_str(format!("{}\n", self.result).as_str());
            }
            file.write(format!("[Date \"{}\"]\n[Round \"{}\"]\n[White \"{}\"]\n[Black \"{}\"]\n[Result \"{}\"]\n", self.date, self.round, white_str, black_str, self.result).as_bytes());
            file.write(enumerated_actions_rollouts.as_bytes());
            println!("Round {} over", self.round);
        }
    }

    pub fn generate_pgn_file(n: usize) {
        let mut game: GameData;
        let mut round: i16 = 1;
        let mut file = match File::create(format!("elo_pathfinding{}.pgn", n)) {
            Err(why) => panic!("couldn't create {}", why),
            Ok(file) => file,
        };

        let mut vec_games: Vec<GameData> = vec![];

        for mode1 in [50, 11, 21, 41] {
            // Round robin tournament between
            // 50 - random
            // 13,23,43 - BFS, DFS, A* 1s MCTS
            // GBFS ignored as the performance is mid compared to BFS and A*
            // BFS and A* both follow same trend and yet speed is significantly different
            // DFS follows a different trend
            // Total playtime should be 12 * number of repeated games
            // -----50, 13, 23, 43------
            for mode2 in [50, 11, 21, 41] {
                if mode1 == mode2 {
                    continue;
                }
                for _ in 0..n {
                    game = GameData::new(round, mode1, mode2);
                    vec_games.push(game);
                    round += 1;
                }
            }
        }
        file = match File::create(format!("elo_mcts_times{}.pgn", n)) {
            Err(why) => panic!("couldn't create {}", why),
            Ok(file) => file,
        };
        for mode1 in [11, 12, 13, 14] {
            // Round robin tournament between
            // MCTS of different times
            // Intended to compare effect of time against performance
            // Total playtime should be 12 * number of repeated games
            // -----11,12,13,14, 21,22,23,24, 41,42,43,44------
            for mode2 in [11, 12, 13, 14] {
                if mode1 == mode2 {
                    continue;
                }
                for _ in 0..n {
                    game = GameData::new(round, mode1, mode2);
                    vec_games.push(game);
                    round += 1;
                }
            }
        }
        println!("{}", vec_games.len());
        vec_games
            .par_iter_mut()
            .for_each(|x| x.playout_write(&file));
    }
    // Ok(())
}
