extern crate rand;

pub mod bitboard;
pub mod graph;
pub use std::collections::VecDeque;

pub use bitboard::bitboard_implementations::QuoridorBitboard;

pub use bitboard::bitboard_implementations::Bitboard;
pub use bitboard::bitboard_implementations::RustFullBitboard;
pub use bitboard::bitboard_implementations::RustPartialBitboard;
pub use graph::graph_implementations::RustDynamicGraph;
pub use graph::graph_implementations::RustStaticGraph;

pub use graph::graph_implementations::Graph;

use rand::prelude::*;
use rand_chacha::ChaCha8Rng;
fn main() {
    let mut rng = ChaCha8Rng::seed_from_u64(2);

    let mut board0: RustPartialBitboard = RustPartialBitboard::new(1);

    let mut available: [bool; 140];
    let mut action: i16;

    println!("{:?}", board0.get_available_actions_fast());
    for i in 0..10 {
        let mut board0 = RustPartialBitboard::new(1);
        let mut board1 = RustFullBitboard::new(10);
        let mut board2 = RustDynamicGraph::new(1);
        let mut board3 = RustStaticGraph::new(1);
        println!("{}", i);
        while !board0.is_over() && !board1.is_over() && !board2.is_over() && !board3.is_over() {
            if board0.get_available_actions_slow() == board1.get_available_actions_slow()
                && board1.get_available_actions_slow() == board2.get_available_actions_slow()
                && board2.get_available_actions_slow() == board3.get_available_actions_slow()
            {
                available = board0.get_available_actions_slow();
                action = rng.gen_range(0..140);
                while !available[action as usize] {
                    action = rng.gen_range(0..140);
                }
                board0.take_action(action);
                board1.take_action(action);
                board2.take_action(action);
                board3.take_action(action);
                if !(board0.is_over() == board1.is_over()
                    && board1.is_over() == board2.is_over()
                    && board2.is_over() == board3.is_over())
                {
                    println!("OVER NOT EQUAL");
                    panic!("AHHH")
                }
                if board0.is_over() {
                    board0.display();

                    break;
                }
            } else {
                println!("NOT EQ");
                break;
            }
        }
    }
}
