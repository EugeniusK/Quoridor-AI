pub mod final_mcts {
    extern crate rand;
    extern crate rand_chacha;
    use ordered_float::NotNan;
    pub use rand_chacha::ChaCha8Rng;

    use crate::final_board::final_board::RustBoard;
    use std::time::Instant;

    #[derive(Clone, Debug, Copy)]
    pub struct ActionIdx {
        pub action: i16,
        pub idx: u32,
    }
    #[derive(Debug)]
    pub struct MctsNode {
        pub action: i16,
        pub idx: u32,
        pub parent_idx: u32,

        pub simulations_won: f32,
        pub simulations_run: f32,

        pub children_action_idx: Vec<ActionIdx>,
        pub actions_not_performed: Vec<i16>,
        pub is_leaf: bool,
    }

    pub struct MctsTree {
        pub nodes: Vec<MctsNode>,
        exploration_weight: f32,
        pub board: RustBoard,
    }

    pub fn arr_actions_to_vec(arr: [bool; 140]) -> Vec<i16> {
        let mut output_vec: Vec<i16> = vec![];
        for action in 0..140 {
            if arr[action] {
                output_vec.push(action as i16)
            }
        }
        output_vec
    }
    impl MctsTree {
        pub fn new(mut board: RustBoard) -> MctsTree {
            MctsTree {
                nodes: vec![MctsNode {
                    action: -1,
                    idx: 0,
                    parent_idx: 0,

                    simulations_run: 0.0,
                    simulations_won: 0.0,

                    children_action_idx: vec![],
                    actions_not_performed: board.get_available_actions_fast(),

                    is_leaf: true,
                }],
                exploration_weight: 2.0,
                board: board,
            }
        }

        pub fn clear(&mut self) -> () {
            self.nodes.clear();
        }

        pub fn reset_tree(&mut self, mut board: RustBoard) -> () {
            self.nodes.clear();
            self.nodes = vec![MctsNode {
                action: -1,
                idx: 0,
                parent_idx: 0,

                simulations_run: 0.0,
                simulations_won: 0.0,

                children_action_idx: vec![],
                actions_not_performed: board.get_available_actions_fast(),

                is_leaf: true,
            }];
            self.board = board;
        }

        pub fn get_board_state(&self, idx: usize) -> RustBoard {
            let mut actions: Vec<i16> = vec![];
            let mut board_actions_applied: RustBoard = self.board.clone();
            let mut action: i16;
            let mut node_idx: usize = idx;
            while self.nodes[node_idx].action != -1 {
                action = self.nodes[node_idx].action;
                actions.push(action);
                node_idx = self.nodes[node_idx].parent_idx as usize;
            }
            for action_idx in (0..actions.len()).rev() {
                board_actions_applied.take_action(actions[action_idx]);
            }
            board_actions_applied
        }

        pub fn select(&self) -> usize {
            let mut selected_idx: usize = 0;
            let calculate_uct = |idx: &u32| -> NotNan<f32> {
                if self.nodes[*idx as usize].simulations_run == 0.0 {
                    match NotNan::new(f32::INFINITY) {
                        Ok(result) => return result,
                        Err(_) => panic!("NAN in MCTS calculation"),
                    }
                }

                match NotNan::new(
                    self.nodes[*idx as usize].simulations_won
                        / self.nodes[*idx as usize].simulations_run
                        + (self.exploration_weight
                            * self.nodes[self.nodes[*idx as usize].parent_idx as usize]
                                .simulations_run
                                .ln()
                            / self.nodes[*idx as usize].simulations_run)
                            .sqrt(),
                ) {
                    Ok(result) => result,
                    Err(_) => panic!("NAN in MCTS calculation"),
                }
            };
            loop {
                if (self.nodes[selected_idx].actions_not_performed.len() != 0)
                    | self.nodes[selected_idx].is_leaf
                {
                    return selected_idx;
                }
                match self.nodes[selected_idx]
                    .children_action_idx
                    .iter()
                    .map(|x: &ActionIdx| x.idx)
                    .filter(|&x| x != 0)
                    .max_by_key(calculate_uct)
                {
                    Some(idx) => selected_idx = idx as usize,
                    None => panic!("NO CHILD NODE"),
                }
            }
        }

        pub fn expand(&mut self, idx: usize) {
            let mut board_state = self.get_board_state(idx);

            if self.nodes[idx].actions_not_performed.len() != 0 {
                let action = self.nodes[idx].actions_not_performed.pop().unwrap();
                board_state.take_action(action);

                self.nodes[idx].is_leaf = false;

                let child_idx: usize = self.nodes.len();
                if board_state.is_over() {
                    self.nodes.push(MctsNode {
                        action: action as i16,
                        idx: child_idx as u32,
                        parent_idx: idx as u32,

                        simulations_run: 0.0,
                        simulations_won: 0.0,

                        children_action_idx: vec![],
                        actions_not_performed: vec![],

                        is_leaf: true,
                    });
                } else {
                    self.nodes.push(MctsNode {
                        action: action as i16,
                        idx: child_idx as u32,
                        parent_idx: idx as u32,

                        simulations_run: 0.0,
                        simulations_won: 0.0,

                        children_action_idx: vec![],
                        actions_not_performed: board_state.get_available_actions_fast(),

                        is_leaf: true,
                    });
                }
                self.nodes[idx].children_action_idx.push(ActionIdx {
                    action: action as i16,
                    idx: child_idx as u32,
                })
            }
        }

        pub fn simulate(&self, idx: usize) -> f32 {
            let mut board = self.get_board_state(idx);

            let mut action: i16;
            while !board.is_over() {
                action = board.get_random_action();
                board.take_action(action);
            }
            if board.get_turn() == self.get_board_state(idx).get_turn() {
                1.0
            } else if board.get_turn() == 3 - self.get_board_state(idx).get_turn() {
                0.0
            } else {
                0.5
            }
        }

        pub fn backpropagate(&mut self, mut idx: u32, mut result: f32) {
            let mut parent_idx: u32 = self.nodes[idx as usize].parent_idx;
            loop {
                self.nodes[idx as usize].simulations_run += 1.0;
                self.nodes[idx as usize].simulations_won += result;
                if idx + parent_idx == 0 {
                    break;
                }
                result = 1.0 - result;
                idx = parent_idx;
                parent_idx = self.nodes[idx as usize].parent_idx;
            }
        }

        pub fn rollout_choose_timed(&mut self, limit: f64) -> (i16, i32) {
            let mut leaf: usize;
            let start: Instant = Instant::now();
            let mut count = 0;
            while start.elapsed().as_secs_f64() < limit {
                leaf = self.select();
                self.expand(leaf);
                let result = self.simulate(self.nodes.len() - 1);
                self.backpropagate(leaf as u32, result);
                count += 1;
            }
            let calculate_winrate = |x: &u32| -> NotNan<f32> {
                match NotNan::new(
                    self.nodes[*x as usize].simulations_won
                        / self.nodes[*x as usize].simulations_run,
                ) {
                    Ok(result) => return result,
                    Err(_) => return NotNan::new(0.0).unwrap(),
                }
            };
            match self.nodes[0]
                .children_action_idx
                .iter()
                .map(|x| x.idx)
                .max_by_key(calculate_winrate)
            {
                Some(result) => {
                    return (self.nodes[result as usize].action, count);
                }
                None => panic!("NO RETURN"),
            }
        }
        pub fn random_choose(&mut self) -> i16 {
            self.board.get_random_action()
        }
    }
}
