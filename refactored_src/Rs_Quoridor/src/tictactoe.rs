pub mod tictactoe_implementation {
    use crate::board::board::QuoridorBoard;
    extern crate rand;
    extern crate rand_chacha;
    use core::num;

    use crate::rand::*;
    use rand_chacha::ChaCha8Rng;
    #[derive(Clone, Copy, Debug)]
    pub struct TicTacToe {
        pub positions: [i16; 9],
        pub over: bool,
        pub turn: i16,
    }

    impl QuoridorBoard for TicTacToe {
        fn flip_turn(&mut self) {
            self.turn = 3 - self.turn
        }
        fn number_actions(&self) -> i16 {
            9
        }
        fn new(mode: i16) -> TicTacToe {
            TicTacToe {
                positions: [0; 9],
                over: false,
                turn: 1,
            }
        }
        fn take_action(&mut self, action: i16) {
            self.positions[action as usize] = self.turn;

            if self.turn == 1 {
                if (self.positions[0] == 1 && self.positions[3] == 1 && self.positions[6] == 1)
                    | (self.positions[1] == 1 && self.positions[4] == 1 && self.positions[7] == 1)
                    | (self.positions[2] == 1 && self.positions[5] == 1 && self.positions[8] == 1)
                    | (self.positions[0] == 1 && self.positions[1] == 1 && self.positions[2] == 1)
                    | (self.positions[3] == 1 && self.positions[4] == 1 && self.positions[5] == 1)
                    | (self.positions[6] == 1 && self.positions[7] == 1 && self.positions[8] == 1)
                    | (self.positions[0] == 1 && self.positions[4] == 1 && self.positions[8] == 1)
                    | (self.positions[2] == 1 && self.positions[4] == 1 && self.positions[6] == 1)
                {
                    self.over = true;
                } else {
                    self.turn = 2
                }
            } else if self.turn == 2 {
                if (self.positions[0] == 2 && self.positions[3] == 2 && self.positions[6] == 2)
                    | (self.positions[1] == 2 && self.positions[4] == 2 && self.positions[7] == 2)
                    | (self.positions[2] == 2 && self.positions[5] == 2 && self.positions[8] == 2)
                    | (self.positions[0] == 2 && self.positions[1] == 2 && self.positions[2] == 2)
                    | (self.positions[3] == 2 && self.positions[4] == 2 && self.positions[5] == 2)
                    | (self.positions[6] == 2 && self.positions[7] == 2 && self.positions[8] == 2)
                    | (self.positions[0] == 2 && self.positions[4] == 2 && self.positions[8] == 2)
                    | (self.positions[2] == 2 && self.positions[4] == 2 && self.positions[6] == 2)
                {
                    self.over = true;
                } else {
                    self.turn = 1
                }
            }
            if !self.positions.contains(&0) {
                if self.over == false {
                    self.turn = -1;
                    self.over = true;
                }
            }
            // self.display();
        }
        fn get_turn(&self) -> i16 {
            self.turn
        }
        fn is_over(&self) -> bool {
            self.over
        }
        fn get_available_actions_fast(&mut self) -> Vec<i16> {
            let mut available_actions: Vec<i16> = vec![];
            for x in 0..9 {
                if self.positions[x] == 0 {
                    available_actions.push(x as i16);
                }
            }
            available_actions
        }
        fn is_action_available(&mut self, action_number: i16) -> bool {
            self.positions[action_number as usize] == 0
        }
        fn get_valid_actions(&mut self, mode: i16) -> Vec<i16> {
            self.get_available_actions_fast()
        }
    }
    impl TicTacToe {
        pub fn display(&self) {
            let mut output_board = String::new();
            for row in 0..3 {
                for col in 0..3 {
                    if self.positions[row * 3 + col] == 1 {
                        output_board.push_str(" X ")
                    } else if self.positions[row * 3 + col] == 2 {
                        output_board.push_str(" O ")
                    } else {
                        output_board.push_str("   ")
                    }
                    if col != 2 {
                        output_board.push('\u{2503}')
                    }
                }
                output_board.push('\n');
                if row != 2 {
                    output_board.push_str(
                        "\u{2501}\u{2501}\u{2501}\u{254B}\u{2501}\u{2501}\u{2501}\u{254B}\u{2501}\u{2501}\u{2501}\n",
                    )
                }
            }
            println!("{}", output_board);
        }
    }
}
