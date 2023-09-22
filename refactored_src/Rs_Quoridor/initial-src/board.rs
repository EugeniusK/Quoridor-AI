pub mod board {

    use crate::rand::*;
    use rand_chacha::ChaCha8Rng;
    pub trait QuoridorBoard {
        fn number_actions(&self) -> i16;
        fn new(mode: i16) -> Self;
        fn take_action(&mut self, action: i16);
        fn get_turn(&self) -> i16;
        fn is_over(&self) -> bool;
        fn get_available_actions_fast(&mut self) -> Vec<i16>;
        fn is_action_available(&mut self, action_number: i16) -> bool;
        fn get_valid_actions(&mut self, mode: i16) -> Vec<i16>;
        fn get_random_action(&mut self) -> i16 {
            let mut rng: ChaCha8Rng = ChaCha8Rng::from_entropy();
            let number_actions = self.number_actions();
            let mut action: i16 = rng.gen_range(0..number_actions);
            while !self.is_action_available(action) {
                action = rng.gen_range(0..number_actions);
            }
            action
        }
    }
}
