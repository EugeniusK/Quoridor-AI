extern crate rand;
extern crate rand_chacha;
// use board::board::QuoridorBoardMini;

pub use rand_chacha::ChaCha8Rng;
pub use std::collections::{BinaryHeap, VecDeque};
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
pub use bitboard_mini::mini_bitboard_implementations::BitboardMini;
pub use bitboard_mini::mini_bitboard_implementations::RustFullBitboardMini;
pub use bitboard_mini::mini_bitboard_implementations::RustPartialBitboardMini;

pub mod mcts;
pub use mcts::mcts_implementation::MctsTree;

pub mod test;
pub use test::quoridor_tests;
pub use test::quoridor_tests::*;

pub mod tictactoe;
pub use tictactoe::tictactoe_implementation::TicTacToe;

// pub mod candidate_graph_pathfinding;
// pub use candidate_graph_pathfinding::candidate_bfs::{
//     bfs_candidate0, bfs_candidate1, bfs_candidate2, bfs_candidate3, bfs_candidate4, bfs_candidate5,
// };
fn main() {
    // let mut board: RustDynamicGraph = RustDynamicGraph::new(1);
    // println!("{:?}", board.get_available_actions_fast());
    // let mut board: RustDynamicGraph = RustDynamicGraph::new(3);
    // println!("{:?}", board.get_available_actions_fast());

    // generate_data(10, 1);
    // generate_data(10, 5);
    // generate_data(10, 6);
    // generate_data(10, 7);
    // generate_data(10, 8);
    // generate_data(10, 1);
    // generate_data(10, 2);
    generate_actions(100);

    // let mut test1: Test_Compare<RustFullBitboard, RustDynamicGraph> = Test_Compare::new(1, 1);
    // test1.compare(5000);

    // let mut test1: Test_Compare<RustFullBitboard, RustDynamicGraph> = Test_Compare::new(1, 2);
    // test1.compare(5000);
    // let mut test1: Test_Compare<RustFullBitboard, RustDynamicGraph> = Test_Compare::new(1, 3);
    // test1.compare(50000);
    // let mut test1: Test_Compare<RustStaticGraph, RustDynamicGraph> = Test_Compare::new(1, 6);
    // test1.compare(5000);
    // let mut test1: Test_Compare<RustStaticGraph, RustDynamicGraph> = Test_Compare::new(1, 7);
    // test1.compare(5000);
    // let mut test1: Test_Compare<RustStaticGraph, RustDynamicGraph> = Test_Compare::new(1, 8);
    // test1.compare(5000);
    // let mut test1: Test_Compare<RustStaticGraph, RustDynamicGraph> = Test_Compare::new(1, 3);
    // test1.compare(50000);
    // let mut test1: Test_Compare<RustStaticGraph, RustDynamicGraph> = Test_Compare::new(1, 1);
    // test1.compare(50000);
    // let mut test2: Test_Compare<RustStaticGraph, RustPartialBitboard> = Test_Compare::new(1, 2);
    // test2.compare(500);
    // let mut test3: Test_Compare<RustStaticGraph, RustFullBitboard> = Test_Compare::new(1, 1);
    // test3.compare(500);
    // let mut test1: Test_Compare<RustStaticGraph, RustDynamicGraph> = Test_Compare::new(1, 1);
    // test1.compare(5000);
    // let mut test2: Test_Compare<RustStaticGraph, RustPartialBitboard> = Test_Compare::new(1, 1);
    // test2.compare(5000);
    // let mut test3: Test_Compare<RustStaticGraph, RustFullBitboard> = Test_Compare::new(1, 1);
    // test3.compare(5000);
    // let mut test3: Test_Compare<RustStaticGraphMini, RustDynamicGraphMini> =
    //     Test_Compare::new(1, 1);
    // test3.compare(50000);
    // let mut test3: Test_Compare<RustStaticGraphMini, RustPartialBitboardMini> =
    //     Test_Compare::new(1, 1);
    // test3.compare(50000);
    // let mut test3: Test_Compare<RustStaticGraphMini, RustFullBitboardMini> =
    //     Test_Compare::new(1, 1);
    // test3.compare(50000);
}
