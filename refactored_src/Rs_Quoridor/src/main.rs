extern crate rand;
extern crate rand_chacha;
use rand::prelude::*;

pub use rand_chacha::ChaCha8Rng;
pub use std::collections::VecDeque;
pub mod bitboard;
pub mod board;
pub use bitboard::bitboard_implementations::Bitboard;
pub use bitboard::bitboard_implementations::QuoridorBitboard;
pub use bitboard::bitboard_implementations::RustFullBitboard;
pub use bitboard::bitboard_implementations::RustPartialBitboard;

pub mod graph;
pub use graph::graph_implementations::Graph;
pub use graph::graph_implementations::RustDynamicGraph;
pub use graph::graph_implementations::RustStaticGraph;

pub mod mcts;
fn main() {
    const EXPLORATION_PARAMETER: i32 = 2;

    pub struct MctsTree<T> {
        board_state: T,
        simulations_won: f32,
        simulations_run: f32,
        valid_actions: [bool; 81],
        valid_actions_generated: bool,
        // children: [Box<MctsTree<T>>; 81],
    }

    impl MctsTree<RustFullBitboard> {
        pub fn simulation(&mut self) -> f64 {
            println!("{}", self.board_state.get_turn());
            let mut rng: ChaCha8Rng = ChaCha8Rng::from_entropy();

            let start_turn: i16 = self.board_state.get_turn();
            let mut random_action: i16;
            while !self.board_state.is_over() {
                random_action = rng.gen_range(0..140);
                while !self.board_state.is_action_available(random_action) {
                    random_action = rng.gen_range(0..140);
                }
                self.board_state.take_action(random_action);
            }
            self.board_state.display();
            if start_turn == self.board_state.get_turn() {
                return 1.0;
            } else {
                return -1.0;
            }
        }
    }

    let mut a: MctsTree<RustFullBitboard> = MctsTree {
        board_state: RustFullBitboard::new(1),
        simulations_run: 0.0,
        simulations_won: 0.0,
        valid_actions: [false; 81],
        valid_actions_generated: false,
    };

    println!("{}", a.simulation());
}
