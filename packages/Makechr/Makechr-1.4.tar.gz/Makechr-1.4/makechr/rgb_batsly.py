COLOR_TOLERANCE = 64


# From: http://www.thealmightyguru.com/Games/Hacking/Wiki/index.php?title=NES_Palette
                # 00        10        20        30
RGB_COLORS = [  [0x666765,0xb1b1af,0xffffff,0xffffff],
                [0x001f9d,0x0855ea,0x4dadff,0xbae5ff],
                [0x210dad,0x473dff,0x8795ff,0xd1dbff],
                [0x45049c,0x7730fe,0xb986ff,0xe6d5ff],
                [0x6b036e,0xad2cce,0xf180ff,0xfdd2ff],
                [0x72031e,0xbd2a64,0xff7ad3,0xffcff5],
                [0x651100,0xb53a00,0xff875f,0xffd5c5],
                [0x451f00,0x8f4c00,0xef9812,0xffdba3],
                [0x232e00,0x636000,0xc9ab00,0xefe391],
                [0x003900,0x1b7000,0x7fbe00,0xd0ec8f],
                [0x003d00,0x007700,0x47c820,0xb9f0a6],
                [0x003821,0x00743c,0x2cc870,0xaef0c7],
                [0x003266,0x006d99,0x2fc4cc,0xafeeee],
                [0x000000,0x000000,0x51514f,0xbbbcba],
                [0x000000,0x000000,0x000000,0x000000],
                [0x000000,0x000000,0x000000,0x000000],
              ]



def transpose(matrix):
  return [list(k) for k in zip(*matrix)]


def flatten(matrix):
  return [e for sublist in matrix for e in sublist]


BLACK = 0xf


def to_lookup_table(elems):
  answer = {}
  for i,val in enumerate(elems):
    answer[val] = i
  # Set black.
  answer[0] = BLACK
  return answer


RGB_COLORS = flatten(transpose(RGB_COLORS))
RGB_XLAT = to_lookup_table(RGB_COLORS)
