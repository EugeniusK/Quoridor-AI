#[cfg(test)]
mod tests {
    use crate::final_board;
    pub use final_board::final_board::RustBoard;

    use crate::rand::Rng;
    use crate::rand::SeedableRng;
    use crate::rand_chacha;
    use chrono::Utc;
    pub use rand_chacha::ChaCha8Rng;

    use std::collections::VecDeque;

    use std::fs;

    use std::error::Error;
    use std::time::Instant;
    #[test]
    fn bfs_dfs() {
        let mut test: Test_Compare = Test_Compare::new(1, 2);
        assert!(test.compare(500));
    }
    #[test]
    fn bfs_gbfs() {
        let mut test: Test_Compare = Test_Compare::new(1, 2);
        assert!(test.compare(500));
    }
    #[test]
    fn bfs_astar() {
        let mut test: Test_Compare = Test_Compare::new(1, 2);
        assert!(test.compare(500));
    }
    #[test]
    fn dfs_gbfs() {
        let mut test: Test_Compare = Test_Compare::new(1, 2);
        assert!(test.compare(500));
    }
    #[test]
    fn dfs_astar() {
        let mut test: Test_Compare = Test_Compare::new(1, 2);
        assert!(test.compare(500));
    }
    #[test]
    fn gbfs_astar() {
        let mut test: Test_Compare = Test_Compare::new(1, 2);
        assert!(test.compare(500));
    }

    pub struct Test_Compare {
        board1: RustBoard,
        board2: RustBoard,
    }
    impl Test_Compare {
        pub fn new(path_finding_one: i16, path_finding_two: i16) -> Test_Compare {
            Test_Compare {
                board1: RustBoard::new(path_finding_one),
                board2: RustBoard::new(path_finding_two),
            }
        }
        pub fn compare(&self, n: usize) -> bool {
            let mut pass = true;

            let mut actions_taken = 0;
            let mut rng = ChaCha8Rng::seed_from_u64(2);

            let mut board1: RustBoard;
            let mut board2: RustBoard;
            let mut action1: i16;
            let mut action2: i16;
            let mut action: i16;
            let mut board1_available: Vec<i16>;
            let mut board2_available: Vec<i16>;

            'main: for _x in 0..n {
                board1 = self.board1;
                board2 = self.board2;
                while !board1.is_over() && !board2.is_over() {
                    board1_available = board1.get_available_actions_fast();
                    board2_available = board2.get_available_actions_fast();

                    if board1_available != board2_available {
                        pass = false;
                        break 'main;
                    } else {
                        action = rng.gen_range(0..140);
                        action1 = action;
                        action2 = action;

                        while !board1_available.contains(&action)
                            | !board2_available.contains(&action)
                        {
                            action = rng.gen_range(0..140);
                            action1 = action;
                            action2 = action;
                        }
                        board1.take_action(action2);
                        board2.take_action(action1);

                        actions_taken += 1;
                        if board1.is_over() != board2.is_over() {
                            pass = false;
                            break 'main;
                        }
                    }
                }
            }
            pass
        }
    }
}
