pub mod peformance_tests {
    use crate::final_board;
    use crate::final_mcts::final_mcts::MctsTree;
    pub use final_board::final_board::RustBoard;

    use crate::rand_chacha;
    pub use rand_chacha::ChaCha8Rng;

    use chrono::Utc;

    use std::collections::VecDeque;

    use chrono::DateTime;
    use chrono::Local;
    use std::error::Error;
    use std::fs;
    use std::time::Instant;
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
                _ => panic!("WHITE IS INVALID MODE"),
            }
            match self.white {
                mode if mode / 10 == 1 => board_black = RustBoard::new(1), // BFS
                mode if mode / 10 == 2 => board_black = RustBoard::new(2), // DFS
                mode if mode / 10 == 3 => board_black = RustBoard::new(3), // GBFS
                mode if mode / 10 == 4 => board_black = RustBoard::new(4), // A*
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
            }
        }
    }

    pub fn generate_pgn_file(n: usize) {
        let mut data: GameData;
        let mut round: i16 = 1;
        let mut results: Vec<GameData> = vec![];
        for mode1 in [
            10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34, 40, 41, 42, 43, 44,
        ] {
            for mode2 in [
                10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 30, 31, 32, 33, 34, 40, 41, 42, 43, 44,
            ] {
                for _ in 0..n {
                    data = GameData::new(round, mode1, mode2);
                    data.playout();
                    results.push(data);
                    round += 1;
                }
                println!("{:?}", results);
            }
        }
    }
}
