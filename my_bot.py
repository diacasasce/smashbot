import melee
from bot import Bot
import numpy as np
import os


class MyCustomBot(Bot):
    ACTION_MOVE_LEFT = 0
    ACTION_MOVE_RIGHT = 1
    ACTION_JUMP = 2
    ACTION_ATTACK = 3
    ACTION_DEFEND = 4
    num_actions = 5

    num_states = 10

    def __init__(self, port, character, costume, console):
        super().__init__(port, character, costume, console)
        self.last_gamestate = None
        self.Q_file = 'matriz_q.npy'
        if os.path.exists(self.Q_file):
            self.Q = np.load(self.Q_file)
        else:
            self.Q = np.zeros((self.num_states, self.num_actions))
        self.last_gamestate = None

    def choose_action(self, state, epsilon=1.0):
        if np.random.rand() < epsilon:
            return np.random.choice(self.num_actions)
        return np.argmax(self.Q[state])

    def update_Q(self, state, action, reward, new_state, alpha=0.1, gamma=0.9):
        best_prediction = np.max(self.Q[new_state])
        current_value = self.Q[state, action]
        self.Q[state, action] += alpha * (reward + gamma * best_prediction - current_value)
        np.save(self.Q_file, self.Q)

    def execute_action(self, action, gamestate):
        my_state = gamestate.players[self.port]
        enemy_state = gamestate.players[1 if self.port != 1 else 2]
        stage = gamestate.stage
        edge_position = melee.stages.EDGE_POSITION[stage]

        is_facing_enemy = (my_state.facing and my_state.position.x < enemy_state.position.x) or (
                    not my_state.facing and my_state.position.x > enemy_state.position.x)

        if (action == self.ACTION_MOVE_LEFT and my_state.position.x < -edge_position + 10) or \
                (action == self.ACTION_MOVE_RIGHT and my_state.position.x > edge_position - 10):
            action = np.random.choice([self.ACTION_MOVE_RIGHT, self.ACTION_MOVE_LEFT, self.ACTION_JUMP])

        self.controller.release_all()

        if action == self.ACTION_MOVE_LEFT:
            self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0, 0.5)
        elif action == self.ACTION_MOVE_RIGHT:
            self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 1, 0.5)
        elif action == self.ACTION_JUMP:
            self.controller.press_button(melee.enums.Button.BUTTON_Y)
        elif action == self.ACTION_ATTACK:
            if gamestate.distance < 25 and is_facing_enemy:
                self.controller.press_button(melee.enums.Button.BUTTON_A)
        elif action == self.ACTION_DEFEND:
            if gamestate.distance < 8 and enemy_state.action in [melee.enums.Action.NEUTRAL_ATTACK_1,
                                                                 melee.enums.Action.DASH_ATTACK,
                                                                 melee.enums.Action.FSMASH_MID]:
                self.controller.press_button(melee.enums.Button.BUTTON_R)

    def play(self, gamestate):
        if self.last_gamestate is None:
            self.last_gamestate = gamestate
            return

        current_state = self.discretize_state(gamestate)
        action = self.choose_action(current_state)

        self.execute_action(action, gamestate)

        new_state = self.discretize_state(gamestate)
        reward = self.calculate_reward(gamestate, self.last_gamestate)
        self.update_Q(current_state, action, reward, new_state)

        self.last_gamestate = gamestate

    def discretize_state(self, gamestate):
        my_state = gamestate.players[self.port]
        enemy_state = gamestate.players[1 if self.port != 1 else 2]

        distance_to_enemy = abs(my_state.position.x - enemy_state.position.x)
        is_enemy_attacking = enemy_state.action in [melee.enums.Action.NEUTRAL_ATTACK_1,
                                                    melee.enums.Action.DASH_ATTACK]

        if distance_to_enemy < 10:
            distance = 0
        elif distance_to_enemy < 30:
            distance = 1
        else:
            distance = 2

        enemy_action = 1 if is_enemy_attacking else 0

        discretized_state = distance * 2 + enemy_action
        return discretized_state

    def calculate_reward(self, gamestate, last_gamestate):
        my_state = gamestate.players[self.port]
        enemy_state = gamestate.players[1 if self.port != 1 else 2]

        last_my_state = last_gamestate.players[self.port]
        last_enemy_state = last_gamestate.players[1 if self.port != 1 else 2]

        stage = gamestate.stage
        edge_position = melee.stages.EDGE_POSITION[stage]

        reward = 0
        if enemy_state.percent > last_enemy_state.percent:
            reward += 4

        if my_state.percent > last_my_state.percent:
            reward -= 2

        if abs(my_state.position.x) > edge_position - 12:
            reward -= 4

        if enemy_state.stock < last_enemy_state.stock:
            reward += 5

        if enemy_state.stock > last_enemy_state.stock:
            reward -= 5

        return reward
