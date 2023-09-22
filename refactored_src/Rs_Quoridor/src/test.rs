pub mod quoridor_tests {

    use crate::board;
    pub use board::board::QuoridorBoard;

    use crate::bitboard;
    pub use bitboard::bitboard_implementations::Bitboard;
    pub use bitboard::bitboard_implementations::QuoridorBitboard;
    pub use bitboard::bitboard_implementations::RustFullBitboard;
    pub use bitboard::bitboard_implementations::RustPartialBitboard;

    use crate::graph;
    pub use graph::graph_implementations::Graph;
    pub use graph::graph_implementations::RustDynamicGraph;
    pub use graph::graph_implementations::RustStaticGraph;

    use crate::bitboard_mini;
    pub use bitboard_mini::mini_bitboard_implementations::BitboardMini;
    pub use bitboard_mini::mini_bitboard_implementations::QuoridorBitboardMini;
    pub use bitboard_mini::mini_bitboard_implementations::RustFullBitboardMini;
    pub use bitboard_mini::mini_bitboard_implementations::RustPartialBitboardMini;

    use crate::graph_mini;
    pub use graph_mini::mini_graph_implementations::GraphMini;
    pub use graph_mini::mini_graph_implementations::RustDynamicGraphMini;
    pub use graph_mini::mini_graph_implementations::RustStaticGraphMini;

    use crate::rand::Rng;
    use crate::rand::SeedableRng;
    use crate::rand_chacha;
    pub use rand_chacha::ChaCha8Rng;

    use chrono::Utc;

    use serde::Serialize;
    use std::collections::VecDeque;

    use std::fs;

    use std::error::Error;
    use std::time::Instant;
    #[derive(Clone, Copy, Debug, serde::Serialize)]
    pub struct GameDataBasic {
        num_walls: i16,
        num_moves: i16,
        num_actions: i16,
        time_taken: f64,
        type_board: i16,
        mode: i16,
    }
    pub struct Test_Compare<T: QuoridorBoard + Copy, U: QuoridorBoard + Copy> {
        board1: T,
        board2: U,
    }
    impl<T: QuoridorBoard + Copy, U: QuoridorBoard + Copy> Test_Compare<T, U> {
        pub fn new(path_finding_one: i16, path_finding_two: i16) -> Test_Compare<T, U> {
            Test_Compare {
                board1: T::new(path_finding_one),
                board2: U::new(path_finding_two),
            }
        }

        pub fn compare(&self, n: usize) {
            let mut actions_taken = 0;
            let mut rng = ChaCha8Rng::seed_from_u64(2);

            let mut board1: T;
            let mut board2: U;
            let mut action1: i16;
            let mut action2: i16;
            let mut action: i16;
            let mut board1_available: Vec<i16>;
            let mut board2_available: Vec<i16>;

            if self.board1.number_actions() != self.board2.number_actions() {
                panic!("BOARDS ARE DIFFERENT SIZES");
            }
            for _x in 0..n {
                board1 = self.board1;
                board2 = self.board2;
                while !board1.is_over() && !board2.is_over() {
                    board1_available = board1.get_available_actions_fast();
                    board2_available = board2.get_available_actions_fast();

                    if board1_available != board2_available {
                        println!("{:?}", board1_available);
                        println!("{:?}", board2_available);
                        panic!("BOARDS RETURN DIFFERENT VALID ACTIONS");
                    } else {
                        action = rng.gen_range(0..board1.number_actions());
                        action1 = action;
                        action2 = action;

                        while !board1_available.contains(&action)
                            | !board2_available.contains(&action)
                        {
                            action = rng.gen_range(0..board1.number_actions());
                            action1 = action;
                            action2 = action;
                        }
                        board1.take_action(action2);
                        board2.take_action(action1);

                        actions_taken += 1;
                        if board1.is_over() != board2.is_over() {
                            panic!("BOARDS DISAGREE IF OVER");
                        }
                    }
                }
            }
            println!("PASS");
            println!("Average actions: {}", actions_taken / n);
        }
    }

    pub fn generate_data(n: usize, mode: i16) -> Result<(), Box<dyn Error>> {
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
            RustStaticGraph,
            RustDynamicGraph,
            RustPartialBitboard,
            RustFullBitboard,
        );
        let (mut times1, mut times2, mut times3, mut times4): (f64, f64, f64, f64);
        let mut start: Instant;
        let (mut num_walls, mut num_moves): (i16, i16);
        'main: for _ in 0..n {
            (num_walls, num_moves) = (0, 0);
            board1 = RustStaticGraph::new(mode);
            board2 = RustDynamicGraph::new(mode);
            board3 = RustPartialBitboard::new(mode);
            board4 = RustFullBitboard::new(mode);
            (times1, times2, times3, times4) = (0.0, 0.0, 0.0, 0.0);
            'game: loop {
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
                    type_board: 1,
                    mode,
                });
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times2 / 10.0,
                    type_board: 2,
                    mode,
                });
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times3 / 10.0,
                    type_board: 3,
                    mode,
                });
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times4 / 10.0,
                    type_board: 4,
                    mode,
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
    pub fn generate_data_mini(n: usize, mode: i16) -> Result<(), Box<dyn Error>> {
        let mut data: Vec<GameDataBasic> = vec![];
        let file_string: String = fs::read_to_string("mini_benchmark_actions.txt")
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

        let (mut board5, mut board6, mut board7, mut board8): (
            RustStaticGraphMini,
            RustDynamicGraphMini,
            RustPartialBitboardMini,
            RustFullBitboardMini,
        );
        let (mut times5, mut times6, mut times7, mut times8): (f64, f64, f64, f64);
        let mut start: Instant;
        let (mut num_walls, mut num_moves): (i16, i16);
        'main: for _ in 0..n {
            (num_walls, num_moves) = (0, 0);
            board5 = RustStaticGraphMini::new(mode);
            board6 = RustDynamicGraphMini::new(mode);
            board7 = RustPartialBitboardMini::new(mode);
            board8 = RustFullBitboardMini::new(mode);
            (times5, times6, times7, times8) = (0.0, 0.0, 0.0, 0.0);
            'game: loop {
                for _ in 0..10 {
                    start = Instant::now();
                    board5.get_available_actions_fast();
                    times5 += start.elapsed().as_secs_f64();
                    start = Instant::now();
                    board6.get_available_actions_fast();
                    times6 += start.elapsed().as_secs_f64();
                    start = Instant::now();
                    board7.get_available_actions_fast();
                    times7 += start.elapsed().as_secs_f64();
                    start = Instant::now();
                    board8.get_available_actions_fast();
                    times8 += start.elapsed().as_secs_f64();
                }
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times5 / 10.0,
                    type_board: 5,
                    mode,
                });
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times6 / 10.0,
                    type_board: 6,
                    mode,
                });
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times7 / 10.0,
                    type_board: 7,
                    mode,
                });
                data.push(GameDataBasic {
                    num_walls,
                    num_moves,
                    num_actions: num_walls + num_moves,
                    time_taken: times8 / 10.0,
                    type_board: 8,
                    mode,
                });
                match actions.pop_front() {
                    Some(action) => {
                        if action == -1 {
                            break 'game;
                        }
                        board5.take_action(action);
                        board6.take_action(action);
                        board7.take_action(action);
                        board8.take_action(action);

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
        let mut wtr = csv::Writer::from_path(format!("./data/mini_{}-{}.csv", now, n))?;
        for record in data {
            wtr.serialize(record)?;
        }
        wtr.flush()?;
        Ok(())
    }

    pub fn generate_actions(n: usize) {
        let mut board: RustDynamicGraph;
        let mut actions: Vec<i16> = vec![];
        let mut random_action: i16;
        for _ in 0..n {
            board = RustDynamicGraph::new(1);
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
    pub fn generate_actions_mini(n: usize) {
        let mut board: RustDynamicGraphMini;
        let mut actions: Vec<i16> = vec![];
        let mut random_action: i16;
        for _ in 0..n {
            board = RustDynamicGraphMini::new(1);
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
}
