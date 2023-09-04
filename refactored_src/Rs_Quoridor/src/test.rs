pub mod test_compare {

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

    use crate::rand::Rng;
    use crate::rand::SeedableRng;
    use crate::rand_chacha;
    pub use rand_chacha::ChaCha8Rng;
    pub fn compare(n: usize) {
        let mut rng = ChaCha8Rng::seed_from_u64(2);

        let mut available: Vec<i16>;
        let mut action: i16;

        let mut actions_played = 0.0;
        for i in 1..=n {
            let mut board0 = RustPartialBitboard::new(1);
            let mut board1 = RustFullBitboard::new(10);
            let mut board2 = RustDynamicGraph::new(1);
            let mut board3 = RustStaticGraph::new(1);

            while !board0.is_over() && !board1.is_over() && !board2.is_over() && !board3.is_over() {
                if (board2.p1_pos < 0)
                    | (board2.p2_pos < 0)
                    | (board3.p1_pos < 0)
                    | (board3.p2_pos < 0)
                    | (board2.p1_pos > 80)
                    | (board2.p2_pos > 80)
                    | (board3.p1_pos > 80)
                    | (board3.p2_pos > 80)
                {
                    board0.display();
                    board1.display();
                    board2.display();
                    board3.display();
                }
                if board0.get_available_actions_fast() == board1.get_available_actions_fast()
                    && board1.get_available_actions_fast() == board2.get_available_actions_fast()
                    && board2.get_available_actions_fast() == board3.get_available_actions_fast()
                {
                    available = board0.get_available_actions_fast();
                    action = rng.gen_range(0..140);
                    while !available.contains(&action) {
                        action = rng.gen_range(0..140);
                    }
                    board0.take_action(action);
                    board1.take_action(action);
                    board2.take_action(action);
                    board3.take_action(action);
                    actions_played += 1.0;
                    if !(board0.is_over() == board1.is_over()
                        && board1.is_over() == board2.is_over()
                        && board2.is_over() == board3.is_over())
                    {
                        println!("OVER NOT EQUAL");
                        panic!("AHHH")
                    }
                    if board0.is_over() {
                        // print!("{}-{} ", i, actions_played);
                        if i % 1000 == 0 {
                            println!("{} {} ", i, (actions_played / i as f32));
                            board0.display();
                        }
                        break;
                    }
                } else {
                    println!("NOT EQ");
                    break;
                }
            }
        }
    }
}

// let mut wins = 0.0;

//     for x in 1..=1 {
//         let mut tree: MctsTree<RustDynamicGraph>;

//         let mut a: RustDynamicGraph = RustDynamicGraph::new(1);
//         let mut random_action: i16;
//         let mut ai_action: i16;
//         loop {
//             // random opponent
//             random_action = a.get_random_action();
//             // println!("RANDOM TURN {} {}", a.get_turn(), random_action);
//             a.take_action(random_action);
//             if a.is_over() {
//                 // a.display();
//                 println!("{}", wins / x as f32);

//                 // println!("OVER RANDOM, {}", a.get_turn());
//                 break;
//             }
//             // AI opponent
//             // tree.reset_tree(a);
//             tree = MctsTree::new(a);
//             ai_action = tree.rollout_choose(50000);
//             println!("AI TURN {} {}", a.get_turn(), ai_action);

//             a.take_action(ai_action);
//             a.display();
//             if a.is_over() {
//                 // a.display();
//                 println!("{}", wins / x as f32);
//                 wins += 1.0;
//                 // println!("OVER AI, {}", a.get_turn());
//                 break;
//             }
//         }
//     }
//     println!("{}", wins / 100.0);
