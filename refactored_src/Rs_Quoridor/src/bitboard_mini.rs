pub mod mini_bitboard_implementations {
    use crate::board::board::QuoridorBoard;
    use crate::VecDeque;
    use std::ops::*;
    pub const BITBOARD_SHIFT_ARR: [isize; 12] = [-18, 2, 18, -2, -36, -16, 4, 20, 36, 16, -4, -20];

    #[derive(Clone, Copy, PartialEq, Debug)]
    pub struct QuoridorBitboardMini {
        pub bitboard: u128,
    }
    #[derive(Clone, Copy, Debug)]
    pub struct RustPartialBitboardMini {
        pub p1: QuoridorBitboardMini,
        pub p2: QuoridorBitboardMini,
        pub walls: QuoridorBitboardMini,
        pub p1_walls_placed: i16,
        pub p2_walls_placed: i16,
        pub turn: i16,
        pub over: bool,
        pub mode: i16,
    }

    pub const BITBOARD_MINI_FULL: QuoridorBitboardMini = QuoridorBitboardMini {
        bitboard: 340282366920938463463374466694279856128,
    };
    pub const BITBOARD_MINI_BLANK: QuoridorBitboardMini = QuoridorBitboardMini { bitboard: 0 };
    pub const BITBOARD_MINI_NORTH_MASK: QuoridorBitboardMini = QuoridorBitboardMini {
        bitboard: 340282366920938463463302549837730283520,
    };
    pub const BITBOARD_MINI_EAST_MASK: QuoridorBitboardMini = QuoridorBitboardMini {
        bitboard: 169808226154284360436713285728065290240,
    };
    pub const BITBOARD_MINI_SOUTH_MASK: QuoridorBitboardMini = QuoridorBitboardMini {
        bitboard: 664613997892457936451762792651816960,
    };
    pub const BITBOARD_MINI_WEST_MASK: QuoridorBitboardMini = QuoridorBitboardMini {
        bitboard: 339616452308568720873426571456130580480,
    };

    pub trait BitboardMini: QuoridorBoard {
        fn undo_action(&mut self, action: i16);
        fn is_direction_valid(&self, board: QuoridorBitboardMini, direction: i16) -> bool;
        fn is_wall_valid(&self, wall_number: i16) -> bool;
        fn is_move_valid(&self, move_number: i16) -> bool;
        fn can_place_wall(&self) -> bool;
        fn is_action_available(&mut self, action_number: i16) -> bool {
            if action_number < 32 {
                if self.can_place_wall() && self.is_wall_valid(action_number) {
                    self.take_action(action_number);
                    let path_1: QuoridorBitboardMini = self.search(1);
                    let path_2: QuoridorBitboardMini = self.search(2);
                    self.undo_action(action_number);

                    if path_1 != BITBOARD_MINI_BLANK && path_2 != BITBOARD_MINI_BLANK {
                        return true;
                    }
                }
                false
            } else {
                return self.is_move_valid(action_number);
            }
        }
        fn get_available_actions_slow(&mut self) -> Vec<i16> {
            let mut available_actions: Vec<i16> = vec![];
            for action in 0..44 {
                if BitboardMini::is_action_available(self, action) {
                    available_actions.push(action);
                }
            }
            available_actions
        }

        fn get_pos(&self, player_number: i16) -> i16;
        fn get_walls(&self) -> QuoridorBitboardMini;
        fn search(&self, player_number: i16) -> QuoridorBitboardMini;
        fn display(&self) -> () {
            let mut output_board = String::new();
            let (mut north, mut east, mut south, mut west): (bool, bool, bool, bool);
            let mut pos: i16;
            let tmp_board: QuoridorBitboardMini = QuoridorBitboardMini { bitboard: 1 << 127 };
            for row in 0..5 {
                for col in 0..5 {
                    pos = row * 5 + col;
                    if self.get_pos(1) == pos {
                        output_board.push_str(" 1 ")
                    } else if self.get_pos(2) == pos {
                        output_board.push_str(" 2 ")
                    } else {
                        output_board.push_str("   ")
                    }

                    if col != 4 {
                        if self.is_direction_valid(tmp_board >> (row * 18 + col * 2) as isize, 1) {
                            output_board.push('\u{2502}')
                        } else {
                            output_board.push('\u{2503}')
                        }
                    }
                }
                output_board.push('\n');

                for col in 0..5 {
                    if row != 4 {
                        if self.is_direction_valid(tmp_board >> (row * 18 + col * 2) as isize, 2) {
                            output_board.push_str("\u{2500}\u{2500}\u{2500}")
                        } else {
                            output_board.push_str("\u{2501}\u{2501}\u{2501}")
                        }
                        if col != 4 {
                            north = !self
                                .is_direction_valid(tmp_board >> (row * 18 + col * 2) as isize, 1);
                            east = !self.is_direction_valid(
                                tmp_board >> (row * 18 + col * 2 + 2) as isize,
                                2,
                            );
                            south = !self.is_direction_valid(
                                tmp_board >> (row * 18 + 18 + col * 2) as isize,
                                1,
                            );
                            west = !self
                                .is_direction_valid(tmp_board >> (row * 18 + col * 2) as isize, 2);
                            if north == false && east == false && south == false && west == false {
                                output_board.push('\u{253c}')
                            } else if north == false
                                && east == false
                                && south == false
                                && west == true
                            {
                                output_board.push('\u{253d}')
                            } else if north == false
                                && east == true
                                && south == false
                                && west == false
                            {
                                output_board.push('\u{253e}')
                            } else if north == false
                                && east == true
                                && south == false
                                && west == true
                            {
                                output_board.push('\u{253f}')
                            } else if north == true
                                && east == false
                                && south == false
                                && west == false
                            {
                                output_board.push('\u{2540}')
                            } else if north == false
                                && east == false
                                && south == true
                                && west == false
                            {
                                output_board.push('\u{2541}')
                            } else if north == true
                                && east == false
                                && south == true
                                && west == false
                            {
                                output_board.push('\u{2542}')
                            } else if north == true
                                && east == false
                                && south == false
                                && west == true
                            {
                                output_board.push('\u{2543}')
                            } else if north == true
                                && east == true
                                && south == false
                                && west == false
                            {
                                output_board.push('\u{2544}')
                            } else if north == false
                                && east == false
                                && south == true
                                && west == true
                            {
                                output_board.push('\u{2545}')
                            } else if north == false
                                && east == true
                                && south == true
                                && west == false
                            {
                                output_board.push('\u{2546}')
                            } else if north == true
                                && east == true
                                && south == false
                                && west == true
                            {
                                output_board.push('\u{2547}')
                            } else if north == false
                                && east == true
                                && south == true
                                && west == true
                            {
                                output_board.push('\u{2548}')
                            } else if north == true
                                && east == false
                                && south == true
                                && west == true
                            {
                                output_board.push('\u{2549}')
                            } else if north == true
                                && east == true
                                && south == true
                                && west == false
                            {
                                output_board.push('\u{254A}')
                            } else if north == true && east == true && south == true && west == true
                            {
                                output_board.push('\u{254B}')
                            }
                        }
                    }
                }
                output_board.push('\n');
            }
            println!("{}", output_board);
        }
        fn bfs(
            &self,
            start_bitboard: QuoridorBitboardMini,
            player_number: i16,
        ) -> QuoridorBitboardMini {
            let mut frontier: VecDeque<QuoridorBitboardMini> = VecDeque::with_capacity(25);
            frontier.push_back(start_bitboard);

            let mut explored: QuoridorBitboardMini = QuoridorBitboardMini::new(0);

            let mut in_frontier: QuoridorBitboardMini = QuoridorBitboardMini::new(0);
            in_frontier += start_bitboard;

            let mut parent: [QuoridorBitboardMini; 25] = [BITBOARD_MINI_BLANK; 25];
            let mut bitboard: QuoridorBitboardMini;
            let mut new_bitboard: QuoridorBitboardMini;

            while frontier.len() != 0 {
                match frontier.pop_front() {
                    Some(popped) => {
                        bitboard = popped;
                        in_frontier -= bitboard;
                    }
                    None => panic!("EMPTY FRONTIER IN bfs"),
                }
                explored += bitboard;
                for direction in 0..4 {
                    new_bitboard = bitboard >> BITBOARD_SHIFT_ARR[direction];

                    if self.is_direction_valid(bitboard, direction as i16)
                        && explored & new_bitboard == BITBOARD_MINI_BLANK
                        && in_frontier & new_bitboard == BITBOARD_MINI_BLANK
                    {
                        parent[new_bitboard.hash()] = bitboard;

                        if (player_number == 1
                            && new_bitboard.bitboard >= 664613997892457936451903530140172288)
                            | (player_number == 2 && new_bitboard.bitboard <= 36028797018963968)
                        {
                            let mut stack: [QuoridorBitboardMini; 25] =
                                [QuoridorBitboardMini { bitboard: 0 }; 25];
                            stack[0] = new_bitboard;
                            let mut stack_idx: usize = 1;

                            let mut new_bitboard_idx: usize;

                            loop {
                                if parent[new_bitboard.hash()].hash() == 255 {
                                    break;
                                }
                                new_bitboard_idx = new_bitboard.hash();

                                stack[stack_idx] = parent[new_bitboard_idx];
                                stack_idx += 1;
                                new_bitboard = parent[new_bitboard_idx];
                            }

                            let mut path: QuoridorBitboardMini = BITBOARD_MINI_BLANK;
                            stack_idx -= 1;
                            loop {
                                path += stack[stack_idx];

                                if stack_idx != 0 {
                                    match stack[stack_idx - 1].hash() as isize
                                        - stack[stack_idx].hash() as isize
                                    {
                                        -5 => path += stack[stack_idx] >> -9,
                                        1 => path += stack[stack_idx] >> 1,
                                        5 => path += stack[stack_idx] >> 9,
                                        -1 => path += stack[stack_idx] >> -1,
                                        _ => {
                                            panic!("INVALID PARENT BITBOARD")
                                        }
                                    }
                                }
                                if stack_idx == 0 {
                                    return path;
                                }
                                stack_idx -= 1;
                            }
                        }
                        frontier.push_back(new_bitboard);
                        in_frontier += new_bitboard;
                    }
                }
            }
            return QuoridorBitboardMini { bitboard: 0 };
        }
    }
    impl QuoridorBitboardMini {
        pub fn new(mode: i16) -> QuoridorBitboardMini {
            if mode == 0 {
                QuoridorBitboardMini { bitboard: 0 }
            } else if mode == 1 {
                QuoridorBitboardMini {
                    bitboard: 2251799813685248,
                }
            } else if mode == 2 {
                QuoridorBitboardMini {
                    bitboard: 10633823966279326983230456482242756608,
                }
            } else {
                panic!("INVALID NEW BITBOARD")
            }
        }

        pub fn set_bit(&mut self, idx: usize) {
            if idx < 128 {
                self.bitboard |= 1 << (127 - idx);
            } else {
                panic!("ACCESSING INVALID INDEX")
            }
        }
        pub fn clear_bit(&mut self, idx: usize) {
            if idx < 128 {
                self.bitboard &= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF ^ 1 << (127 - idx);
            } else {
                panic!("ACCESSING INVALID INDEX")
            }
        }
        pub fn get_bit(&self, idx: usize) -> bool {
            if idx < 128 {
                return !((self.bitboard & 1 << (127 - idx)) == 0);
            } else {
                panic!("ACCESSING INVALID INDEX")
            }
        }
        pub fn display(&self) -> () {
            let mut displayboard: String = String::new();
            displayboard.push_str("_________\n");
            for row in 0..9 {
                for col in 0..9 {
                    if self.get_bit(row * 9 + col) {
                        displayboard.push('x')
                    } else {
                        displayboard.push(' ')
                    }
                }
                displayboard.push('\n');
            }
            displayboard.push_str("_________\n");

            println!("{}", displayboard);
        }
        pub fn hash(&self) -> usize {
            if self.bitboard != 0 {
                match self.bitboard {
                    170141183460469231731687303715884105728 => return 0,
                    42535295865117307932921825928971026432 => return 1,
                    10633823966279326983230456482242756608 => return 2,
                    2658455991569831745807614120560689152 => return 3,
                    664613997892457936451903530140172288 => return 4,
                    649037107316853453566312041152512 => return 5,
                    162259276829213363391578010288128 => return 6,
                    40564819207303340847894502572032 => return 7,
                    10141204801825835211973625643008 => return 8,
                    2535301200456458802993406410752 => return 9,
                    2475880078570760549798248448 => return 10,
                    618970019642690137449562112 => return 11,
                    154742504910672534362390528 => return 12,
                    38685626227668133590597632 => return 13,
                    9671406556917033397649408 => return 14,
                    9444732965739290427392 => return 15,
                    2361183241434822606848 => return 16,
                    590295810358705651712 => return 17,
                    147573952589676412928 => return 18,
                    36893488147419103232 => return 19,
                    36028797018963968 => return 20,
                    9007199254740992 => return 21,
                    2251799813685248 => return 22,
                    562949953421312 => return 23,
                    140737488355328 => return 24,
                    _ => {
                        println! {"{}", self.bitboard};
                        self.display();
                        panic!("BITBOARD WRONG")
                    }
                };
            }
            255
        }
    }

    impl QuoridorBoard for RustPartialBitboardMini {
        fn flip_turn(&mut self) {
            self.turn = 3 - self.turn
        }
        fn number_actions(&self) -> i16 {
            44
        }
        fn get_available_actions_fast(&mut self) -> Vec<i16> {
            let mut available_actions: Vec<i16> = vec![];
            if self.can_place_wall() {
                let mut path_available: bool = false;
                let mut previous_paths_1: Vec<QuoridorBitboardMini> = Vec::new();
                let mut previous_paths_2: Vec<QuoridorBitboardMini> = Vec::new();
                let mut path_1: QuoridorBitboardMini;
                let mut path_2: QuoridorBitboardMini;
                let mut path_traversed_1: bool;
                let mut path_traversed_2: bool;
                for action_number in 0..32 {
                    if self.is_wall_valid(action_number) {
                        if !path_available {
                            self.take_action(action_number);
                            path_1 = self.search(1);
                            path_2 = self.search(2);
                            if path_1 != BITBOARD_MINI_BLANK && path_2 != BITBOARD_MINI_BLANK {
                                previous_paths_1.push(path_1);
                                previous_paths_2.push(path_2);
                                available_actions.push(action_number);
                                path_available = true;
                            }
                            self.undo_action(action_number);
                        } else {
                            self.take_action(action_number);
                            path_traversed_1 = false;
                            for path in &previous_paths_1 {
                                if *path & self.get_walls() == BITBOARD_MINI_BLANK {
                                    path_traversed_1 = true;
                                    break;
                                }
                            }
                            path_traversed_2 = false;
                            for path in &previous_paths_2 {
                                if *path & self.get_walls() == BITBOARD_MINI_BLANK {
                                    path_traversed_2 = true;
                                    break;
                                }
                            }
                            if !path_traversed_1 | !path_traversed_2 {
                                if !path_traversed_1 {
                                    path_1 = self.search(1);
                                    if path_1 != BITBOARD_MINI_BLANK {
                                        previous_paths_1.push(path_1);
                                    }
                                } else {
                                    path_1 = previous_paths_1[0];
                                }
                                if !path_traversed_2 {
                                    path_2 = self.search(2);
                                    if path_2 != BITBOARD_MINI_BLANK {
                                        previous_paths_2.push(path_2)
                                    }
                                } else {
                                    path_2 = previous_paths_2[0];
                                }
                                if path_1 != BITBOARD_MINI_BLANK && path_2 != BITBOARD_MINI_BLANK {
                                    available_actions.push(action_number);
                                }
                            } else {
                                available_actions.push(action_number);
                            }
                            self.undo_action(action_number)
                        }
                    }
                }
            }
            for action_number in 32..44 {
                if self.is_move_valid(action_number) {
                    available_actions.push(action_number);
                }
            }

            available_actions
        }
        fn get_valid_actions(&mut self, mode: i16) -> Vec<i16> {
            if mode == 1 {
                RustPartialBitboardMini::get_available_actions_slow(self)
            } else if mode == 2 {
                RustPartialBitboardMini::get_available_actions_fast(self)
            } else {
                RustPartialBitboardMini::get_available_actions_fast(self)
            }
        }
        fn is_action_available(&mut self, action_number: i16) -> bool {
            BitboardMini::is_action_available(self, action_number)
        }
        fn new(mode: i16) -> RustPartialBitboardMini {
            RustPartialBitboardMini {
                p1: QuoridorBitboardMini::new(1),
                p2: QuoridorBitboardMini::new(2),
                walls: QuoridorBitboardMini::new(0),
                p1_walls_placed: 0,
                p2_walls_placed: 0,
                turn: 1,
                over: false,
                mode: mode,
            }
        }

        fn take_action(&mut self, action: i16) {
            if action < 32 {
                if action < 16 {
                    self.walls
                        .set_bit((9 + (action % 4) * 2 + 18 * (3 - action / 4)) as usize);
                    self.walls
                        .set_bit((9 + (action % 4) * 2 + 18 * (3 - action / 4) + 1) as usize);
                    self.walls
                        .set_bit((9 + (action % 4) * 2 + 18 * (3 - action / 4) + 2) as usize);
                } else {
                    self.walls
                        .set_bit(((action % 4) * 2 + 18 * (8 - action / 4) + 1) as usize);
                    self.walls
                        .set_bit(((action % 4) * 2 + 18 * (8 - action / 4) + 1 - 9) as usize);
                    self.walls
                        .set_bit(((action % 4) * 2 + 18 * (8 - action / 4) + 1 - 18) as usize);
                }

                if self.turn == 1 {
                    self.p1_walls_placed += 1;
                    self.turn = 2;
                } else {
                    self.p2_walls_placed += 1;
                    self.turn = 1;
                }
            } else {
                if self.turn == 1 {
                    self.p1 >>= BITBOARD_SHIFT_ARR[(action - 32) as usize];
                    if self.p1.hash() <= 4 {
                        self.over = true;
                    } else {
                        self.turn = 2;
                    }
                } else {
                    self.p2 >>= BITBOARD_SHIFT_ARR[(action - 32) as usize];
                    if self.p2.hash() >= 20 {
                        self.over = true;
                    } else {
                        self.turn = 1;
                    }
                }
            }
        }
        fn get_turn(&self) -> i16 {
            self.turn
        }

        fn is_over(&self) -> bool {
            self.over
        }
    }
    impl BitboardMini for RustPartialBitboardMini {
        fn undo_action(&mut self, action: i16) {
            if action < 32 {
                if action < 16 {
                    self.walls
                        .clear_bit((9 + (action % 4) * 2 + 18 * (3 - action / 4)) as usize);
                    self.walls
                        .clear_bit((9 + (action % 4) * 2 + 18 * (3 - action / 4) + 1) as usize);
                    self.walls
                        .clear_bit((9 + (action % 4) * 2 + 18 * (3 - action / 4) + 2) as usize);
                } else {
                    self.walls
                        .clear_bit(((action % 4) * 2 + 18 * (8 - action / 4) + 1) as usize);
                    self.walls
                        .clear_bit(((action % 4) * 2 + 18 * (8 - action / 4) + 1 - 9) as usize);
                    self.walls
                        .clear_bit(((action % 4) * 2 + 18 * (8 - action / 4) + 1 - 18) as usize);
                }

                if self.turn == 2 {
                    self.p1_walls_placed -= 1;
                    self.turn = 1;
                } else {
                    self.p2_walls_placed -= 1;
                    self.turn = 2;
                }
            }
        }
        fn is_direction_valid(&self, board: QuoridorBitboardMini, direction: i16) -> bool {
            if direction == 0 {
                (board >> -9 & self.walls == BITBOARD_MINI_BLANK)
                    && (board >> -9 & BITBOARD_MINI_NORTH_MASK & BITBOARD_MINI_FULL
                        != BITBOARD_MINI_BLANK)
            } else if direction == 1 {
                (board >> 1 & self.walls == BITBOARD_MINI_BLANK)
                    && (board >> 1 & BITBOARD_MINI_EAST_MASK & BITBOARD_MINI_FULL
                        != BITBOARD_MINI_BLANK)
            } else if direction == 2 {
                (board >> 9 & self.walls == BITBOARD_MINI_BLANK)
                    && (board >> 9 & BITBOARD_MINI_SOUTH_MASK & BITBOARD_MINI_FULL
                        != BITBOARD_MINI_BLANK)
            } else if direction == 3 {
                (board >> -1 & self.walls == BITBOARD_MINI_BLANK)
                    && (board >> -1 & BITBOARD_MINI_WEST_MASK & BITBOARD_MINI_FULL
                        != BITBOARD_MINI_BLANK)
            } else {
                panic!("INVALID DIRECTION")
            }
        }

        fn is_move_valid(&self, move_number: i16) -> bool {
            let in_turn_bitboard: QuoridorBitboardMini;
            let out_turn_bitboard: QuoridorBitboardMini;

            if self.turn == 1 {
                in_turn_bitboard = self.p1;
                out_turn_bitboard = self.p2;
            } else {
                in_turn_bitboard = self.p2;
                out_turn_bitboard = self.p1;
            }

            if move_number < 36 {
                return self.is_direction_valid(in_turn_bitboard, move_number - 32)
                    && in_turn_bitboard
                        >> BITBOARD_SHIFT_ARR[(move_number - 32) as usize] as isize
                        != out_turn_bitboard;
            } else {
                if move_number % 2 == 0 {
                    return self.is_direction_valid(in_turn_bitboard, (move_number - 36) / 2)
                        && in_turn_bitboard
                            >> BITBOARD_SHIFT_ARR[((move_number - 36) / 2) as usize] as isize
                            == out_turn_bitboard
                        && self.is_direction_valid(out_turn_bitboard, (move_number - 36) / 2);
                } else {
                    return (self
                        .is_direction_valid(in_turn_bitboard, ((move_number - 35) / 2) % 4)
                        && in_turn_bitboard
                            >> BITBOARD_SHIFT_ARR[(((move_number - 35) / 2) % 4) as usize]
                            == out_turn_bitboard
                        && !self
                            .is_direction_valid(out_turn_bitboard, ((move_number - 35) / 2) % 4)
                        && self
                            .is_direction_valid(out_turn_bitboard, ((move_number - 37) / 2) % 4))
                        | (self
                            .is_direction_valid(in_turn_bitboard, ((move_number - 37) / 2) % 4)
                            && in_turn_bitboard
                                >> BITBOARD_SHIFT_ARR[(((move_number - 37) / 2) % 4) as usize]
                                == out_turn_bitboard
                            && !self.is_direction_valid(
                                out_turn_bitboard,
                                ((move_number - 37) / 2) % 4,
                            )
                            && self.is_direction_valid(
                                out_turn_bitboard,
                                ((move_number - 35) / 2) % 4,
                            ));
                }
            }
        }

        fn is_wall_valid(&self, wall_number: i16) -> bool {
            let idx: usize;
            if wall_number < 16 {
                idx = (9 + (wall_number % 4) * 2 + 18 * (3 - wall_number / 4)) as usize;
                return self.walls.get_bit(idx as usize) == false
                    && self.walls.get_bit((idx + 1) as usize) == false
                    && self.walls.get_bit((idx + 2) as usize) == false;
            } else {
                idx = ((wall_number % 4) * 2 + 18 * (8 - wall_number / 4) + 1) as usize;
                return self.walls.get_bit(idx as usize) == false
                    && self.walls.get_bit((idx - 9) as usize) == false
                    && self.walls.get_bit((idx - 18) as usize) == false;
            }
        }

        fn can_place_wall(&self) -> bool {
            (self.turn == 1 && self.p1_walls_placed < 5)
                | (self.turn == 2 && self.p2_walls_placed < 5)
        }

        fn get_pos(&self, player_number: i16) -> i16 {
            if player_number == 1 {
                self.p1.hash() as i16
            } else {
                self.p2.hash() as i16
            }
        }

        fn get_walls(&self) -> QuoridorBitboardMini {
            self.walls
        }

        fn search(&self, player_number: i16) -> QuoridorBitboardMini {
            if self.mode == 1 {
                if player_number == 1 {
                    self.bfs(self.p1, 1)
                } else {
                    self.bfs(self.p2, 2)
                }
            } else {
                if player_number == 1 {
                    self.bfs(self.p1, 1)
                } else {
                    self.bfs(self.p2, 2)
                }
            }
        }
    }

    impl Add for QuoridorBitboardMini {
        type Output = Self;

        fn add(self, rhs: Self) -> Self {
            Self {
                bitboard: self.bitboard + rhs.bitboard,
            }
        }
    }
    impl AddAssign for QuoridorBitboardMini {
        fn add_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard: self.bitboard + rhs.bitboard,
            }
        }
    }
    impl Sub for QuoridorBitboardMini {
        type Output = Self;

        fn sub(self, rhs: Self) -> Self {
            Self {
                bitboard: self.bitboard - rhs.bitboard,
            }
        }
    }
    impl SubAssign for QuoridorBitboardMini {
        fn sub_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard: self.bitboard - rhs.bitboard,
            }
        }
    }
    impl BitAnd for QuoridorBitboardMini {
        type Output = Self;

        fn bitand(self, rhs: Self) -> Self {
            Self {
                bitboard: self.bitboard & rhs.bitboard,
            }
        }
    }
    impl BitAndAssign for QuoridorBitboardMini {
        fn bitand_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard: self.bitboard & rhs.bitboard,
            }
        }
    }
    impl BitOr for QuoridorBitboardMini {
        type Output = Self;

        fn bitor(self, rhs: Self) -> Self {
            Self {
                bitboard: self.bitboard | rhs.bitboard,
            }
        }
    }
    impl BitOrAssign for QuoridorBitboardMini {
        fn bitor_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard: self.bitboard | rhs.bitboard,
            }
        }
    }
    impl BitXor for QuoridorBitboardMini {
        type Output = Self;

        fn bitxor(self, rhs: Self) -> Self {
            Self {
                bitboard: self.bitboard ^ rhs.bitboard,
            }
        }
    }
    impl BitXorAssign for QuoridorBitboardMini {
        fn bitxor_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard: self.bitboard ^ rhs.bitboard,
            }
        }
    }
    impl Not for QuoridorBitboardMini {
        type Output = Self;

        fn not(self) -> Self::Output {
            Self {
                bitboard: !self.bitboard,
            }
        }
    }
    impl Shl<isize> for QuoridorBitboardMini {
        type Output = Self;
        fn shl(self, rhs: isize) -> Self::Output {
            if rhs < 0 {
                Self {
                    bitboard: self.bitboard,
                } >> -rhs
            } else if rhs == 0 {
                self
            } else if rhs < 128 {
                Self {
                    bitboard: self.bitboard << rhs,
                }
            } else {
                Self {
                    bitboard: self.bitboard,
                } << (rhs - 128)
            }
        }
    }
    impl ShlAssign<isize> for QuoridorBitboardMini {
        fn shl_assign(&mut self, rhs: isize) {
            if rhs < 0 {
                *self = Self {
                    bitboard: self.bitboard,
                } >> -rhs
            } else if rhs == 0 {
            } else if rhs < 128 {
                *self = Self {
                    bitboard: self.bitboard << rhs,
                }
            } else {
                *self = Self { bitboard: 0 } << (rhs - 128)
            }
        }
    }
    impl Shr<isize> for QuoridorBitboardMini {
        type Output = Self;
        fn shr(self, rhs: isize) -> Self::Output {
            if rhs < 0 {
                Self {
                    bitboard: self.bitboard,
                } << -rhs
            } else if rhs == 0 {
                self
            } else if rhs < 128 {
                Self {
                    bitboard: self.bitboard >> rhs,
                }
            } else {
                Self { bitboard: 0 } >> (rhs - 128)
            }
        }
    }
    impl ShrAssign<isize> for QuoridorBitboardMini {
        fn shr_assign(&mut self, rhs: isize) {
            if rhs < 0 {
                *self = Self {
                    bitboard: self.bitboard,
                } << -rhs
            } else if rhs == 0 {
            } else if rhs < 128 {
                *self = Self {
                    bitboard: self.bitboard >> rhs,
                }
            } else {
                *self = Self { bitboard: 0 } >> (rhs - 128)
            }
        }
    }
}
