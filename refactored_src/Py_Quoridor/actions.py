GraphShiftDict = {
    128: -9,
    129: 1,
    130: 9,
    131: -1,
    132: -18,
    133: -8,
    134: 2,
    135: 10,
    136: 18,
    137: 8,
    138: -2,
    139: -10,
}

ActionStringDict = {
    128: "N",
    129: "E",
    130: "S",
    131: "W",
    132: "NN",
    133: "NE",
    134: "EE",
    135: "SE",
    136: "SS",
    137: "SW",
    138: "WW",
    139: "NW",
}


def get_available_actions_1(self) -> list:
    return [x for x in range(140) if is_action_available(self, x) != None]


def get_available_actions_2(self) -> list:
    available_actions = []

    previous_valid_paths = []
    previous_valid_paths_1 = []
    previous_valid_paths_2 = []

    walls_valid = False
    if self.turn == 1 and self.p1_walls_placed < 10:
        walls_valid = True
    elif self.turn == 2 and self.p2_walls_placed < 10:
        walls_valid = True

    if walls_valid:
        for action_number in range(128):
            # validate walls
            if self.is_wall_valid(action_number):
                if len(previous_valid_paths) == 0:
                    self.take_action(action_number)
                    path_1 = self.search(self.p1_pos, 1)
                    path_2 = self.search(self.p2_pos, 2)

                    if path_1 is not None and path_2 is not None:
                        previous_valid_paths_1.append(path_1)
                        previous_valid_paths_2.append(path_2)
                        available_actions.append(action_number)
                    self.undo_action(action_number)

                else:
                    self.take_action(action_number)

                    path_traversed_1 = False
                    for path in previous_valid_paths_1:
                        for idx in range(len(path) - 1):
                            shift = path[idx + 1] - path[idx]
                            if path[idx + 1] == -1 or path[idx] == -1:
                                break
                            if shift == -9 and not self.is_direction_valid(
                                path[idx], 0
                            ):
                                break
                            elif shift == 1 and not self.is_direction_valid(
                                path[idx], 1
                            ):
                                break
                            elif shift == 9 and not self.is_direction_valid(
                                path[idx], 2
                            ):
                                break
                            elif shift == -1 and not self.is_direction_valid(
                                path[idx], 3
                            ):
                                break
                        else:
                            path_traversed_1 = True
                            break

                    path_traversed_2 = False
                    for path in previous_valid_paths_2:
                        for idx in range(len(path) - 1):
                            shift = path[idx + 1] - path[idx]
                            if path[idx + 1] == -1 or path[idx] == -1:
                                break
                            if shift == -9 and not self.is_direction_valid(
                                path[idx], 0
                            ):
                                break
                            elif shift == 1 and not self.is_direction_valid(
                                path[idx], 1
                            ):
                                break
                            elif shift == 9 and not self.is_direction_valid(
                                path[idx], 2
                            ):
                                break
                            elif shift == -1 and not self.is_direction_valid(
                                path[idx], 3
                            ):
                                break
                        else:
                            path_traversed_2 = True
                            break

                    if path_traversed_1 and path_traversed_2:
                        available_actions.append(action_number)
                    else:
                        if not path_traversed_1:
                            path_1 = self.search(self.p1_pos, 1)
                            if path_1 is not None:
                                previous_valid_paths_1.append(path)
                        if not path_traversed_2:
                            path_2 = self.search(self.p2_pos, 2)
                            if path_2 is not None:
                                previous_valid_paths_2.append(path)
                        if path_1 is not None and path_2 is not None:
                            available_actions.append(action_number)
                    self.undo_action(action_number)

    if self.turn == 1:
        in_turn_pos, out_turn_pos = self.p1_pos, self.p2_pos
    else:
        in_turn_pos, out_turn_pos = self.p2_pos, self.p1_pos

    for action_number in range(128, 132):
        if self.is_direction_valid(in_turn_pos, action_number - 128):
            if in_turn_pos + GraphShiftDict[action_number] != out_turn_pos:
                available_actions.append(action_number)
            else:
                direction = action_number - 128
                if self.is_direction_valid(out_turn_pos, direction):
                    available_actions.append(132 + 2 * direction)
                else:
                    if self.is_direction_valid(out_turn_pos, (direction + 1) % 4):
                        available_actions.append(132 + (2 * direction + 1) % 8)
                    if self.is_direction_valid(out_turn_pos, (direction - 1) % 4):
                        available_actions.append(132 + (2 * direction - 1) % 8)
    return available_actions


def is_action_available(self, action_number):
    if action_number < 128:
        walls_valid = False
        if self.turn == 1 and self.p1_walls_placed < 10:
            walls_valid = True
        elif self.turn == 2 and self.p2_walls_placed < 10:
            walls_valid = True
        if walls_valid and self.is_wall_valid(action_number):
            self.take_action(action_number)
            path_1 = self.search(self.p1_pos, 1)
            path_2 = self.search(self.p2_pos, 2)
            # print(action_number, path_1, path_2)

            if path_1 is not None and path_2 is not None:
                self.undo_action(action_number)
                return action_number
            self.undo_action(action_number)
    else:
        if self.turn == 1:
            in_turn_pos, out_turn_pos = self.p1_pos, self.p2_pos
        else:
            in_turn_pos, out_turn_pos = self.p2_pos, self.p1_pos

        if action_number < 132:
            if self.is_direction_valid(in_turn_pos, action_number - 128):
                if in_turn_pos + GraphShiftDict[action_number] != out_turn_pos:
                    return action_number
        else:
            if action_number % 2 == 0:
                if (
                    self.is_direction_valid(in_turn_pos, (action_number - 132) // 2)
                    and in_turn_pos + GraphShiftDict[128 + (action_number - 132) // 2]
                    == out_turn_pos
                    and self.is_direction_valid(
                        out_turn_pos, (action_number - 132) // 2
                    )
                ):
                    return action_number
            else:
                dir1 = ((action_number - 131) // 2) % 4
                dir2 = ((action_number - 133) // 2) % 4
                if (
                    self.is_direction_valid(in_turn_pos, dir1)
                    and in_turn_pos + GraphShiftDict[128 + dir1] == out_turn_pos
                    and not self.is_direction_valid(out_turn_pos, dir1)
                    and self.is_direction_valid(out_turn_pos, dir2)
                ) or (
                    self.is_direction_valid(in_turn_pos, dir2)
                    and in_turn_pos + GraphShiftDict[128 + dir2] == out_turn_pos
                    and not self.is_direction_valid(out_turn_pos, dir2)
                    and self.is_direction_valid(out_turn_pos, dir1)
                ):
                    return action_number
    return
