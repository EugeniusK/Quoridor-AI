pub mod bitboard_implementations {
    use crate::board::board::QuoridorBoard;
    use crate::util;
    use crate::VecDeque;
    use std::ops::*;

    pub use util::util::{find_idx, find_null, find_nulli16, min_idx};
    pub const BITBOARD_SHIFT_ARR: [isize; 12] = [-34, 2, 34, -2, -68, -32, 4, 36, 68, 32, -4, -36];

    #[derive(Clone, Copy, PartialEq, Eq, Debug)]
    pub struct QuoridorBitboard {
        // Bits in bitboard_0 are for index 0~63 and so on
        pub bitboard_0: u64,
        pub bitboard_1: u64,
        pub bitboard_2: u64,
        pub bitboard_3: u64,
        pub bitboard_4: u64,
    }
    #[derive(Clone, Copy, Debug)]

    pub struct RustPartialBitboard {
        pub p1: QuoridorBitboard,
        pub p2: QuoridorBitboard,
        pub walls: QuoridorBitboard,
        pub p1_walls_placed: i16,
        pub p2_walls_placed: i16,
        pub turn: i16,
        pub over: bool,
        pub mode: i16,
    }
    #[derive(Clone, Copy, Debug)]

    pub struct RustFullBitboard {
        pub p1: QuoridorBitboard,
        pub p2: QuoridorBitboard,
        pub walls_and_metadata: QuoridorBitboard,
    }

    // pub const RUST_PARTIAL_BITBOARD_BLANK: RustPartialBitboard = RustPartialBitboard {
    //     p1: BITBOARD_BLANK,
    //     p2: BITBOARD_BLANK,
    //     walls: BITBOARD_BLANK,
    //     p1_walls_placed: 0,
    //     p2_walls_placed: 0,
    //     turn: 1,
    //     over: false,
    //     mode: 1,
    // };
    // pub const RUST_FULL_BITBOARD_BLANK: RustFullBitboard = RustFullBitboard {
    //     p1: BITBOARD_BLANK,
    //     p2: BITBOARD_BLANK,
    //     walls_and_metadata: BITBOARD_BLANK,
    // };

    pub const BITBOARD_FULL: QuoridorBitboard = QuoridorBitboard {
        bitboard_0: 18446744073709551615,
        bitboard_1: 18446744073709551615,
        bitboard_2: 18446744073709551615,
        bitboard_3: 18446744073709551615,
        bitboard_4: 18446744071562067968,
    };

    pub const BITBOARD_BLANK: QuoridorBitboard = QuoridorBitboard {
        bitboard_0: 0,
        bitboard_1: 0,
        bitboard_2: 0,
        bitboard_3: 0,
        bitboard_4: 0,
    };
    pub const BITBOARD_NORTH_MASK: QuoridorBitboard = QuoridorBitboard {
        bitboard_0: 18446744073709551615,
        bitboard_1: 18446744073709551615,
        bitboard_2: 18446744073709551615,
        bitboard_3: 18446744073709551615,
        bitboard_4: 18446462598732840960,
    };
    pub const BITBOARD_EAST_MASK: QuoridorBitboard = QuoridorBitboard {
        bitboard_0: 9223301667573723135,
        bitboard_1: 17870278923326062335,
        bitboard_2: 18410715001810583535,
        bitboard_3: 18444492256715866110,
        bitboard_4: 18446603334073712640,
    };
    pub const BITBOARD_SOUTH_MASK: QuoridorBitboard = QuoridorBitboard {
        bitboard_0: 140737488355327,
        bitboard_1: 18446744073709551615,
        bitboard_2: 18446744073709551615,
        bitboard_3: 18446744073709551615,
        bitboard_4: 18446744071562067968,
    };
    pub const BITBOARD_WEST_MASK: QuoridorBitboard = QuoridorBitboard {
        bitboard_0: 18446603335147446271,
        bitboard_1: 17293813772942573055,
        bitboard_2: 18374685929911615455,
        bitboard_3: 18442240439722180605,
        bitboard_4: 18446462594437873664,
    };
    pub trait Bitboard: QuoridorBoard {
        fn undo_action(&mut self, action: i16);
        fn is_direction_valid(&self, board: QuoridorBitboard, direction: i16) -> bool;
        fn is_wall_valid(&self, wall_number: i16) -> bool;
        fn is_move_valid(&self, move_number: i16) -> bool;
        fn can_place_wall(&self) -> bool;
        fn is_action_available(&mut self, action_number: i16) -> bool {
            if action_number < 128 {
                if self.can_place_wall() && self.is_wall_valid(action_number) {
                    self.take_action(action_number);
                    let path_1: QuoridorBitboard = self.search(1);
                    let path_2: QuoridorBitboard = self.search(2);
                    self.undo_action(action_number);

                    if path_1 != BITBOARD_BLANK && path_2 != BITBOARD_BLANK {
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
            for action in 0..140 {
                if Bitboard::is_action_available(self, action) {
                    available_actions.push(action);
                }
            }
            available_actions
        }

        fn get_pos(&self, player_number: i16) -> i16;
        fn get_walls(&self) -> QuoridorBitboard;
        fn search(&self, player_number: i16) -> QuoridorBitboard;
        fn display(&self) -> () {
            let mut output_board = String::new();
            let (mut north, mut east, mut south, mut west): (bool, bool, bool, bool);
            let mut pos: i16;
            let tmp_board = QuoridorBitboard {
                bitboard_0: 1 << 63,
                bitboard_1: 0,
                bitboard_2: 0,
                bitboard_3: 0,
                bitboard_4: 0,
            };
            for row in 0..9 {
                for col in 0..9 {
                    pos = row * 9 + col;
                    if self.get_pos(1) == pos {
                        output_board.push_str(" 1 ")
                    } else if self.get_pos(2) == pos {
                        output_board.push_str(" 2 ")
                    } else {
                        output_board.push_str("   ")
                    }

                    if col != 8 {
                        if self.is_direction_valid(tmp_board >> (row * 34 + col * 2) as isize, 1) {
                            output_board.push('\u{2502}')
                        } else {
                            output_board.push('\u{2503}')
                        }
                    }
                }
                output_board.push('\n');
                for col in 0..9 {
                    if row != 8 {
                        if self.is_direction_valid(tmp_board >> (row * 34 + col * 2) as isize, 2) {
                            output_board.push_str("\u{2500}\u{2500}\u{2500}")
                        } else {
                            output_board.push_str("\u{2501}\u{2501}\u{2501}")
                        }
                        if col != 8 {
                            north = !self
                                .is_direction_valid(tmp_board >> (row * 34 + col * 2) as isize, 1);
                            east = !self.is_direction_valid(
                                tmp_board >> (row * 34 + col * 2 + 2) as isize,
                                2,
                            );
                            south = !self.is_direction_valid(
                                tmp_board >> (row * 34 + 34 + col * 2) as isize,
                                1,
                            );
                            west = !self
                                .is_direction_valid(tmp_board >> (row * 34 + col * 2) as isize, 2);
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
        fn bfs(&self, start_bitboard: QuoridorBitboard, player_number: i16) -> QuoridorBitboard {
            let mut frontier: [QuoridorBitboard; 81] = [BITBOARD_BLANK; 81];

            frontier[0] = start_bitboard;
            let mut head_pointer: usize = 0;
            let mut tail_pointer: usize = 1;

            let mut explored: QuoridorBitboard = QuoridorBitboard::new(0);

            let mut in_frontier: QuoridorBitboard = QuoridorBitboard::new(0);
            in_frontier += start_bitboard;

            let mut parent: [QuoridorBitboard; 81] = [BITBOARD_BLANK; 81];
            let mut bitboard: QuoridorBitboard;
            let mut new_bitboard: QuoridorBitboard;

            while head_pointer != tail_pointer {
                bitboard = frontier[head_pointer];
                head_pointer = (head_pointer + 1) % 81;
                in_frontier -= bitboard;
                explored += bitboard;
                for direction in 0..4 {
                    new_bitboard = bitboard >> BITBOARD_SHIFT_ARR[direction];

                    if self.is_direction_valid(bitboard, direction as i16)
                        && explored & new_bitboard == BITBOARD_BLANK
                        && in_frontier & new_bitboard == BITBOARD_BLANK
                    {
                        parent[new_bitboard.hash()] = bitboard;

                        if (player_number == 1 && new_bitboard.bitboard_0 >= 140737488355328)
                            | (player_number == 2
                                && new_bitboard.bitboard_4 >= 2147483648
                                && new_bitboard.bitboard_4 <= 140737488355328)
                        {
                            let mut stack: [QuoridorBitboard; 81] = [QuoridorBitboard {
                                bitboard_0: 0,
                                bitboard_1: 0,
                                bitboard_2: 0,
                                bitboard_3: 0,
                                bitboard_4: 0,
                            };
                                81];
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

                            let mut path: QuoridorBitboard = BITBOARD_BLANK;
                            stack_idx -= 1;
                            loop {
                                path += stack[stack_idx];

                                if stack_idx != 0 {
                                    match stack[stack_idx - 1].hash() as isize
                                        - stack[stack_idx].hash() as isize
                                    {
                                        -9 => path += stack[stack_idx] >> -17,
                                        1 => path += stack[stack_idx] >> 1,
                                        9 => path += stack[stack_idx] >> 17,
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
                        frontier[tail_pointer] = new_bitboard;
                        tail_pointer = (tail_pointer + 1) % 81;
                        in_frontier += new_bitboard;
                    }
                }
            }
            return QuoridorBitboard {
                bitboard_0: 0,
                bitboard_1: 0,
                bitboard_2: 0,
                bitboard_3: 0,
                bitboard_4: 0,
            };
        }
        fn dfs(&self, start_bitboard: QuoridorBitboard, player_number: i16) -> QuoridorBitboard {
            let mut frontier: [QuoridorBitboard; 81] = [BITBOARD_BLANK; 81];

            frontier[0] = start_bitboard;
            let mut tail_pointer: usize = 1;

            let mut explored: QuoridorBitboard = QuoridorBitboard::new(0);

            let mut in_frontier: QuoridorBitboard = QuoridorBitboard::new(0);
            in_frontier += start_bitboard;

            let mut parent: [QuoridorBitboard; 81] = [BITBOARD_BLANK; 81];
            let mut bitboard: QuoridorBitboard;
            let mut new_bitboard: QuoridorBitboard;

            while 0 != tail_pointer {
                bitboard = frontier[tail_pointer - 1];
                tail_pointer = (tail_pointer - 1) % 81;
                in_frontier -= bitboard;
                explored += bitboard;
                for direction in 0..4 {
                    new_bitboard = bitboard >> BITBOARD_SHIFT_ARR[direction];

                    if self.is_direction_valid(bitboard, direction as i16)
                        && explored & new_bitboard == BITBOARD_BLANK
                        && in_frontier & new_bitboard == BITBOARD_BLANK
                    {
                        parent[new_bitboard.hash()] = bitboard;

                        if (player_number == 1 && new_bitboard.bitboard_0 >= 140737488355328)
                            | (player_number == 2
                                && new_bitboard.bitboard_4 >= 2147483648
                                && new_bitboard.bitboard_4 <= 140737488355328)
                        {
                            let mut stack: [QuoridorBitboard; 81] = [QuoridorBitboard {
                                bitboard_0: 0,
                                bitboard_1: 0,
                                bitboard_2: 0,
                                bitboard_3: 0,
                                bitboard_4: 0,
                            };
                                81];
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

                            let mut path: QuoridorBitboard = BITBOARD_BLANK;
                            stack_idx -= 1;
                            loop {
                                path += stack[stack_idx];

                                if stack_idx != 0 {
                                    match stack[stack_idx - 1].hash() as isize
                                        - stack[stack_idx].hash() as isize
                                    {
                                        -9 => path += stack[stack_idx] >> -17,
                                        1 => path += stack[stack_idx] >> 1,
                                        9 => path += stack[stack_idx] >> 17,
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
                        frontier[tail_pointer] = new_bitboard;
                        tail_pointer = (tail_pointer + 1) % 81;
                        in_frontier += new_bitboard;
                    }
                }
            }
            return QuoridorBitboard {
                bitboard_0: 0,
                bitboard_1: 0,
                bitboard_2: 0,
                bitboard_3: 0,
                bitboard_4: 0,
            };
        }
        fn gbfs(&self, start_bitboard: QuoridorBitboard, player_number: i16) -> QuoridorBitboard {
            let mut frontier: [QuoridorBitboard; 81] = [BITBOARD_BLANK; 81];
            let mut heuristic: [usize; 81] = [255; 81];
            // use heuristic as a key to sort frontier
            frontier[0] = start_bitboard;
            heuristic[0] = {
                if player_number == 1 {
                    start_bitboard.hash() / 9
                } else {
                    8 - start_bitboard.hash() / 9
                }
            };

            let mut frontier_count = 1;

            let mut explored: QuoridorBitboard = QuoridorBitboard::new(0);

            let mut in_frontier: QuoridorBitboard = QuoridorBitboard::new(0);
            in_frontier += start_bitboard;

            let mut parent: [QuoridorBitboard; 81] = [BITBOARD_BLANK; 81];
            let mut bitboard: QuoridorBitboard;
            let mut new_bitboard: QuoridorBitboard;

            let mut heuristic_min_idx: usize;
            let mut heuristic_null_idx: usize;

            while frontier_count != 0 {
                heuristic_min_idx = min_idx(&heuristic);
                bitboard = frontier[heuristic_min_idx];
                heuristic[heuristic_min_idx] = 255;

                in_frontier -= bitboard;
                explored += bitboard;
                frontier_count -= 1;
                for direction in 0..4 {
                    new_bitboard = bitboard >> BITBOARD_SHIFT_ARR[direction];

                    if self.is_direction_valid(bitboard, direction as i16)
                        && explored & new_bitboard == BITBOARD_BLANK
                        && in_frontier & new_bitboard == BITBOARD_BLANK
                    {
                        parent[new_bitboard.hash()] = bitboard;

                        if (player_number == 1 && new_bitboard.bitboard_0 >= 140737488355328)
                            | (player_number == 2
                                && new_bitboard.bitboard_4 >= 2147483648
                                && new_bitboard.bitboard_4 <= 140737488355328)
                        {
                            let mut stack: [QuoridorBitboard; 81] = [QuoridorBitboard {
                                bitboard_0: 0,
                                bitboard_1: 0,
                                bitboard_2: 0,
                                bitboard_3: 0,
                                bitboard_4: 0,
                            };
                                81];
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

                            let mut path: QuoridorBitboard = BITBOARD_BLANK;
                            stack_idx -= 1;
                            loop {
                                path += stack[stack_idx];

                                if stack_idx != 0 {
                                    match stack[stack_idx - 1].hash() as isize
                                        - stack[stack_idx].hash() as isize
                                    {
                                        -9 => path += stack[stack_idx] >> -17,
                                        1 => path += stack[stack_idx] >> 1,
                                        9 => path += stack[stack_idx] >> 17,
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
                        heuristic_null_idx = find_null(&heuristic);

                        frontier[heuristic_null_idx] = new_bitboard;
                        heuristic[heuristic_null_idx] = {
                            if player_number == 1 {
                                start_bitboard.hash() / 9
                            } else {
                                8 - start_bitboard.hash() / 9
                            }
                        };
                        in_frontier += new_bitboard;
                        frontier_count += 1;
                    }
                }
            }
            return QuoridorBitboard {
                bitboard_0: 0,
                bitboard_1: 0,
                bitboard_2: 0,
                bitboard_3: 0,
                bitboard_4: 0,
            };
        }
        fn astar(&self, start_bitboard: QuoridorBitboard, player_number: i16) -> QuoridorBitboard {
            let mut frontier: [QuoridorBitboard; 81] = [BITBOARD_BLANK; 81];
            let mut frontier_hashes: [i16; 81] = [255; 81];

            let mut f_sum: [usize; 81] = [255; 81];
            // index 0 of f_sum is the lowest path_cost of position 0 and so on
            let mut path_cost: [usize; 81] = [255; 81];
            // index 0 of path_cost is the lowest path_cost of position 0 and so on
            frontier[0] = start_bitboard;
            frontier_hashes[0] = start_bitboard.hash() as i16;
            f_sum[start_bitboard.hash()] = 0 + {
                if player_number == 1 {
                    start_bitboard.hash() / 9
                } else {
                    8 - start_bitboard.hash() / 9
                }
            };
            path_cost[start_bitboard.hash()] = 0;

            let mut frontier_count = 1;

            let mut in_frontier: QuoridorBitboard = QuoridorBitboard::new(0);
            in_frontier += start_bitboard;

            let mut parent: [QuoridorBitboard; 81] = [BITBOARD_BLANK; 81];
            let mut bitboard: QuoridorBitboard;
            let mut new_bitboard: QuoridorBitboard;
            let mut popped_path_cost: usize;

            let mut f_null_idx: usize;
            let mut popped_idx: usize;

            let mut hashed: usize;
            while frontier_count != 0 {
                hashed = min_idx(&f_sum);
                popped_path_cost = path_cost[hashed];
                popped_idx = find_idx(&frontier_hashes, hashed as i16);
                bitboard = frontier[popped_idx];
                frontier[popped_idx] = BITBOARD_BLANK;
                frontier_hashes[popped_idx] = 255;

                f_sum[hashed] = 255;
                in_frontier -= bitboard;
                frontier_count -= 1;

                for direction in 0..4 {
                    new_bitboard = bitboard >> BITBOARD_SHIFT_ARR[direction];

                    if self.is_direction_valid(bitboard, direction as i16) {
                        if (player_number == 1 && new_bitboard.bitboard_0 >= 140737488355328)
                            | (player_number == 2
                                && new_bitboard.bitboard_4 >= 2147483648
                                && new_bitboard.bitboard_4 <= 140737488355328)
                        {
                            parent[new_bitboard.hash()] = bitboard;
                            let mut stack: [QuoridorBitboard; 81] = [QuoridorBitboard {
                                bitboard_0: 0,
                                bitboard_1: 0,
                                bitboard_2: 0,
                                bitboard_3: 0,
                                bitboard_4: 0,
                            };
                                81];
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

                            let mut path: QuoridorBitboard = BITBOARD_BLANK;
                            stack_idx -= 1;
                            loop {
                                path += stack[stack_idx];

                                if stack_idx != 0 {
                                    match stack[stack_idx - 1].hash() as isize
                                        - stack[stack_idx].hash() as isize
                                    {
                                        -9 => path += stack[stack_idx] >> -17,
                                        1 => path += stack[stack_idx] >> 1,
                                        9 => path += stack[stack_idx] >> 17,
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
                        hashed = new_bitboard.hash();
                        f_null_idx = find_nulli16(&frontier_hashes);
                        if popped_path_cost + 1 < path_cost[hashed] {
                            parent[hashed] = bitboard;
                            path_cost[hashed] = popped_path_cost + 1;
                            f_sum[hashed] = popped_path_cost + 1 + {
                                if player_number == 1 {
                                    (hashed / 9) as usize
                                } else {
                                    (8 - hashed / 9) as usize
                                }
                            };

                            if in_frontier & new_bitboard == BITBOARD_BLANK {
                                frontier[f_null_idx] = new_bitboard;
                                frontier_hashes[f_null_idx] = hashed as i16;
                                in_frontier += new_bitboard;
                                frontier_count += 1;
                            }
                        }
                    }
                }
            }
            return QuoridorBitboard {
                bitboard_0: 0,
                bitboard_1: 0,
                bitboard_2: 0,
                bitboard_3: 0,
                bitboard_4: 0,
            };
        }
    }

    impl QuoridorBitboard {
        pub fn new(mode: i16) -> QuoridorBitboard {
            if mode == 0 {
                QuoridorBitboard {
                    bitboard_0: 0,
                    bitboard_1: 0,
                    bitboard_2: 0,
                    bitboard_3: 0,
                    bitboard_4: 0,
                }
            } else if mode == 1 {
                QuoridorBitboard {
                    bitboard_0: 0,
                    bitboard_1: 0,
                    bitboard_2: 0,
                    bitboard_3: 0,
                    bitboard_4: 549755813888,
                }
            } else if mode == 2 {
                QuoridorBitboard {
                    bitboard_0: 36028797018963968,
                    bitboard_1: 0,
                    bitboard_2: 0,
                    bitboard_3: 0,
                    bitboard_4: 0,
                }
            } else {
                panic!("INVALID NEW BITBOARD")
            }
        }

        pub fn set_bit(&mut self, idx: usize) {
            if idx < 64 {
                self.bitboard_0 |= 1 << (63 - idx);
            } else if idx < 128 {
                self.bitboard_1 |= 1 << (127 - idx);
            } else if idx < 192 {
                self.bitboard_2 |= 1 << (191 - idx);
            } else if idx < 256 {
                self.bitboard_3 |= 1 << (255 - idx);
            } else if idx < 320 {
                self.bitboard_4 |= 1 << (319 - idx);
            } else {
                panic!("ACCESSING INVALID INDEX")
            }
        }
        pub fn clear_bit(&mut self, idx: usize) {
            if idx < 64 {
                self.bitboard_0 &= 0xFFFFFFFFFFFFFFFF ^ 1 << (63 - idx);
            } else if idx < 128 {
                self.bitboard_1 &= 0xFFFFFFFFFFFFFFFF ^ 1 << (127 - idx);
            } else if idx < 192 {
                self.bitboard_2 &= 0xFFFFFFFFFFFFFFFF ^ 1 << (191 - idx);
            } else if idx < 256 {
                self.bitboard_3 &= 0xFFFFFFFFFFFFFFFF ^ 1 << (255 - idx);
            } else if idx < 320 {
                self.bitboard_4 &= 0xFFFFFFFFFFFFFFFF ^ 1 << (319 - idx);
            } else {
                panic!("ACCESSING INVALID INDEX")
            }
        }
        pub fn get_bit(&self, idx: usize) -> bool {
            if idx < 64 {
                return !((self.bitboard_0 & 1 << (63 - idx)) == 0);
            } else if idx < 128 {
                return !((self.bitboard_1 & 1 << (127 - idx)) == 0);
            } else if idx < 192 {
                return !((self.bitboard_2 & 1 << (191 - idx)) == 0);
            } else if idx < 256 {
                return !((self.bitboard_3 & 1 << (255 - idx)) == 0);
            } else if idx < 320 {
                return !((self.bitboard_4 & 1 << (319 - idx)) == 0);
            } else {
                panic!("ACCESSING INVALID INDEX")
            }
        }
        pub fn display(&self) -> () {
            let mut displayboard: String = String::new();
            displayboard.push_str("_________________\n");
            for row in 0..17 {
                for col in 0..17 {
                    if self.get_bit(row * 17 + col) {
                        displayboard.push('x')
                    } else {
                        displayboard.push(' ')
                    }
                }
                displayboard.push('\n');
            }
            displayboard.push_str("_________________\n");

            println!("{}", displayboard);
        }
        pub fn hash(&self) -> usize {
            if self.bitboard_0 != 0
                && self.bitboard_1 != 0
                && self.bitboard_2 != 0
                && self.bitboard_3 != 0
                && self.bitboard_4 != 0
            {
                return 255;
            }
            if self.bitboard_0 != 0 {
                match self.bitboard_0 {
                    9223372036854775808 => return 0,
                    2305843009213693952 => return 1,
                    576460752303423488 => return 2,
                    144115188075855872 => return 3,
                    36028797018963968 => return 4,
                    9007199254740992 => return 5,
                    2251799813685248 => return 6,
                    562949953421312 => return 7,
                    140737488355328 => return 8,
                    536870912 => return 9,
                    134217728 => return 10,
                    33554432 => return 11,
                    8388608 => return 12,
                    2097152 => return 13,
                    524288 => return 14,
                    131072 => return 15,
                    32768 => return 16,
                    8192 => return 17,
                    _ => {
                        println! {"{}", self.bitboard_0};
                        panic!("BITBOARD 0 WRONG")
                    }
                };
            } else if self.bitboard_1 != 0 {
                match self.bitboard_1 {
                    576460752303423488 => return 18,
                    144115188075855872 => return 19,
                    36028797018963968 => return 20,
                    9007199254740992 => return 21,
                    2251799813685248 => return 22,
                    562949953421312 => return 23,
                    140737488355328 => return 24,
                    35184372088832 => return 25,
                    8796093022208 => return 26,
                    33554432 => return 27,
                    8388608 => return 28,
                    2097152 => return 29,
                    524288 => return 30,
                    131072 => return 31,
                    32768 => return 32,
                    8192 => return 33,
                    2048 => return 34,
                    512 => return 35,
                    _ => panic!("BITBOARD 1 WRONG"),
                };
            } else if self.bitboard_2 != 0 {
                match self.bitboard_2 {
                    36028797018963968 => return 36,
                    9007199254740992 => return 37,
                    2251799813685248 => return 38,
                    562949953421312 => return 39,
                    140737488355328 => return 40,
                    35184372088832 => return 41,
                    8796093022208 => return 42,
                    2199023255552 => return 43,
                    549755813888 => return 44,
                    2097152 => return 45,
                    524288 => return 46,
                    131072 => return 47,
                    32768 => return 48,
                    8192 => return 49,
                    2048 => return 50,
                    512 => return 51,
                    128 => return 52,
                    32 => return 53,
                    _ => panic!("BITBOARD 2 WRONG"),
                };
            } else if self.bitboard_3 != 0 {
                match self.bitboard_3 {
                    2251799813685248 => return 54,
                    562949953421312 => return 55,
                    140737488355328 => return 56,
                    35184372088832 => return 57,
                    8796093022208 => return 58,
                    2199023255552 => return 59,
                    549755813888 => return 60,
                    137438953472 => return 61,
                    34359738368 => return 62,
                    131072 => return 63,
                    32768 => return 64,
                    8192 => return 65,
                    2048 => return 66,
                    512 => return 67,
                    128 => return 68,
                    32 => return 69,
                    8 => return 70,
                    2 => return 71,
                    _ => panic!("BITBOARD 3 WRONG"),
                };
            } else if self.bitboard_4 != 0 {
                match self.bitboard_4 {
                    140737488355328 => return 72,
                    35184372088832 => return 73,
                    8796093022208 => return 74,
                    2199023255552 => return 75,
                    549755813888 => return 76,
                    137438953472 => return 77,
                    34359738368 => return 78,
                    8589934592 => return 79,
                    2147483648 => return 80,
                    _ => panic!("BITBOARD 4 WRONG"),
                };
            }
            255
        }
    }

    impl RustFullBitboard {
        fn get_turn(&self) -> i16 {
            (self.walls_and_metadata.bitboard_4 as i16 & 1) + 1
        }

        fn change_turn(&mut self) {
            self.walls_and_metadata.bitboard_4 ^= 1;
        }

        pub fn get_walls_left(&self, player_number: i16) -> i16 {
            if player_number == 1 {
                ((self.walls_and_metadata.bitboard_4 >> 1) & 0x000000000000000F) as i16
            } else {
                ((self.walls_and_metadata.bitboard_4 >> 5) & 0x000000000000000F) as i16
            }
        }

        pub fn add_walls(&mut self, player_number: i16) {
            if player_number == 1 {
                self.walls_and_metadata.bitboard_4 = (self.walls_and_metadata.bitboard_4
                    & 0xFFFFFFFFFFFFFFE1)
                    | (((self.walls_and_metadata.bitboard_4 >> 1) & 0x000000000000000F) + 1) << 1
            } else {
                self.walls_and_metadata.bitboard_4 = (self.walls_and_metadata.bitboard_4
                    & 0xFFFFFFFFFFFFFE1F)
                    | (((self.walls_and_metadata.bitboard_4 >> 5) & 0x000000000000000F) + 1) << 5
            }
        }

        pub fn subtract_walls(&mut self, player_number: i16) {
            if player_number == 1 {
                self.walls_and_metadata.bitboard_4 = (self.walls_and_metadata.bitboard_4
                    & 0xFFFFFFFFFFFFFFE1)
                    | (((self.walls_and_metadata.bitboard_4 >> 1) & 0x000000000000000F) - 1) << 1
            } else {
                self.walls_and_metadata.bitboard_4 = (self.walls_and_metadata.bitboard_4
                    & 0xFFFFFFFFFFFFFE1F)
                    | (((self.walls_and_metadata.bitboard_4 >> 5) & 0x000000000000000F) - 1) << 5
            }
        }
        fn get_over(&self) -> bool {
            (self.walls_and_metadata.bitboard_4 >> 9) & 1 == 1
        }
        fn set_over(&mut self) {
            self.walls_and_metadata.bitboard_4 |= 0x0000000000000200;
        }

        fn get_mode(&self) -> i16 {
            ((self.walls_and_metadata.bitboard_4 >> 10) & 0x000000000000000F) as i16
        }
    }

    impl QuoridorBoard for RustFullBitboard {
        fn number_actions(&self) -> i16 {
            140
        }
        fn get_available_actions_fast(&mut self) -> Vec<i16> {
            let mut available_actions: Vec<i16> = vec![];
            if self.can_place_wall() {
                let mut path_available: bool = false;
                let mut previous_paths_1: Vec<QuoridorBitboard> = Vec::new();
                let mut previous_paths_2: Vec<QuoridorBitboard> = Vec::new();
                let mut path_1: QuoridorBitboard;
                let mut path_2: QuoridorBitboard;
                let mut path_traversed_1: bool;
                let mut path_traversed_2: bool;
                for action_number in 0..128 {
                    if self.is_wall_valid(action_number) {
                        if !path_available {
                            self.take_action(action_number);
                            path_1 = self.search(1);
                            path_2 = self.search(2);
                            if path_1 != BITBOARD_BLANK && path_2 != BITBOARD_BLANK {
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
                                if *path & self.get_walls() == BITBOARD_BLANK {
                                    path_traversed_1 = true;
                                    break;
                                }
                            }
                            path_traversed_2 = false;
                            for path in &previous_paths_2 {
                                if *path & self.get_walls() == BITBOARD_BLANK {
                                    path_traversed_2 = true;
                                    break;
                                }
                            }
                            if !path_traversed_1 | !path_traversed_2 {
                                if !path_traversed_1 {
                                    path_1 = self.search(1);
                                    if path_1 != BITBOARD_BLANK {
                                        previous_paths_1.push(path_1);
                                    }
                                } else {
                                    path_1 = previous_paths_1[0];
                                }
                                if !path_traversed_2 {
                                    path_2 = self.search(2);
                                    if path_2 != BITBOARD_BLANK {
                                        previous_paths_2.push(path_2)
                                    }
                                } else {
                                    path_2 = previous_paths_2[0];
                                }
                                if path_1 != BITBOARD_BLANK && path_2 != BITBOARD_BLANK {
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
            for action_number in 128..140 {
                if self.is_move_valid(action_number) {
                    available_actions.push(action_number);
                }
            }

            available_actions
        }
        fn get_valid_actions(&mut self, mode: i16) -> Vec<i16> {
            if mode == 1 {
                RustFullBitboard::get_available_actions_slow(self)
            } else if mode == 2 {
                RustFullBitboard::get_available_actions_fast(self)
            } else {
                RustFullBitboard::get_available_actions_fast(self)
            }
        }
        fn is_action_available(&mut self, action_number: i16) -> bool {
            Bitboard::is_action_available(self, action_number)
        }
        fn new(mode: i16) -> RustFullBitboard {
            let mut board = RustFullBitboard {
                p1: QuoridorBitboard::new(1),
                p2: QuoridorBitboard::new(2),
                walls_and_metadata: QuoridorBitboard::new(0),
            };
            board.walls_and_metadata.bitboard_4 = (mode as u64) << 10;
            board
        }
        fn take_action(&mut self, action: i16) {
            if action < 128 {
                if action < 64 {
                    self.walls_and_metadata
                        .set_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8)) as usize);
                    self.walls_and_metadata
                        .set_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8) + 1) as usize);
                    self.walls_and_metadata
                        .set_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8) + 2) as usize);
                } else {
                    self.walls_and_metadata
                        .set_bit(((action % 8) * 2 + 34 * (16 - action / 8) + 1) as usize);
                    self.walls_and_metadata
                        .set_bit(((action % 8) * 2 + 34 * (16 - action / 8) - 16) as usize);
                    self.walls_and_metadata
                        .set_bit(((action % 8) * 2 + 34 * (16 - action / 8) - 33) as usize);
                }

                if self.get_turn() == 1 {
                    self.add_walls(1);
                    self.change_turn();
                } else {
                    self.add_walls(2);
                    self.change_turn();
                }
            } else {
                if self.get_turn() == 1 {
                    self.p1 >>= BITBOARD_SHIFT_ARR[(action - 128) as usize];
                    if self.p1.hash() <= 8 {
                        self.set_over();
                    } else {
                        self.change_turn();
                    }
                } else {
                    self.p2 >>= BITBOARD_SHIFT_ARR[(action - 128) as usize];
                    if self.p2.hash() >= 72 {
                        self.set_over();
                    } else {
                        self.change_turn();
                    }
                }
            }
        }
        fn get_turn(&self) -> i16 {
            self.get_turn()
        }
        fn is_over(&self) -> bool {
            self.get_over()
        }
    }
    impl Bitboard for RustFullBitboard {
        fn undo_action(&mut self, action: i16) {
            if action < 128 {
                if action < 64 {
                    self.walls_and_metadata
                        .clear_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8)) as usize);
                    self.walls_and_metadata
                        .clear_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8) + 1) as usize);
                    self.walls_and_metadata
                        .clear_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8) + 2) as usize);
                } else {
                    self.walls_and_metadata
                        .clear_bit(((action % 8) * 2 + 34 * (16 - action / 8) + 1) as usize);
                    self.walls_and_metadata
                        .clear_bit(((action % 8) * 2 + 34 * (16 - action / 8) - 16) as usize);
                    self.walls_and_metadata
                        .clear_bit(((action % 8) * 2 + 34 * (16 - action / 8) - 33) as usize);
                }

                if self.get_turn() == 2 {
                    self.subtract_walls(1);
                    self.change_turn();
                } else {
                    self.subtract_walls(2);
                    self.change_turn();
                }
            }
        }
        fn is_direction_valid(&self, board: QuoridorBitboard, direction: i16) -> bool {
            if direction == 0 {
                (board >> -17 & self.walls_and_metadata == BITBOARD_BLANK)
                    && (board >> -17 & BITBOARD_NORTH_MASK & BITBOARD_FULL != BITBOARD_BLANK)
            } else if direction == 1 {
                (board >> 1 & self.walls_and_metadata == BITBOARD_BLANK)
                    && (board >> 1 & BITBOARD_EAST_MASK & BITBOARD_FULL != BITBOARD_BLANK)
            } else if direction == 2 {
                (board >> 17 & self.walls_and_metadata == BITBOARD_BLANK)
                    && (board >> 17 & BITBOARD_SOUTH_MASK & BITBOARD_FULL != BITBOARD_BLANK)
            } else if direction == 3 {
                (board >> -1 & self.walls_and_metadata == BITBOARD_BLANK)
                    && (board >> -1 & BITBOARD_WEST_MASK & BITBOARD_FULL != BITBOARD_BLANK)
            } else {
                panic!("INVALID DIRECTION")
            }
        }

        fn is_move_valid(&self, move_number: i16) -> bool {
            let in_turn_bitboard: QuoridorBitboard;
            let out_turn_bitboard: QuoridorBitboard;

            if self.get_turn() == 1 {
                in_turn_bitboard = self.p1;
                out_turn_bitboard = self.p2;
            } else {
                in_turn_bitboard = self.p2;
                out_turn_bitboard = self.p1;
            }

            if move_number < 132 {
                return self.is_direction_valid(in_turn_bitboard, move_number - 128)
                    && in_turn_bitboard
                        >> BITBOARD_SHIFT_ARR[(move_number - 128) as usize] as isize
                        != out_turn_bitboard;
            } else {
                if move_number % 2 == 0 {
                    return self.is_direction_valid(in_turn_bitboard, (move_number - 132) / 2)
                        && in_turn_bitboard
                            >> BITBOARD_SHIFT_ARR[((move_number - 132) / 2) as usize] as isize
                            == out_turn_bitboard
                        && self.is_direction_valid(out_turn_bitboard, (move_number - 132) / 2);
                } else {
                    return (self
                        .is_direction_valid(in_turn_bitboard, ((move_number - 131) / 2) % 4)
                        && in_turn_bitboard
                            >> BITBOARD_SHIFT_ARR[(((move_number - 131) / 2) % 4) as usize]
                            == out_turn_bitboard
                        && !self
                            .is_direction_valid(out_turn_bitboard, ((move_number - 131) / 2) % 4)
                        && self
                            .is_direction_valid(out_turn_bitboard, ((move_number - 133) / 2) % 4))
                        | (self
                            .is_direction_valid(in_turn_bitboard, ((move_number - 133) / 2) % 4)
                            && in_turn_bitboard
                                >> BITBOARD_SHIFT_ARR[(((move_number - 133) / 2) % 4) as usize]
                                == out_turn_bitboard
                            && !self.is_direction_valid(
                                out_turn_bitboard,
                                ((move_number - 133) / 2) % 4,
                            )
                            && self.is_direction_valid(
                                out_turn_bitboard,
                                ((move_number - 131) / 2) % 4,
                            ));
                }
            }
        }

        fn is_wall_valid(&self, wall_number: i16) -> bool {
            let idx: usize;
            if wall_number < 64 {
                idx = (17 + (wall_number % 8) * 2 + 34 * (7 - wall_number / 8)) as usize;
                return self.walls_and_metadata.get_bit(idx as usize) == false
                    && self.walls_and_metadata.get_bit((idx + 1) as usize) == false
                    && self.walls_and_metadata.get_bit((idx + 2) as usize) == false;
            } else {
                idx = ((wall_number % 8) * 2 + 34 * (16 - wall_number / 8) + 1) as usize;
                return self.walls_and_metadata.get_bit(idx as usize) == false
                    && self.walls_and_metadata.get_bit((idx - 17) as usize) == false
                    && self.walls_and_metadata.get_bit((idx - 34) as usize) == false;
            }
        }

        fn can_place_wall(&self) -> bool {
            (self.get_turn() == 1 && self.get_walls_left(1) < 10)
                | (self.get_turn() == 2 && self.get_walls_left(2) < 10)
        }

        fn get_pos(&self, player_number: i16) -> i16 {
            if player_number == 1 {
                self.p1.hash() as i16
            } else {
                self.p2.hash() as i16
            }
        }
        fn get_walls(&self) -> QuoridorBitboard {
            self.walls_and_metadata
        }

        fn search(&self, player_number: i16) -> QuoridorBitboard {
            if self.get_mode() == 1 {
                if player_number == 1 {
                    self.bfs(self.p1, 1)
                } else {
                    self.bfs(self.p2, 2)
                }
            } else if self.get_mode() == 2 {
                if player_number == 1 {
                    self.dfs(self.p1, 1)
                } else {
                    self.dfs(self.p2, 2)
                }
            } else if self.get_mode() == 3 {
                if player_number == 1 {
                    self.gbfs(self.p1, 1)
                } else {
                    self.gbfs(self.p2, 2)
                }
            } else if self.get_mode() == 4 {
                if player_number == 1 {
                    self.astar(self.p1, 1)
                } else {
                    self.astar(self.p2, 2)
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
    impl QuoridorBoard for RustPartialBitboard {
        fn number_actions(&self) -> i16 {
            140
        }
        fn get_available_actions_fast(&mut self) -> Vec<i16> {
            let mut available_actions: Vec<i16> = vec![];
            if self.can_place_wall() {
                let mut path_available: bool = false;
                let mut previous_paths_1: Vec<QuoridorBitboard> = Vec::new();
                let mut previous_paths_2: Vec<QuoridorBitboard> = Vec::new();
                let mut path_1: QuoridorBitboard;
                let mut path_2: QuoridorBitboard;
                let mut path_traversed_1: bool;
                let mut path_traversed_2: bool;
                for action_number in 0..128 {
                    if self.is_wall_valid(action_number) {
                        if !path_available {
                            self.take_action(action_number);
                            path_1 = self.search(1);
                            path_2 = self.search(2);
                            if path_1 != BITBOARD_BLANK && path_2 != BITBOARD_BLANK {
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
                                if *path & self.get_walls() == BITBOARD_BLANK {
                                    path_traversed_1 = true;
                                    break;
                                }
                            }
                            path_traversed_2 = false;
                            for path in &previous_paths_2 {
                                if *path & self.get_walls() == BITBOARD_BLANK {
                                    path_traversed_2 = true;
                                    break;
                                }
                            }
                            if !path_traversed_1 | !path_traversed_2 {
                                if !path_traversed_1 {
                                    path_1 = self.search(1);
                                    if path_1 != BITBOARD_BLANK {
                                        previous_paths_1.push(path_1);
                                    }
                                } else {
                                    path_1 = previous_paths_1[0];
                                }
                                if !path_traversed_2 {
                                    path_2 = self.search(2);
                                    if path_2 != BITBOARD_BLANK {
                                        previous_paths_2.push(path_2)
                                    }
                                } else {
                                    path_2 = previous_paths_2[0];
                                }
                                if path_1 != BITBOARD_BLANK && path_2 != BITBOARD_BLANK {
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
            for action_number in 128..140 {
                if self.is_move_valid(action_number) {
                    available_actions.push(action_number);
                }
            }

            available_actions
        }
        fn get_valid_actions(&mut self, mode: i16) -> Vec<i16> {
            if mode == 1 {
                RustPartialBitboard::get_available_actions_slow(self)
            } else if mode == 2 {
                RustPartialBitboard::get_available_actions_fast(self)
            } else {
                RustPartialBitboard::get_available_actions_fast(self)
            }
        }
        fn is_action_available(&mut self, action_number: i16) -> bool {
            Bitboard::is_action_available(self, action_number)
        }
        fn new(mode: i16) -> RustPartialBitboard {
            RustPartialBitboard {
                p1: QuoridorBitboard::new(1),
                p2: QuoridorBitboard::new(2),
                walls: QuoridorBitboard::new(0),
                p1_walls_placed: 0,
                p2_walls_placed: 0,
                turn: 1,
                over: false,
                mode: mode,
            }
        }

        fn take_action(&mut self, action: i16) {
            if action < 128 {
                if action < 64 {
                    self.walls
                        .set_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8)) as usize);
                    self.walls
                        .set_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8) + 1) as usize);
                    self.walls
                        .set_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8) + 2) as usize);
                } else {
                    self.walls
                        .set_bit(((action % 8) * 2 + 34 * (16 - action / 8) + 1) as usize);
                    self.walls
                        .set_bit(((action % 8) * 2 + 34 * (16 - action / 8) - 16) as usize);
                    self.walls
                        .set_bit(((action % 8) * 2 + 34 * (16 - action / 8) - 33) as usize);
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
                    self.p1 >>= BITBOARD_SHIFT_ARR[(action - 128) as usize];
                    if self.p1.hash() <= 8 {
                        self.over = true;
                    } else {
                        self.turn = 2;
                    }
                } else {
                    self.p2 >>= BITBOARD_SHIFT_ARR[(action - 128) as usize];
                    if self.p2.hash() >= 72 {
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
    impl Bitboard for RustPartialBitboard {
        fn undo_action(&mut self, action: i16) {
            if action < 128 {
                if action < 64 {
                    self.walls
                        .clear_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8)) as usize);
                    self.walls
                        .clear_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8) + 1) as usize);
                    self.walls
                        .clear_bit((17 + (action % 8) * 2 + 34 * (7 - action / 8) + 2) as usize);
                } else {
                    self.walls
                        .clear_bit(((action % 8) * 2 + 34 * (16 - action / 8) + 1) as usize);
                    self.walls
                        .clear_bit(((action % 8) * 2 + 34 * (16 - action / 8) - 16) as usize);
                    self.walls
                        .clear_bit(((action % 8) * 2 + 34 * (16 - action / 8) - 33) as usize);
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
        fn is_direction_valid(&self, board: QuoridorBitboard, direction: i16) -> bool {
            if direction == 0 {
                (board >> -17 & self.walls == BITBOARD_BLANK)
                    && (board >> -17 & BITBOARD_NORTH_MASK & BITBOARD_FULL != BITBOARD_BLANK)
            } else if direction == 1 {
                (board >> 1 & self.walls == BITBOARD_BLANK)
                    && (board >> 1 & BITBOARD_EAST_MASK & BITBOARD_FULL != BITBOARD_BLANK)
            } else if direction == 2 {
                (board >> 17 & self.walls == BITBOARD_BLANK)
                    && (board >> 17 & BITBOARD_SOUTH_MASK & BITBOARD_FULL != BITBOARD_BLANK)
            } else if direction == 3 {
                (board >> -1 & self.walls == BITBOARD_BLANK)
                    && (board >> -1 & BITBOARD_WEST_MASK & BITBOARD_FULL != BITBOARD_BLANK)
            } else {
                panic!("INVALID DIRECTION")
            }
        }

        fn is_move_valid(&self, move_number: i16) -> bool {
            let in_turn_bitboard: QuoridorBitboard;
            let out_turn_bitboard: QuoridorBitboard;

            if self.turn == 1 {
                in_turn_bitboard = self.p1;
                out_turn_bitboard = self.p2;
            } else {
                in_turn_bitboard = self.p2;
                out_turn_bitboard = self.p1;
            }

            if move_number < 132 {
                return self.is_direction_valid(in_turn_bitboard, move_number - 128)
                    && in_turn_bitboard
                        >> BITBOARD_SHIFT_ARR[(move_number - 128) as usize] as isize
                        != out_turn_bitboard;
            } else {
                if move_number % 2 == 0 {
                    return self.is_direction_valid(in_turn_bitboard, (move_number - 132) / 2)
                        && in_turn_bitboard
                            >> BITBOARD_SHIFT_ARR[((move_number - 132) / 2) as usize] as isize
                            == out_turn_bitboard
                        && self.is_direction_valid(out_turn_bitboard, (move_number - 132) / 2);
                } else {
                    return (self
                        .is_direction_valid(in_turn_bitboard, ((move_number - 131) / 2) % 4)
                        && in_turn_bitboard
                            >> BITBOARD_SHIFT_ARR[(((move_number - 131) / 2) % 4) as usize]
                            == out_turn_bitboard
                        && !self
                            .is_direction_valid(out_turn_bitboard, ((move_number - 131) / 2) % 4)
                        && self
                            .is_direction_valid(out_turn_bitboard, ((move_number - 133) / 2) % 4))
                        | (self
                            .is_direction_valid(in_turn_bitboard, ((move_number - 133) / 2) % 4)
                            && in_turn_bitboard
                                >> BITBOARD_SHIFT_ARR[(((move_number - 133) / 2) % 4) as usize]
                                == out_turn_bitboard
                            && !self.is_direction_valid(
                                out_turn_bitboard,
                                ((move_number - 133) / 2) % 4,
                            )
                            && self.is_direction_valid(
                                out_turn_bitboard,
                                ((move_number - 131) / 2) % 4,
                            ));
                }
            }
        }

        fn is_wall_valid(&self, wall_number: i16) -> bool {
            let idx: usize;
            if wall_number < 64 {
                idx = (17 + (wall_number % 8) * 2 + 34 * (7 - wall_number / 8)) as usize;
                return self.walls.get_bit(idx as usize) == false
                    && self.walls.get_bit((idx + 1) as usize) == false
                    && self.walls.get_bit((idx + 2) as usize) == false;
            } else {
                idx = ((wall_number % 8) * 2 + 34 * (16 - wall_number / 8) + 1) as usize;
                return self.walls.get_bit(idx as usize) == false
                    && self.walls.get_bit((idx - 17) as usize) == false
                    && self.walls.get_bit((idx - 34) as usize) == false;
            }
        }

        fn can_place_wall(&self) -> bool {
            (self.turn == 1 && self.p1_walls_placed < 10)
                | (self.turn == 2 && self.p2_walls_placed < 10)
        }

        fn get_pos(&self, player_number: i16) -> i16 {
            if player_number == 1 {
                self.p1.hash() as i16
            } else {
                self.p2.hash() as i16
            }
        }

        fn get_walls(&self) -> QuoridorBitboard {
            self.walls
        }

        fn search(&self, player_number: i16) -> QuoridorBitboard {
            if self.mode == 1 {
                if player_number == 1 {
                    self.bfs(self.p1, 1)
                } else {
                    self.bfs(self.p2, 2)
                }
            } else if self.mode == 2 {
                if player_number == 1 {
                    self.dfs(self.p1, 1)
                } else {
                    self.dfs(self.p2, 2)
                }
            } else if self.mode == 3 {
                if player_number == 1 {
                    self.gbfs(self.p1, 1)
                } else {
                    self.gbfs(self.p2, 2)
                }
            } else if self.mode == 4 {
                if player_number == 1 {
                    self.astar(self.p1, 1)
                } else {
                    self.astar(self.p2, 2)
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

    impl Add for QuoridorBitboard {
        type Output = Self;

        fn add(self, rhs: Self) -> Self {
            Self {
                bitboard_0: self.bitboard_0 + rhs.bitboard_0,
                bitboard_1: self.bitboard_1 + rhs.bitboard_1,
                bitboard_2: self.bitboard_2 + rhs.bitboard_2,
                bitboard_3: self.bitboard_3 + rhs.bitboard_3,
                bitboard_4: self.bitboard_4 + rhs.bitboard_4,
            }
        }
    }
    impl AddAssign for QuoridorBitboard {
        fn add_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard_0: self.bitboard_0 + rhs.bitboard_0,
                bitboard_1: self.bitboard_1 + rhs.bitboard_1,
                bitboard_2: self.bitboard_2 + rhs.bitboard_2,
                bitboard_3: self.bitboard_3 + rhs.bitboard_3,
                bitboard_4: self.bitboard_4 + rhs.bitboard_4,
            }
        }
    }
    impl Sub for QuoridorBitboard {
        type Output = Self;

        fn sub(self, rhs: Self) -> Self {
            Self {
                bitboard_0: self.bitboard_0 - rhs.bitboard_0,
                bitboard_1: self.bitboard_1 - rhs.bitboard_1,
                bitboard_2: self.bitboard_2 - rhs.bitboard_2,
                bitboard_3: self.bitboard_3 - rhs.bitboard_3,
                bitboard_4: self.bitboard_4 - rhs.bitboard_4,
            }
        }
    }
    impl SubAssign for QuoridorBitboard {
        fn sub_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard_0: self.bitboard_0 - rhs.bitboard_0,
                bitboard_1: self.bitboard_1 - rhs.bitboard_1,
                bitboard_2: self.bitboard_2 - rhs.bitboard_2,
                bitboard_3: self.bitboard_3 - rhs.bitboard_3,
                bitboard_4: self.bitboard_4 - rhs.bitboard_4,
            }
        }
    }
    impl BitAnd for QuoridorBitboard {
        type Output = Self;

        fn bitand(self, rhs: Self) -> Self {
            Self {
                bitboard_0: self.bitboard_0 & rhs.bitboard_0,
                bitboard_1: self.bitboard_1 & rhs.bitboard_1,
                bitboard_2: self.bitboard_2 & rhs.bitboard_2,
                bitboard_3: self.bitboard_3 & rhs.bitboard_3,
                bitboard_4: self.bitboard_4 & rhs.bitboard_4,
            }
        }
    }
    impl BitAndAssign for QuoridorBitboard {
        fn bitand_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard_0: self.bitboard_0 & rhs.bitboard_0,
                bitboard_1: self.bitboard_1 & rhs.bitboard_1,
                bitboard_2: self.bitboard_2 & rhs.bitboard_2,
                bitboard_3: self.bitboard_3 & rhs.bitboard_3,
                bitboard_4: self.bitboard_4 & rhs.bitboard_4,
            }
        }
    }
    impl BitOr for QuoridorBitboard {
        type Output = Self;

        fn bitor(self, rhs: Self) -> Self {
            Self {
                bitboard_0: self.bitboard_0 | rhs.bitboard_0,
                bitboard_1: self.bitboard_1 | rhs.bitboard_1,
                bitboard_2: self.bitboard_2 | rhs.bitboard_2,
                bitboard_3: self.bitboard_3 | rhs.bitboard_3,
                bitboard_4: self.bitboard_4 | rhs.bitboard_4,
            }
        }
    }
    impl BitOrAssign for QuoridorBitboard {
        fn bitor_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard_0: self.bitboard_0 | rhs.bitboard_0,
                bitboard_1: self.bitboard_1 | rhs.bitboard_1,
                bitboard_2: self.bitboard_2 | rhs.bitboard_2,
                bitboard_3: self.bitboard_3 | rhs.bitboard_3,
                bitboard_4: self.bitboard_4 | rhs.bitboard_4,
            }
        }
    }
    impl BitXor for QuoridorBitboard {
        type Output = Self;

        fn bitxor(self, rhs: Self) -> Self {
            Self {
                bitboard_0: self.bitboard_0 ^ rhs.bitboard_0,
                bitboard_1: self.bitboard_1 ^ rhs.bitboard_1,
                bitboard_2: self.bitboard_2 ^ rhs.bitboard_2,
                bitboard_3: self.bitboard_3 ^ rhs.bitboard_3,
                bitboard_4: self.bitboard_4 ^ rhs.bitboard_4,
            }
        }
    }
    impl BitXorAssign for QuoridorBitboard {
        fn bitxor_assign(&mut self, rhs: Self) {
            *self = Self {
                bitboard_0: self.bitboard_0 ^ rhs.bitboard_0,
                bitboard_1: self.bitboard_1 ^ rhs.bitboard_1,
                bitboard_2: self.bitboard_2 ^ rhs.bitboard_2,
                bitboard_3: self.bitboard_3 ^ rhs.bitboard_3,
                bitboard_4: self.bitboard_4 ^ rhs.bitboard_4,
            }
        }
    }
    impl Not for QuoridorBitboard {
        type Output = Self;

        fn not(self) -> Self::Output {
            Self {
                bitboard_0: !self.bitboard_0,
                bitboard_1: !self.bitboard_1,
                bitboard_2: !self.bitboard_2,
                bitboard_3: !self.bitboard_3,
                bitboard_4: !self.bitboard_4,
            }
        }
    }
    impl Shl<isize> for QuoridorBitboard {
        type Output = Self;
        fn shl(self, rhs: isize) -> Self::Output {
            if rhs < 0 {
                Self {
                    bitboard_0: self.bitboard_0,
                    bitboard_1: self.bitboard_1,
                    bitboard_2: self.bitboard_2,
                    bitboard_3: self.bitboard_3,
                    bitboard_4: self.bitboard_4,
                } >> -rhs
            } else if rhs == 0 {
                self
            } else if rhs < 64 {
                Self {
                    bitboard_0: (self.bitboard_0).wrapping_shl(rhs as u32)
                        + (self.bitboard_1 >> (64 - rhs)),
                    bitboard_1: (self.bitboard_1).wrapping_shl(rhs as u32)
                        + (self.bitboard_2 >> (64 - rhs)),
                    bitboard_2: (self.bitboard_2).wrapping_shl(rhs as u32)
                        + (self.bitboard_3 >> (64 - rhs)),
                    bitboard_3: (self.bitboard_3).wrapping_shl(rhs as u32)
                        + (self.bitboard_4 >> (64 - rhs)),
                    bitboard_4: (self.bitboard_4).wrapping_shl(rhs as u32)
                        + (self.bitboard_0 >> (64 - rhs)),
                }
            } else if rhs == 64 {
                Self {
                    bitboard_0: self.bitboard_1,
                    bitboard_1: self.bitboard_2,
                    bitboard_2: self.bitboard_3,
                    bitboard_3: self.bitboard_4,
                    bitboard_4: self.bitboard_0,
                }
            } else {
                Self {
                    bitboard_0: self.bitboard_1,
                    bitboard_1: self.bitboard_2,
                    bitboard_2: self.bitboard_3,
                    bitboard_3: self.bitboard_4,
                    bitboard_4: self.bitboard_0,
                } << (rhs - 64)
            }
        }
    }
    impl ShlAssign<isize> for QuoridorBitboard {
        fn shl_assign(&mut self, rhs: isize) {
            if rhs < 0 {
                *self = Self {
                    bitboard_0: self.bitboard_0,
                    bitboard_1: self.bitboard_1,
                    bitboard_2: self.bitboard_2,
                    bitboard_3: self.bitboard_3,
                    bitboard_4: self.bitboard_4,
                } >> -rhs
            } else if rhs == 0 {
            } else if rhs < 64 {
                *self = Self {
                    bitboard_0: (self.bitboard_0).wrapping_shl(rhs as u32)
                        + (self.bitboard_1 >> (64 - rhs)),
                    bitboard_1: (self.bitboard_1).wrapping_shl(rhs as u32)
                        + (self.bitboard_2 >> (64 - rhs)),
                    bitboard_2: (self.bitboard_2).wrapping_shl(rhs as u32)
                        + (self.bitboard_3 >> (64 - rhs)),
                    bitboard_3: (self.bitboard_3).wrapping_shl(rhs as u32)
                        + (self.bitboard_4 >> (64 - rhs)),
                    bitboard_4: (self.bitboard_4).wrapping_shl(rhs as u32)
                        + (self.bitboard_0 >> (64 - rhs)),
                }
            } else if rhs == 64 {
                *self = Self {
                    bitboard_0: self.bitboard_1,
                    bitboard_1: self.bitboard_2,
                    bitboard_2: self.bitboard_3,
                    bitboard_3: self.bitboard_4,
                    bitboard_4: self.bitboard_0,
                }
            } else {
                *self = Self {
                    bitboard_0: self.bitboard_1,
                    bitboard_1: self.bitboard_2,
                    bitboard_2: self.bitboard_3,
                    bitboard_3: self.bitboard_4,
                    bitboard_4: self.bitboard_0,
                } << (rhs - 64)
            }
        }
    }
    impl Shr<isize> for QuoridorBitboard {
        type Output = Self;
        fn shr(self, rhs: isize) -> Self::Output {
            if rhs < 0 {
                Self {
                    bitboard_0: self.bitboard_0,
                    bitboard_1: self.bitboard_1,
                    bitboard_2: self.bitboard_2,
                    bitboard_3: self.bitboard_3,
                    bitboard_4: self.bitboard_4,
                } << -rhs
            } else if rhs == 0 {
                self
            } else if rhs < 64 {
                Self {
                    bitboard_0: (self.bitboard_0 >> rhs)
                        + (self.bitboard_4).wrapping_shl((64 - rhs) as u32),
                    bitboard_1: (self.bitboard_1 >> rhs)
                        + (self.bitboard_0).wrapping_shl((64 - rhs) as u32),
                    bitboard_2: (self.bitboard_2 >> rhs)
                        + (self.bitboard_1).wrapping_shl((64 - rhs) as u32),
                    bitboard_3: (self.bitboard_3 >> rhs)
                        + (self.bitboard_2).wrapping_shl((64 - rhs) as u32),
                    bitboard_4: (self.bitboard_4 >> rhs)
                        + (self.bitboard_3).wrapping_shl((64 - rhs) as u32),
                }
            } else if rhs == 64 {
                Self {
                    bitboard_0: self.bitboard_4,
                    bitboard_1: self.bitboard_0,
                    bitboard_2: self.bitboard_1,
                    bitboard_3: self.bitboard_2,
                    bitboard_4: self.bitboard_3,
                }
            } else {
                Self {
                    bitboard_0: self.bitboard_4,
                    bitboard_1: self.bitboard_0,
                    bitboard_2: self.bitboard_1,
                    bitboard_3: self.bitboard_2,
                    bitboard_4: self.bitboard_3,
                } >> (rhs - 64)
            }
        }
    }
    impl ShrAssign<isize> for QuoridorBitboard {
        fn shr_assign(&mut self, rhs: isize) {
            if rhs < 0 {
                *self = Self {
                    bitboard_0: self.bitboard_0,
                    bitboard_1: self.bitboard_1,
                    bitboard_2: self.bitboard_2,
                    bitboard_3: self.bitboard_3,
                    bitboard_4: self.bitboard_4,
                } << -rhs
            } else if rhs == 0 {
            } else if rhs < 64 {
                *self = Self {
                    bitboard_0: (self.bitboard_0 >> rhs)
                        + (self.bitboard_4).wrapping_shl((64 - rhs) as u32),
                    bitboard_1: (self.bitboard_1 >> rhs)
                        + (self.bitboard_0).wrapping_shl((64 - rhs) as u32),
                    bitboard_2: (self.bitboard_2 >> rhs)
                        + (self.bitboard_1).wrapping_shl((64 - rhs) as u32),
                    bitboard_3: (self.bitboard_3 >> rhs)
                        + (self.bitboard_2).wrapping_shl((64 - rhs) as u32),
                    bitboard_4: (self.bitboard_4 >> rhs)
                        + (self.bitboard_3).wrapping_shl((64 - rhs) as u32),
                }
            } else if rhs == 64 {
                *self = Self {
                    bitboard_0: self.bitboard_4,
                    bitboard_1: self.bitboard_0,
                    bitboard_2: self.bitboard_1,
                    bitboard_3: self.bitboard_2,
                    bitboard_4: self.bitboard_3,
                }
            } else {
                *self = Self {
                    bitboard_0: self.bitboard_4,
                    bitboard_1: self.bitboard_0,
                    bitboard_2: self.bitboard_1,
                    bitboard_3: self.bitboard_2,
                    bitboard_4: self.bitboard_3,
                } >> (rhs - 64)
            }
        }
    }
}
