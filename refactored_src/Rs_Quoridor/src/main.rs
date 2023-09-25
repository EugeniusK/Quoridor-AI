extern crate rand;
extern crate rand_chacha;
pub use rand_chacha::ChaCha8Rng;
pub use std::collections::{BinaryHeap, VecDeque};
pub use std::rc::Rc;

pub use std::mem;

pub mod final_board;
pub use final_board::final_board::RustBoard;
pub mod final_mcts;
pub mod perf;
pub use perf::peformance_tests::*;
// pub mod game;
pub mod test;
pub mod util;
use std::time::Instant;

fn main() {
    //     let mut board = RustBoard::new(1);
    //     let mut tree = final_mcts::final_mcts::MctsTree::new(board);
    //     tree.rollout_choose_timed(5.0);
    //     tree.reset_tree(board);
    //     tree.rollout_choose_timed(1.0);
    //     tree.reset_tree(board);
    //     tree.rollout_choose_timed(5.0);
    //     tree.reset_tree(board);
    //     let mut board = RustBoard::new(3);
    //     let mut tree = final_mcts::final_mcts::MctsTree::new(board);
    //     tree.rollout_choose_timed(5.0);
    //     tree.reset_tree(board);
    //     tree.rollout_choose_timed(1.0);
    //     tree.reset_tree(board);
    //     tree.rollout_choose_timed(5.0);
    //     tree.reset_tree(board);
    generate_pgn_file(10);

    // let mut board: RustBoard = RustBoard::new(1);
    // for a in [
    //     124, 127, 12, 98, 20, 70, 72, 115, 23, 19, 30, 4, 121, 93, 16, 56, 27, 126, 77, 129, 129,
    //     66, 129, 49, 128, 97,
    // ] {
    //     println!(" {} {}", a, board.is_action_available(a));
    //     board.take_action(a);
    //     board.display();
    //     println!("{:?}", board.get_available_actions_slow())
    // }
    // board.display();
}
