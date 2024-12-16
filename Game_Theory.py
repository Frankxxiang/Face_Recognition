
def to_move(self, state):
        # 返回当前轮到哪个玩家
        pass
    
def is_terminal(self, state):
        # 判断当前状态是否为终止状态
        pass
    
def utility(self, state, player):
        # 返回当前状态的效用值
        pass
    
def actions(self, state):
        # 返回当前状态的所有可能动作
        pass
    
def result(self, state, action):
        # 返回执行动作后的新状态
        pass

def minimax_search(game, state):
    player = game.to_move(state)
    value, move = max_value(game, state)
    return move

def max_value(game, state):
    if game.is_terminal(state):
        return game.utility(state, game.to_move(state)), None
    v = float('-inf')
    move = None
    for a in game.actions(state):
        v2, a2 = min_value(game, game.result(state, a))
        if v2 > v:
            v, move = v2, a
    return v, move

def min_value(game, state):
    if game.is_terminal(state):
        return game.utility(state, game.to_move(state)), None
    v = float('inf')
    move = None
    for a in game.actions(state):
        v2, a2 = max_value(game, game.result(state, a))
        if v2 < v:
            v, move = v2, a
    return v, move
