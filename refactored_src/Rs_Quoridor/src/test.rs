fn main() {
    let mut rng = ChaCha8Rng::seed_from_u64(2);

    let mut board0 = RustPartialBitboard::new(1);
    let mut board1 = RustFullBitboard::new(1);
    let mut board2 = RustDynamicGraph::new(1);
    let mut board3 = RustStaticGraph::new(1);

    let mut available: [bool; 140];
    let mut action: i16;

    let mut actions_played = 0;
    for i in 0..10 {
        actions_played = 0;
        let mut board0 = RustPartialBitboard::new(1);
        let mut board1 = RustFullBitboard::new(10);
        let mut board2 = RustDynamicGraph::new(1);
        let mut board3 = RustStaticGraph::new(1);

        while !board0.is_over() && !board1.is_over() && !board2.is_over() && !board3.is_over() {
            if board0.get_available_actions_fast() == board1.get_available_actions_fast()
                && board1.get_available_actions_fast() == board2.get_available_actions_fast()
                && board2.get_available_actions_fast() == board3.get_available_actions_fast()
            {
                available = board0.get_available_actions_fast();
                action = rng.gen_range(0..140);
                while !available[action as usize] {
                    action = rng.gen_range(0..140);
                }
                board0.take_action(action);
                board1.take_action(action);
                board2.take_action(action);
                board3.take_action(action);
                actions_played += 1;
                if !(board0.is_over() == board1.is_over()
                    && board1.is_over() == board2.is_over()
                    && board2.is_over() == board3.is_over())
                {
                    println!("OVER NOT EQUAL");
                    panic!("AHHH")
                }
                if board0.is_over() {
                    println!("{} {}", i, actions_played);
                    break;
                }
            } else {
                println!("NOT EQ");
                break;
            }
        }
    }
}
