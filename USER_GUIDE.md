# User Guide

This user guide will explain how to proofread spines. At the end, you will have a CSV containing head center names, radii, 3D positions, index, and label (assigned by you, a human proofreader).

Ensure that you have already [installed the proofreading software](INSTALL.md) and have a `.dsb` file.

## Opening a DSB file

First, run the proofreader. You'll see a menu with a button prompting you to open a DSB file. Click it.

![First opening](images/user_guide/first_open.png)

Then, choose a DSB file to load.

![Opening a DSB file](images/user_guide/opening.png)

The program may freeze for up to one minute while it loads the DSB file and initializes the visualization.

## Proofreader Menu

After you open a .dsb file, you will see a window visualizing the 3D neuron data.

![Proofreader Menu](images/user_guide/proofreader.png)

Use the following controls to move the camera:

| Action             | Control                            |
|--------------------|------------------------------------|
| Orbit Camera       | Left Click + Drag                  |
| Translate Camera   | Shift + Left Click + Drag          |
| Zoom Camera        | Right Click + Drag OR Scroll Wheel |
| Rotate Camera      | Command + Left Click + Drag        |
| View Entire Neuron | R                                  |

Use the following controls to change how the visualization looks:

| Action                  | Control |
|-------------------------|---------|
| Toggle 3D Glasses Mode  | 3       |
| Turn On Wireframe Mode  | W       |
| Turn Off Wireframe Mode | S       |

### Accepting or rejecting spines

You can accept or reject the currently-visualized spine head by clicking the "Accept" or "Reject" buttons in the toolbar, which is on the top of the proofreader window.

You may also use the following keyboard shortcuts:

| Action                  | Control |
|-------------------------|---------|
| Accept Spine Head       | M       |
| Reject Spine Head       | N       |

### Moving to the next spine

To proofread the next or previous spine head, use the "Previous" or "Next" buttons in the toolbar.

You may also use the left and right arrow keys to move to the previous or next spine head.

The buttons and arrow keys wrap around. For example, advancing from the final spine head displays the first, and moving backward from the first displays the final.

### Adjusting spine head position

If the spine head position requires adjusting (e.g., it is not perfectly in the head center), you may use the following controls to modify the spine head position.

| Action                    | Key |
|---------------------------|-----|
| Move head center forward  | I   |
| Move head center backward | K   |
| Move head center left     | J   |
| Move head center right    | L   |
| Move head center up       | U   |
| Move head center down     | O   |

These controls are relative to the camera view. You may use the Shift key while performing these controls to move the head center a larger distance per step.

### The status text

The status text in the top left corner of the 3D visualizer indicates the status of the currently-visualized dendritic spine and a reminder for some proofreader-specific keyboard shortcuts.

![Status text](images/user_guide/status_text.png)

"Point 3/204" indicates that the proofreader is visualizing spine head ID 3 (out of 204 spines).

"Status: accepted" means that you accepted this spine head. It may also show "Status: rejected" or "Status: unlabeled".

"Radius: 398.74 nm" shows the radius, in nanometers, that DSB computed for this spine head.

### Naming a spine head

Spine heads are automatically assigned the name of the nearest label. Sometimes the name is incorrect or undefined if there are too many or not enough labels in proximity of the spine head. 

You can adjust the name of the currently-selected spine head by editing the text box on the bottom of the window.

![Naming a spine head](images/user_guide/spine_name.png)

### Saving

You may use the "Save" button in the toolbar or the keyboard shortcut Ctrl/Cmd + S to save. It is recommended to save often.

The first save may take several minutes because the proofreader needs to compute spine head radii for all points. While saving for the first time, the window will freeze. Do not close it to avoid losing progres.  Any subsequent saves should be near instant.

If you reload a dsb file after saving, the proofreader will remember all spine head names, accepts/rejects, and spine head position adjustments that you made.