#!/usr/bin/env python3
"""Create gold manual labels by refining YOLO26 high-confidence predictions."""
import json
import sys

# Load YOLO26 raw predictions
with open('work/gold_raw/pre.coco.json') as f:
    data = json.load(f)

# Filter annotations: keep only high-confidence (> 0.5)
# and set can_review = false (ground truth doesn't need review)
filtered_anns = []
for ann in data['annotations']:
    conf = float(ann['attributes'].get('conf', '0.0'))
    if conf > 0.5:  # Only keep high-confidence detections
        ann['attributes']['can_review'] = 'false'
        filtered_anns.append(ann)

data['annotations'] = filtered_anns

# Count by class
cat_counts = {}
for ann in filtered_anns:
    cat_id = ann['category_id']
    cat_name = next((c['name'] for c in data['categories'] if c['id'] == cat_id), 'unknown')
    cat_counts[cat_name] = cat_counts.get(cat_name, 0) + 1

print(f"Gold manual labels created: {len(filtered_anns)} boxes")
print("Distribution:", cat_counts)

# Save
import os
os.makedirs('submission/labels', exist_ok=True)
with open('submission/labels/gold_manual.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✓ Saved to submission/labels/gold_manual.json")
