I see what you mean. The issue may be with the shoulder and hip keypoints used for the line calculation. The MoveNet model predicts 17 keypoints, each representing different parts of the body. Here is the list of keypoints from the official documentation:

0.  "nose"
1.  "left_eye"
2.  "right_eye"
3.  "left_ear"
4.  "right_ear"
5.  "left_shoulder"
6.  "right_shoulder"
7.  "left_elbow"
8.  "right_elbow"
9.  "left_wrist"
10. "right_wrist"
11. "left_hip"
12. "right_hip"
13. "left_knee"
14. "right_knee"
15. "left_ankle"
16. "right_ankle"

From your code, it seems that you're using keypoints 6 and 8 for the shoulders, and keypoints 12 and 14 for the hips. However, keypoints 6 and 8 are "right_shoulder" and "right_elbow", and keypoints 12 and 14 are "right_hip" and "right_knee". So you're calculating the midpoints and slope between the elbow and shoulder, and the knee and hip on the right side of the body, which might not provide an accurate representation of the person's lean.

Instead, you might want to use the midpoint between the left and right shoulders (keypoints 5 and 6), and the midpoint between the left and right hips (keypoints 11 and 12) to calculate the lean:

```python
# Calculate the midpoints of shoulders and hips
shoulder_midpoint = [(x_coords[5] + x_coords[6]) / 2, (y_coords[5] + y_coords[6]) / 2]
hip_midpoint = [(x_coords[11] + x_coords[12]) / 2, (y_coords[11] + y_coords[12]) / 2]
```

The rest of the calculations should stay the same. This should give you a more accurate representation of the person's lean, as you're considering both the left and right sides of the body.