extern crate rand;
extern crate rand_chacha;
pub use rand_chacha::ChaCha8Rng;
pub use std::collections::{BinaryHeap, VecDeque};
pub use std::rc::Rc;

pub mod board;
pub use board::board::QuoridorBoard;

pub use std::mem;

pub mod bitboard;
pub mod bitboard_mini;
pub mod graph;
pub mod graph_mini;
pub mod mcts;
pub mod test;
pub use test::quoridor_tests::*;

pub mod util;

fn main() {
    let mut test1: Test_Compare<RustFullBitboard, RustDynamicGraph> = Test_Compare::new(1, 1);
    test1.compare(5000);

    let mut test1: Test_Compare<RustFullBitboard, RustDynamicGraph> = Test_Compare::new(1, 2);
    test1.compare(5000);
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
