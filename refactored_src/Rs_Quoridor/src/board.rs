pub mod board {

    pub trait QuoridorBoard {
        fn new(mode: i16) -> Self;
        fn take_action(&mut self, action: i16);
        fn get_turn(&self) -> i16;
        fn is_over(&self) -> bool;
    }
}
