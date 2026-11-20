#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复算《润泽说 道可道之数字学（整理稿）》中全部可验证命题。

用法：python3 scripts/verify.py
全部通过则退出码 0；任一失败则报出该条并以 1 退出。
"""

FAILS = []


def dr(n: int) -> int:
    """数字根：各位相加至一位。"""
    n = abs(int(n))
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def check(name: str, got, want):
    ok = got == want
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}: got={got} want={want}")
    if not ok:
        FAILS.append((name, got, want))


def line_sums(m):
    """取九宫的全部线：三行、三列、两对角。"""
    rows = [sum(r) for r in m]
    cols = [sum(m[r][c] for r in range(3)) for c in range(3)]
    d1 = m[0][0] + m[1][1] + m[2][2]
    d2 = m[0][2] + m[1][1] + m[2][0]
    return rows + cols + [d1, d2]


def line_root_set(m):
    return {dr(s) for s in line_sums(m)}


def main():
    # ---------- 一、数字根 ----------
    check("54871 各位和", sum(map(int, "54871")), 25)
    check("54871 数字根", dr(54871), 7)
    check("95824 数字根", dr(95824), 1)
    check("400 / 121 同根", (dr(400), dr(121)), (4, 4))

    # ---------- 二、十二周期 ----------
    groups = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    sums = [sum(g) for g in groups]
    roots = [dr(s) for s in sums]
    diffs = [sums[i + 1] - sums[i] for i in range(3)]
    check("十二周期 组和", sums, [6, 15, 24, 33])
    check("十二周期 组根恒 6", roots, [6, 6, 6, 6])
    check("十二周期 组间恒差 9", diffs, [9, 9, 9])

    tri = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    check("147/258/369 根", [dr(sum(g)) for g in tri], [3, 6, 9])

    # ---------- 三、九宫幻方 ----------
    M3 = [[3, 8, 1], [5, 7, 9], [4, 6, 2]]
    M6 = [[8, 3, 4], [1, 5, 9], [6, 7, 2]]
    M9 = [[8, 4, 6], [1, 3, 5], [9, 2, 7]]

    check("三幻方 线根集合", line_root_set(M3), {3})
    check("三幻方 线和集合", sorted(set(line_sums(M3))), [12, 21])
    check("三幻方 中心", M3[1][1], 7)

    check("六幻方 线根集合", line_root_set(M6), {6})
    check("六幻方 严格等和(15)", sorted(set(line_sums(M6))), [15])
    check("六幻方 中心", M6[1][1], 5)

    check("九幻方 线根集合", line_root_set(M9), {9})
    check("九幻方 线和集合", sorted(set(line_sums(M9))), [9, 18])
    check("九幻方 中心", M9[1][1], 3)

    # 三行/三列相乘取根：每图各走完 3、6、9 全套（不含对角）
    for nm, m in (("三", M3), ("六", M6), ("九", M9)):
        row_mul = {dr(r[0] * r[1] * r[2]) for r in m}
        col_mul = {dr(m[0][c] * m[1][c] * m[2][c]) for c in range(3)}
        check(f"{nm}幻方 行乘积根走全 3/6/9", row_mul, {3, 6, 9})
        check(f"{nm}幻方 列乘积根走全 3/6/9", col_mul, {3, 6, 9})

    # 十二道映射
    check("十二道映射", (7 + 3, 5 + 6, 3 + 9), (10, 11, 12))

    # ---------- 四、142857 ----------
    BASE = 142857
    perms = sorted(str(BASE * k) for k in range(1, 7))
    check("142857×1..6 均为六位", all(len(s) == 6 for s in perms), True)
    check("142857×1..6 数字集合相同",
          {tuple(sorted(s)) for s in perms}, {tuple(sorted("142857"))})
    check("142857×1..6 各位和恒 27",
          {sum(int(c) for c in s) for s in perms}, {27})
    check("142857×1..6 数字根恒 9",
          {dr(BASE * k) for k in range(1, 7)}, {9})
    check("142857×7", BASE * 7, 999999)
    check("1/7 循环节", (1 / 7), 0.14285714285714285)
    check("22/7 整数与小数的前三", (22 // 7, str(22 / 7)[2:9]), (3, "1428571"))

    # ---------- 五、对称与零位移 ----------
    check("配对和恒 9", [(a + b) for a, b in [(1, 8), (2, 7), (3, 6), (4, 5)]], [9, 9, 9, 9])
    check("加九根不变", all(dr(n + 9) == dr(n) for n in range(1, 100)), True)
    check("乘九根恒 9", {dr(n * 9) for n in range(1, 100)}, {9})

    # ---------- 六、7×4×1 ----------
    check("7×4×1 归 1", dr(7 * 4 * 1), 1)

    print("\n" + "=" * 52)
    if FAILS:
        print(f"失败 {len(FAILS)} 条：")
        for f in FAILS:
            print("  -", f)
        raise SystemExit(1)
    print("全部命题通过。")


if __name__ == "__main__":
    main()
