from collections import deque

def pos_to_coord(pos):
    """将棋盘位置转换为坐标"""
    return ord(pos[0]) - ord('A'), pos[1]-1

def is_valid_coord(coord, board_size):
    """检查坐标是否在棋盘上"""
    x, y = coord
    return 0 <= x < board_size[1] and 0 <= y < board_size[0]

def is_valid_state(state, board_size):
    """检查新状态是否有效：没有棋子重叠"""
    positions = [pos[:2] for pos in state]  # 只考虑坐标部分
    return len(positions) == len(set(positions))

def bfs_path(start, target, board_size, knight_moves):
    """广度优先搜索，找到最短路径并考虑棋子不重叠的约束"""
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        current_state, path = queue.popleft()
        if current_state == target:
            return path

        for i in range(6):
            knight_pos, color = current_state[i][:2], current_state[i][2]
            for move in knight_moves:
                new_pos = (knight_pos[0] + move[0], knight_pos[1] + move[1])
                if is_valid_coord(new_pos, board_size):
                    new_state = list(current_state)
                    new_state[i] = (new_pos[0], new_pos[1], color)
                    new_state = tuple(sorted(new_state, key=lambda x: (x[2], x[0], x[1])))
                    if new_state not in visited and is_valid_state(new_state, board_size):
                        queue.append((new_state, path + [new_state]))
                        visited.add(new_state)
    return []

def print_board_table(state, board_size):
    """打印当前棋盘状态为表格形式"""
    board = [['E' for _ in range(board_size[1])] for _ in range(board_size[0])]
    for pos in state:
        x, y, color = pos
        board[y][x] = 'R' if color == 'Red' else 'B'
    table = "    A   B   C\n  +---+---+---+\n"
    for y in range(board_size[0]-1, -1, -1):
        row = f"{y+1} | " + " | ".join(board[y]) + " |"
        table += row + "\n  +---+---+---+\n"
    return table

def main():
    board_size = (4, 3)
    start_positions = [('A', 1, 'Red'), ('B', 1, 'Red'), ('C', 1, 'Red'),
                       ('A', 4, 'Blue'), ('B', 4, 'Blue'), ('C', 4, 'Blue')]
    target_positions = [('A', 1, 'Blue'), ('B', 1, 'Blue'), ('C', 1, 'Blue'),
                        ('A', 4, 'Red'), ('B', 4, 'Red'), ('C', 4, 'Red')]
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    start_state = tuple(sorted([pos_to_coord(pos) + (pos[2],) for pos in start_positions], key=lambda x: (x[2], x[0], x[1])))
    target_state = tuple(sorted([pos_to_coord(pos) + (pos[2],) for pos in target_positions], key=lambda x: (x[2], x[0], x[1])))

    path = bfs_path(start_state, target_state, board_size, knight_moves)

    for state in path:
        print(print_board_table(state, board_size))
    print(len(path)-1)

if __name__ == "__main__":
    main()
