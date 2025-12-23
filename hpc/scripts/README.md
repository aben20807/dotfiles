# Example

```bash
$ sbatch check_ib_nodes.slurm

$ cat ib_check_122.out
==== IB full-mesh connectivity check ====
Nodes: cnode3-011 cnode3-012

==== Collect IB interfaces (ALL ports) ====
--- cnode3-011 --- 
ibp24s0 100.126.6.86/16
ibp64s0 100.126.6.87/16
ibp79s0 100.126.6.88/16
ibp94s0 100.126.6.89/16
ibp154s0 100.126.6.82/16
ibp192s0 100.126.6.83/16
ibp206s0 100.126.6.84/16
ibp220s0 100.126.6.85/16
--- cnode3-012 --- 
ibp24s0 100.126.6.94/16
ibp64s0 100.126.6.95/16
ibp79s0 100.126.6.96/16
ibp94s0 100.126.6.97/16
ibp154s0 100.126.6.90/16
ibp192s0 100.126.6.91/16
ibp206s0 100.126.6.92/16
ibp220s0 100.126.6.93/16

==== Cross-node full-mesh IB ping ====

[SRC cnode3-011:ibp24s0 (100.126.6.86)]
  ✅ ibp24s0 -> cnode3-012:ibp24s0 (100.126.6.94)

[SRC cnode3-011:ibp64s0 (100.126.6.87)]
  ❌ ibp64s0 -> cnode3-012:ibp24s0 (100.126.6.94)

[SRC cnode3-011:ibp79s0 (100.126.6.88)]
  ❌ ibp79s0 -> cnode3-012:ibp24s0 (100.126.6.94)

[SRC cnode3-011:ibp94s0 (100.126.6.89)]
  ❌ ibp94s0 -> cnode3-012:ibp24s0 (100.126.6.94)

[SRC cnode3-011:ibp154s0 (100.126.6.82)]
  ❌ ibp154s0 -> cnode3-012:ibp24s0 (100.126.6.94)

[SRC cnode3-011:ibp192s0 (100.126.6.83)]
  ❌ ibp192s0 -> cnode3-012:ibp24s0 (100.126.6.94)

[SRC cnode3-011:ibp206s0 (100.126.6.84)]
  ❌ ibp206s0 -> cnode3-012:ibp24s0 (100.126.6.94)

[SRC cnode3-011:ibp220s0 (100.126.6.85)]
  ❌ ibp220s0 -> cnode3-012:ibp24s0 (100.126.6.94)

[SRC cnode3-012:ibp24s0 (100.126.6.94)]
  ✅ ibp24s0 -> cnode3-011:ibp24s0 (100.126.6.86)

[SRC cnode3-012:ibp64s0 (100.126.6.95)]
  ❌ ibp64s0 -> cnode3-011:ibp24s0 (100.126.6.86)

[SRC cnode3-012:ibp79s0 (100.126.6.96)]
  ❌ ibp79s0 -> cnode3-011:ibp24s0 (100.126.6.86)

[SRC cnode3-012:ibp94s0 (100.126.6.97)]
  ❌ ibp94s0 -> cnode3-011:ibp24s0 (100.126.6.86)

[SRC cnode3-012:ibp154s0 (100.126.6.90)]
  ❌ ibp154s0 -> cnode3-011:ibp24s0 (100.126.6.86)

[SRC cnode3-012:ibp192s0 (100.126.6.91)]
  ❌ ibp192s0 -> cnode3-011:ibp24s0 (100.126.6.86)

[SRC cnode3-012:ibp206s0 (100.126.6.92)]
  ❌ ibp206s0 -> cnode3-011:ibp24s0 (100.126.6.86)

[SRC cnode3-012:ibp220s0 (100.126.6.93)]
  ❌ ibp220s0 -> cnode3-011:ibp24s0 (100.126.6.86)

==== IB full-mesh check completed ====
```
