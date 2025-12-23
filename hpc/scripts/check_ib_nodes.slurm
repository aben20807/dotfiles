#!/bin/bash
#SBATCH -p p02
#SBATCH -N 2
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=ib_check
#SBATCH --output=ib_check_%j.out
#SBATCH --error=ib_check_%j.err

set -u

echo "==== IB full-mesh connectivity check ===="
NODES=($(scontrol show hostnames "$SLURM_NODELIST"))
echo "Nodes: ${NODES[*]}"

declare -A IB_INFO

echo
echo "==== Collect IB interfaces (ALL ports) ===="
for NODE in "${NODES[@]}"; do
    echo "--- $NODE ---"
    INFO=$(srun -N1 -n1 -w "$NODE" bash -c '
        ip -o -4 addr show | awk '"'"'$2 ~ /^(ib|ibp)/ {print $2, $4}'"'"'
    ')
    if [[ -z "$INFO" ]]; then
        echo "  ❌ No IB IP found"
    else
        echo "$INFO"
    fi  
    IB_INFO[$NODE]="$INFO"
done

echo
echo "==== Cross-node full-mesh IB ping ===="

for SRC in "${NODES[@]}"; do
    SRC_INFO="${IB_INFO[$SRC]}"
    [[ -z "$SRC_INFO" ]] && continue

    while read -r SRC_IF SRC_CIDR; do
        SRC_IP=${SRC_CIDR%%/*}
        echo
        echo "[SRC $SRC:$SRC_IF ($SRC_IP)]"

        for DST in "${NODES[@]}"; do
            [[ "$SRC" == "$DST" ]] && continue
            DST_INFO="${IB_INFO[$DST]}"
            [[ -z "$DST_INFO" ]] && continue

            while read -r DST_IF DST_CIDR; do
                DST_IP=${DST_CIDR%%/*}
                srun -N1 -n1 -w "$SRC" bash -c "
                    ping -I $SRC_IF -c 1 -W 1 $DST_IP >/dev/null
                "
                if [[ $? -eq 0 ]]; then
                    echo "  ✅ $SRC_IF -> $DST:$DST_IF ($DST_IP)"
                else
                    echo "  ❌ $SRC_IF -> $DST:$DST_IF ($DST_IP)"
                fi
            done <<< "$DST_INFO"
        done
    done <<< "$SRC_INFO"
done

echo
echo "==== IB full-mesh check completed ===="