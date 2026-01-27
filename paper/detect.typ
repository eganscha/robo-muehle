= PART OF COMPUTER VISION

== Perspective Normalization via Homography
Reliable board-state estimation requires a consistent coordinate frame under changes in camera pose (tilt, in-plane rotation, distance). This is addressed via planar perspective normalization: once the board region is detected, it is rectified into a fixed, top-down view using a homography (projective transformation). Homographies are applicable when the observed structure is well-approximated as planar under a projective camera model. A homography maps points between two planes according to

𝑝′ ∼ 𝐻𝑝, 𝐻 ∈ 𝑅3×3,

where image points are written in homogeneous form  𝑝 = (𝑥,𝑦,1)⊤. The symbol ∼ denotes equality up to a non-zero scale factor. After transformation, the inhomogeneous coordinates are recovered by normalizing with the third component (), i.e., , . This additional third coordinate enables translation and projective effects (e.g., foreshortening) to be expressed as a single matrix operation. This 3×3 setup and its degrees of freedom are standard in multi-view geometry.

In the implemented pipeline, board localization is performed by a learned detector that returns a bounding box. From that box, the four corners are extracted in a fixed order (top-left, top-right, bottom-right, bottom-left) and mapped to a predefined square output geometry. The homography 𝐻 is computed and applied with OpenCV’s perspective transform utilities (getPerspectiveTransform and warpPerspective). warpPerspective performs inverse-mapped, per-pixel resampling under the estimated homography, producing a rectified board image in a fixed target grid.

The canonical board view is rendered at a steady resolution (e.g., 1000×1000 px) so that downstream steps - index mapping, thresholding, and plausibility checks – operate in a stable pixel metric.

A design trade-off comes with estimating corners from a bounding box: it is simple and fast, but not as robust to extreme viewpoints as methods that explicitly regress corners or trace the board edge. In practice, that means the camera pose needs to stay within a limited range for reliable rectification.

== Stone/stack Detection and Candidate Extraction
Object detection is split into three parts: (1) board detection, (2) stones detection on the board, and (3) stack detection off the board. The stone and stack detectors use two classes (black and white) to directly infer color during detection. Inference is executed via the Ultralytics YOLO runtime interface, which exposes per-detection bounding boxes, class IDs, and the confidence scores.

A critical geometric constraint applies to stone detection: stones are detected only on the rectified board image. To prevent a mismatch between training and runtime use induced by perspective distortion, stones-model training images are warped into the same canonical geometry prior to labeling and training. This ensures that the learned appearance distribution matches the runtime input distribution (top-down board appearance).

Stack detection is performed in the original camera frame (off-board region) and therefore operates in unrectified image coordinates; no pre-warping is applied to stack training data. Stack detections are used to estimate off-board piece availability

#figure(
  image("WhatsApp Image 2026-01-27 at 16.17.42.jpeg", width: 80%),
  caption: [Qualitative detection example Left: raw camera frame with board bounding box and off-board stack detections. Right: rectified top-down board view used for on-board stone detection and subsequent index mapping.],
) <fig>

Candidate extraction converts each predicted bounding box into a point hypothesis using its center (𝑐𝑥,𝑐𝑦). Ultralytics provides box conversions including [𝑥center,𝑦center,𝑤,ℎ], which enables direct retrieval of centers for subsequent mapping.

Detections are filtered in two stages:

1. Minimum confidence filter: anything below a fixed confidence threshold cmin is discarded.
2. Spatial plausibility filter (after mapping): once a detection is assigned to the nearest board index (see Section II.C), any detection whose center lies farther than a maximum distance dmax from that index is rejected. This distance threshold dmax is scaled by the estimated board grid spacing in pixels, so it stays consistent across different canonical resolutions.
If several detections land on the same board position, the best candidate wins: one hypothesis per index, usually the one with the highest confidence. If there is a tie, the closer center-to-index distance breaks it. This produces a sparse and stable set of per-position candidates suitable for discrete state reconstruction.

== Index Mapping and State Building
The normalized board view provides a deterministic mapping from image-space hypotheses to the discrete Nine Men’s Morris state. Playable positions are represented as a fixed set of indices with normalized coordinates (𝑥𝑟𝑒𝑙,𝑦𝑟𝑒𝑙) ∈ [0,1] and stored in a CSV file. At runtime, those coordinates are mapped to pixel coordinates in the canonical image via (𝑥𝑖,𝑦𝑖) = ( 𝑥𝑟𝑒𝑙𝑆,𝑦𝑟𝑒𝑙𝑆), where S is the board’s canonical side length in pixels.

Each detected stone center (𝑐𝑥,𝑐𝑦) is assigned to the nearest index by Euclidean distance:

To increase robustness against spurious detections, a scale-aware acceptance radius is applied. This radius is based on the board geometry, e.g. the typical grid spacing, computed as the median distance to the nearest neighbor among the indices in pixel space. Detections exceeding a chosen fraction of this spacing are rejected as implausible placements.

The final output is a fixed-length occupancy array over the 24 positions using a ternary encoding compatible with the game logic: 0 for empty, −1 for black, +1 for white. In addition, temporal state tracking compares the estimated occupancy array against the previously known game state and reports a delta (changed indices) only after the same changed state is observed consistently across several consecutive frames, thereby reducing flicker-induced false updates.

== Assumptions and Limitations
Performance depends on the validity of the planar-board assumption and on accurate board localization. Errors in bounding-box localization directly affect corner derivation and therefore propagate into the homography, shifting mapped stone centers and increasing index-assignment ambiguity. Motion blur, strong specular reflections, partial board edge occlusion, and low contrast backgrounds can cause additional degradation. These limitations motivate either tighter constraints on camera placement and lighting or the replacement of box-derived corners with corner regression/segmentation-based localization under wider viewpoint variations.
