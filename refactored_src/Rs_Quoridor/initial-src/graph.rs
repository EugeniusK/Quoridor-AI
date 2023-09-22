pub mod graph_implementations {

    use crate::board::board::QuoridorBoard;
    use crate::util;
    pub use util::util::{find_idx, find_null, find_nulli16, min_idx};
    #[derive(Clone, Copy, Debug)]
    pub struct RustStaticGraph {
        pub p1_pos: i16,
        pub p2_pos: i16,
        pub p1_walls_placed: i16,
        pub p2_walls_placed: i16,
        pub turn: i16,
        pub over: bool,
        pub hor_walls_placed: [bool; 64],
        pub ver_walls_placed: [bool; 64],
        pub mode: i16,
    }
    #[derive(Clone, Copy, Debug)]

    pub struct RustDynamicGraph {
        pub nodes: [[bool; 4]; 81],
        pub p1_pos: i16,
        pub p2_pos: i16,
        pub p1_walls_placed: i16,
        pub p2_walls_placed: i16,
        pub turn: i16,
        pub over: bool,
        pub hor_walls_placed: [bool; 64],
        pub ver_walls_placed: [bool; 64],
        pub mode: i16,
    }
    pub const GRAPH_SHIFT_ARR: [i16; 12] = [-9, 1, 9, -1, -18, -8, 2, 10, 18, 8, -2, -10];
    pub const GRAPH_ADJ_LIST: [[bool; 4]; 81] = [
        [false, true, true, false],
        [false, true, true, true],
        [false, true, true, true],
        [false, true, true, true],
        [false, true, true, true],
        [false, true, true, true],
        [false, true, true, true],
        [false, true, true, true],
        [false, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, true, false],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, true, true, true],
        [true, false, true, true],
        [true, true, false, false],
        [true, true, false, true],
        [true, true, false, true],
        [true, true, false, true],
        [true, true, false, true],
        [true, true, false, true],
        [true, true, false, true],
        [true, true, false, true],
        [true, false, false, true],
    ];

    pub const RUST_STATIC_GRAPH_BLANK: RustStaticGraph = RustStaticGraph {
        p1_pos: 0,
        p2_pos: 0,
        p1_walls_placed: 0,
        p2_walls_placed: 0,
        turn: 0,
        over: false,
        hor_walls_placed: [false; 64],
        ver_walls_placed: [false; 64],
        mode: 0,
    };

    pub const RUST_DYNAMIC_GRAPH_BLANK: RustDynamicGraph = RustDynamicGraph {
        nodes: [[false; 4]; 81],
        p1_pos: 0,
        p2_pos: 0,
        p1_walls_placed: 0,
        p2_walls_placed: 0,
        turn: 0,
        over: false,
        hor_walls_placed: [false; 64],
        ver_walls_placed: [false; 64],
        mode: 0,
    };

    pub trait Graph: QuoridorBoard {
        fn undo_action(&mut self, action: i16);
        fn is_direction_valid(&self, pos: i16, direction: i16) -> bool;
        fn is_wall_valid(&self, wall_number: i16) -> bool;
        fn is_move_valid(&self, move_number: i16) -> bool;
        fn can_place_wall(&self) -> bool;
        fn is_action_available(&mut self, action_number: i16) -> bool {
            if action_number < 128 {
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
            for action in 0..140 {
                if Graph::is_action_available(self, action) {
                    available_actions.push(action);
                }
            }
            available_actions
        }
        fn get_pos(&self, player_number: i16) -> i16;
        fn search(&self, player_number: i16) -> [i16; 81];
        fn display(&self) -> () {
            let mut output_board = String::new();
            let (mut north, mut east, mut south, mut west): (bool, bool, bool, bool);
            let mut pos: i16;
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
                        if self.is_direction_valid(pos, 1) {
                            output_board.push('\u{2502}')
                        } else {
                            output_board.push('\u{2503}')
                        }
                    }
                }
                output_board.push('\n');

                for col in 0..9 {
                    pos = row * 9 + col;
                    if row != 8 {
                        if self.is_direction_valid(pos, 2) {
                            output_board.push_str("\u{2500}\u{2500}\u{2500}")
                        } else {
                            output_board.push_str("\u{2501}\u{2501}\u{2501}")
                        }
                        if col != 8 {
                            north = !self.is_direction_valid(pos, 1);
                            east = !self.is_direction_valid(pos + 1, 2);
                            south = !self.is_direction_valid(pos + 9, 1);
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

        fn bfs(&self, start_pos: i16, player_number: i16) -> [i16; 81] {
            let mut frontier: [i16; 81] = [-1; 81];

            frontier[0] = start_pos;
            let mut head_pointer: usize = 0;
            let mut tail_pointer: usize = 1;

            let mut explored: [bool; 81] = [false; 81];

            let mut in_frontier: [bool; 81] = [false; 81];
            in_frontier[start_pos as usize] = true;

            let mut parent: [i16; 81] = [-1; 81];
            let mut pos: i16;
            let mut new_pos: i16;
            while head_pointer != tail_pointer {
                pos = frontier[head_pointer];
                head_pointer = (head_pointer + 1) % 81;
                in_frontier[pos as usize] = false;

                explored[pos as usize] = true;

                for direction in 0..4 {
                    new_pos = pos + GRAPH_SHIFT_ARR[direction];
                    if self.is_direction_valid(pos, direction as i16)
                        && !explored[new_pos as usize]
                        && !in_frontier[new_pos as usize]
                    {
                        parent[new_pos as usize] = pos;
                        if (player_number == 1 && new_pos <= 8)
                            | (player_number == 2 && new_pos >= 72)
                        {
                            let mut stack: [i16; 81] = [-1; 81];
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
                            let mut path: [i16; 81] = [-1; 81];
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
                        frontier[tail_pointer] = new_pos;
                        tail_pointer = (tail_pointer + 1) % 81;
                        in_frontier[new_pos as usize] = true;
                    }
                }
            }
            return [-1; 81];
        }

        fn dfs(&self, start_pos: i16, player_number: i16) -> [i16; 81] {
            let mut frontier: [i16; 81] = [-1; 81];

            frontier[0] = start_pos;
            let mut tail_pointer: usize = 1;

            let mut explored: [bool; 81] = [false; 81];

            let mut in_frontier: [bool; 81] = [false; 81];
            in_frontier[start_pos as usize] = true;

            let mut parent: [i16; 81] = [-1; 81];
            let mut pos: i16;
            let mut new_pos: i16;
            while 0 != tail_pointer {
                pos = frontier[tail_pointer - 1];
                tail_pointer = (tail_pointer - 1) % 81;
                in_frontier[pos as usize] = false;
                explored[pos as usize] = true;
                for direction in 0..4 {
                    new_pos = pos + GRAPH_SHIFT_ARR[direction];
                    if self.is_direction_valid(pos, direction as i16)
                        && !explored[new_pos as usize]
                        && !in_frontier[new_pos as usize]
                    {
                        parent[new_pos as usize] = pos;
                        if (player_number == 1 && new_pos <= 8)
                            | (player_number == 2 && new_pos >= 72)
                        {
                            let mut stack: [i16; 81] = [-1; 81];
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
                            let mut path: [i16; 81] = [-1; 81];
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
                        frontier[tail_pointer] = new_pos;
                        tail_pointer = (tail_pointer + 1) % 81;
                        in_frontier[new_pos as usize] = true;
                    }
                }
            }
            return [-1; 81];
        }

        fn gbfs(&self, start_pos: i16, player_number: i16) -> [i16; 81] {
            let mut frontier: [i16; 81] = [-1; 81];
            let mut heuristic: [usize; 81] = [255; 81];
            // use heuristic as a key to sort frontier
            frontier[0] = start_pos;
            heuristic[0] = {
                if player_number == 1 {
                    (start_pos / 9) as usize
                } else {
                    (8 - start_pos / 9) as usize
                }
            };

            let mut frontier_count = 1;

            let mut explored: [bool; 81] = [false; 81];

            let mut in_frontier: [bool; 81] = [false; 81];
            in_frontier[start_pos as usize] = true;

            let mut parent: [i16; 81] = [-1; 81];
            let mut pos: i16;
            let mut new_pos: i16;

            let mut heuristic_min_idx: usize;
            let mut heuristic_null_idx: usize;

            while frontier_count != 0 {
                heuristic_min_idx = min_idx(&heuristic);
                pos = frontier[heuristic_min_idx];
                heuristic[heuristic_min_idx] = 255;

                in_frontier[pos as usize] = false;

                explored[pos as usize] = true;
                frontier_count -= 1;
                for direction in 0..4 {
                    new_pos = pos + GRAPH_SHIFT_ARR[direction];
                    if self.is_direction_valid(pos, direction as i16)
                        && !explored[new_pos as usize]
                        && !in_frontier[new_pos as usize]
                    {
                        parent[new_pos as usize] = pos;
                        if (player_number == 1 && new_pos <= 8)
                            | (player_number == 2 && new_pos >= 72)
                        {
                            let mut stack: [i16; 81] = [-1; 81];
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
                            let mut path: [i16; 81] = [-1; 81];
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
                        heuristic_null_idx = find_null(&heuristic);
                        frontier[heuristic_null_idx] = new_pos;
                        heuristic[heuristic_null_idx] = {
                            if player_number == 1 {
                                (new_pos / 9) as usize
                            } else {
                                (8 - new_pos / 9) as usize
                            }
                        };
                        in_frontier[new_pos as usize] = true;
                        frontier_count += 1;
                    }
                }
            }
            return [-1; 81];
        }
        fn astar(&self, start_pos: i16, player_number: i16) -> [i16; 81] {
            let mut frontier: [i16; 81] = [255; 81];

            let mut f_sum: [usize; 81] = [255; 81];
            // index 0 of f_sum is the lowest path_cost of position 0 and so on
            let mut path_cost: [usize; 81] = [255; 81];
            // index 0 of path_cost is the lowest path_cost of position 0 and so on
            frontier[0] = start_pos;
            f_sum[start_pos as usize] = 0 + {
                if player_number == 1 {
                    (start_pos / 9) as usize
                } else {
                    (8 - start_pos / 9) as usize
                }
            };
            path_cost[start_pos as usize] = 0;

            let mut frontier_count = 1;

            let mut in_frontier: [bool; 81] = [false; 81];
            in_frontier[start_pos as usize] = true;

            let mut parent: [i16; 81] = [-1; 81];
            let mut pos: i16;
            let mut new_pos: i16;
            let mut popped_path_cost: usize;

            let mut f_null_idx: usize;

            while frontier_count != 0 {
                pos = min_idx(&f_sum) as i16;
                popped_path_cost = path_cost[pos as usize];
                frontier[find_idx(&frontier, pos)] = -1;

                f_sum[pos as usize] = 255;
                in_frontier[pos as usize] = false;

                frontier_count -= 1;
                for direction in 0..4 {
                    new_pos = pos + GRAPH_SHIFT_ARR[direction];
                    if self.is_direction_valid(pos, direction as i16) {
                        if (player_number == 1 && new_pos <= 8)
                            | (player_number == 2 && new_pos >= 72)
                        {
                            parent[new_pos as usize] = pos;
                            let mut stack: [i16; 81] = [-1; 81];
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
                            let mut path: [i16; 81] = [-1; 81];
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
                        f_null_idx = find_nulli16(&frontier);
                        if popped_path_cost + 1 < path_cost[new_pos as usize] {
                            parent[new_pos as usize] = pos;
                            path_cost[new_pos as usize] = popped_path_cost + 1;
                            f_sum[new_pos as usize] = popped_path_cost + 1 + {
                                if player_number == 1 {
                                    (new_pos / 9) as usize
                                } else {
                                    (8 - new_pos / 9) as usize
                                }
                            };

                            if !in_frontier[new_pos as usize] {
                                frontier[f_null_idx] = new_pos;
                                in_frontier[new_pos as usize] = true;
                                frontier_count += 1;
                            }
                        }
                    }
                }
            }
            return [-1; 81];
        }
    }
    impl QuoridorBoard for RustStaticGraph {
        fn number_actions(&self) -> i16 {
            140
        }
        fn get_available_actions_fast(&mut self) -> Vec<i16> {
            let mut available_actions: Vec<i16> = vec![];
            if self.can_place_wall() {
                let mut path_available: bool = false;
                let mut previous_paths_1: Vec<[i16; 81]> = Vec::new();
                let mut previous_paths_2: Vec<[i16; 81]> = Vec::new();
                let mut path_1: [i16; 81];
                let mut path_2: [i16; 81];
                let mut path_traversed_1: bool;
                let mut path_traversed_2: bool;
                let mut path_valid: bool;
                let mut shift: i16;
                for action_number in 0..128 {
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
                                for idx in 0..81 {
                                    if path[idx + 1] == -1 {
                                        break;
                                    }
                                    shift = path[idx + 1] - path[idx];
                                    if !((shift == -9 && self.is_direction_valid(path[idx], 0))
                                        | (shift == 1 && self.is_direction_valid(path[idx], 1))
                                        | (shift == 9 && self.is_direction_valid(path[idx], 2))
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
                                for idx in 0..81 {
                                    if path[idx + 1] == -1 {
                                        break;
                                    }
                                    shift = path[idx + 1] - path[idx];
                                    if !((shift == -9 && self.is_direction_valid(path[idx], 0))
                                        | (shift == 1 && self.is_direction_valid(path[idx], 1))
                                        | (shift == 9 && self.is_direction_valid(path[idx], 2))
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
            for action_number in 128..140 {
                if self.is_move_valid(action_number) {
                    available_actions.push(action_number);
                }
            }

            available_actions
        }
        fn get_valid_actions(&mut self, mode: i16) -> Vec<i16> {
            if mode == 1 {
                RustStaticGraph::get_available_actions_slow(self)
            } else if mode == 2 {
                RustStaticGraph::get_available_actions_fast(self)
            } else {
                RustStaticGraph::get_available_actions_fast(self)
            }
        }
        fn is_action_available(&mut self, action_number: i16) -> bool {
            Graph::is_action_available(self, action_number)
        }
        fn new(mode: i16) -> RustStaticGraph {
            RustStaticGraph {
                p1_pos: 76,
                p2_pos: 4,
                p1_walls_placed: 0,
                p2_walls_placed: 0,
                turn: 1,
                over: false,
                hor_walls_placed: [false; 64],
                ver_walls_placed: [false; 64],
                mode: mode,
            }
        }
        fn take_action(&mut self, action: i16) {
            if action < 128 {
                if action < 64 {
                    self.hor_walls_placed[action as usize] = true;
                } else {
                    self.ver_walls_placed[(action - 64) as usize] = true;
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
                    self.p1_pos += GRAPH_SHIFT_ARR[(action - 128) as usize];
                    if self.p1_pos <= 8 {
                        self.over = true;
                    } else {
                        self.turn = 2;
                    }
                } else {
                    self.p2_pos += GRAPH_SHIFT_ARR[(action - 128) as usize];
                    if self.p2_pos >= 72 {
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
    impl Graph for RustStaticGraph {
        fn undo_action(&mut self, action: i16) {
            if action < 128 {
                if action < 64 {
                    self.hor_walls_placed[action as usize] = false;
                } else {
                    self.ver_walls_placed[(action - 64) as usize] = false;
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
                    if pos % 9 == 0 {
                        !self.hor_walls_placed[(pos % 9 + 8 * (8 - pos / 9)) as usize]
                    } else if pos % 9 == 8 {
                        !self.hor_walls_placed[(pos % 9 + 8 * (8 - pos / 9) - 1) as usize]
                    } else {
                        !self.hor_walls_placed[(pos % 9 + 8 * (8 - pos / 9) - 1) as usize]
                            && !self.hor_walls_placed[(pos % 9 + 8 * (8 - pos / 9)) as usize]
                    }
                } else if direction == 1 {
                    if pos < 9 {
                        !self.ver_walls_placed[(pos % 9 + (7 - pos / 9) * 8) as usize]
                    } else if pos >= 72 {
                        !self.ver_walls_placed[(pos % 9 + (8 - pos / 9) * 8) as usize]
                    } else {
                        !self.ver_walls_placed[(pos % 9 + (7 - pos / 9) * 8) as usize]
                            && !self.ver_walls_placed[(pos % 9 + (8 - pos / 9) * 8) as usize]
                    }
                } else if direction == 2 {
                    if pos % 9 == 0 {
                        !self.hor_walls_placed[(pos % 9 + 8 * (7 - pos / 9)) as usize]
                    } else if pos % 9 == 8 {
                        !self.hor_walls_placed[(pos % 9 + 8 * (7 - pos / 9) - 1) as usize]
                    } else {
                        !self.hor_walls_placed[(pos % 9 + 8 * (7 - pos / 9) - 1) as usize]
                            && !self.hor_walls_placed[(pos % 9 + 8 * (7 - pos / 9)) as usize]
                    }
                } else if direction == 3 {
                    if pos < 9 {
                        !self.ver_walls_placed[(pos % 9 + (7 - pos / 9) * 8 - 1) as usize]
                    } else if pos >= 72 {
                        !self.ver_walls_placed[(pos % 9 + (8 - pos / 9) * 8 - 1) as usize]
                    } else {
                        !self.ver_walls_placed[(pos % 9 + (7 - pos / 9) * 8 - 1) as usize]
                            && !self.ver_walls_placed[(pos % 9 + (8 - pos / 9) * 8 - 1) as usize]
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

            if move_number < 132 {
                return self.is_direction_valid(in_turn_pos, move_number - 128)
                    && in_turn_pos + GRAPH_SHIFT_ARR[(move_number - 128) as usize] != out_turn_pos;
            } else {
                if move_number % 2 == 0 {
                    return self.is_direction_valid(in_turn_pos, (move_number - 132) / 2)
                        && in_turn_pos + GRAPH_SHIFT_ARR[((move_number - 132) / 2) as usize]
                            == out_turn_pos
                        && self.is_direction_valid(out_turn_pos, (move_number - 132) / 2);
                } else {
                    return (self.is_direction_valid(in_turn_pos, ((move_number - 131) / 2) % 4)
                        && in_turn_pos
                            + GRAPH_SHIFT_ARR[(((move_number - 131) / 2) % 4) as usize]
                            == out_turn_pos
                        && !self.is_direction_valid(out_turn_pos, ((move_number - 131) / 2) % 4)
                        && self.is_direction_valid(out_turn_pos, ((move_number - 133) / 2) % 4))
                        | (self.is_direction_valid(in_turn_pos, ((move_number - 133) / 2) % 4)
                            && in_turn_pos
                                + GRAPH_SHIFT_ARR[(((move_number - 133) / 2) % 4) as usize]
                                == out_turn_pos
                            && !self
                                .is_direction_valid(out_turn_pos, ((move_number - 133) / 2) % 4)
                            && self
                                .is_direction_valid(out_turn_pos, ((move_number - 131) / 2) % 4));
                }
            }
        }
        fn is_wall_valid(&self, wall_number: i16) -> bool {
            if wall_number < 64 {
                if wall_number % 8 == 0 {
                    !self.hor_walls_placed[wall_number as usize]
                        && !self.hor_walls_placed[(wall_number + 1) as usize]
                        && !self.ver_walls_placed[wall_number as usize]
                } else if wall_number % 8 == 7 {
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
                if (wall_number - 64) / 8 == 0 {
                    !self.ver_walls_placed[(wall_number - 64) as usize]
                        && !self.ver_walls_placed[(wall_number - 56) as usize]
                        && !self.hor_walls_placed[(wall_number - 64) as usize]
                } else if (wall_number - 64) / 8 == 7 {
                    !self.ver_walls_placed[(wall_number - 72) as usize]
                        && !self.ver_walls_placed[(wall_number - 64) as usize]
                        && !self.hor_walls_placed[(wall_number - 64) as usize]
                } else {
                    !self.ver_walls_placed[(wall_number - 72) as usize]
                        && !self.ver_walls_placed[(wall_number - 64) as usize]
                        && !self.ver_walls_placed[(wall_number - 56) as usize]
                        && !self.hor_walls_placed[(wall_number - 64) as usize]
                }
            }
        }

        fn can_place_wall(&self) -> bool {
            (self.turn == 1 && self.p1_walls_placed < 10)
                | (self.turn == 2 && self.p2_walls_placed < 10)
        }

        fn get_pos(&self, player_number: i16) -> i16 {
            if player_number == 1 {
                self.p1_pos
            } else {
                self.p2_pos
            }
        }

        fn search(&self, player_number: i16) -> [i16; 81] {
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
            } else if self.mode == 3 {
                if player_number == 1 {
                    self.gbfs(self.p1_pos, 1)
                } else {
                    self.gbfs(self.p2_pos, 2)
                }
            } else if self.mode == 4 {
                if player_number == 1 {
                    self.astar(self.p1_pos, 1)
                } else {
                    self.astar(self.p2_pos, 2)
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
    impl QuoridorBoard for RustDynamicGraph {
        fn number_actions(&self) -> i16 {
            140
        }
        fn get_available_actions_fast(&mut self) -> Vec<i16> {
            let mut available_actions: Vec<i16> = vec![];
            if self.can_place_wall() {
                let mut path_available: bool = false;
                let mut previous_paths_1: Vec<[i16; 81]> = Vec::new();
                let mut previous_paths_2: Vec<[i16; 81]> = Vec::new();
                let mut path_1: [i16; 81];
                let mut path_2: [i16; 81];
                let mut path_traversed_1: bool;
                let mut path_traversed_2: bool;
                let mut path_valid: bool;
                let mut shift: i16;
                for action_number in 0..128 {
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
                                for idx in 0..81 {
                                    if path[idx + 1] == -1 {
                                        break;
                                    }
                                    shift = path[idx + 1] - path[idx];
                                    if !((shift == -9 && self.is_direction_valid(path[idx], 0))
                                        | (shift == 1 && self.is_direction_valid(path[idx], 1))
                                        | (shift == 9 && self.is_direction_valid(path[idx], 2))
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
                                for idx in 0..81 {
                                    if path[idx + 1] == -1 {
                                        break;
                                    }
                                    shift = path[idx + 1] - path[idx];
                                    if !((shift == -9 && self.is_direction_valid(path[idx], 0))
                                        | (shift == 1 && self.is_direction_valid(path[idx], 1))
                                        | (shift == 9 && self.is_direction_valid(path[idx], 2))
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
            for action_number in 128..140 {
                if self.is_move_valid(action_number) {
                    available_actions.push(action_number);
                }
            }

            available_actions
        }
        fn get_valid_actions(&mut self, mode: i16) -> Vec<i16> {
            if mode == 1 {
                RustDynamicGraph::get_available_actions_slow(self)
            } else if mode == 2 {
                RustDynamicGraph::get_available_actions_fast(self)
            } else {
                RustDynamicGraph::get_available_actions_fast(self)
            }
        }
        fn is_action_available(&mut self, action_number: i16) -> bool {
            Graph::is_action_available(self, action_number)
        }
        fn new(mode: i16) -> RustDynamicGraph {
            RustDynamicGraph {
                nodes: [
                    [false, true, true, false],
                    [false, true, true, true],
                    [false, true, true, true],
                    [false, true, true, true],
                    [false, true, true, true],
                    [false, true, true, true],
                    [false, true, true, true],
                    [false, true, true, true],
                    [false, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, true, false],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, true, true, true],
                    [true, false, true, true],
                    [true, true, false, false],
                    [true, true, false, true],
                    [true, true, false, true],
                    [true, true, false, true],
                    [true, true, false, true],
                    [true, true, false, true],
                    [true, true, false, true],
                    [true, true, false, true],
                    [true, false, false, true],
                ],
                p1_pos: 76,
                p2_pos: 4,
                p1_walls_placed: 0,
                p2_walls_placed: 0,
                turn: 1,
                over: false,
                hor_walls_placed: [false; 64],
                ver_walls_placed: [false; 64],
                mode: mode,
            }
        }
        fn take_action(&mut self, action: i16) {
            if action < 128 {
                if action < 64 {
                    self.hor_walls_placed[action as usize] = true;
                    let idx = (action % 8 + 9 * (8 - action / 8)) as usize;
                    self.nodes[idx][0] = false;
                    self.nodes[idx + 1][0] = false;
                    self.nodes[idx - 9][2] = false;
                    self.nodes[idx - 8][2] = false;
                } else {
                    self.ver_walls_placed[(action - 64) as usize] = true;
                    let idx = (action % 8 + 9 * (8 - (action - 64) / 8)) as usize;
                    self.nodes[idx][1] = false;
                    self.nodes[idx + 1][3] = false;
                    self.nodes[idx - 9][1] = false;
                    self.nodes[idx - 8][3] = false;
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
                    self.p1_pos += GRAPH_SHIFT_ARR[(action - 128) as usize];
                    if self.p1_pos <= 8 {
                        self.over = true;
                    } else {
                        self.turn = 2;
                    }
                } else {
                    self.p2_pos += GRAPH_SHIFT_ARR[(action - 128) as usize];
                    if self.p2_pos >= 72 {
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
    impl Graph for RustDynamicGraph {
        fn undo_action(&mut self, action: i16) {
            if action < 128 {
                if action < 64 {
                    self.hor_walls_placed[action as usize] = false;
                    let idx = (action % 8 + 9 * (8 - action / 8)) as usize;
                    self.nodes[idx][0] = true;
                    self.nodes[idx + 1][0] = true;
                    self.nodes[idx - 9][2] = true;
                    self.nodes[idx - 8][2] = true;
                } else {
                    self.ver_walls_placed[(action - 64) as usize] = false;
                    let idx = (action % 8 + 9 * (8 - (action - 64) / 8)) as usize;
                    self.nodes[idx][1] = true;
                    self.nodes[idx + 1][3] = true;
                    self.nodes[idx - 9][1] = true;
                    self.nodes[idx - 8][3] = true;
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

            if move_number < 132 {
                return self.is_direction_valid(in_turn_pos, move_number - 128)
                    && in_turn_pos + GRAPH_SHIFT_ARR[(move_number - 128) as usize] != out_turn_pos;
            } else {
                if move_number % 2 == 0 {
                    return self.is_direction_valid(in_turn_pos, (move_number - 132) / 2)
                        && in_turn_pos + GRAPH_SHIFT_ARR[((move_number - 132) / 2) as usize]
                            == out_turn_pos
                        && self.is_direction_valid(out_turn_pos, (move_number - 132) / 2);
                } else {
                    return (self.is_direction_valid(in_turn_pos, ((move_number - 131) / 2) % 4)
                        && in_turn_pos
                            + GRAPH_SHIFT_ARR[(((move_number - 131) / 2) % 4) as usize]
                            == out_turn_pos
                        && !self.is_direction_valid(out_turn_pos, ((move_number - 131) / 2) % 4)
                        && self.is_direction_valid(out_turn_pos, ((move_number - 133) / 2) % 4))
                        | (self.is_direction_valid(in_turn_pos, ((move_number - 133) / 2) % 4)
                            && in_turn_pos
                                + GRAPH_SHIFT_ARR[(((move_number - 133) / 2) % 4) as usize]
                                == out_turn_pos
                            && !self
                                .is_direction_valid(out_turn_pos, ((move_number - 133) / 2) % 4)
                            && self
                                .is_direction_valid(out_turn_pos, ((move_number - 131) / 2) % 4));
                }
            }
        }
        fn is_wall_valid(&self, wall_number: i16) -> bool {
            if wall_number < 64 {
                if wall_number % 8 == 0 {
                    !self.hor_walls_placed[wall_number as usize]
                        && !self.hor_walls_placed[(wall_number + 1) as usize]
                        && !self.ver_walls_placed[wall_number as usize]
                } else if wall_number % 8 == 7 {
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
                if (wall_number - 64) / 8 == 0 {
                    !self.ver_walls_placed[(wall_number - 64) as usize]
                        && !self.ver_walls_placed[(wall_number - 56) as usize]
                        && !self.hor_walls_placed[(wall_number - 64) as usize]
                } else if (wall_number - 64) / 8 == 7 {
                    !self.ver_walls_placed[(wall_number - 72) as usize]
                        && !self.ver_walls_placed[(wall_number - 64) as usize]
                        && !self.hor_walls_placed[(wall_number - 64) as usize]
                } else {
                    !self.ver_walls_placed[(wall_number - 72) as usize]
                        && !self.ver_walls_placed[(wall_number - 64) as usize]
                        && !self.ver_walls_placed[(wall_number - 56) as usize]
                        && !self.hor_walls_placed[(wall_number - 64) as usize]
                }
            }
        }
        fn can_place_wall(&self) -> bool {
            (self.turn == 1 && self.p1_walls_placed < 10)
                | (self.turn == 2 && self.p2_walls_placed < 10)
        }
        fn get_pos(&self, player_number: i16) -> i16 {
            if player_number == 1 {
                self.p1_pos
            } else {
                self.p2_pos
            }
        }
        fn search(&self, player_number: i16) -> [i16; 81] {
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
            } else if self.mode == 3 {
                if player_number == 1 {
                    self.gbfs(self.p1_pos, 1)
                } else {
                    self.gbfs(self.p2_pos, 2)
                }
            } else if self.mode == 4 {
                if player_number == 1 {
                    self.astar(self.p1_pos, 1)
                } else {
                    self.astar(self.p2_pos, 2)
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
