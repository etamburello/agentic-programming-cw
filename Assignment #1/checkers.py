def alternate(board, start=0, n=None):
    """Rearrange board[start:start+2n] from n reds then n blacks into 0,1,0,1,...,0,1."""
    if n is None:
        n = len(board) // 2

    def rec(start, n):
        if n <= 1:
            return
        rec(start + 1, n - 1)
        i = start + 1
        last = start + 2 * n - 1
        while i < last:
            board[i], board[i + 1] = board[i + 1], board[i]
            i += 2

    rec(start, n)
