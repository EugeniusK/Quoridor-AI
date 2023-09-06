extern crate rand;
extern crate rand_chacha;
// use board::board::QuoridorBoardMini;
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
// pub use bitboard_mini::mini_bitboard_implementations::
pub mod mcts;
pub use mcts::mcts_implementation::MctsTree;

pub mod test;
pub use test::test_compare;

pub mod tictactoe;
pub use tictactoe::tictactoe_implementation::TicTacToe;
fn main() {
    // println!("{:?}", board1.get_available_actions_fast());
    // println!("{}", board1.get_random_action());
    let mut action1: i16;
    let (mut wins, mut games_played, mut draws) = (0.0, 0.0, 0.0);

    let mut tree: MctsTree<TicTacToe>;
    for x in 0..100 {
        let mut board1 = TicTacToe::new(1);

        loop {
            // board1.flip_turn();
            tree = MctsTree::new(board1);
            action1 = tree.rollout_choose(50);
            // board1.flip_turn();
            // panic!();
            board1.take_action(action1);
            if board1.is_over() {
                break;
            }
            action1 = board1.get_random_action();

            board1.take_action(action1);
            if board1.is_over() {
                break;
            }
        }
        if board1.get_turn() == 1 {
            wins += 1.0;
        } else if board1.get_turn() == -1 {
            draws += 1.0
        }
        // board1.display();
        games_played += 1.0;
        // board1.display();
        // println!("{:?}", board1.get_available_actions_fast());
    }
    println!(
        "{} games {} of games won {} drawn {} won",
        games_played,
        wins / games_played,
        draws,
        wins
    );
}

// // board.take_action(16);
// // println!("{}", board.is_wall_valid(16));
// // println!("{}", board.is_wall_valid(17));
// // println!("{}", board.is_wall_valid(24));
// // println!("{}", board.is_wall_valid(0));

// let (mut wins, mut games_played) = (0.0, 0.0);
// let mut board1: RustDynamicGraphMini;
// // let mut board2: RustDynamicGraphMini;
// let mut tree: MctsTree<RustDynamicGraphMini>;

// let mut action1: i16;
// for x in 1..=10000 {
//     games_played += 1.0;

//     board1 = RustDynamicGraphMini::new(1);
//     // board2 = RustDynamicGraphMini::new(1);

//     while !board1.is_over() {
//         //&& !board2.is_over() {
//         tree = MctsTree::new(board1);
//         action1 = tree.rollout_choose(50);
//         board1.take_action(action1);

//         action1 = board1.get_random_action();

//         board1.take_action(action1);
//         // println!("{}", action1);
//         // board1.display();
//         // board2.display();
//     }
//     // board1.display();
//     if board1.get_turn() == 1 {
//         wins += 1.0;
//     }
//     if x % 100 == 0 {
//         println!("{} {}", games_played, wins / games_played);
//         board1.display();
//     }
// }
