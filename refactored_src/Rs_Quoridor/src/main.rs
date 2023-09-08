extern crate rand;
extern crate rand_chacha;
use crate::bitboard_mini::mini_bitboard_implementations::BitboardMini;
// use board::board::QuoridorBoardMini;
use crate::rand::Rng;
use crate::rand::SeedableRng;
pub use rand_chacha::ChaCha8Rng;
pub use std::collections::VecDeque;
pub use std::rc::Rc;

pub mod board;
pub use board::board::QuoridorBoard;

pub use std::mem;

pub mod bitboard;
pub use bitboard::bitboard_implementations::Bitboard;
pub use bitboard::bitboard_implementations::QuoridorBitboard;
pub use bitboard::bitboard_implementations::RustFullBitboard;
pub use bitboard::bitboard_implementations::RustPartialBitboard;

pub mod graph;
pub use graph::graph_implementations::Graph;
pub use graph::graph_implementations::RustDynamicGraph;
pub use graph::graph_implementations::RustStaticGraph;

pub mod graph_mini;
pub use graph_mini::mini_graph_implementations::GraphMini;
pub use graph_mini::mini_graph_implementations::RustDynamicGraphMini;
pub use graph_mini::mini_graph_implementations::RustStaticGraphMini;

pub mod bitboard_mini;
pub use bitboard_mini::mini_bitboard_implementations::RustPartialBitboardMini;

pub mod mcts;
pub use mcts::mcts_implementation::MctsTree;

pub mod test;
pub use test::quoridor_tests::Test_Compare;

pub mod tictactoe;
pub use tictactoe::tictactoe_implementation::TicTacToe;
fn main() {
    let mut test1: Test_Compare<RustStaticGraph, RustDynamicGraph> = Test_Compare::new(1, 1);
    test1.compare(500);
    let mut test2: Test_Compare<RustStaticGraph, RustPartialBitboard> = Test_Compare::new(1, 1);
    test2.compare(500);
    let mut test3: Test_Compare<RustStaticGraph, RustFullBitboard> = Test_Compare::new(1, 1);
    test3.compare(500);
    let mut test1: Test_Compare<RustStaticGraph, RustDynamicGraph> = Test_Compare::new(1, 1);
    test1.compare(5000);
    let mut test2: Test_Compare<RustStaticGraph, RustPartialBitboard> = Test_Compare::new(1, 1);
    test2.compare(5000);
    let mut test3: Test_Compare<RustStaticGraph, RustFullBitboard> = Test_Compare::new(1, 1);
    test3.compare(5000);
    let mut test3: Test_Compare<RustStaticGraphMini, RustDynamicGraphMini> =
        Test_Compare::new(1, 1);
    test3.compare(500);
    let mut test3: Test_Compare<RustStaticGraphMini, RustPartialBitboardMini> =
        Test_Compare::new(1, 1);
    test3.compare(500);
}
