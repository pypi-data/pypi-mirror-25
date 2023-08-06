ENV: r1;
SYS: g1;

ENVINIT: !r1;
ENVTRANS:
  [](((r1 & !g1) | (!r1 & g1)) -> ((r1' & r1) | (!r1' & !r1)));
ENVGOAL:
  []<>!(r1 & g1);

SYSINIT: !g1;
SYSTRANS:
  [](((r1 & g1) | (!r1 & !g1)) -> ((g1 & g1') | (!g1 & !g1')));
SYSGOAL:
  []<>((r1 & g1) | (!r1 & !g1));
