extern crate rand;
extern crate rand_chacha;
extern crate rayon;

pub use rand_chacha::ChaCha8Rng;
pub use std::collections::{BinaryHeap, VecDeque};
pub use std::rc::Rc;

pub use std::mem;

pub mod final_board;
pub use final_board::final_board::RustBoard;
pub mod final_mcts;
pub mod perf;
pub use perf::peformance_tests::*;
pub mod test;
pub mod util;

fn main() {
    generate_pgn_file(100);
}
