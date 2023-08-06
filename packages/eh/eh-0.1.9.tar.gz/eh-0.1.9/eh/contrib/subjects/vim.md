vim
How to use vim Macros (quick start):

- Create a recording on register **d**: `qd`
- During recording just perform your commands like normal
- Stop recording: `q`
- Execute Macro from register **d**: `@d`
- Execute the last macro executed: `@@`

How to use vim registers (quick start):

In normal mode:

- To yank into register `d`: `"dy`
- To paste from register `d`: `"dp`
- Yanking without a register goes to the `0` register
- The default register is the `"` register
- The `0` register is populated with **only** yanks
- The `"` register is also populated with `d/D/x/X/c/C/s/S`
- Use `:reg` to view the values in the registers
