using System;
using System.Collections;
using System.Collections.Generic;

public class Point
{
    public int x;
    public int y;
    public Point(int _x, int _y)
    {
        this.x = _x;
        this.y = _y;
    }
}
public class History
{
    public List<Point> Path;
    public List<Point> Children;
    public History(List<Point> p, List<Point> c)
    {
        this.Path = p;
        this.Children = c;
    }
}

public class PathFinder
{
    public PathFinder() { }

    // if v is less then min wrap reflect it to the max size
    // if v is greater than max, reflect it to the mind size
    // Examples:
    //   3 with a min of 0 max of 2 becomes 0
    //   -1 with a min of 0 max of 2 becomes 2.
    private static int ConstrainCircular(int v, int min, int max)
    {
        if (v < min)
        {
            return max + v + min;
        }
        else if (v > max - 1)
        {
            return max - v + min;
        }
        return v;
    }

    public static List<Point> GetAdjacent(Point p, Point size)
    {
        List<int> directions = new List<int>() {1, 0, -1 };
        List<Point> points = new List<Point>();

        for (int i = 0; i < directions.Count; i++)
        {
            for (int j = 0; j < directions.Count; j++)
            {
                Point adj = new Point(p.x + directions[i],
                  p.y + directions[j]);
                // don't add without any offset
                if (adj.x == p.x && adj.y == p.y)
                {
                    continue;
                }
                adj.x = ConstrainCircular(adj.x, 0, size.x);
                adj.y = ConstrainCircular(adj.y, 0, size.y);
                points.Add(adj);
            }
        }
        return points;
    }

    public static Dictionary<string, List<Point>> GetBoardLookup(
      string[][] board)
    {
        Dictionary<string, List<Point>> lookup = new Dictionary<string, List<Point>>();

        for (int i = 0; i < board.Length; i++)
        {
            for (int j = 0; j < board[i].Length; j++)
            {
                string letter = board[i][j];
                if (!lookup.ContainsKey(letter))
                {
                    lookup[letter] = new List<Point>();
                }
                lookup[letter].Add(new Point(i, j));
            }
        }
        return lookup;
    }

    public static List<List<Point>> GetActiveCells(string text, string[][] board)
    {
        Dictionary<string, List<Point>> boardLookup = GetBoardLookup(board);
        Point s = new Point(board.Length, board[0].Length);
        string first = text.Substring(0, 1);
        List<History> histories = new List<History>();

        if (boardLookup.ContainsKey(first))
        {
            List<Point> starts = boardLookup[first];
            for (int i = 0; i < starts.Count; i++)
            {
                histories.Add(new History(
                  new List<Point> {
            starts[i]
                  },
                  GetAdjacent(starts[i], s)));
            }
        }
        string pattern = text.Substring(1);
        while (histories.Count > 0 && pattern.Length > 0)
        {
            List<History> nextHistories = new List<History>();

            for (int i = 0; i < histories.Count; i++)
            {
                first = pattern.Substring(0, 1);
                for (int c = 0; c < histories[i].Children.Count; c++)
                {
                    Point p = histories[i].Children[c];
                    if (board[p.x][p.y] == first)
                    {
                        History h = new History(
                          new List<Point>(histories[i].Path),
                          GetAdjacent(p, s));

                        h.Path.Add(p);
                        nextHistories.Add(h);
                    }
                }
            }
            histories = nextHistories;
            pattern = pattern.Substring(1);
        }

        List<List<Point>> paths = new List<List<Point>>();
        for (int i = 0; i < histories.Count; i++)
        {
            paths.Add(histories[i].Path);
        }
        return paths;
    }

}