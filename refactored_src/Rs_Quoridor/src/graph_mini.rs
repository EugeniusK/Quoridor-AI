pub mod mini_graph_implementations {
    use crate::board::board::QuoridorBoard;
    use crate::VecDeque;

    const WALL_LIMIT: i16 = 5;
    #[derive(Clone, Copy, Debug)]
    pub struct RustStaticGraphMini {
        pub p1_pos: i16,
        pub p2_pos: i16,
        pub p1_walls_placed: i16,
        pub p2_walls_placed: i16,
        pub turn: i16,
        pub over: bool,
        pub hor_walls_placed: [bool; 16],
        pub ver_walls_placed: [bool; 16],
        pub mode: i16,
    }

    #[derive(Clone, Copy, Debug)]

    pub struct RustDynamicGraphMini {
        pub nodes: [[bool; 4]; 25],
        pub p1_pos: i16,
        pub p2_pos: i16,
        pub p1_walls_placed: i16,
        pub p2_walls_placed: i16,
        pub turn: i16,
        pub over: bool,
        pub hor_walls_placed: [bool; 16],
        pub ver_walls_placed: [bool; 16],
        pub mode: i16,
    }
    pub const GRAPH_SHIFT_ARR: [i16; 12] = [-5, 1, 5, -1, -10, -4, 2, 6, 10, 4, -2, -6];
    pub const GRAPH_ADJ_LIST: [[bool; 4]; 25] = [
        [false, true, true, false],
        [false, true, true, true],
        [false, true, true, true],
        [false, true, true, true],
        [false, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, false, false],
        [true, true, false, true],
        [true, true, false, true],
        [true, true, false, true],
        [true, false, false, true],
    ];

    pub const RUST_STATIC_GRAPH_BLANK: RustStaticGraphMini = RustStaticGraphMini {
        p1_pos: 0,
        p2_pos: 0,
        p1_walls_placed: 0,
        p2_walls_placed: 0,
        turn: 0,
        over: false,
        hor_walls_placed: [false; 16],
        ver_walls_placed: [false; 16],
        mode: 0,
    };

    pub const RUST_DYNAMIC_GRAPH_BLANK: RustDynamicGraphMini = RustDynamicGraphMini {
        nodes: [[false; 4]; 25],
        p1_pos: 0,
        p2_pos: 0,
        p1_walls_placed: 0,
        p2_walls_placed: 0,
        turn: 0,
        over: false,
        hor_walls_placed: [false; 16],
        ver_walls_placed: [false; 16],
        mode: 0,
    };

    pub trait GraphMini: QuoridorBoard {
        fn undo_action(&mut self, action: i16);
        fn is_direction_valid(&self, pos: i16, direction: i16) -> bool;
        fn is_wall_valid(&self, wall_number: i16) -> bool;
        fn is_move_valid(&self, move_number: i16) -> bool;
        fn can_place_wall(&self) -> bool;
        fn is_action_available(&mut self, action_number: i16) -> bool {
            if action_number < 32 {
                if self.can_place_wall() && self.is_wall_valid(action_number) {
                    self.take_action(action_number);
                    let path_1 = self.search(1);
                    let path_2 = self.search(2);

                    self.undo_action(action_number);

                    if path_1[0] != -1 && path_2[0] != -1 {
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
                if GraphMini::is_action_available(self, action) {
                    available_actions.push(action);
                }
            }
            available_actions
        }

        // fn get_turn(&self) -> i16;
        // fn is_over(&self) -> bool;
        fn get_pos(&self, player_number: i16) -> i16;
        fn search(&self, player_number: i16) -> [i16; 25];
        fn display(&self) -> () {
            let mut output_board = String::new();
            let (mut north, mut east, mut south, mut west): (bool, bool, bool, bool);
            let mut pos: i16;
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
                        if self.is_direction_valid(pos, 1) {
                            output_board.push('\u{2502}')
                        } else {
                            output_board.push('\u{2503}')
                        }
                    }
                }
                output_board.push('\n');

                for col in 0..5 {
                    pos = row * 5 + col;
                    if row != 4 {
                        if self.is_direction_valid(pos, 2) {
                            output_board.push_str("\u{2500}\u{2500}\u{2500}")
                        } else {
                            output_board.push_str("\u{2501}\u{2501}\u{2501}")
                        }
                        if col != 4 {
                            north = !self.is_direction_valid(pos, 1);
                            east = !self.is_direction_valid(pos + 1, 2);
                            south = !self.is_direction_valid(pos + 5, 1);
                            west = !self.is_direction_valid(pos, 2);
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
        fn bfs(&self, start_pos: i16, player_number: i16) -> [i16; 25] {
            let mut frontier: VecDeque<i16> = VecDeque::with_capacity(25);
            frontier.push_back(start_pos);

            let mut explored: [bool; 25] = [false; 25];

            let mut in_frontier: [bool; 25] = [false; 25];

            let mut parent: [i16; 25] = [-1; 25];
            let mut pos: i16;
            let mut new_pos: i16;
            while frontier.len() != 0 {
                match frontier.pop_front() {
                    Some(popped) => {
                        pos = popped;
                        in_frontier[pos as usize] = false;
                    }
                    None => panic!("EMPTY FRONTIER IN bfs"),
                }
                explored[pos as usize] = true;

                for direction in 0..4 {
                    new_pos = pos + GRAPH_SHIFT_ARR[direction];
                    if self.is_direction_valid(pos, direction as i16)
                        && !explored[new_pos as usize]
                        && !in_frontier[new_pos as usize]
                    {
                        parent[new_pos as usize] = pos;
                        if (player_number == 1 && new_pos <= 4)
                            | (player_number == 2 && new_pos >= 20)
                        {
                            let mut stack: [i16; 25] = [-1; 25];
                            stack[0] = new_pos;
                            let mut stack_idx: usize = 1;
                            loop {
                                if parent[new_pos as usize] == -1 {
                                    stack[stack_idx] = -1;
                                    break;
                                }
                                stack[stack_idx] = parent[new_pos as usize];
                                stack_idx += 1;
                                new_pos = parent[new_pos as usize];
                            }
                            let mut path: [i16; 25] = [-1; 25];
                            path[0] = new_pos;
                            stack_idx -= 1;
                            let mut path_idx: usize = 0;
                            loop {
                                path[path_idx] = stack[stack_idx];
                                if stack_idx == 0 {
                                    return path;
                                }
                                stack_idx -= 1;
                                path_idx += 1;
                            }
                        }
                        frontier.push_back(new_pos);
                        in_frontier[new_pos as usize] = true;
                    }
                }
            }
            return [-1; 25];
        }
        fn dfs(&self, start_pos: i16, player_number: i16) -> [i16; 25] {
            let mut frontier: VecDeque<i16> = VecDeque::with_capacity(25);
            frontier.push_back(start_pos);

            let mut explored: [bool; 25] = [false; 25];

            let mut in_frontier: [bool; 25] = [false; 25];

            let mut parent: [i16; 25] = [-1; 25];
            let mut pos: i16;
            let mut new_pos: i16;
            while frontier.len() != 0 {
                match frontier.pop_back() {
                    Some(popped) => {
                        pos = popped;
                        in_frontier[pos as usize] = false;
                    }
                    None => panic!("EMPTY FRONTIER IN bfs"),
                }
                explored[pos as usize] = true;

                for direction in 0..4 {
                    new_pos = pos + GRAPH_SHIFT_ARR[direction];
                    if self.is_direction_valid(pos, direction as i16)
                        && !explored[new_pos as usize]
                        && !in_frontier[new_pos as usize]
                    {
                        parent[new_pos as usize] = pos;
                        if (player_number == 1 && new_pos <= 4)
                            | (player_number == 2 && new_pos >= 20)
                        {
                            let mut stack: [i16; 25] = [-1; 25];
                            stack[0] = new_pos;
                            let mut stack_idx: usize = 1;
                            loop {
                                if parent[new_pos as usize] == -1 {
                                    stack[stack_idx] = -1;
                                    break;
                                }
                                stack[stack_idx] = parent[new_pos as usize];
                                stack_idx += 1;
                                new_pos = parent[new_pos as usize];
                            }
                            let mut path: [i16; 25] = [-1; 25];
                            path[0] = new_pos;
                            stack_idx -= 1;
                            let mut path_idx: usize = 0;
                            loop {
                                path[path_idx] = stack[stack_idx];
                                if stack_idx == 0 {
                                    return path;
                                }
                                stack_idx -= 1;
                                path_idx += 1;
                            }
                        }
                        frontier.push_back(new_pos);
                        in_frontier[new_pos as usize] = true;
                    }
                }
            }
            return [-1; 25];
        }
    }

    impl QuoridorBoard for RustStaticGraphMini {
        fn number_actions(&self) -> i16 {
            44
        }
        fn get_available_actions_fast(&mut self) -> Vec<i16> {
            let mut available_actions: Vec<i16> = vec![];
            if self.can_place_wall() {
                let mut path_available: bool = false;
                let mut previous_paths_1: Vec<[i16; 25]> = Vec::new();
                let mut previous_paths_2: Vec<[i16; 25]> = Vec::new();
                let mut path_1: [i16; 25];
                let mut path_2: [i16; 25];
                let mut path_traversed_1: bool;
                let mut path_traversed_2: bool;
                let mut path_valid: bool;
                let mut shift: i16;
                for action_number in 0..32 {
                    if self.is_wall_valid(action_number) {
                        if !path_available {
                            self.take_action(action_number);
                            path_1 = self.search(1);
                            path_2 = self.search(2);
                            if path_1[0] != -1 && path_2[0] != -1 {
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
                                path_valid = true;
                                for idx in 0..25 {
                                    if path[idx + 1] == -1 {
                                        break;
                                    }
                                    shift = path[idx + 1] - path[idx];
                                    if !((shift == -5 && self.is_direction_valid(path[idx], 0))
                                        | (shift == 1 && self.is_direction_valid(path[idx], 1))
                                        | (shift == 5 && self.is_direction_valid(path[idx], 2))
                                        | (shift == -1 && self.is_direction_valid(path[idx], 3)))
                                    {
                                        path_valid = false;
                                        break;
                                    }
                                }
                                if path_valid {
                                    path_traversed_1 = true;
                                    break;
                                }
                            }
                            path_traversed_2 = false;
                            for path in &previous_paths_2 {
                                path_valid = true;
                                for idx in 0..25 {
                                    if path[idx + 1] == -1 {
                                        break;
                                    }
                                    shift = path[idx + 1] - path[idx];
                                    if !((shift == -5 && self.is_direction_valid(path[idx], 0))
                                        | (shift == 1 && self.is_direction_valid(path[idx], 1))
                                        | (shift == 5 && self.is_direction_valid(path[idx], 2))
                                        | (shift == -1 && self.is_direction_valid(path[idx], 3)))
                                    {
                                        path_valid = false;
                                        break;
                                    }
                                }
                                if path_valid {
                                    path_traversed_2 = true;
                                    break;
                                }
                            }
                            if !path_traversed_1 | !path_traversed_2 {
                                if !path_traversed_1 {
                                    path_1 = self.search(1);
                                    if path_1[0] != -1 {
                                        previous_paths_1.push(path_1);
                                    }
                                } else {
                                    path_1 = previous_paths_1[0];
                                }
                                if !path_traversed_2 {
                                    path_2 = self.search(2);
                                    if path_2[0] != -1 {
                                        previous_paths_2.push(path_2)
                                    }
                                } else {
                                    path_2 = previous_paths_2[0];
                                }

                                if path_1[0] != -1 && path_2[0] != -1 {
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
                RustStaticGraphMini::get_available_actions_slow(self)
            } else if mode == 2 {
                RustStaticGraphMini::get_available_actions_fast(self)
            } else {
                RustStaticGraphMini::get_available_actions_fast(self)
            }
        }
        fn is_action_available(&mut self, action_number: i16) -> bool {
            GraphMini::is_action_available(self, action_number)
        }
        fn new(mode: i16) -> RustStaticGraphMini {
            RustStaticGraphMini {
                p1_pos: 22,
                p2_pos: 2,
                p1_walls_placed: 0,
                p2_walls_placed: 0,
                turn: 1,
                over: false,
                hor_walls_placed: [false; 16],
                ver_walls_placed: [false; 16],
                mode: mode,
            }
        }
        fn take_action(&mut self, action: i16) {
            if action < 32 {
                if action < 16 {
                    self.hor_walls_placed[action as usize] = true;
                } else {
                    self.ver_walls_placed[(action - 16) as usize] = true;
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
                    self.p1_pos += GRAPH_SHIFT_ARR[(action - 32) as usize];
                    if self.p1_pos <= 4 {
                        self.over = true;
                    } else {
                        self.turn = 2;
                    }
                } else {
                    self.p2_pos += GRAPH_SHIFT_ARR[(action - 32) as usize];
                    if self.p2_pos >= 20 {
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

    impl GraphMini for RustStaticGraphMini {
        fn undo_action(&mut self, action: i16) {
            if action < 32 {
                if action < 16 {
                    self.hor_walls_placed[action as usize] = false;
                } else {
                    self.ver_walls_placed[(action - 16) as usize] = false;
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
        fn is_direction_valid(&self, pos: i16, direction: i16) -> bool {
            if GRAPH_ADJ_LIST[pos as usize][direction as usize] {
                if direction == 0 {
                    if pos % 5 == 0 {
                        !self.hor_walls_placed[(pos % 5 + 4 * (4 - pos / 5)) as usize]
                    } else if pos % 5 == 4 {
                        !self.hor_walls_placed[(pos % 5 + 4 * (4 - pos / 5) - 1) as usize]
                    } else {
                        !self.hor_walls_placed[(pos % 5 + 4 * (4 - pos / 5) - 1) as usize]
                            && !self.hor_walls_placed[(pos % 5 + 4 * (4 - pos / 5)) as usize]
                    }
                } else if direction == 1 {
                    if pos < 5 {
                        !self.ver_walls_placed[(pos % 5 + (3 - pos / 5) * 4) as usize]
                    } else if pos >= 20 {
                        !self.ver_walls_placed[(pos % 5 + (4 - pos / 5) * 4) as usize]
                    } else {
                        !self.ver_walls_placed[(pos % 5 + (3 - pos / 5) * 4) as usize]
                            && !self.ver_walls_placed[(pos % 5 + (4 - pos / 5) * 4) as usize]
                    }
                } else if direction == 2 {
                    if pos % 5 == 0 {
                        !self.hor_walls_placed[(pos % 5 + 4 * (3 - pos / 5)) as usize]
                    } else if pos % 5 == 4 {
                        !self.hor_walls_placed[(pos % 5 + 4 * (3 - pos / 5) - 1) as usize]
                    } else {
                        !self.hor_walls_placed[(pos % 5 + 4 * (3 - pos / 5) - 1) as usize]
                            && !self.hor_walls_placed[(pos % 5 + 4 * (3 - pos / 5)) as usize]
                    }
                } else if direction == 3 {
                    if pos < 5 {
                        !self.ver_walls_placed[(pos % 5 + (3 - pos / 5) * 4 - 1) as usize]
                    } else if pos >= 20 {
                        !self.ver_walls_placed[(pos % 5 + (4 - pos / 5) * 4 - 1) as usize]
                    } else {
                        !self.ver_walls_placed[(pos % 5 + (3 - pos / 5) * 4 - 1) as usize]
                            && !self.ver_walls_placed[(pos % 5 + (4 - pos / 5) * 4 - 1) as usize]
                    }
                } else {
                    panic!("UNKNOWN DIRECTION");
                }
            } else {
                false
            }
        }
        fn is_move_valid(&self, move_number: i16) -> bool {
            let in_turn_pos: i16;
            let out_turn_pos: i16;
            if self.turn == 1 {
                in_turn_pos = self.p1_pos;
                out_turn_pos = self.p2_pos;
            } else {
                in_turn_pos = self.p2_pos;
                out_turn_pos = self.p1_pos;
            }

            if move_number < 36 {
                return self.is_direction_valid(in_turn_pos, move_number - 32)
                    && in_turn_pos + GRAPH_SHIFT_ARR[(move_number - 32) as usize] != out_turn_pos;
            } else {
                if move_number % 2 == 0 {
                    return self.is_direction_valid(in_turn_pos, (move_number - 36) / 2)
                        && in_turn_pos + GRAPH_SHIFT_ARR[((move_number - 36) / 2) as usize]
                            == out_turn_pos
                        && self.is_direction_valid(out_turn_pos, (move_number - 36) / 2);
                } else {
                    return (self.is_direction_valid(in_turn_pos, ((move_number - 35) / 2) % 4)
                        && in_turn_pos + GRAPH_SHIFT_ARR[(((move_number - 35) / 2) % 4) as usize]
                            == out_turn_pos
                        && !self.is_direction_valid(out_turn_pos, ((move_number - 35) / 2) % 4)
                        && self.is_direction_valid(out_turn_pos, ((move_number - 37) / 2) % 4))
                        | (self.is_direction_valid(in_turn_pos, ((move_number - 37) / 2) % 4)
                            && in_turn_pos
                                + GRAPH_SHIFT_ARR[(((move_number - 37) / 2) % 4) as usize]
                                == out_turn_pos
                            && !self
                                .is_direction_valid(out_turn_pos, ((move_number - 37) / 2) % 4)
                            && self
                                .is_direction_valid(out_turn_pos, ((move_number - 35) / 2) % 4));
                }
            }
        }
        fn is_wall_valid(&self, wall_number: i16) -> bool {
            if wall_number < 16 {
                if wall_number % 4 == 0 {
                    !self.hor_walls_placed[wall_number as usize]
                        && !self.hor_walls_placed[(wall_number + 1) as usize]
                        && !self.ver_walls_placed[wall_number as usize]
                } else if wall_number % 4 == 3 {
                    !self.hor_walls_placed[(wall_number - 1) as usize]
                        && !self.hor_walls_placed[wall_number as usize]
                        && !self.ver_walls_placed[wall_number as usize]
                } else {
                    !self.hor_walls_placed[(wall_number - 1) as usize]
                        && !self.hor_walls_placed[wall_number as usize]
                        && !self.hor_walls_placed[(wall_number + 1) as usize]
                        && !self.ver_walls_placed[wall_number as usize]
                }
            } else {
                if (wall_number - 16) / 4 == 0 {
                    !self.ver_walls_placed[(wall_number - 16) as usize]
                        && !self.ver_walls_placed[(wall_number - 12) as usize]
                        && !self.hor_walls_placed[(wall_number - 16) as usize]
                } else if (wall_number - 16) / 4 == 3 {
                    !self.ver_walls_placed[(wall_number - 20) as usize]
                        && !self.ver_walls_placed[(wall_number - 16) as usize]
                        && !self.hor_walls_placed[(wall_number - 16) as usize]
                } else {
                    !self.ver_walls_placed[(wall_number - 20) as usize]
                        && !self.ver_walls_placed[(wall_number - 16) as usize]
                        && !self.ver_walls_placed[(wall_number - 12) as usize]
                        && !self.hor_walls_placed[(wall_number - 16) as usize]
                }
            }
        }

        fn can_place_wall(&self) -> bool {
            (self.turn == 1 && self.p1_walls_placed < WALL_LIMIT)
                | (self.turn == 2 && self.p2_walls_placed < WALL_LIMIT)
        }

        fn get_pos(&self, player_number: i16) -> i16 {
            if player_number == 1 {
                self.p1_pos
            } else {
                self.p2_pos
            }
        }

        fn search(&self, player_number: i16) -> [i16; 25] {
            if self.mode == 1 {
                if player_number == 1 {
                    self.bfs(self.p1_pos, 1)
                } else {
                    self.bfs(self.p2_pos, 2)
                }
            } else if self.mode == 2 {
                if player_number == 1 {
                    self.dfs(self.p1_pos, 1)
                } else {
                    self.dfs(self.p2_pos, 2)
                }
            } else {
                if player_number == 1 {
                    self.bfs(self.p1_pos, 1)
                } else {
                    self.bfs(self.p2_pos, 2)
                }
            }
        }
    }
    impl QuoridorBoard for RustDynamicGraphMini {
        fn number_actions(&self) -> i16 {
            44
        }
        fn get_available_actions_fast(&mut self) -> Vec<i16> {
            let mut available_actions: Vec<i16> = vec![];
            if self.can_place_wall() {
                let mut path_available: bool = false;
                let mut previous_paths_1: Vec<[i16; 25]> = Vec::new();
                let mut previous_paths_2: Vec<[i16; 25]> = Vec::new();
                let mut path_1: [i16; 25];
                let mut path_2: [i16; 25];
                let mut path_traversed_1: bool;
                let mut path_traversed_2: bool;
                let mut path_valid: bool;
                let mut shift: i16;
                for action_number in 0..32 {
                    if self.is_wall_valid(action_number) {
                        if !path_available {
                            self.take_action(action_number);
                            path_1 = self.search(1);
                            path_2 = self.search(2);
                            if path_1[0] != -1 && path_2[0] != -1 {
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
                                path_valid = true;
                                for idx in 0..25 {
                                    if path[idx + 1] == -1 {
                                        break;
                                    }
                                    shift = path[idx + 1] - path[idx];
                                    if !((shift == -5 && self.is_direction_valid(path[idx], 0))
                                        | (shift == 1 && self.is_direction_valid(path[idx], 1))
                                        | (shift == 5 && self.is_direction_valid(path[idx], 2))
                                        | (shift == -1 && self.is_direction_valid(path[idx], 3)))
                                    {
                                        path_valid = false;
                                        break;
                                    }
                                }
                                if path_valid {
                                    path_traversed_1 = true;
                                    break;
                                }
                            }
                            path_traversed_2 = false;
                            for path in &previous_paths_2 {
                                path_valid = true;
                                for idx in 0..25 {
                                    if path[idx + 1] == -1 {
                                        break;
                                    }
                                    shift = path[idx + 1] - path[idx];
                                    if !((shift == -5 && self.is_direction_valid(path[idx], 0))
                                        | (shift == 1 && self.is_direction_valid(path[idx], 1))
                                        | (shift == 5 && self.is_direction_valid(path[idx], 2))
                                        | (shift == -1 && self.is_direction_valid(path[idx], 3)))
                                    {
                                        path_valid = false;
                                        break;
                                    }
                                }
                                if path_valid {
                                    path_traversed_2 = true;
                                    break;
                                }
                            }
                            if !path_traversed_1 | !path_traversed_2 {
                                if !path_traversed_1 {
                                    path_1 = self.search(1);
                                    if path_1[0] != -1 {
                                        previous_paths_1.push(path_1);
                                    }
                                } else {
                                    path_1 = previous_paths_1[0];
                                }
                                if !path_traversed_2 {
                                    path_2 = self.search(2);
                                    if path_2[0] != -1 {
                                        previous_paths_2.push(path_2)
                                    }
                                } else {
                                    path_2 = previous_paths_2[0];
                                }

                                if path_1[0] != -1 && path_2[0] != -1 {
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
                RustDynamicGraphMini::get_available_actions_slow(self)
            } else if mode == 2 {
                RustDynamicGraphMini::get_available_actions_fast(self)
            } else {
                RustDynamicGraphMini::get_available_actions_fast(self)
            }
        }
        fn is_action_available(&mut self, action_number: i16) -> bool {
            GraphMini::is_action_available(self, action_number)
        }
        fn new(mode: i16) -> RustDynamicGraphMini {
            RustDynamicGraphMini {
                nodes: [
                    [false, true, true, false],
                    [false, true, true, true],
                    [false, true, true, true],
                    [false, true, true, true],
                    [false, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, false, false],
                    [true, true, false, true],
                    [true, true, false, true],
                    [true, true, false, true],
                    [true, false, false, true],
                ],
                p1_pos: 22,
                p2_pos: 2,
                p1_walls_placed: 0,
                p2_walls_placed: 0,
                turn: 1,
                over: false,
                hor_walls_placed: [false; 16],
                ver_walls_placed: [false; 16],
                mode: mode,
            }
        }
        fn take_action(&mut self, action: i16) {
            if action < 32 {
                if action < 16 {
                    self.hor_walls_placed[action as usize] = true;
                    let idx = (action % 4 + 5 * (4 - action / 4)) as usize;
                    self.nodes[idx][0] = false;
                    self.nodes[idx + 1][0] = false;
                    self.nodes[idx - 5][2] = false;
                    self.nodes[idx - 4][2] = false;
                } else {
                    self.ver_walls_placed[(action - 16) as usize] = true;
                    let idx = (action % 4 + 5 * (4 - (action - 16) / 4)) as usize;
                    self.nodes[idx][1] = false;
                    self.nodes[idx + 1][3] = false;
                    self.nodes[idx - 5][1] = false;
                    self.nodes[idx - 4][3] = false;
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
                    self.p1_pos += GRAPH_SHIFT_ARR[(action - 32) as usize];
                    if self.p1_pos <= 4 {
                        self.over = true;
                    } else {
                        self.turn = 2;
                    }
                } else {
                    self.p2_pos += GRAPH_SHIFT_ARR[(action - 32) as usize];
                    if self.p2_pos >= 20 {
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
    impl GraphMini for RustDynamicGraphMini {
        fn undo_action(&mut self, action: i16) {
            if action < 32 {
                if action < 16 {
                    self.hor_walls_placed[action as usize] = false;
                    let idx = (action % 4 + 5 * (4 - action / 4)) as usize;
                    self.nodes[idx][0] = true;
                    self.nodes[idx + 1][0] = true;
                    self.nodes[idx - 5][2] = true;
                    self.nodes[idx - 4][2] = true;
                } else {
                    self.ver_walls_placed[(action - 16) as usize] = false;
                    let idx = (action % 4 + 5 * (4 - (action - 16) / 4)) as usize;
                    self.nodes[idx][1] = true;
                    self.nodes[idx + 1][3] = true;
                    self.nodes[idx - 5][1] = true;
                    self.nodes[idx - 4][3] = true;
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
        fn is_direction_valid(&self, pos: i16, direction: i16) -> bool {
            self.nodes[pos as usize][direction as usize]
        }
        fn is_move_valid(&self, move_number: i16) -> bool {
            let in_turn_pos: i16;
            let out_turn_pos: i16;
            if self.turn == 1 {
                in_turn_pos = self.p1_pos;
                out_turn_pos = self.p2_pos;
            } else {
                in_turn_pos = self.p2_pos;
                out_turn_pos = self.p1_pos;
            }

            if move_number < 36 {
                return self.is_direction_valid(in_turn_pos, move_number - 32)
                    && in_turn_pos + GRAPH_SHIFT_ARR[(move_number - 32) as usize] != out_turn_pos;
            } else {
                if move_number % 2 == 0 {
                    return self.is_direction_valid(in_turn_pos, (move_number - 36) / 2)
                        && in_turn_pos + GRAPH_SHIFT_ARR[((move_number - 36) / 2) as usize]
                            == out_turn_pos
                        && self.is_direction_valid(out_turn_pos, (move_number - 36) / 2);
                } else {
                    return (self.is_direction_valid(in_turn_pos, ((move_number - 35) / 2) % 4)
                        && in_turn_pos + GRAPH_SHIFT_ARR[(((move_number - 35) / 2) % 4) as usize]
                            == out_turn_pos
                        && !self.is_direction_valid(out_turn_pos, ((move_number - 35) / 2) % 4)
                        && self.is_direction_valid(out_turn_pos, ((move_number - 37) / 2) % 4))
                        | (self.is_direction_valid(in_turn_pos, ((move_number - 37) / 2) % 4)
                            && in_turn_pos
                                + GRAPH_SHIFT_ARR[(((move_number - 37) / 2) % 4) as usize]
                                == out_turn_pos
                            && !self
                                .is_direction_valid(out_turn_pos, ((move_number - 37) / 2) % 4)
                            && self
                                .is_direction_valid(out_turn_pos, ((move_number - 35) / 2) % 4));
                }
            }
        }
        fn is_wall_valid(&self, wall_number: i16) -> bool {
            if wall_number < 16 {
                if wall_number % 4 == 0 {
                    !self.hor_walls_placed[wall_number as usize]
                        && !self.hor_walls_placed[(wall_number + 1) as usize]
                        && !self.ver_walls_placed[wall_number as usize]
                } else if wall_number % 4 == 3 {
                    !self.hor_walls_placed[(wall_number - 1) as usize]
                        && !self.hor_walls_placed[wall_number as usize]
                        && !self.ver_walls_placed[wall_number as usize]
                } else {
                    !self.hor_walls_placed[(wall_number - 1) as usize]
                        && !self.hor_walls_placed[wall_number as usize]
                        && !self.hor_walls_placed[(wall_number + 1) as usize]
                        && !self.ver_walls_placed[wall_number as usize]
                }
            } else {
                if (wall_number - 16) / 4 == 0 {
                    !self.ver_walls_placed[(wall_number - 16) as usize]
                        && !self.ver_walls_placed[(wall_number - 12) as usize]
                        && !self.hor_walls_placed[(wall_number - 16) as usize]
                } else if (wall_number - 16) / 4 == 3 {
                    !self.ver_walls_placed[(wall_number - 20) as usize]
                        && !self.ver_walls_placed[(wall_number - 16) as usize]
                        && !self.hor_walls_placed[(wall_number - 16) as usize]
                } else {
                    !self.ver_walls_placed[(wall_number - 20) as usize]
                        && !self.ver_walls_placed[(wall_number - 16) as usize]
                        && !self.ver_walls_placed[(wall_number - 12) as usize]
                        && !self.hor_walls_placed[(wall_number - 16) as usize]
                }
            }
        }
        fn can_place_wall(&self) -> bool {
            (self.turn == 1 && self.p1_walls_placed < WALL_LIMIT)
                | (self.turn == 2 && self.p2_walls_placed < WALL_LIMIT)
        }
        fn get_pos(&self, player_number: i16) -> i16 {
            if player_number == 1 {
                self.p1_pos
            } else {
                self.p2_pos
            }
        }
        fn search(&self, player_number: i16) -> [i16; 25] {
            if self.mode == 1 {
                if player_number == 1 {
                    self.bfs(self.p1_pos, 1)
                } else {
                    self.bfs(self.p2_pos, 2)
                }
            } else {
                if player_number == 1 {
                    self.bfs(self.p1_pos, 1)
                } else {
                    self.bfs(self.p2_pos, 2)
                }
            }
        }
    }
}
