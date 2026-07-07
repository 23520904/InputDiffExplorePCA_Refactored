import os

diffs = [
    ('0x00400000', 1, (64, 0)),
    ('0x00200000', 1, (32, 0)),
    ('0x00008000', 1, (0, 32768)),
    ('0x00408000', 2, (64, 32768)),
    ('0x00102000', 2, (16, 8192)),
    ('0x00600000', 2, (96, 0)),
    ('0x20000040', 2, (8192, 64)),
    ('0x00302000', 3, (48, 8192)),
    ('0x00702000', 4, (112, 8192))
]

template = """import sys
sys.path.append('./src')
import train_nets as tn
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

input_diff = {diff}
print(f'HW: {hw}, speck nr5 - input_diff: {{input_diff}} ({hex_val})')
net, h = tn.train_neural_distinguisher(num_epochs=200, num_rounds=5, depth=10, alg='speck_32_64', input_diff=input_diff, train_data_size=10**7, eval_data_size=10**6, verbose='1')
"""

for hex_val, hw, diff in diffs:
    with open(f'scripts/train_speck_nr5_{hex_val}.py', 'w') as f:
        f.write(template.format(diff=diff, hw=hw, hex_val=hex_val))

print('Scripts generated successfully.')
